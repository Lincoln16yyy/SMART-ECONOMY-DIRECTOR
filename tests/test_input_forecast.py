"""Projected input demand, supply thresholds and approval revalidation."""
import unittest
import tempfile
from pathlib import Path

from tools.build_mod import outputs
from tools.validate import validate
from tools.input_forecast import PROFILES, GOODS, LABELS_PT
from tools.labor import REQUIREMENTS
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class InputForecastTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.producer = building('building_tooling_workshop')
        self.producer['production_methods'] = ['pm_crude_tools']
        self.target = state(buildings=[self.producer])
        self.c.states = [self.target]
        self.c.market_goods['tools'] = dict(market_goods_buy_orders=100,
                                           market_goods_sell_orders=40,
                                           market_goods_has_goods_shortage=True)
        self.wood(100, 68.75)

    def wood(self, buy, sell):
        self.c.market_goods['wood'] = dict(market_goods_buy_orders=buy,
                                          market_goods_sell_orders=sell,
                                          market_goods_has_goods_shortage=False)

    def eligible(self):
        return self.c.condition(self.c.definitions['sed_tools_candidate_eligible'], self.target)

    def test_founding_revalidates_material_supply_before_insertion(self):
        c = self.c
        target = state()
        c.states = [target]
        self.wood(100, 68.75)
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_tools_candidate_eligible'], target))
        self.wood(100, 68.74)
        c.run('sed_run_tools_approval', target)
        self.assertEqual(c.constructions, [])

    def test_founding_accounts_for_technologically_available_methods(self):
        c = self.c
        target = state()
        c.states = [target]
        self.assertEqual(c.number('sed_founding_input_iron_mine_coal', target), 0)
        c.readings['technologies'] = ['atmospheric_engine']
        self.assertGreater(c.number('sed_founding_input_iron_mine_coal', target), 0)

    def test_founding_takes_one_maximum_per_method_group(self):
        c = self.c
        target = state()
        c.states = [target]
        c.readings['technologies'] = ['steelworking', 'mechanical_tools', 'vulcanization']
        self.assertEqual(c.number('sed_founding_input_tooling_workshop_wood', target), 30)
        self.assertEqual(c.number('sed_founding_input_tooling_workshop_steel', target), 30)

    def test_pending_founding_reserves_inputs_without_double_counting(self):
        c = self.c
        target = state()
        c.states = [target]
        target['variables'].update(sed_tools_request_pending=True, sed_tools_intent_level=0,
                                   sed_tools_intent_variant=1)
        self.assertEqual(c.number('sed_input_pending_wood', target), 37.5)
        producer = building('building_tooling_workshop', occupancy=0)
        producer['production_methods'] = ['pm_crude_tools']
        target['buildings'].append(producer)
        self.assertEqual(c.number('sed_input_pending_wood', target), 37.5)
        target['buildings'].clear()
        target['variables'].pop('sed_tools_request_pending')
        self.assertEqual(c.number('sed_input_pending_wood', target), 0)

    def test_automatic_founds_an_input_supplier_before_the_missing_factory(self):
        c = self.c
        target = state()
        c.states = [target]
        self.wood(100, 50)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertIn('sed_input_priority_wood', c.variables)
        self.assertEqual([project['building'] for project in c.constructions],
                         ['building_logging_camp'])

    def test_projected_wood_shortfall_prioritizes_a_viable_logging_camp(self):
        c = self.c
        logging = building('building_logging_camp')
        logging['production_methods'] = ['pm_simple_forestry']
        upstream = state(buildings=[logging])
        c.states.append(upstream)
        self.wood(100, 68.74)
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())
        self.assertIn('sed_input_priority_wood', c.variables)
        self.assertEqual(c.variable_lists['sed_input_blocked_wood'], [self.target])
        blocker = c.definitions['sed_input_blocks_wood_tools_tooling_workshop']
        self.assertTrue(c.condition(blocker, self.target))
        self.assertFalse(c.condition(blocker, upstream))
        self.assertEqual(c.variable_lists['sed_wood_candidates'], [upstream])
        self.assertEqual(upstream['variables']['sed_plan_wood_rank'], 1)

        logging['level_after_queued_constructions'] = 2
        c.run('sed_refresh_diagnostics')
        self.assertNotIn('sed_wood_candidates', c.variable_lists)
        self.assertEqual(c.variable_lists['sed_input_blocked_wood'], [self.target])
        self.assertEqual(c.variables['sed_plan_waiting'], 1)

        logging['level_after_queued_constructions'] = 1
        self.wood(100, 68.75)
        c.run('sed_run_wood_approval', upstream)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_input_priority_wood', c.variables)
        self.assertNotIn('sed_input_blocked_wood', c.variable_lists)

        self.wood(100, 68.74)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual([order['building'] for order in c.constructions], ['building_logging_camp'])

    def test_automatic_picks_the_largest_eligible_supplier_across_states(self):
        low = building('building_logging_camp')
        low['production_methods'] = ['pm_simple_forestry', 'pm_hardwood']
        high = building('building_logging_camp')
        high['production_methods'] = ['pm_simple_forestry']
        blocked = building('building_logging_camp', occupancy=0.5)
        blocked['production_methods'] = ['pm_electric_saw_mills']
        high_state = state(buildings=[high])
        self.c.states.extend([state(buildings=[low]), high_state, state(buildings=[blocked])])
        self.wood(100, 68.74)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.variable_lists['sed_plan_1_wood'], [high_state])
        self.assertEqual(self.c.constructions, [
            {'building': 'building_logging_camp', 'state': high_state}
        ])

    def test_automatic_queues_the_higher_output_variant_in_the_same_state(self):
        bakery = building('building_food_industry')
        bakery['production_methods'] = ['pm_bakery']
        wheat = building('building_wheat_farm')
        wheat['production_methods'] = ['pm_simple_farming']
        rice = building('building_rice_farm')
        rice['production_methods'] = ['pm_simple_farming_building_rice_farm']
        farms = state(buildings=[wheat, rice])
        c = self.c
        c.states = [state(buildings=[bakery]), farms]
        c.market_goods['tools']['market_goods_has_goods_shortage'] = False
        c.market_goods['groceries'] = dict(market_goods_buy_orders=100,
                                           market_goods_sell_orders=40,
                                           market_goods_has_goods_shortage=True)
        c.market_goods['grain'] = dict(market_goods_buy_orders=100,
                                       market_goods_sell_orders=70,
                                       market_goods_has_goods_shortage=False)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [{'building': 'building_rice_farm', 'state': farms}])
        self.assertEqual(farms['variables']['sed_grain_intent_variant'], 3)

    def test_blocker_list_shows_three_most_populous_affected_states_and_clears_on_disable(self):
        self.wood(100, 68.74)
        states = [state(buildings=[self.producer.copy()], population=200000 + i * 10000)
                  for i in range(4)]
        self.c.states = states
        self.c.run('sed_refresh_diagnostics')
        self.assertEqual(self.c.variable_lists['sed_input_blocked_wood'], states[:0:-1])
        self.c.run('sed_disable_country')
        self.assertNotIn('sed_input_blocked_wood', self.c.variable_lists)

    def test_inoperable_downstream_producer_does_not_create_input_priority(self):
        self.wood(100, 68.74)
        self.producer['has_failed_hires'] = True
        self.c.run('sed_refresh_diagnostics')
        self.assertNotIn('sed_input_priority_wood', self.c.variables)

    def test_profiles_cover_known_producers_and_labels(self):
        self.assertEqual(set(PROFILES), set(REQUIREMENTS))
        self.assertEqual(set(GOODS), set(LABELS_PT))
        for methods in PROFILES.values():
            for quantities in methods.values():
                self.assertTrue(all(isinstance(value, (int, float)) for value in quantities.values()))

    def test_active_methods_sum_only_their_inputs(self):
        self.producer['production_methods'] = ['pm_crude_tools',
                                               'pm_rotary_valve_engine_building_tooling_workshop',
                                               'pm_assembly_lines_building_tooling_workshop']
        for good, quantity in (('wood', 30), ('coal', 15), ('electricity', 5), ('iron', 0)):
            actual = self.c.number(self.c.definitions['sed_input_tooling_workshop_' + good], self.target)
            self.assertEqual(actual, quantity)

    def test_exact_supply_threshold_with_demand_stress(self):
        c = self.c
        c.run('sed_refresh_diagnostics')
        self.assertTrue(self.eligible())
        self.wood(100, 68.74)
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())
        self.assertEqual(c.variables['sed_tools_forecast_states'], 1)
        self.assertEqual(c.variables['sed_tools_input_states'], 0)

    def test_absent_input_market_blocks_without_error(self):
        c = self.c
        c.market_goods.pop('wood')
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())
        c.run('sed_run_tools_approval', self.target)
        self.assertEqual(c.constructions, [])

    def test_queued_unincorporated_producer_reserves_market_inputs(self):
        c = self.c
        self.wood(100, 80)
        queued = building('building_tooling_workshop', queued_levels=1)
        queued['production_methods'] = ['pm_crude_tools']
        c.states.append(state(incorporated=False, buildings=[queued]))
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())
        queued['level_after_queued_constructions'] = 1
        c.run('sed_refresh_diagnostics')
        self.assertTrue(self.eligible())

    def test_unfilled_jobs_reserve_inputs_until_the_workforce_reading_changes(self):
        c = self.c
        self.wood(100, 70)
        self.producer['occupancy'] = 0.8
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())
        self.producer['occupancy'] = 1
        c.run('sed_refresh_diagnostics')
        self.assertTrue(self.eligible())

    def logging(self):
        producer = building('building_logging_camp')
        producer['production_methods'] = ['pm_electric_saw_mills']
        self.target['buildings'] = [producer]
        self.c.market_goods['wood'] = dict(market_goods_buy_orders=100,
                                          market_goods_sell_orders=40,
                                          market_goods_has_goods_shortage=True)
        self.c.market_goods['tools'].update(market_goods_buy_orders=1000,
                                            market_goods_sell_orders=1000,
                                            market_goods_has_goods_shortage=False)

    def test_local_power_uses_the_affected_state(self):
        c = self.c
        self.logging()
        self.target['state_goods']['electricity'].update(state_goods_production=51,
                                                        state_goods_consumption=100)
        c.states.append(state())
        c.run('sed_refresh_diagnostics')
        self.assertFalse(c.condition(c.definitions['sed_wood_candidate_eligible'], self.target))
        self.target['state_goods']['electricity']['state_goods_production'] = 53.125
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_wood_candidate_eligible'], self.target))

    def test_local_pending_inputs_are_not_shared_between_states(self):
        c = self.c
        self.logging()
        self.target['state_goods']['electricity'].update(state_goods_production=53.125,
                                                        state_goods_consumption=100)
        queued = building('building_tooling_workshop', queued_levels=1)
        queued['production_methods'] = ['pm_crude_tools', 'pm_assembly_lines_building_tooling_workshop']
        other = state(buildings=[queued])
        c.states.append(other)
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_wood_candidate_eligible'], self.target))
        other['buildings'] = []
        self.target['buildings'].append(queued)
        c.run('sed_refresh_diagnostics')
        self.assertFalse(c.condition(c.definitions['sed_wood_candidate_eligible'], self.target))

    def test_approval_refreshes_changed_market_after_an_eligible_reading(self):
        c = self.c
        c.run('sed_refresh_diagnostics')
        self.assertTrue(self.eligible())
        self.wood(100, 68.74)
        c.run('sed_run_tools_approval', self.target)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_method_change_is_revalidated_before_approval(self):
        c = self.c
        c.run('sed_refresh_diagnostics')
        self.producer['production_methods'] = ['pm_pig_iron']
        c.market_goods['iron'] = dict(market_goods_buy_orders=100, market_goods_sell_orders=50,
                                     market_goods_has_goods_shortage=False)
        c.run('sed_run_tools_approval', self.target)
        self.assertEqual(c.constructions, [])

    def test_automatic_waits_for_input_capacity_without_consuming_the_month(self):
        c = self.c
        # Keep this scenario focused on waiting when the upstream is unavailable.
        self.target['variables']['sed_wood_ignored'] = True
        self.wood(100, 68.74)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)
        self.wood(100, 68.75)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.constructions[0]['building'], 'building_tooling_workshop')

    def test_queued_future_output_is_not_credited_as_current_supply(self):
        c = self.c
        self.wood(100, 60)
        future = building('building_logging_camp', queued_levels=10)
        future['production_methods'] = ['pm_simple_forestry']
        c.states.append(state(buildings=[future]))
        c.run('sed_refresh_diagnostics')
        self.assertFalse(self.eligible())

    def test_forecast_snapshots_are_cleared_on_disable(self):
        c = self.c
        c.run('sed_refresh_diagnostics')
        c.run('sed_disable_country')
        self.assertFalse(any(key.startswith('sed_input_') for key in c.variables))
        self.assertFalse(any(key.startswith('sed_input_') for key in self.target['variables']))

    def test_validator_rejects_removed_forecast_guard_or_refresh(self):
        for filename, old, new in (
            ('common/scripted_triggers/sed_triggers.txt',
             ' sed_input_tooling_workshop_safe = yes\n', ''),
            ('common/scripted_effects/sed_effects.txt',
             'sed_auto_run_direct = {\n sed_refresh_input_readings = yes', 'sed_auto_run_direct = {'),
        ):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                for name, data in outputs().items():
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                target = root / filename
                text = target.read_text(encoding='utf-8-sig')
                self.assertIn(old, text)
                target.write_text(text.replace(old, new, 1), encoding='utf-8-sig')
                errors = validate(root)
                self.assertTrue(any('forecast guard' in error or 'forecast refresh' in error
                                    for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
