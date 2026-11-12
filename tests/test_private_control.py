"""Read-only view of Controllable Private Construction flags.

The Director never writes these variables and never injects can_build_* rules;
these tests only pin the detection/reading contract and the panel wiring.
Synthetic test: does not prove the other mod's restrictions apply in game.
"""
import unittest

from tools.build_mod import COMPETING_BUILDERS, PRIVATE_CONTROL_FLAGS, localization, outputs


def body(script, key):
    start = script.index(f'{key} = {{')
    end = script.index('\n}', start)
    return script[start:end]


class PrivateControlTests(unittest.TestCase):
    def setUp(self):
        self.definitions = {name: data.decode('utf-8-sig') for name, data in outputs().items()}
        self.triggers = self.definitions['common/scripted_triggers/sed_triggers.txt']
        self.guis = self.definitions['common/scripted_guis/sed_scripted_guis.txt']

    def test_detection_reads_every_known_flag_and_nothing_else(self):
        trigger = body(self.triggers, 'sed_private_control_configured')
        for name, option, pt, en in PRIVATE_CONTROL_FLAGS:
            with self.subTest(flag=option):
                self.assertIn(f'has_variable = {option}', trigger)
        self.assertEqual(trigger.count('has_variable'), len(PRIVATE_CONTROL_FLAGS))
        # The panel explains the known restrictions one by one.
        for name, option, pt, en in PRIVATE_CONTROL_FLAGS:
            self.assertIn(option, self.guis)

    def test_control_flags_do_not_block_the_direct_executor(self):
        # Restricting private investors is not a construction automation: the
        # Director must keep its own executable mode available.
        competing = body(self.triggers, 'sed_competing_builder_configured')
        for name, option, pt, en in COMPETING_BUILDERS:
            self.assertIn(f'has_variable = {option}', competing)
        self.assertNotIn('zw_var_auto_invest', competing)
        self.assertNotIn('zw_var_no_foreign_private_investment', competing)
        self.assertNotIn('zw_var_intervene_investment_from_abroad', competing)
        self.assertNotIn('sed_private_control_configured = yes',
                         body(self.triggers, 'sed_auto_executor_safe'))

    def test_panel_shows_the_section_only_when_a_flag_is_set(self):
        self.assertIn('has_variable = sed_enabled sed_private_control_configured = yes', self.guis)
        hint = 'sed_auto_current_queue_control_visible_sgui ='
        line = next(l for l in self.guis.splitlines() if l.startswith(hint))
        self.assertIn('construction_queue_num_queued_private_levels > 0', line)
        self.assertIn('sed_private_control_configured = yes', line)

    def test_localization_covers_every_toggle_in_both_languages(self):
        keys = ['sed_private_control_title', 'sed_private_control_help',
                'sed_auto_current_queue_control']
        keys += [f'sed_private_control_{name}' for name, option, pt, en in PRIVATE_CONTROL_FLAGS]
        for language in ('braz_por', 'english'):
            text = localization(language)
            for key in keys:
                with self.subTest(language=language, key=key):
                    self.assertIn(f' {key}:0 "', text)


if __name__ == '__main__':
    unittest.main()
