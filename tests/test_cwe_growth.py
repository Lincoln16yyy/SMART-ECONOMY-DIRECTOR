"""Exercise the growth preset and its construction limits in isolation."""

import unittest
from unittest.mock import patch

from script_harness import Country
from tools.cwe_compat import budget_scripts
from tools.cwe_growth import SWITCHES, preset_scripts
from tools.pdx_script import parse


class GrowthPresetTests(unittest.TestCase):
    def setUp(self):
        _, values = budget_scripts({'base': {'pm_construction_0': 200}})
        scripts = preset_scripts()
        script = values + scripts['common/scripted_effects/sed_cwe_growth_effects.txt']
        script += scripts['common/scripted_triggers/sed_cwe_growth_triggers.txt']
        script += 'sed_cwe_ensure_journal = {} sed_cwe_disable_country = { remove_variable = sed_cwe_enabled }'
        self.country = Country({entry.key: entry.value for entry in parse(script)})
        self.country.active_journal = True  # Already set up in this save.

    def test_start_and_pause_the_automatic_managers(self):
        c = self.country
        c.run('sed_cwe_start_growth_effect')
        self.assertTrue(c.variables['sed_cwe_enabled'])
        self.assertTrue(all(c.variables[key] == 1 for key in SWITCHES))
        self.assertEqual(c.variables['OGAS_building_queue_config'], 12)
        self.assertEqual(c.variables['cnm_pm_manage_frequency'], 2)
        c.run('sed_cwe_stop_growth_effect')
        self.assertTrue(all(c.variables[key] == 0 for key in SWITCHES))
        self.assertNotIn('sed_cwe_enabled', c.variables)

    def test_growth_blocks_new_work_when_queue_or_budget_is_exhausted(self):
        c = self.country
        c.run('sed_cwe_start_growth_effect')
        guard = c.definitions['sed_cwe_growth_allows_queue']
        for reading, value in [('net_total_income', -1), ('gold_reserves', 199),
                               ('construction_queue_government_duration', 12),
                               ('is_construction_paused', True)]:
            with self.subTest(reading=reading):
                self.assertTrue(c.condition(guard, c.country_scope()))
                with patch.dict(c.readings, {reading: value}):
                    self.assertFalse(c.condition(guard, c.country_scope()))
