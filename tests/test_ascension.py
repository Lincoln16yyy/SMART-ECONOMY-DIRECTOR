"""Testa o plano de ascensão com leituras fornecidas ao harness."""
import unittest

from script_harness import Country, state
from test_diagnostics import script_definitions


class AscensionTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), prestige=50, army_power_projection=25,
                         net_total_income=500, principal=0, gold_reserves=10000)
        self.c.run('sed_enable_country')

    def rival(self, prestige, **extra):
        return dict(prestige=prestige, army_power_projection=80, is_subject=False,
                    is_at_war=False, is_country_type='recognized',
                    **{'relations:root': 40}, **extra)

    def test_rank_uses_closest_higher_prestige_and_ignores_decentralized(self):
        c = self.c
        next_country = self.rival(60)
        c.other_countries = [self.rival(100), next_country, self.rival(50)]
        decentralized = self.rival(55)
        decentralized['is_country_type'] = 'decentralized'
        c.other_countries.append(decentralized)
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_rank'], 3)
        self.assertIs(c.variables['sed_asc_next'], next_country)
        self.assertEqual(c.variables['sed_asc_gap'], 10)
        c.readings['prestige'] = 110
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_rank'], 1)
        self.assertNotIn('sed_asc_next', c.variables)

    def test_diplomacy_filters_rivals_and_keeps_subject_advice_separate(self):
        c = self.c
        partner = self.rival(60, has_overlapping_interests=True)
        enemy = self.rival(300, pacts=['rivalry'], has_overlapping_interests=True)
        c.other_countries = [enemy, partner, self.rival(400)]
        c.run('sed_asc_refresh')
        self.assertIs(c.variables['sed_asc_partner'], partner)
        c.readings.update(is_subject=True, overlord=enemy, liberty_desire=33)
        c.run('sed_asc_refresh')
        self.assertNotIn('sed_asc_partner', c.variables)
        self.assertIs(c.variables['sed_asc_overlord'], enemy)
        self.assertEqual(c.variables['sed_asc_liberty'], 33)

    def test_annual_snapshot_and_actions_are_not_counted_twice(self):
        c = self.c
        c.variables['sed_asc_queue_before'] = 0
        c.readings['construction_queue_num_queued_government_levels'] = 1
        c.variables['sed_tax_last_change_month'] = 1836 * 12
        c.run('sed_asc_record_actions')
        c.run('sed_asc_record_actions')
        c.readings.update(month=11, prestige=73)
        c.run('sed_asc_refresh')
        self.assertNotIn('sed_asc_prestige_delta', c.variables)
        c.readings.update(year=1837, month=0)
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_prestige_delta'], 23)
        self.assertEqual(c.variables['sed_asc_construction_annual'], 1)
        self.assertEqual(c.variables['sed_asc_tax_annual'], 1)
        self.assertEqual(c.variables['sed_asc_construction_count'], 0)
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_prestige_delta'], 23)

    def test_priority_moves_from_research_to_budget_or_war(self):
        c = self.c
        c.states = [state(infrastructure_delta=-1)]
        c.variables['sed_plan_goal'] = 1
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_priority'], 5)
        c.readings['net_total_income'] = -10
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_priority'], 3)
        c.readings['is_diplomatic_play_target'] = True
        c.run('sed_asc_refresh')
        self.assertEqual(c.variables['sed_asc_priority'], 2)
