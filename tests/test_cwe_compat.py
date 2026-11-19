"""Regression checks for the scoped Cold War Era construction edition."""

import unittest

from script_harness import Country, building, construction_sector, state
from tools.cwe_compat import automation_scripts, budget_scripts, fiscal_scripts, shortage_trigger
from tools.pdx_script import parse


class ColdWarEraTests(unittest.TestCase):
    def setUp(self):
        budget, values = budget_scripts({'materials': {'pm_construction_0': 200},
                                        'size': {'pm_construction_size_1': 100}})
        candidates, effects = automation_scripts()
        self.country = Country({entry.key: entry.value
                                for entry in parse(budget + values + candidates + effects)},
                               net_total_income=1050)
        sector = construction_sector(level=2)
        sector['production_methods'] = ['pm_construction_0', 'pm_construction_size_1']
        self.rail_state = state(-5, buildings=[sector])
        self.admin_state = state(tax_capacity_usage=200, tax_capacity=100)
        self.country.states = [self.admin_state, self.rail_state]
        self.country.variables['sed_cwe_enabled'] = True

    def test_construction_prices_use_all_active_groups_and_block_unknown_methods(self):
        c = self.country
        self.assertEqual(c.number('sed_cwe_weekly_material_cost', c.country_scope()), 1050)
        c.readings['net_total_income'] = 1049
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.constructions, [])
        c.readings['net_total_income'] = 1050
        self.rail_state['buildings'][0]['production_methods'].pop()
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_cwe_last_attempt', c.variables)

    def test_railway_wins_then_waits_for_the_next_month(self):
        c = self.country
        c.run('sed_cwe_automatic_review')
        c.run('sed_cwe_automatic_review')
        self.assertEqual([item['building'] for item in c.constructions], ['building_railway'])
        c.readings['month'] = 1
        self.rail_state['infrastructure_delta'] = 0
        c.run('sed_cwe_automatic_review')
        self.assertEqual([item['building'] for item in c.constructions],
                         ['building_railway', 'building_government_administration'])

    def test_review_reports_only_confirmed_queue_insertion(self):
        c = self.country
        c.construction_accepted = False
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.variables['sed_cwe_result'], 4)
        self.assertNotIn('sed_cwe_queue_before', c.variables)
        c.construction_accepted = True
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.variables['sed_cwe_result'], 4)
        c.readings['month'] = 1
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.variables['sed_cwe_result'], 1)

    def test_journal_is_added_once_for_existing_enabled_games(self):
        c = self.country
        c.run('sed_cwe_ensure_journal')
        c.run('sed_cwe_ensure_journal')
        self.assertEqual(c.journals_added, 1)

    def test_ogas_general_manager_owns_the_queue_when_enabled(self):
        c = self.country
        c.variables['cnm_auto_construct_manager'] = 1
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_cwe_last_attempt', c.variables)
        c.variables['cnm_auto_construct_manager'] = 0
        c.run('sed_cwe_automatic_review')
        self.assertEqual([item['building'] for item in c.constructions], ['building_railway'])

    def test_ogas_railway_manager_only_suppresses_director_railways(self):
        c = self.country
        c.variables['cnm_auto_railway_manager'] = 1
        c.run('sed_cwe_automatic_review')
        self.assertEqual([item['building'] for item in c.constructions],
                         ['building_government_administration'])

    def test_paused_or_existing_director_stops_the_cwe_dispatcher(self):
        c = self.country
        c.variables['sed_enabled'] = True
        c.run('sed_cwe_automatic_review')
        c.variables.pop('sed_enabled')
        c.readings['is_construction_paused'] = True
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.constructions, [])


class ColdWarEraFiscalTests(unittest.TestCase):
    def setUp(self):
        triggers, values = budget_scripts({'basic': {'pm_construction_0': 200}})
        fiscal_triggers, fiscal_effects = fiscal_scripts()
        self.definitions = {entry.key: entry.value for entry in parse(
            triggers + values + fiscal_triggers + fiscal_effects)}
        self.country = Country(self.definitions, net_total_income=-300, net_fixed_income=-200,
                               gold_reserves=10, military_expenses=300, in_default=True)
        self.country.variables['sed_cwe_enabled'] = True

    def test_policy_runs_under_ogas_and_restores_after_a_simulated_reload(self):
        c = self.country
        c.variables['cnm_auto_construct_manager'] = 1
        c.run('sed_cwe_apply_budget_policy')
        self.assertEqual(c.readings['tax_level'], 'high')
        self.assertEqual(c.readings['government_wage_level'], 'low')
        self.assertEqual(c.readings['military_wage_level'], 'low')
        loaded = Country(self.definitions, **c.readings)
        loaded.variables.update(c.variables)
        loaded.run('sed_cwe_apply_budget_policy')
        self.assertEqual(loaded.tax_changes, [])
        self.assertEqual(loaded.wage_changes, [])
        self.assertEqual(loaded.military_wage_changes, [])
        loaded.run('sed_cwe_disable_country')
        self.assertEqual(loaded.readings['tax_level'], 'medium')
        self.assertEqual(loaded.readings['government_wage_level'], 'medium')
        self.assertEqual(loaded.readings['military_wage_level'], 'medium')
        self.assertNotIn('sed_cwe_enabled', loaded.variables)

    def test_military_wages_are_not_cut_during_war(self):
        c = self.country
        c.readings['is_at_war'] = True
        c.run('sed_cwe_apply_budget_policy')
        self.assertEqual(c.military_wage_changes, [])
        self.assertNotIn('sed_cwe_military_wage_saved', c.variables)


class ColdWarEraShortageTests(unittest.TestCase):
    def test_only_an_active_producer_with_inputs_responds_to_shortage(self):
        entry, = parse(shortage_trigger({'iron': {'pm_iron_0'}}))
        self.assertEqual(entry.key, 'sed_cwe_building_shortage_supplier')
        c = Country({entry.key: entry.value})
        c.market_goods['iron'] = {'market_goods_has_goods_shortage': True}
        mine = building('building_iron_mine')
        mine['production_methods'] = ['pm_iron_0']
        self.assertTrue(c.condition(entry.value, mine))
        mine['building_has_goods_shortage'] = True
        self.assertFalse(c.condition(entry.value, mine))
        mine['building_has_goods_shortage'] = False
        mine['production_methods'] = []
        self.assertFalse(c.condition(entry.value, mine))
