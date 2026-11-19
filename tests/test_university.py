"""Teste sintético do enfileiramento de universidades."""
import unittest

from script_harness import Country, building, construction_sector, state
from test_diagnostics import script_definitions


class UniversityTests(unittest.TestCase):
    def setUp(self):
        self.country = Country(script_definitions(), country_innovation=25, max_innovation=60,
                               net_total_income=2000, principal=0, gold_reserves=1000000,
                               construction_queue_num_queued_government_levels=0)
        self.country.market_goods['paper'] = dict(market_goods_sell_orders=40,
                                                  market_goods_has_goods_shortage=False)
        self.country.states = [state(population=100000), state(population=400000)]
        self.country.run('sed_enable_country')

    def test_coordination_dispatches_university_and_confirms_the_queue(self):
        c = self.country
        c.variables['advisor_enabled'] = True
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 11)
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)
        self.assertEqual([job['building'] for job in c.constructions], ['building_university'])
        self.assertIs(c.constructions[0]['state'], c.states[1])
        self.assertEqual(c.variables['sed_auto_review_status'], 1)
        self.assertEqual(c.variables['sed_build_budget_project_points'], 400)
        c.run('sed_auto_run_direct')
        self.assertEqual(len(c.constructions), 1)

    def test_innovation_cap_and_supply_gates(self):
        c = self.country
        self.assertTrue(c.condition(c.definitions['sed_university_ready'], c.country_scope()))
        c.readings['country_innovation'] = c.readings['max_innovation']
        self.assertFalse(c.condition(c.definitions['sed_university_ready'], c.country_scope()))
        c.readings['country_innovation'] = 25
        c.market_goods['paper']['market_goods_has_goods_shortage'] = True
        self.assertFalse(c.condition(c.definitions['sed_university_ready'], c.country_scope()))

    def test_rejects_understaffed_expansions_and_sites_without_workers(self):
        c = self.country
        gate = c.definitions['sed_university_candidate']
        self.assertFalse(c.condition(gate, state(population=100)))
        self.assertFalse(c.condition(gate, state(buildings=[building('building_university', occupancy=0.5)])))

    def test_university_waits_for_a_clear_public_queue(self):
        c = self.country
        c.readings['construction_queue_num_queued_government_levels'] = 1
        self.assertFalse(c.condition(c.definitions['sed_university_ready'], c.country_scope()))


    def test_material_budget_blocks_dispatch(self):
        c = self.country
        c.states[0]['buildings'].append(construction_sector())
        c.states[0]['buildings'][-1]['production_methods'] = ['pm_wooden_buildings']
        c.readings.update(net_total_income=1, gold_reserves=200)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_auto_review_status'], 22)
