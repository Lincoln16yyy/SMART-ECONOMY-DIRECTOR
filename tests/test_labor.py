"""State labor reference regressions; demographic proxy, not engine employment."""
import unittest

from tools.build_mod import SUPPLY_TARGETS, variants
from tools.labor import REQUIREMENTS
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class LaborTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def producer(self, good='wood'):
        item = next(item for item in SUPPLY_TARGETS if item['good'] == good)
        producer = building(item['building'])
        producer['production_methods'] = [item['methods'][0]]
        target = state(population=100000, buildings=[producer], state_unemployment_rate=0.2,
                       **{'pop_type_percent_state(pop_type:peasants)': 0})
        self.c.states = [target]
        self.c.market_goods[good] = dict(market_goods_has_goods_shortage=True,
                                        market_goods_buy_orders=100, market_goods_sell_orders=20)
        return target, producer

    def test_registry_covers_all_supported_producers(self):
        kinds = {variant['building'] for item in SUPPLY_TARGETS for variant in variants(item)}
        self.assertTrue(kinds <= REQUIREMENTS.keys())
        self.assertTrue(all(isinstance(workers, int) and workers > 0 for workers in REQUIREMENTS.values()))

    def test_founding_revalidates_workers_before_insertion(self):
        c = self.c
        target = state(population=100000, state_unemployment_rate=0.21,
                       **{'pop_type_percent_state(pop_type:peasants)': 0})
        c.states = [target]
        c.market_goods['iron']['market_goods_has_goods_shortage'] = True
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_iron_candidate_eligible'], target))
        target['state_population'] = 50000
        c.run('sed_run_iron_approval', target)
        self.assertEqual(c.constructions, [])

    def test_pending_founding_reserves_workers_before_building_exists(self):
        c = self.c
        target = state(population=100000, state_unemployment_rate=0.4,
                       **{'pop_type_percent_state(pop_type:peasants)': 0})
        c.states = [target]
        target['variables'].update(sed_iron_request_pending=True, sed_iron_intent_level=0,
                                   sed_iron_intent_variant=1)
        self.assertEqual(c.number('sed_state_labor_committed', target), 5250)
        target['buildings'].append(building('building_iron_mine', occupancy=0))
        self.assertEqual(c.number('sed_state_labor_committed', target), 5250)
        target['buildings'].clear()
        target['variables'].pop('sed_iron_request_pending')
        self.assertEqual(c.number('sed_state_labor_committed', target), 0)

    def test_exact_labor_boundary_and_population_changes_are_read_live(self):
        c = self.c
        target, _ = self.producer()
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_available'], 5000)
        self.assertTrue(c.condition(c.definitions['sed_wood_candidate_eligible'], target))
        target['state_population'] = 99980
        self.assertFalse(c.condition(c.definitions['sed_wood_candidate_eligible'], target))
        c.run('sed_run_wood_approval', target)
        self.assertEqual(c.constructions, [])

    def test_existing_vacancies_are_deducted_and_have_a_distinct_rejection_reason(self):
        c = self.c
        target, producer = self.producer()
        producer.update(level=2, level_after_queued_constructions=2, occupancy=0.8)
        c.run('sed_refresh_diagnostics')
        self.assertAlmostEqual(target['variables']['sed_labor_committed'], 2000)
        self.assertAlmostEqual(target['variables']['sed_labor_available'], 3000)
        self.assertEqual(c.variables['sed_wood_labor_states'], 1)
        self.assertEqual(c.variables['sed_wood_understaffed_states'], 0)
        self.assertEqual(c.variables['sed_wood_hiring_states'], 0)
        self.assertNotIn('sed_wood_candidates', c.variable_lists)

    def test_queued_other_producer_reserves_workers_and_cancellation_releases_them(self):
        c = self.c
        target, _ = self.producer()
        iron = building('building_iron_mine', queued_levels=1)
        target['buildings'].append(iron)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_committed'], 5250)
        self.assertEqual(target['variables']['sed_labor_available'], 0)
        iron['level_after_queued_constructions'] = 1
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_available'], 5000)
        self.assertIn('sed_wood_candidates', c.variable_lists)

    def test_peasant_reference_and_workforce_ratio_are_clamped(self):
        c = self.c
        target, _ = self.producer()
        target.update(state_unemployment_rate=0,
                      **{'pop_type_percent_state(pop_type:peasants)': 0.4})
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_pool'], 5000)
        target.update(state_unemployment_rate=-1,
                      **{'pop_type_percent_state(pop_type:peasants)': -1})
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_available'], 0)
        target.update(state_unemployment_rate=2,
                      **{'pop_type_percent_state(pop_type:peasants)': 2,
                         'modifier:state_working_adult_ratio_add': 2})
        c.run('sed_refresh_diagnostics')
        self.assertEqual(target['variables']['sed_labor_pool'], 100000)

    def test_automatic_worker_shortage_does_not_consume_attempt(self):
        c = self.c
        target, _ = self.producer()
        target['state_unemployment_rate'] = 0
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)
        target['state_unemployment_rate'] = 0.2
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)

    def test_grain_alternatives_use_their_own_worker_reference(self):
        c = self.c
        target, _ = self.producer('grain')
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_grain_candidate_eligible'], target))
        target['buildings'] = [building('building_rice_farm')]
        target['buildings'][0]['production_methods'] = ['pm_simple_farming_building_rice_farm']
        c.run('sed_refresh_diagnostics')
        self.assertFalse(c.condition(c.definitions['sed_grain_candidate_eligible'], target))
        target['state_unemployment_rate'] = 0.4
        self.assertTrue(c.condition(c.definitions['sed_grain_candidate_eligible'], target))

    def test_disabling_clears_labor_state_snapshots(self):
        c = self.c
        target, _ = self.producer()
        c.run('sed_refresh_diagnostics')
        c.run('sed_disable_country')
        self.assertFalse(any(key.startswith('sed_labor_') for key in target['variables']))


if __name__ == '__main__':
    unittest.main()
