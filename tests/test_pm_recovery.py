"""Input-shortage recovery through existing production-method controls."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state


class MethodRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.producer = building('building_logging_camp', shortage=True)
        self.producer['production_methods'] = ['pm_saw_mills', 'pm_road_carts']
        self.target = state(buildings=[self.producer])
        self.c.states = [self.target]
        self.c.readings['technologies'] = ['steelworking']
        self.c.market_goods['tools'].update(market_goods_has_goods_shortage=True,
                                            market_goods_buy_orders=100, market_goods_sell_orders=0)
        self.c.run('sed_set_mode_automatic')

    def test_normal_review_removes_the_scarce_input_and_keeps_other_groups(self):
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.producer['production_methods'], ['pm_road_carts', 'pm_simple_forestry'])
        self.assertEqual(self.c.variables['sed_auto_review_status'], 25)
        self.assertEqual(self.c.constructions, [])
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(len(self.c.production_method_changes), 1)

    def test_an_unidentified_building_shortage_does_not_authorize_a_change(self):
        self.c.market_goods['tools']['market_goods_has_goods_shortage'] = False
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])
        self.assertNotIn('sed_pm_upgrade_last_attempt_month', self.c.variables)

    def test_remaining_shortages_in_other_groups_prevent_an_ineffective_change(self):
        self.producer['production_methods'].append('pm_chainsaws')
        self.c.market_goods['oil']['market_goods_has_goods_shortage'] = True
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])

    def test_local_electricity_shortage_can_select_the_intermediate_method(self):
        self.producer['production_methods'] = ['pm_electric_saw_mills', 'pm_road_carts']
        self.c.market_goods['tools'].update(market_goods_has_goods_shortage=False,
                                            market_goods_buy_orders=100, market_goods_sell_orders=100)
        self.target['state_goods']['electricity'].update(state_goods_production=10, state_goods_consumption=21)
        self.c.run('sed_recover_existing_industry')
        self.assertIn('pm_saw_mills', self.producer['production_methods'])
        self.assertNotIn('pm_electric_saw_mills', self.producer['production_methods'])

    def test_nominal_output_floor_prevents_excessive_reduction(self):
        self.producer['production_methods'] = ['pm_electric_saw_mills']
        self.target['state_goods']['electricity'].update(state_goods_production=0, state_goods_consumption=20)
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])

    def test_output_floor_accounts_for_secondary_output_shifts(self):
        self.producer['production_methods'].append('pm_hardwood')
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])

    def test_recovery_can_apply_to_queued_expansion_and_an_unincorporated_state(self):
        self.producer['level_after_queued_constructions'] = 2
        self.target.update(is_incorporated=False, infrastructure_delta=-10)
        self.target['variables'].update(sed_wood_request_pending=True, sed_wood_intent_level=1,
                                        sed_wood_intent_variant=1)
        self.c.readings['construction_queue_num_queued_government_levels'] = 1
        self.c.run('sed_auto_apply_monthly')
        self.assertIn('pm_simple_forestry', self.producer['production_methods'])
        self.assertEqual(self.c.readings['construction_queue_num_queued_government_levels'], 1)

    def test_recovery_is_available_in_default(self):
        self.c.readings['in_default'] = True
        self.c.run('sed_auto_apply_monthly')
        self.assertIn('pm_simple_forestry', self.producer['production_methods'])
        self.assertEqual(self.c.variables['sed_auto_review_status'], 25)

    def test_recovery_overrides_upgrade_cooldown_and_delays_reupgrade(self):
        self.target['variables']['sed_pm_cooldown_logging_camp'] = 999999
        self.c.run('sed_auto_apply_monthly')
        self.assertIn('pm_simple_forestry', self.producer['production_methods'])
        self.c.readings['month'] = 1
        self.producer['building_has_goods_shortage'] = False
        self.c.market_goods['tools'].update(market_goods_has_goods_shortage=False,
                                            market_goods_buy_orders=100, market_goods_sell_orders=100)
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=True,
                                           market_goods_buy_orders=100, market_goods_sell_orders=40)
        self.c.run('sed_modernize_existing_industry')
        self.assertEqual(len(self.c.production_method_changes), 1)

    def test_failed_recovery_is_not_reported_as_success(self):
        self.c.production_method_accepted = False
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.variables['sed_auto_review_status'], 24)
        self.assertIn('pm_saw_mills', self.producer['production_methods'])
        self.assertNotIn('sed_pm_cooldown_logging_camp', self.target['variables'])

    def test_external_pm_manager_and_ignored_building_have_precedence(self):
        self.c.variables['advisor_pm_balance_enabled'] = True
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])
        self.c.variables.pop('advisor_pm_balance_enabled')
        self.target['variables']['sed_wood_ignored'] = True
        self.c.run('sed_recover_existing_industry')
        self.assertEqual(self.c.production_method_changes, [])


if __name__ == '__main__':
    unittest.main()
