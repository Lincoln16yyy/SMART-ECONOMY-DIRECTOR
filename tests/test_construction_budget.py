"""Regressions for the direct executor's material stress benchmark."""
import unittest

from tools.build_mod import SUPPLY_TARGETS
from tools.construction_budget import BASE_PRICES, PROFILES
from test_diagnostics import script_definitions
from script_harness import Country, building, construction_sector, railway, state


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
                self.assertAlmostEqual(c.variables['sed_build_budget_weekly'], min(expected * 10, expected * points), places=4)
                self.assertEqual(c.variables['sed_build_budget_known'], 1)

    def test_mixed_methods_use_the_highest_cost_and_project_point_cap(self):
        c = self.c
        self.sector('pm_steel_frame_buildings')
        self.sector('pm_wooden_buildings')
        c.readings['modifier:country_construction_add'] = 100
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_points'], 25)
        self.assertEqual(c.variables['sed_build_budget_point_cost'], 1750)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 12950)

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
        c.readings.update(principal=0, gold_reserves=88599)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        c.readings['gold_reserves'] = 88600
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_review_status'], 1)

    def test_income_can_cover_reference_while_reserve_branch_requires_no_debt(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        c.readings.update(principal=1, gold_reserves=1000000)
        c.run('sed_refresh_direct_budget')
        self.assertFalse(c.condition(c.definitions['sed_direct_budget_safe'], c.country_scope()))
        c.readings['net_total_income'] = 3500
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

    def test_small_sector_does_not_charge_free_capacity_at_the_material_rate(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        c.readings['modifier:country_construction_add'] = 100
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_points'], 25)
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 3500)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 3500)

    def test_sector_levels_and_occupancy_recompute_the_material_cap(self):
        c = self.c
        sector = self.sector('pm_wooden_buildings')
        sector.update(level=3, occupancy=0.5)
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 5250)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 5250)
        sector['occupancy'] = 0
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 0)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 0)

    def test_mixed_states_sum_material_cap_without_reusing_previous_readings(self):
        c = self.c
        wood = self.sector('pm_wooden_buildings')
        iron = self.sector('pm_iron_frame_buildings')
        wood.update(level=2, occupancy=0.5)
        iron.update(level=2, occupancy=1)
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 16100)
        c.states.pop()
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 3500)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 3500)

    def test_first_priority_duration_and_materials_extend_required_reserve(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        c.states.append(state(-10, can_construct=True))
        c.run('sed_refresh_national_plan')
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_project_points'], 800)
        self.assertAlmostEqual(c.variables['sed_build_budget_project_weeks'], 80)
        self.assertEqual(c.variables['sed_build_budget_project_materials'], 1400000)
        self.assertEqual(c.variables['sed_build_budget_funding_weeks'], 84)
        self.assertEqual(c.variables['sed_build_budget_required_gold'], 285800)

    def test_existing_queue_adds_work_and_extends_the_funding_horizon(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        self.target()
        c.states.append(state(buildings=[building('building_iron_mine', queued_levels=2),
                                        building('building_tooling_workshop', queued_levels=1)]))
        c.readings['construction_queue_num_queued_government_levels'] = 3
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_build_budget_queue_levels_known'], 3)
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 1400)
        self.assertEqual(c.variables['sed_build_budget_queue_weeks'], 140)
        self.assertEqual(c.variables['sed_build_budget_funding_weeks'], 164)

    def test_unknown_queue_work_and_zero_capacity_have_explicit_fallbacks(self):
        c = self.c
        c.readings['construction_queue_num_queued_government_levels'] = 1
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_levels_unknown'], 1)
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 6000)
        self.assertEqual(c.variables['sed_build_budget_queue_weeks'], 600)
        c.readings['modifier:country_construction_add'] = 0
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_weeks'], 0)
        self.assertFalse(c.condition(c.definitions['sed_direct_budget_safe'], c.country_scope()))

    def test_tracked_founding_is_budgeted_before_the_building_exists(self):
        c = self.c
        target = state()
        target['variables'].update(sed_tools_request_pending=True, sed_tools_intent_level=0,
                                   sed_tools_intent_variant=1)
        c.states = [target]
        c.readings['construction_queue_num_queued_government_levels'] = 1
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 600)
        self.assertEqual(c.variables['sed_build_budget_queue_levels_unknown'], 0)
        target['buildings'].append(building('building_tooling_workshop', queued_levels=1))
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 600)

    def test_empty_government_queue_releases_old_work_estimates(self):
        c = self.c
        c.states = [state(buildings=[building('building_iron_mine', queued_levels=2)])]
        c.readings['construction_queue_num_queued_government_levels'] = 2
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 800)
        c.readings['construction_queue_num_queued_government_levels'] = 0
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_queue_points'], 0)

    def test_concurrent_public_projects_can_use_the_full_national_capacity(self):
        c = self.c
        sector = self.sector('pm_wooden_buildings')
        sector['level'] = 100
        c.readings.update(construction_queue_num_queued_government_levels=2,
                          **{'modifier:country_construction_add': 100})
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_active_points'], 75)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 131250)

    def test_reserve_financing_can_resume_direct_investment_with_a_covered_deficit(self):
        c = self.c
        self.sector('pm_wooden_buildings')
        self.target()
        c.readings.update(net_total_income=-10, principal=0, gold_reserves=91459)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)
        c.readings['gold_reserves'] = 91460
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_review_status'], 1)

    def test_debt_or_operating_deficit_prevents_reserve_financing(self):
        c = self.c
        self.target()
        c.readings.update(net_total_income=-10, principal=1, gold_reserves=1000000)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        c.readings.update(principal=0, net_fixed_income=-1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_project_cap_still_limits_large_sector_material_reference(self):
        c = self.c
        sector = self.sector('pm_wooden_buildings')
        sector['level'] = 100
        c.readings['modifier:country_construction_add'] = 1000
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_material_capacity'], 350000)
        self.assertEqual(c.variables['sed_build_budget_weekly'], 43750)

    def test_budget_variables_are_cleared_on_disable(self):
        c = self.c
        self.sector('pm_iron_frame_buildings')
        c.run('sed_refresh_diagnostics')
        c.run('sed_disable_country')
        self.assertFalse(any(key.startswith('sed_build_budget_') for key in c.variables))


if __name__ == '__main__':
    unittest.main()
