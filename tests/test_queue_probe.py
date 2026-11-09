"""Rules and packaging checks for the optional diagnostic, not engine tests."""
import tempfile
from pathlib import Path
import unittest
import zipfile

from tools.build_queue_probe import (
    BUILDINGS, BUILDING_VARIABLES, COUNTRY_VARIABLES, NAME, outputs, package, validate,
)
from tools.build_mod import outputs as director_outputs
from tools.pdx_script import parse
from script_harness import Country, building, state


def definitions():
    return {entry.key: entry.value for name, data in outputs().items()
            if name.startswith('common/') for entry in parse(data.decode('utf-8-sig'))}


class QueueProbeTests(unittest.TestCase):
    def test_snapshot_distinguishes_projects_levels_and_per_building_difference(self):
        c = Country(definitions(), num_queued_government_constructions=2,
                    num_queued_private_constructions=1,
                    construction_queue_num_queued_government_levels=5,
                    construction_queue_num_queued_private_levels=3)
        existing = building('building_railway', level=4, queued_levels=2)
        first = building('building_iron_mine', level=0, queued_levels=1)
        untouched = building('building_urban_center', level=5, queued_levels=9)
        c.states = [state(buildings=[existing, first, untouched])]
        c.run('sedqp_enable')
        self.assertEqual([c.variables['sedqp_' + key] for key in
                          ('public_projects', 'private_projects', 'public_levels', 'private_levels')],
                         [2, 1, 5, 3])
        self.assertEqual(c.variable_lists['sedqp_buildings'], [existing, first])
        self.assertEqual(existing['variables']['sedqp_delta'], 2)
        self.assertEqual(first['variables']['sedqp_current'], 0)
        self.assertEqual(first['variables']['sedqp_after'], 1)
        self.assertNotIn('variables', untouched)
        self.assertEqual(c.constructions, [])

    def test_refresh_replaces_snapshot_and_does_not_clamp_unexpected_negative_difference(self):
        c = Country(definitions())
        b = building(BUILDINGS[0], level=4, queued_levels=2)
        c.states = [state(buildings=[b])]
        c.run('sedqp_enable')
        b['level_after_queued_constructions'] = 3  # Surface anomalies, do not invent zero.
        c.readings.update(month=4, year=1840)
        c.run('sedqp_refresh')
        self.assertEqual(c.variable_lists['sedqp_buildings'], [b])
        self.assertEqual(b['variables']['sedqp_delta'], -1)
        self.assertEqual((c.variables['sedqp_month'], c.variables['sedqp_year']), (5, 1840))
        c.states = []
        c.run('sedqp_refresh')
        self.assertNotIn('sedqp_buildings', c.variable_lists)
        self.assertEqual(c.constructions, [])

    def test_disabled_and_nonplayer_do_not_collect(self):
        c = Country(definitions())
        c.run('sedqp_refresh')
        self.assertEqual(c.variables, {})
        c.readings['is_player'] = False
        c.run('sedqp_enable')
        self.assertEqual(c.variables, {})
        self.assertEqual(c.journals_added, 0)

    def test_cleanup_removes_only_probe_state_and_preserves_director_and_projects(self):
        c = Country(definitions())
        b = building(BUILDINGS[0], level=2, queued_levels=4)
        b['variables'] = {'sed_example': 17}
        c.states = [state(buildings=[b])]
        c.variables['sed_enabled'] = True
        c.variable_lists['sed_railway_candidates'] = c.states[:]
        c.run('sedqp_enable')
        self.assertTrue(set(COUNTRY_VARIABLES) <= set(c.variables))
        self.assertTrue(set(BUILDING_VARIABLES) <= set(b['variables']))
        c.run('sedqp_disable')
        self.assertEqual(c.variables, {'sed_enabled': True})
        self.assertEqual(b['variables'], {'sed_example': 17})
        self.assertIn('sed_railway_candidates', c.variable_lists)
        self.assertEqual(b['level_after_queued_constructions'], 6)
        self.assertEqual(c.constructions, [])

    def test_diagnostic_rejects_construction_and_foreign_writes(self):
        for key, source, replacement in [
            ('common/scripted_effects/sedqp_effects.txt', 'sedqp_refresh = yes', 'start_building_construction = building_railway'),
            ('common/scripted_effects/sedqp_effects.txt', 'name = sedqp_current', 'name = advisor_enabled'),
            ('common/decisions/sedqp_decisions.txt', 'sedqp_enable = yes', 'start_building_construction = building_railway'),
            ('common/scripted_guis/sedqp_guis.txt', 'sedqp_refresh = yes', 'trigger_event = bad_event')]:
            with self.subTest(replacement=replacement):
                files = outputs()
                files[key] = files[key].replace(source.encode(), replacement.encode(), 1)
                with self.assertRaises(ValueError):
                    validate(files)

    def test_probe_package_is_deterministic_and_separate_from_director(self):
        self.assertFalse(any('sedqp' in name or 'Probe' in name for name in director_outputs()))
        with tempfile.TemporaryDirectory() as tmp:
            one, two = package(Path(tmp) / 'one.zip'), package(Path(tmp) / 'two.zip')
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                expected = {name if name == NAME + '.mod' else NAME + '/' + name: data
                            for name, data in outputs().items()}
                self.assertEqual(set(archive.namelist()), set(expected))
                self.assertTrue(all(archive.read(name) == data for name, data in expected.items()))
        self.assertFalse(any(name.startswith(('events/', 'common/on_actions/')) for name in outputs()))


if __name__ == '__main__':
    unittest.main()
