"""Regressions for the direct executor's material stress benchmark."""
import unittest

from tools.build_mod import SUPPLY_TARGETS
from tools.construction_budget import BASE_PRICES, PROFILES
from test_diagnostics import script_definitions
from script_harness import Country, building, construction_sector, state


class ConstructionBudgetTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def sector(self, method):
        sector = construction_sector()
        sector['production_methods'] = [method]
        self.c.states.append(state(buildings=[sector]))
        return sector

    def target(self):
        item = next(item for item in SUPPLY_TARGETS if item['good'] == 'wood')
        producer = building(item['building'])
        producer['production_methods'] = [item['methods'][0]]
        target = state(buildings=[producer])
        self.c.states.append(target)
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=True,
                                          market_goods_buy_orders=100, market_goods_sell_orders=20)
        return target

    def test_four_verified_profiles_produce_the_expected_material_reference(self):
        for method, points, inputs in PROFILES:
            with self.subTest(method=method):
                self.setUp()
                c = self.c
                self.sector(method)
                c.run('sed_refresh_direct_budget')
                expected = sum(BASE_PRICES[good] * amount for good, amount in inputs.items()) * 1.75 / points
                self.assertAlmostEqual(c.variables['sed_build_budget_point_cost'], expected, places=5)
                self.assertAlmostEqual(c.variables['sed_build_budget_weekly'], expected * 10, places=4)
                self.assertEqual(c.variables['sed_build_budget_known'], 1)

    def test_mixed_methods_use_the_highest_cost_and_project_point_cap(self):
        c = self.c
        self.sector('pm_steel_frame_buildings')
        self.sector('pm_wooden_buildings')
        c.readings['modifier:country_construction_add'] = 100
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_points'], 25)
        self.assertEqual(c.variables['sed_build_budget_point_cost'], 1750)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 43750)

    def test_insufficient_reference_coverage_blocks_without_consuming_attempt(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        self.target()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 22)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_reserve_and_weekly_income_boundaries_revalidate_before_execution(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        self.target()
        c.readings.update(principal=0, gold_reserves=452599)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        c.readings['gold_reserves'] = 452600
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_review_status'], 1)

    def test_income_can_cover_reference_while_reserve_branch_requires_no_debt(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        c.readings.update(principal=1, gold_reserves=1000000)
        c.run('sed_refresh_direct_budget')
        self.assertFalse(c.condition(c.definitions['sed_direct_budget_safe'], c.country_scope()))
        c.readings['net_total_income'] = 17500
        c.run('sed_refresh_direct_budget')
        self.assertTrue(c.condition(c.definitions['sed_direct_budget_safe'], c.country_scope()))

    def test_unknown_active_method_blocks_direct_but_assisted_approval_remains_available(self):
        c = self.c
        self.sector('pm_unknown_construction')
        target = self.target()
        c.readings.update(net_total_income=100000, gold_reserves=1000000)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_build_budget_known'], 0)
        self.assertEqual(c.variables['sed_auto_review_status'], 22)
        self.assertEqual(c.constructions, [])
        c.run('sed_set_mode_assisted')
        c.run('sed_run_wood_approval', target)
        self.assertEqual(len(c.constructions), 1)

    def test_method_change_after_diagnosis_is_checked_by_approval(self):
        c = self.c
        sector = self.sector('pm_wooden_buildings')
        target = self.target()
        c.readings['net_total_income'] = 20000
        c.run('sed_set_mode_automatic')
        c.run('sed_refresh_diagnostics')
        sector['production_methods'] = ['pm_unknown_construction']
        c.run('sed_run_wood_approval', target)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_no_sector_material_reference_and_zero_capacity_are_distinct(self):
        c = self.c
        self.target()
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_weekly'], 0)
        c.readings['modifier:country_construction_add'] = 0
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 22)
        self.assertEqual(c.constructions, [])

    def test_budget_variables_are_cleared_on_disable(self):
        c = self.c
        self.sector('pm_iron_frame_buildings')
        c.run('sed_refresh_diagnostics')
        c.run('sed_disable_country')
        self.assertFalse(any(key.startswith('sed_build_budget_') for key in c.variables))


if __name__ == '__main__':
    unittest.main()
