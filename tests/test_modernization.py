"""Continuous main-method upgrades through the normal automatic review."""
import unittest

from tools.production_methods import EXTERNAL_PM_VARIABLES
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class ModernizationTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.producer = building('building_logging_camp')
        self.producer['production_methods'] = ['pm_simple_forestry', 'pm_hardwood', 'pm_road_carts']
        self.target = state(buildings=[self.producer])
        self.c.states = [self.target]
        self.c.readings['technologies'] = ['steelworking']
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=True,
                                           market_goods_buy_orders=100, market_goods_sell_orders=40)
        self.c.run('sed_set_mode_automatic')

    def test_normal_review_upgrades_existing_industry_and_preserves_other_groups(self):
        c = self.c
        c.run('sed_auto_apply_monthly')
        self.assertEqual(self.producer['production_methods'], ['pm_hardwood', 'pm_road_carts', 'pm_saw_mills'])
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_auto_review_status'], 23)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.production_method_changes), 1)
        self.assertEqual(c.variables['sed_pm_reserved_tools'], 6.25)

    def test_national_choice_and_input_reservation_scale_with_building_levels(self):
        large = building('building_logging_camp', level=2)
        large['production_methods'] = ['pm_simple_forestry']
        target = state(buildings=[large])
        self.c.states.append(target)
        self.c.run('sed_auto_apply_monthly')
        self.assertIn('pm_saw_mills', large['production_methods'])
        self.assertIn('pm_simple_forestry', self.producer['production_methods'])
        self.assertEqual(self.c.variables['sed_pm_reserved_tools'], 12.5)

    def test_input_boundary_revalidates_without_consuming_an_ineligible_attempt(self):
        c = self.c
        c.market_goods['tools'].update(market_goods_buy_orders=100, market_goods_sell_orders=53.12)
        c.run('sed_modernize_existing_industry')
        self.assertEqual(c.production_method_changes, [])
        self.assertNotIn('sed_pm_upgrade_last_attempt_month', c.variables)
        c.market_goods['tools']['market_goods_sell_orders'] = 53.125
        c.run('sed_modernize_existing_industry')
        self.assertIn('pm_saw_mills', self.producer['production_methods'])

    def test_staffing_hiring_shortage_and_pending_expansion_prevent_upgrades(self):
        for field, value in [('occupancy', 0.89), ('has_failed_hires', True),
                             ('building_has_goods_shortage', True), ('level_after_queued_constructions', 2)]:
            original = self.producer[field]
            self.producer[field] = value
            self.c.run('sed_modernize_existing_industry')
            self.assertEqual(self.c.production_method_changes, [])
            self.producer[field] = original

    def test_demand_and_technology_are_required(self):
        self.c.market_goods['wood']['market_goods_has_goods_shortage'] = False
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])
        self.c.market_goods['wood']['market_goods_has_goods_shortage'] = True
        self.c.readings['technologies'] = []
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])

    def test_auto_apply_pms_flag_leaves_that_building_to_the_other_mod(self):
        # Auto-Apply PMs publishes one toggle per building. The Director yields
        # instead of fighting for the same main method group.
        c = self.c
        c.variables['zw_var_auto_pm_building_logging_camp'] = True
        c.run('sed_modernize_existing_industry')
        self.assertEqual(c.production_method_changes, [])
        del c.variables['zw_var_auto_pm_building_logging_camp']
        c.run('sed_modernize_existing_industry')
        self.assertIn('pm_saw_mills', self.producer['production_methods'])

    def test_auto_apply_pms_group_flag_covers_every_farm_type(self):
        for farm in ('building_wheat_farm', 'building_rye_farm', 'building_rice_farm',
                     'building_maize_farm', 'building_millet_farm'):
            with self.subTest(farm=farm):
                self.assertIn('zw_var_auto_pm_building_group_farms',
                              EXTERNAL_PM_VARIABLES[farm])
        self.assertIn('zw_var_auto_pm_building_group_plantations',
                      EXTERNAL_PM_VARIABLES['building_cotton_plantation'])
        # A group toggle must not leak to a building outside that group.
        self.assertNotIn('zw_var_auto_pm_building_group_farms',
                         EXTERNAL_PM_VARIABLES['building_logging_camp'])

    def test_three_month_cooldown_prevents_immediate_followup_upgrade(self):
        c = self.c
        c.run('sed_modernize_existing_industry')
        c.readings['technologies'].append('electrical_generation')
        for month in (1, 2):
            c.readings['month'] = month
            c.run('sed_set_mode_assisted')
            c.run('sed_set_mode_automatic')
            c.run('sed_modernize_existing_industry')
            self.assertEqual(len(c.production_method_changes), 1)
        c.readings['month'] = 3
        c.run('sed_modernize_existing_industry')
        self.assertIn('pm_electric_saw_mills', self.producer['production_methods'])
        self.assertEqual(len(c.production_method_changes), 2)

    def test_failed_activation_consumes_the_attempt_and_survives_disable(self):
        c = self.c
        c.production_method_accepted = False
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 24)
        self.assertIn('pm_simple_forestry', self.producer['production_methods'])
        self.assertNotIn('sed_pm_cooldown_logging_camp', self.target['variables'])
        c.run('sed_disable_country')
        self.assertIn('sed_pm_upgrade_last_attempt_month', c.variables)
        c.run('sed_enable_country')
        c.run('sed_set_mode_automatic')
        c.production_method_accepted = True
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.production_method_changes), 1)

    def test_manual_mode_and_unmanaged_aroai_prevent_upgrades(self):
        self.c.run('sed_set_mode_manual')
        self.c.variables['sed_mode_automatic'] = True
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])
        self.c.run('sed_set_mode_automatic')
        self.c.variables['aroai_autobuild'] = True
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])

    def test_observed_wage_unit_reduces_the_upgrade_score(self):
        self.target['variables'].update(sed_investment_wage_known=1, sed_investment_wage_unit=0.2)
        self.c.run('sed_modernize_existing_industry')
        self.assertIn('pm_saw_mills', self.producer['production_methods'])
        # Scenario gain 200 and 250 extra wage-weighted jobs per level.
        self.assertAlmostEqual(self.target['variables']['sed_pm_upgrade_score'], 150)

    def test_wage_cost_can_block_a_materially_positive_upgrade(self):
        self.target['variables'].update(sed_investment_wage_known=1, sed_investment_wage_unit=1)
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])
        self.assertEqual(self.target['variables']['sed_pm_upgrade_score'], 0)

    def test_coordinator_suspends_external_construction_after_the_upgrade(self):
        c = self.c
        c.variables.update(advisor_enabled=True, advisor_auto_construction_enabled=1)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 13)
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)
        self.assertEqual(c.variables['sed_auto_review_status'], 23)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_coord_executor'], 13)
        c.run('sed_set_mode_assisted')
        self.assertEqual(c.variables['advisor_auto_construction_enabled'], 1)

    def test_existing_advisor_pm_managers_prevent_competing_method_changes(self):
        for option in ('advisor_pm_balance_enabled', 'advisor_labor_auto_enabled'):
            self.c.variables[option] = True
            self.c.run('sed_modernize_existing_industry')
            self.assertEqual(self.c.production_method_changes, [])
            self.c.variables.pop(option)
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(len(self.c.production_method_changes), 1)


if __name__ == '__main__':
    unittest.main()
