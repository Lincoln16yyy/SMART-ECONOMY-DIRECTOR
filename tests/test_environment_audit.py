"""Regression cases for research evidence, not tests of the Director in the engine."""

import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from tools.audit_environment import audit, definitions, installed_mod_name, save_summary


class SourceAuditTests(unittest.TestCase):
    def test_comments_quotes_nested_blocks_and_line_numbers(self):
        text = '\ufeff# fake = { }\nreal = { text = "# }" inner = { x = 1 } }\nnext = { }'
        result = definitions(text)
        self.assertEqual([(v['id'], v['line']) for v in result], [('real', 2), ('next', 3)])

    def test_injection_is_distinguished_from_full_definition(self):
        result = definitions('INJECT:building_x = {} building_x = {}')
        self.assertEqual([v['operation'] for v in result], ['INJECT', 'definition'])
        self.assertEqual([v['id'] for v in result], ['building_x', 'building_x'])

    def test_inject_or_create_and_try_inject_share_the_target_identity(self):
        result = definitions('INJECT_OR_CREATE:x = {} TRY_INJECT:x = {} REPLACE:x = {}')
        self.assertEqual([v['id'] for v in result], ['x', 'x', 'x'])
        self.assertEqual([v['operation'] for v in result],
                         ['INJECT_OR_CREATE', 'TRY_INJECT', 'REPLACE'])

    def test_unbalanced_input_is_not_silently_accepted(self):
        for value in ['x = {', '} x = {}']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                definitions(value)

    def test_native_and_wine_paths(self):
        self.assertEqual(installed_mod_name('C:\\users\\x\\mod\\A'), 'A')
        self.assertEqual(installed_mod_name('/home/x/mod/A'), 'A')

    def test_field_comparison_ignores_comments_and_whitespace(self):
        first = definitions('pm = { ai_value = 1 goods = { x = 3 } }', True)[0]['fields']
        second = definitions('pm={# note\nai_value=1 goods={ x=3 }}', True)[0]['fields']
        changed = definitions('pm = { ai_value=2 goods={ x=4 } }', True)[0]['fields']
        self.assertEqual(first, second)
        self.assertNotEqual(first['goods'], changed['goods'])

    def test_repeated_fields_are_preserved_in_fingerprint(self):
        fields = definitions('pm={ x=1 x=2 y={ z=1 } }', True)[0]['fields']
        self.assertEqual(len(fields['x']), 2)
        self.assertEqual(len(fields['y']), 1)

    def test_save_markers_never_become_active_flags(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'binary.v3'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('gamestate', b'\x00advisor_enabled advisor_auto_construction_enabled')
            result = save_summary(path)
            self.assertEqual(result['encoding'], 'binary')
            self.assertEqual(result['automation_state'], 'unverified_requires_country_scoped_decode')
            self.assertEqual(result['marker_occurrences_not_active_flags']['advisor_enabled'], 1)

    def test_collisions_missing_mods_and_archive_are_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            game = base / 'install/game'
            user = base / 'user'
            for path in [game / 'common/buildings', game.parent / 'launcher', user]:
                path.mkdir(parents=True)
            (game.parent / 'launcher/launcher-settings.json').write_text('{"rawVersion":"1.15.0"}')
            (game / 'common/buildings/base.txt').write_text('building_x = {}')
            (user / 'content_load.json').write_text(json.dumps({'enabledMods': [
                {'path': 'C:\\mod\\A'}, {'path': 'C:\\mod\\B'}, {'path': 'C:\\mod\\missing'}]}))
            for mod in ['A', 'B']:
                folder = user / 'mod' / mod / 'common/buildings'
                folder.mkdir(parents=True)
                (folder / 'base.txt').write_text('building_x = {}')
            vanilla_pm = game / 'common/production_methods'
            mod_pm = user / 'mod/A/common/production_methods'
            vanilla_pm.mkdir()
            mod_pm.mkdir()
            (vanilla_pm / 'pm.txt').write_text('pm_x={ ai_value=1 goods={ x=3 } }')
            (mod_pm / 'pm.txt').write_text('pm_x={ ai_value=2 goods={ x=4 } }')
            archive_path = base / 'kuromi.zip'
            with zipfile.ZipFile(archive_path, 'w') as archive:
                archive.writestr('K/.metadata/metadata.json', '{"version":"8.0"}')
                archive.writestr('K/common/buildings/k.txt', 'INJECT:building_x = {}')
            result = audit(game, user, archive_path)
            self.assertEqual(len(result['shared_top_level_entries']), 1)
            self.assertFalse(result['mods'][2]['found'])
            self.assertEqual(result['mods'][0]['same_path_as_vanilla'],
                             ['common/buildings/base.txt', 'common/production_methods/pm.txt'])
            pm = next(e for e in result['mods'][0]['entries_also_in_vanilla'] if e['id'] == 'pm_x')
            self.assertEqual(pm['different_token_fields_from_vanilla'], ['ai_value', 'goods'])
            candidate = result['kuromi_archive']['entries_also_in_enabled_mods'][0]
            self.assertEqual(candidate['operation'], 'INJECT')
            self.assertEqual(candidate['enabled_providers'], ['A', 'B'])
            self.assertEqual(result['parse_issues'], [])


if __name__ == '__main__':
    unittest.main()
