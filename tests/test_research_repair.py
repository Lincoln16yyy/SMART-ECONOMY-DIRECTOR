import tempfile
import unittest
from pathlib import Path
from tools.repair_government_research import technologies
from tools.pdx_script import parse


class ResearchRepairTests(unittest.TestCase):
    def test_general_candidates_preserve_real_prerequisites(self):
        with tempfile.TemporaryDirectory() as temporary:
            game = Path(temporary)
            folder = game / 'common/technology/technologies'
            folder.mkdir(parents=True)
            (folder / 'test.txt').write_text('''
                first = { era = era_1 category = production }
                second = { era = era_2 category = society unlocking_technologies = { first } }
                disabled = { era = era_1 category = military can_research = no }
            ''')
            data = technologies(game)
            self.assertEqual(data['second']['requirements'], ['first'])
            self.assertEqual(data['second']['era'], 2)
            self.assertNotIn('disabled', data)
