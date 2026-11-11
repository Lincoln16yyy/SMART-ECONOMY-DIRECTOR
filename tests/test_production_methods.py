"""Initial production-method setup for Director-founded industries."""
import unittest

from tools.production_methods import PROFILES
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class FoundingMethodTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.producer = building('building_tooling_workshop')
        self.producer['production_methods'] = ['pm_pig_iron']
        self.target = state(buildings=[self.producer])
        self.c.states = [self.target]
        self.c.run('sed_set_mode_automatic')
        self.target['variables']['sed_tools_found_pm_pending'] = 1

    def test_initial_setup_applies_one_method_per_group_and_runs_once(self):
        c = self.c
        c.run('sed_configure_founded_industries')
        expected = {group['method'] for group in PROFILES['building_tooling_workshop']}
        self.assertEqual(set(self.producer['production_methods']), expected)
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])
        changes = len(c.production_method_changes)
        self.producer['production_methods'] = ['pm_pig_iron']
        c.run('sed_configure_founded_industries')
        self.assertEqual(len(c.production_method_changes), changes)
        self.assertEqual(self.producer['production_methods'], ['pm_pig_iron'])

    def test_changed_input_supply_defers_setup_until_it_is_viable(self):
        c = self.c
        c.market_goods['wood'].update(market_goods_buy_orders=100, market_goods_sell_orders=50)
        c.run('sed_configure_founded_industries')
        self.assertEqual(c.production_method_changes, [])
        self.assertIn('sed_tools_found_pm_pending', self.target['variables'])
        c.market_goods['wood']['market_goods_sell_orders'] = 68.75
        c.run('sed_configure_founded_industries')
        self.assertIn('pm_crude_tools', self.producer['production_methods'])

    def test_all_methods_are_preflighted_before_any_change(self):
        self.target['blocked_methods'] = [PROFILES['building_tooling_workshop'][-1]['method']]
        self.c.run('sed_configure_founded_industries')
        self.assertEqual(self.c.production_method_changes, [])
        self.target['blocked_methods'] = []
        self.c.run('sed_configure_founded_industries')
        self.assertTrue(self.c.production_method_changes)

    def test_already_active_methods_do_not_need_activation_permission(self):
        method = PROFILES['building_tooling_workshop'][-1]['method']
        self.producer['production_methods'].append(method)
        self.target['blocked_methods'] = [method]
        self.c.run('sed_configure_founded_industries')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])
        self.assertTrue(self.c.production_method_changes)

    def test_worker_shortage_defers_initial_configuration(self):
        self.producer['occupancy'] = 0
        self.target.update(state_unemployment_rate=0,
                           **{'pop_type_percent_state(pop_type:peasants)': 0})
        self.c.run('sed_configure_founded_industries')
        self.assertEqual(self.c.production_method_changes, [])
        self.target['state_unemployment_rate'] = 0.2
        self.c.run('sed_configure_founded_industries')
        self.assertTrue(self.c.production_method_changes)

    def test_two_configurations_do_not_reuse_the_same_market_headroom(self):
        other_producer = building('building_tooling_workshop')
        other_producer['production_methods'] = ['pm_pig_iron']
        other = state(buildings=[other_producer])
        other['variables']['sed_tools_found_pm_pending'] = 1
        self.c.states.append(other)
        self.c.market_goods['wood'].update(market_goods_buy_orders=100, market_goods_sell_orders=75)
        self.c.run('sed_configure_founded_industries')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])
        self.assertIn('sed_tools_found_pm_pending', other['variables'])
        self.c.market_goods['wood']['market_goods_sell_orders'] = 100
        self.c.run('sed_configure_founded_industries')
        self.assertNotIn('sed_tools_found_pm_pending', other['variables'])

    def test_matching_configuration_does_not_reserve_inputs_again(self):
        self.producer['production_methods'] = [group['method'] for group in PROFILES['building_tooling_workshop']]
        other_producer = building('building_tooling_workshop')
        other_producer['production_methods'] = ['pm_pig_iron']
        other = state(buildings=[other_producer])
        other['variables']['sed_tools_found_pm_pending'] = 1
        self.c.states.append(other)
        self.c.market_goods['wood'].update(market_goods_buy_orders=100, market_goods_sell_orders=68.75)
        self.c.run('sed_configure_founded_industries')
        self.assertNotIn('sed_tools_found_pm_pending', other['variables'])

    def test_mode_exit_discards_pending_setup_and_conflicting_modes_block_execution(self):
        self.c.run('sed_set_mode_assisted')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])
        self.target['variables']['sed_tools_found_pm_pending'] = 1
        self.c.run('sed_configure_founded_industries')
        self.assertEqual(self.c.production_method_changes, [])
        self.c.variables['sed_mode_automatic'] = True
        self.c.run('sed_configure_founded_industries')
        self.assertEqual(self.c.production_method_changes, [])

    def test_expansion_by_another_builder_discards_initial_configuration(self):
        self.producer['level_after_queued_constructions'] = 2
        self.c.run('sed_configure_founded_industries')
        self.assertEqual(self.c.production_method_changes, [])
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])

    def test_cancellation_and_disable_clear_pending_configuration(self):
        self.target['buildings'] = []
        self.c.run('sed_configure_founded_industries')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])
        self.target['variables']['sed_tools_found_pm_pending'] = 1
        self.c.run('sed_disable_country')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])

    def test_successful_automatic_founding_tracks_setup_until_a_building_exists(self):
        c = self.c
        self.target['buildings'] = []
        self.target['variables'].pop('sed_tools_found_pm_pending')
        c.market_goods['tools'].update(market_goods_has_goods_shortage=True)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(self.target['variables']['sed_tools_found_pm_pending'], 1)
        c.run('sed_configure_founded_industries')
        self.assertEqual(c.production_method_changes, [])
        self.target['buildings'] = [self.producer]
        c.run('sed_configure_founded_industries')
        self.assertIn('pm_crude_tools', self.producer['production_methods'])

    def test_failed_insertion_does_not_authorize_method_changes(self):
        self.target['buildings'] = []
        self.target['variables'].pop('sed_tools_found_pm_pending')
        self.c.market_goods['tools'].update(market_goods_has_goods_shortage=True)
        self.c.construction_accepted = False
        self.c.run('sed_auto_apply_monthly')
        self.assertNotIn('sed_tools_found_pm_pending', self.target['variables'])


if __name__ == '__main__':
    unittest.main()
