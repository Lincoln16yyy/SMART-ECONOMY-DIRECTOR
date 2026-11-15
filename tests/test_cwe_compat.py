"""Regression checks for the scoped Cold War Era construction edition."""

import unittest

from script_harness import Country, construction_sector, state
from tools.cwe_compat import automation_scripts, budget_scripts
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

    def test_paused_or_existing_director_stops_the_cwe_dispatcher(self):
        c = self.country
        c.variables['sed_enabled'] = True
        c.run('sed_cwe_automatic_review')
        c.variables.pop('sed_enabled')
        c.readings['is_construction_paused'] = True
        c.run('sed_cwe_automatic_review')
        self.assertEqual(c.constructions, [])
