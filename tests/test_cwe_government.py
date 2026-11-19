"""Regression coverage for the law ranking's empty-slot fallback."""

import unittest

from script_harness import Country
from tools.cwe_government import score_fallbacks
from tools.pdx_script import parse


class GovernmentRankingTests(unittest.TestCase):
    def test_empty_and_present_slots_have_numeric_scores(self):
        definitions = {entry.key: entry.value for entry in parse(score_fallbacks())}
        country = Country(definitions)
        for slot in (1, 2, 3):
            with self.subTest(slot=slot):
                score = f'sg_cwe_top_{slot}_score_or_empty'
                self.assertEqual(country.number(score, country.country_scope()), -1000)
                country.variables[f'sg_top_{slot}_score'] = 52
                self.assertEqual(country.number(score, country.country_scope()), 52)
