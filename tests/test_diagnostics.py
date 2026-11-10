import tempfile
from pathlib import Path
import unittest
import zipfile

from tools.build_mod import ROOT, ACTION_NAMES, STATE_VARIABLES, SUPPLY_DIAGNOSTICS, SUPPLY_TARGETS, country_variables, outputs, runtime_variables
from tools.package_mod import package
from tools.pdx_script import parse, child, walk
from tools.validate import validate
from script_harness import Country, building, construction_sector, railway, state


def script_definitions():
    result = {}
    for name, data in outputs().items():
        if name.startswith('common/'):
            result.update((entry.key, entry.value) for entry in parse(data.decode('utf-8-sig')))
    return result


class DiagnosisTests(unittest.TestCase):
    def setUp(self):
        self.definitions = script_definitions()

    def country(self, **readings):
        country = Country(self.definitions, **readings)
        country.run('sed_enable_country')
        return country

    def test_modes_are_exclusive_and_auto_event_is_not_duplicated(self):
        c = self.country()
        self.assertIn('sed_mode_assisted', c.variables)
        for mode in ('automatic', 'manual', 'assisted', 'automatic'):
            c.run('sed_set_mode_' + mode)
            self.assertEqual([m for m in ('manual', 'assisted', 'automatic')
                              if 'sed_mode_' + m in c.variables], [mode])
        self.assertEqual(c.scheduled_events, [('sed_pulse.1', 23)])

    def test_auto_review_reports_blocker_without_queuing(self):
        cases = [
            ({'in_default': True}, {}, 10),
            ({'construction_queue_num_queued_government_levels': 1}, {}, 11),
            ({'construction_queue_num_queued_private_levels': 1}, {}, 11),
            ({'is_construction_paused': True}, {}, 12),
            ({}, {'advisor_auto_construction_enabled': True}, 13),
            ({}, {'zw_var_expand_building': True}, 13),
            ({}, {'aroai_autobuild': True}, 13),
            ({}, {}, 2),
        ]
        for readings, variables, expected in cases:
            with self.subTest(readings=readings, variables=variables):
                c = self.country(construction_queue_num_queued_government_levels=0)
                c.run('sed_set_mode_automatic')
                c.readings.update(readings)
                c.variables.update(variables)
                c.states = [] if expected == 2 else [state(-5, buildings=[railway()])]
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.variables['sed_auto_action_status'], expected)
                self.assertEqual(c.constructions, [])
                self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_independent_supply_chain_options_block_auto_and_update_live_panel(self):
        for option in ('zw_var_more_construction_sectors',
                       'zw_var_scsab_construct_railway',
                       'zw_var_scsab_construct_power_plant',
                       'zw_var_scsab_gov_admin',
                       'zw_var_scsab_gov_admin_for_tax'):
            with self.subTest(option=option):
                c = self.country(construction_queue_num_queued_government_levels=0)
                c.states = [state(-5, buildings=[railway()])]
                c.run('sed_set_mode_automatic')
                c.variables[option] = 1
                self.assertNotIn('zw_var_expand_building', c.variables)
                self.assertTrue(self.auto_panel_shown(c, 'current_competing'))
                self.assertFalse(self.auto_panel_shown(c, 'current_clear'))
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.variables['sed_auto_review_status'], 13)
                self.assertEqual(c.constructions, [])
                self.assertNotIn('sed_auto_last_attempt_month', c.variables)
                del c.variables[option]
                self.assertFalse(self.auto_panel_shown(c, 'current_competing'))
                self.assertTrue(self.auto_panel_shown(c, 'current_clear'))
                c.run('sed_auto_apply_monthly')
                self.assertEqual(len(c.constructions), 1)

    def test_institution_target_identifies_tool_without_enabling_general_admin(self):
        c = self.country(construction_queue_num_queued_government_levels=0)
        c.variables['zw_var_scsab_gov_admin_for_institution'] = 35
        c.states = [state(-5, buildings=[railway()])]
        self.assertFalse(c.condition(self.definitions['sed_competing_builder_configured'], c.country_scope()))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_coord_executor'], 2)
        self.assertEqual(c.variables['zw_var_scsab_construct_railway'], 1)
        self.assertNotIn('zw_var_scsab_gov_admin', c.variables)
        self.assertEqual(c.variables['zw_var_scsab_gov_admin_for_institution'], 35)

    def test_builder_configuration_does_not_block_assisted_or_mutate_foreign_options(self):
        c = self.country(construction_queue_num_queued_government_levels=0)
        option = 'zw_var_scsab_construct_railway'
        c.variables[option] = 3
        target = state(-5, buildings=[railway()])
        c.states = [target]
        c.run('sed_run_railway_approval', target)
        self.assertEqual(len(c.constructions), 1)
        c.run('sed_disable_country')
        self.assertEqual(c.variables[option], 3)

    def test_auto_review_queues_only_one_and_stops_at_month_limit(self):
        c = self.country(construction_queue_num_queued_government_levels=0)
        c.run('sed_set_mode_automatic')
        c.states = [state(-5, buildings=[railway()]), state(-2, buildings=[railway()])]
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_action_status'], 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_action_status'], 16)

    def test_supply_requires_shortage_active_output_and_available_producer(self):
        for item in SUPPLY_TARGETS:
            with self.subTest(good=item['good']):
                c = self.country()
                producer = building(item['building'])
                producer['production_methods'] = [item['methods'][0]]
                target = state(buildings=[producer])
                c.states = [target]
                effect = 'sed_refresh_supply_candidates'
                key = 'sed_' + item['good'] + '_candidates'
                c.run(effect)
                self.assertNotIn(key, c.variable_lists)
                c.market_goods[item['good']] = {'market_goods_has_goods_shortage': True}
                c.run(effect)
                self.assertEqual(c.variable_lists[key], [target])
                for field, invalid in [('production_methods', []), ('occupancy', 0.79),
                                       ('has_failed_hires', True),
                                       ('building_has_goods_shortage', True),
                                       ('level_after_queued_constructions', 2)]:
                    original = producer[field]
                    producer[field] = invalid
                    c.run(effect)
                    self.assertNotIn(key, c.variable_lists, field)
                    producer[field] = original
                c.run('sed_run_' + item['good'] + '_approval', target)
                self.assertEqual(len(c.constructions), 1)
                self.assertIn('sed_' + item['good'] + '_request_pending', target['variables'])
                c.run('sed_run_' + item['good'] + '_approval', target)
                self.assertEqual(len(c.constructions), 1)

    def test_manual_approval_allows_running_game_and_negative_balance(self):
        for action, factory in [('railway', railway), ('construction', construction_sector)]:
            with self.subTest(action=action):
                c = self.country(is_game_paused=False, net_total_income=-100,
                                 num_queued_government_constructions=3)
                target = state(-2 if action == 'railway' else 0, buildings=[factory()])
                c.run('sed_run_' + action + '_approval', target)
                self.assertEqual(len(c.constructions), 1)

    def test_auto_railway_priority_matches_recommendation_order(self):
        c = self.country(construction_queue_num_queued_government_levels=0)
        c.run('sed_set_mode_automatic')
        mild = state(-2, buildings=[railway()])
        severe = state(-10, buildings=[railway()])
        c.states = [mild, severe]
        c.run('sed_refresh_railway_candidates')
        self.assertIs(c.variable_lists['sed_railway_candidates'][0], severe)
        c.run('sed_auto_apply_monthly')
        self.assertIs(c.constructions[0]['state'], severe)

    def test_construction_refresh_preserves_unrelated_supply_pending(self):
        c = self.country()
        producer = building('building_logging_camp', queued_levels=1)
        target = state(buildings=[construction_sector(), producer])
        target['variables'].update(sed_construction_request_pending=True,
                                   sed_wood_request_pending=True)
        c.states = [target]
        c.run('sed_refresh_construction_candidates')
        self.assertNotIn('sed_construction_request_pending', target['variables'])
        self.assertIn('sed_wood_request_pending', target['variables'])

    def test_auto_failed_insertion_has_distinct_status_and_no_second_attempt(self):
        for action in ['railway'] + [item['good'] for item in SUPPLY_TARGETS]:
            with self.subTest(action=action):
                c = self.country(construction_queue_num_queued_government_levels=0)
                c.run('sed_set_mode_automatic')
                c.construction_accepted = False
                if action == 'railway':
                    producer = railway()
                else:
                    item = next(item for item in SUPPLY_TARGETS if item['good'] == action)
                    producer = building(item['building'])
                    producer['production_methods'] = [item['methods'][0]]
                    c.market_goods[action] = {'market_goods_has_goods_shortage': True}
                c.states = [state(-2 if action == 'railway' else 0, buildings=[producer]),
                            state(-3 if action == 'railway' else 0, buildings=[producer.copy()])]
                c.run('sed_auto_apply_monthly')
                self.assertEqual(len(c.constructions), 1)
                self.assertEqual(c.variables['sed_auto_action_status'], 15)
                self.assertTrue(all('sed_' + action + '_request_pending' not in target['variables']
                                    for target in c.states))
                self.assertNotIn('sed_queue_levels_before', c.variables)

    def test_scheduled_event_rechecks_mode_and_activation(self):
        event = next(entry.value for entry in parse(
            outputs()['events/sed_events.txt'].decode('utf-8-sig'))
                     if entry.key == 'sed_pulse.1')
        for mode in ('automatic', 'assisted', 'manual', 'disabled'):
            with self.subTest(mode=mode):
                c = self.country(construction_queue_num_queued_government_levels=0)
                c.states = [state(-3, buildings=[railway()])]
                c.run('sed_set_mode_automatic')
                if mode == 'disabled':
                    c.run('sed_disable_country')
                else:
                    c.run('sed_set_mode_' + mode)
                if c.condition(child(event, 'trigger'), c.country_scope()):
                    c.execute(child(event, 'immediate'), c.country_scope())
                self.assertEqual(len(c.constructions), int(mode == 'automatic'))
                self.assertNotIn('sed_auto_event_pending', c.variables)
                if mode != 'disabled':
                    c.run('sed_monthly_update')
                    self.assertEqual(len(c.scheduled_events), 2 if mode == 'automatic' else 1)

    def test_supply_rejection_counts_are_disjoint_and_reset_for_every_good(self):
        for item in SUPPLY_TARGETS:
            good = item['good']
            with self.subTest(good=good):
                c = self.country()
                c.market_goods[good] = {'market_goods_has_goods_shortage': True}

                def producer_state():
                    producer = building(item['building'])
                    producer['production_methods'] = [item['methods'][0]]
                    return state(buildings=[producer])

                targets = [producer_state() for _ in range(10)]
                targets[0]['buildings'][0]['level_after_queued_constructions'] = 2
                # Also fails incorporation; only the preceding queue reason counts.
                targets[0]['is_incorporated'] = False
                targets[1]['is_incorporated'] = False
                targets[1]['buildings'][0]['occupancy'] = 0.2
                targets[2]['buildings'][0]['occupancy'] = 0.79
                targets[2]['buildings'][0]['has_failed_hires'] = True
                targets[3]['buildings'][0]['has_failed_hires'] = True
                targets[3]['buildings'][0]['building_has_goods_shortage'] = True
                targets[4]['buildings'][0]['building_has_goods_shortage'] = True
                targets[4]['buildings'][0]['production_methods'] = []
                targets[5]['buildings'][0]['production_methods'] = []
                targets[5]['can_construct_building'] = False
                targets[6]['can_construct_building'] = False
                targets[8]['variables']['sed_' + good + '_ignored'] = True
                targets[8]['is_incorporated'] = False
                targets[9]['infrastructure_delta'] = -2
                c.states = targets + [state()]  # States without this producer are excluded.
                c.run('sed_refresh_supply_candidates')
                self.assertEqual(c.variables['sed_' + good + '_producer_states'], 10)
                for reason in SUPPLY_DIAGNOSTICS[1:]:
                    self.assertEqual(c.variables['sed_' + good + '_' + reason], 1, reason)
                self.assertEqual(c.variable_lists['sed_' + good + '_candidates'], [targets[7]])
                c.states = []
                c.run('sed_refresh_supply_candidates')
                for reason in SUPPLY_DIAGNOSTICS:
                    self.assertEqual(c.variables['sed_' + good + '_' + reason], 0, reason)
                self.assertNotIn('sed_' + good + '_candidates', c.variable_lists)

    def test_supply_empty_diagnostics_only_show_for_shortage_without_candidates(self):
        c = self.country()
        for item in SUPPLY_TARGETS:
            good = item['good']
            shown = child(self.definitions['sed_' + good + '_no_candidates_visible_sgui'], 'is_shown')
            self.assertFalse(c.condition(shown, c.country_scope()))
            c.market_goods[good] = {'market_goods_has_goods_shortage': True}
            self.assertTrue(c.condition(shown, c.country_scope()))
            c.variable_lists['sed_' + good + '_candidates'] = [state()]
            self.assertFalse(c.condition(shown, c.country_scope()))
            c.variable_lists.clear()
        c.run('sed_disable_country')
        self.assertFalse(c.condition(shown, c.country_scope()))

    def test_ignore_and_restore_all_action_types_in_every_mode(self):
        for name in ACTION_NAMES:
            for mode in ('manual', 'assisted', 'automatic'):
                with self.subTest(action=name, mode=mode):
                    c = self.country(num_queued_government_constructions=3,
                                     construction_queue_num_queued_government_levels=0)
                    c.run('sed_set_mode_' + mode)
                    if name == 'railway':
                        producer = railway()
                    elif name == 'construction':
                        producer = construction_sector()
                    else:
                        item = next(item for item in SUPPLY_TARGETS if item['good'] == name)
                        producer = building(item['building'])
                        producer['production_methods'] = [item['methods'][0]]
                        c.market_goods[name] = {'market_goods_has_goods_shortage': True}
                    target = state(-2 if name == 'railway' else 0, buildings=[producer])
                    c.states = [target]
                    c.run('sed_refresh_diagnostics')
                    gui = self.definitions['sed_ignore_' + name + '_sgui']
                    self.assertTrue(c.condition(child(gui, 'is_valid'), target))
                    c.execute(child(gui, 'effect'), target)
                    self.assertIn('sed_' + name + '_ignored', target['variables'])
                    self.assertNotIn('sed_' + name + '_candidates', c.variable_lists)
                    c.run('sed_refresh_diagnostics')
                    c.run('sed_monthly_update')
                    c.run('sed_run_' + name + '_approval', target)
                    self.assertEqual(c.constructions, [])
                    if mode == 'automatic':
                        c.run('sed_auto_apply_monthly')
                        self.assertEqual(c.constructions, [])
                    self.assertFalse(c.condition(child(gui, 'is_valid'), target))
                    restore = self.definitions['sed_restore_ignored_sgui']
                    self.assertTrue(c.condition(child(restore, 'is_shown'), c.country_scope()))
                    c.execute(child(restore, 'effect'), c.country_scope())
                    self.assertNotIn('sed_' + name + '_ignored', target['variables'])
                    self.assertEqual(c.variable_lists['sed_' + name + '_candidates'], [target])
                    self.assertEqual(c.constructions, [])
                    self.assertFalse(c.condition(child(restore, 'is_shown'), c.country_scope()))

    def test_ignored_preferences_are_specific_and_restore_preserves_queued_work(self):
        c = self.country(num_queued_government_constructions=3)
        wood = building('building_logging_camp')
        wood['production_methods'] = ['pm_simple_forestry']
        c.market_goods['wood'] = {'market_goods_has_goods_shortage': True}
        target = state(0, buildings=[wood, construction_sector()])
        other = state(-3, buildings=[railway(queued_levels=1)])
        other['variables']['sed_railway_request_pending'] = True
        c.states = [target, other]
        c.run('sed_ignore_construction', target)
        self.assertFalse(c.condition(self.definitions['sed_construction_candidate_eligible'], target))
        self.assertTrue(c.condition(self.definitions['sed_wood_candidate_eligible'], target))
        self.assertNotIn('sed_construction_ignored', other['variables'])
        c.run('sed_restore_ignored')
        self.assertIn('sed_railway_request_pending', other['variables'])
        self.assertEqual(other['buildings'][0]['level_after_queued_constructions'], 2)
        self.assertEqual(c.constructions, [])

    def test_ignore_and_restore_effects_revalidate_player_and_activation(self):
        for readings, disable in [({'is_player': False}, False), ({}, True)]:
            c = self.country(**readings)
            target = state(-2, buildings=[railway()])
            c.states = [target]
            if disable:
                c.run('sed_disable_country')
            c.run('sed_ignore_railway', target)
            self.assertNotIn('sed_railway_ignored', target['variables'])
            target['variables']['sed_railway_ignored'] = True
            c.run('sed_restore_ignored')
            self.assertIn('sed_railway_ignored', target['variables'])
            self.assertEqual(c.constructions, [])

    def test_auto_uses_another_state_after_preferred_railway_is_ignored(self):
        c = self.country(construction_queue_num_queued_government_levels=0)
        preferred = state(-10, buildings=[railway()])
        alternative = state(-2, buildings=[railway()])
        c.states = [preferred, alternative]
        c.run('sed_ignore_railway', preferred)
        self.assertEqual(c.variables['sed_railway_ignored_states'], 1)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertIs(c.constructions[0]['state'], alternative)
        self.assertIn('sed_railway_ignored', preferred['variables'])

    def test_details_controls_expand_and_collapse_without_running_economic_actions(self):
        c = self.country()
        shown = child(self.definitions['sed_details_visible_sgui'], 'is_shown')
        show = self.definitions['sed_show_details_sgui']
        hide = self.definitions['sed_hide_details_sgui']
        self.assertFalse(c.condition(shown, c.country_scope()))
        self.assertTrue(c.condition(child(show, 'is_valid'), c.country_scope()))
        c.execute(child(show, 'effect'), c.country_scope())
        self.assertTrue(c.condition(shown, c.country_scope()))
        self.assertFalse(c.condition(child(show, 'is_shown'), c.country_scope()))
        self.assertTrue(c.condition(child(hide, 'is_valid'), c.country_scope()))
        c.execute(child(hide, 'effect'), c.country_scope())
        self.assertFalse(c.condition(shown, c.country_scope()))
        self.assertEqual(c.constructions, [])
        c.run('sed_disable_country')
        self.assertFalse(c.condition(child(show, 'is_shown'), c.country_scope()))

    def test_controls_have_native_button_chrome_and_legible_text(self):
        tree = parse(outputs()['gui/journal_entry_widgets/sed_diagnostics.gui'].decode('utf-8-sig'))
        buttons = [entry.value for entry in walk(tree) if entry.key == 'button']
        self.assertGreaterEqual(len(buttons), 30)
        queue = next(block for block in buttons if child(block, 'text') == 'sed_open_queue')
        self.assertEqual(child(queue, 'onclick'),
                         "[InformationPanelBar.OpenPanelTab('production_methods', 'construction_queues')]")
        for block in buttons:
            styles = [entry.value for entry in block if entry.key == 'using']
            self.assertIn('default_button', styles)
            self.assertIn('fontsize_large', styles)
            dimensions = [int(entry.key) for entry in child(block, 'size')]
            self.assertGreaterEqual(dimensions[1], 48)
            self.assertLessEqual(dimensions[0], 500)
            self.assertTrue(child(block, 'onclick'))
        for entry in walk(tree):
            if entry.key == 'textbox':
                styles = [value.value for value in entry.value if value.key == 'using']
                self.assertTrue({'fontsize_large', 'fontsize_xxl'} & set(styles))
                self.assertEqual(child(entry.value, 'multiline'), 'yes')
                self.assertEqual(child(entry.value, 'minimumsize'), child(entry.value, 'maximumsize'))

    def test_recommendation_cards_grow_with_content_and_precede_diagnostics(self):
        text = outputs()['gui/journal_entry_widgets/sed_diagnostics.gui'].decode('utf-8-sig')
        tree = parse(text)
        # The former fixed row height clipped enlarged text and status messages.
        self.assertFalse(any(entry.key in ('fixedgridbox', 'addrow') for entry in walk(tree)))
        self.assertEqual(sum(entry.key == 'datamodel' for entry in walk(tree)), 4 * len(ACTION_NAMES))
        self.assertLess(text.index('text = "sed_recommendations_title"'),
                        text.index('text = "sed_metric_operating_balance"'))
        self.assertEqual(sum(entry.key == 'text' and entry.value == 'sed_supply_no_candidate'
                             for entry in walk(tree)), len(SUPPLY_TARGETS))

    def card_fixture(self, name):
        c = self.country(num_queued_government_constructions=3)
        if name == 'railway':
            producer = railway()
        elif name == 'construction':
            producer = construction_sector()
        else:
            item = next(item for item in SUPPLY_TARGETS if item['good'] == name)
            producer = building(item['building'])
            producer['production_methods'] = [item['methods'][0]]
            c.market_goods[name] = {'market_goods_has_goods_shortage': True}
        target = state(-2 if name == 'railway' else 0, buildings=[producer])
        c.states = [target]
        return c, target, producer

    def test_card_mode_switch_does_not_approve_and_suppresses_pending_auto_event(self):
        event = next(entry.value for entry in parse(
            outputs()['events/sed_events.txt'].decode('utf-8-sig')) if entry.key == 'sed_pulse.1')
        for name in ACTION_NAMES:
            for mode in ('manual', 'automatic'):
                with self.subTest(action=name, mode=mode):
                    c, target, producer = self.card_fixture(name)
                    c.run('sed_set_mode_' + mode)
                    gui = self.definitions[f'sed_{name}_switch_assisted_sgui']
                    self.assertTrue(c.condition(child(gui, 'is_valid'), target))
                    c.execute(child(gui, 'effect'), target)
                    self.assertIn('sed_mode_assisted', c.variables)
                    self.assertNotIn('sed_mode_automatic', c.variables)
                    self.assertNotIn('sed_mode_manual', c.variables)
                    self.assertFalse(c.condition(child(gui, 'is_shown'), target))
                    c.execute(child(event, 'immediate'), c.country_scope())
                    self.assertEqual(c.constructions, [])
                    self.assertNotIn(f'sed_{name}_request_pending', target['variables'])

    def test_card_ready_and_blocking_states_follow_current_mode_and_guards(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                shown = lambda suffix: c.condition(child(
                    self.definitions[f'sed_{name}_{suffix}_sgui'], 'is_shown'), target)
                self.assertTrue(shown('ready'))
                self.assertFalse(shown('switch_assisted'))
                self.assertFalse(shown('refresh_card'))
                c.readings['construction_queue_num_queued_private_levels'] = 1
                self.assertFalse(shown('ready'))
                self.assertTrue(shown('blocked_private'))
                c.readings.update(construction_queue_num_queued_private_levels=0, in_default=True)
                self.assertTrue(shown('blocked_default'))
                self.assertFalse(shown('ready'))
                c.run('sed_set_mode_manual')
                self.assertTrue(shown('switch_assisted'))
                self.assertFalse(shown('blocked_private'))
                self.assertFalse(shown('blocked_default'))
                target['variables'][f'sed_{name}_request_pending'] = True
                self.assertFalse(shown('switch_assisted'))
                self.assertFalse(shown('ready'))
                self.assertFalse(shown('refresh_card'))
                self.assertTrue(shown('pending'))
                c.run('sed_disable_country')
                self.assertFalse(shown('switch_assisted'))
                self.assertFalse(shown('ready'))

    def test_stale_card_refresh_revalidates_and_never_approves(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.run('sed_refresh_diagnostics')
                gui = self.definitions[f'sed_{name}_refresh_card_sgui']
                producer['occupancy'] = 0
                self.assertTrue(c.condition(child(gui, 'is_valid'), target))
                c.readings['gdp'] = 123
                c.execute(child(gui, 'effect'), target)
                self.assertEqual(c.variables['sed_gdp'], 123)
                self.assertNotIn(f'sed_{name}_candidates', c.variable_lists)
                self.assertEqual(c.constructions, [])
                producer['occupancy'] = 1
                c.readings['gdp'] = 456
                self.assertFalse(c.condition(child(gui, 'is_valid'), target))
                c.execute(child(gui, 'effect'), target)
                self.assertEqual(c.variables['sed_gdp'], 123)  # Callback revalidated.
                producer['occupancy'] = 0
                c.run('sed_disable_country')
                c.execute(child(gui, 'effect'), target)
                self.assertNotIn('sed_gdp', c.variables)
                self.assertEqual(c.constructions, [])

    def auto_panel_shown(self, c, suffix):
        return c.condition(child(self.definitions[f'sed_auto_{suffix}_visible_sgui'],
                                 'is_shown'), c.country_scope())

    def test_live_external_options_list_reports_each_option_without_mutating_state(self):
        options = {
            'advisor': 'advisor_auto_construction_enabled',
            'chains': 'zw_var_expand_building',
            'sectors': 'zw_var_more_construction_sectors',
            'railways': 'zw_var_scsab_construct_railway',
            'power': 'zw_var_scsab_construct_power_plant',
            'admin': 'zw_var_scsab_gov_admin',
            'tax': 'zw_var_scsab_gov_admin_for_tax',
            'aroai': 'aroai_autobuild',
        }
        c = self.country()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')  # Archived queue blocker, independent of options.
        self.assertFalse(self.auto_panel_shown(c, 'builders'))
        for name, option in options.items():
            with self.subTest(option=option):
                c.variables[option] = 1
                before = c.variables.copy()
                self.assertTrue(self.auto_panel_shown(c, 'builders'))
                self.assertTrue(self.auto_panel_shown(c, 'current_queue'))
                self.assertFalse(self.auto_panel_shown(c, 'current_competing'))
                for shown_name in options:
                    self.assertEqual(self.auto_panel_shown(c, 'builder_' + shown_name),
                                     shown_name == name)
                self.assertEqual(c.variables, before)
                self.assertEqual(c.constructions, [])
                del c.variables[option]
                self.assertFalse(self.auto_panel_shown(c, 'builders'))
                self.assertFalse(self.auto_panel_shown(c, 'builder_' + name))
        c.variables.update({option: 1 for option in options.values()})
        for name in options:
            self.assertTrue(self.auto_panel_shown(c, 'builder_' + name))
        for mode in ('manual', 'assisted'):
            c.run('sed_set_mode_' + mode)
            self.assertFalse(self.auto_panel_shown(c, 'builders'))
            for name in options:
                self.assertFalse(self.auto_panel_shown(c, 'builder_' + name))
        c.run('sed_set_mode_automatic')
        c.run('sed_disable_country')
        self.assertFalse(self.auto_panel_shown(c, 'builders'))
        for name in options:
            self.assertFalse(self.auto_panel_shown(c, 'builder_' + name))

    def test_auto_panel_explains_pending_review_before_any_execution(self):
        c = self.country()
        c.run('sed_set_mode_automatic')
        self.assertTrue(self.auto_panel_shown(c, 'pending'))
        self.assertTrue(self.auto_panel_shown(c, 'unrecorded'))
        self.assertTrue(self.auto_panel_shown(c, 'current_queue'))
        self.assertFalse(self.auto_panel_shown(c, 'idle'))
        self.assertFalse(self.auto_panel_shown(c, 'last_review'))
        c.run('sed_refresh_diagnostics')
        self.assertNotIn('sed_auto_review_status', c.variables)
        self.assertEqual(c.scheduled_events, [('sed_pulse.1', 23)])
        self.assertEqual(c.constructions, [])

    def test_auto_review_record_survives_refresh_and_mode_changes_but_cleans_on_disable(self):
        c = self.country(year=1840, month=11)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 11)
        self.assertEqual((c.variables['sed_auto_review_year'], c.variables['sed_auto_review_month']), (1840, 12))
        c.run('sed_set_mode_manual')
        self.assertEqual(c.variables['sed_auto_action_status'], 0)
        self.assertTrue(self.auto_panel_shown(c, 'status_queue'))
        self.assertTrue(self.auto_panel_shown(c, 'last_review'))
        self.assertFalse(self.auto_panel_shown(c, 'current_queue'))
        c.readings.update(year=1841, month=0)
        c.run('sed_refresh_diagnostics')
        self.assertEqual((c.variables['sed_auto_review_year'], c.variables['sed_auto_review_month']), (1840, 12))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual((c.variables['sed_auto_review_year'], c.variables['sed_auto_review_month']), (1841, 1))
        c.run('sed_disable_country')
        for name in ('status', 'year', 'month'):
            self.assertNotIn('sed_auto_review_' + name, c.variables)
        self.assertFalse(self.auto_panel_shown(c, 'last_review'))

    def test_auto_current_blockers_are_live_exclusive_and_do_not_rewrite_history(self):
        c = self.country()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')  # Queue occupied at the recorded review.
        c.readings.update(in_default=True, is_construction_paused=True)
        c.variables['advisor_auto_construction_enabled'] = True
        def only(expected):
            for name in ('default', 'queue', 'paused', 'competing', 'clear'):
                self.assertEqual(self.auto_panel_shown(c, 'current_' + name), name == expected)
            self.assertEqual(c.variables['sed_auto_review_status'], 11)
            self.assertEqual(c.constructions, [])
        only('default')
        c.readings['in_default'] = False
        only('queue')
        c.readings['construction_queue_num_queued_government_levels'] = 0
        only('paused')
        c.readings['is_construction_paused'] = False
        only('competing')
        del c.variables['advisor_auto_construction_enabled']
        only('clear')
        self.assertTrue(self.auto_panel_shown(c, 'status_queue'))  # Dated historical result.

    def test_legacy_status_does_not_invent_review_date_and_event_records_new_result(self):
        c = self.country()
        c.variables['sed_auto_action_status'] = 11  # Existing save from the previous version.
        c.run('sed_set_mode_automatic')
        self.assertTrue(self.auto_panel_shown(c, 'unrecorded'))
        self.assertFalse(self.auto_panel_shown(c, 'last_review'))
        self.assertFalse(self.auto_panel_shown(c, 'status_queue'))
        event = next(entry.value for entry in parse(
            outputs()['events/sed_events.txt'].decode('utf-8-sig')) if entry.key == 'sed_pulse.1')
        c.execute(child(event, 'immediate'), c.country_scope())
        self.assertTrue(self.auto_panel_shown(c, 'last_review'))
        self.assertTrue(self.auto_panel_shown(c, 'status_queue'))
        self.assertTrue(self.auto_panel_shown(c, 'idle'))
        self.assertFalse(self.auto_panel_shown(c, 'unrecorded'))
        self.assertFalse(self.auto_panel_shown(c, 'pending'))
        self.assertEqual(c.constructions, [])
        c.run('sed_monthly_update')
        self.assertTrue(self.auto_panel_shown(c, 'pending'))

    def test_direct_effects_refuse_manual_missing_and_conflicting_modes(self):
        for name in ACTION_NAMES:
            for modes in (('manual',), (), ('manual', 'assisted'),
                          ('manual', 'automatic'), ('manual', 'assisted', 'automatic')):
                with self.subTest(action=name, modes=modes):
                    c, target, producer = self.card_fixture(name)
                    c.readings['construction_queue_num_queued_government_levels'] = 0
                    for mode in ('manual', 'assisted', 'automatic'):
                        c.variables.pop('sed_mode_' + mode, None)
                    c.variables.update({'sed_mode_' + mode: True for mode in modes})
                    c.run(f'sed_run_{name}_approval', target)
                    self.assertEqual(c.constructions, [])
                    self.assertNotIn('sed_auto_last_attempt_month', c.variables)
                    self.assertNotIn(f'sed_{name}_request_pending', target['variables'])

    def test_direct_effect_revalidates_switch_to_manual_after_analysis(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                self.assertTrue(c.condition(self.definitions[f'sed_{name}_approval_valid'], target))
                c.run('sed_set_mode_manual')
                c.run(f'sed_run_{name}_approval', target)
                self.assertEqual(c.constructions, [])
                c.run('sed_set_mode_assisted')
                c.run(f'sed_run_{name}_approval', target)
                self.assertEqual(len(c.constructions), 1)
                self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_mutating_effects_revalidate_all_auto_guards_without_consuming_attempt(self):
        blockers = [
            ({'construction_queue_num_queued_government_levels': 1}, {}),
            ({'construction_queue_num_queued_private_levels': 1}, {}),
            ({'is_construction_paused': True}, {}),
            ({'in_default': True}, {}),
        ] + [({}, {option: 1}) for option in (
            'advisor_auto_construction_enabled', 'aroai_autobuild',
            'zw_var_expand_building', 'zw_var_more_construction_sectors',
            'zw_var_scsab_construct_railway', 'zw_var_scsab_construct_power_plant',
            'zw_var_scsab_gov_admin', 'zw_var_scsab_gov_admin_for_tax')]
        for name in ACTION_NAMES:
            for readings, variables in blockers:
                with self.subTest(action=name, readings=readings, variables=variables):
                    c, target, producer = self.card_fixture(name)
                    c.readings['construction_queue_num_queued_government_levels'] = 0
                    c.run('sed_set_mode_automatic')
                    self.assertTrue(c.condition(self.definitions[f'sed_{name}_approval_valid'], target))
                    c.readings.update(readings)
                    c.variables.update(variables)
                    c.run(f'sed_run_{name}_approval', target)
                    self.assertEqual(c.constructions, [])
                    self.assertNotIn('sed_auto_last_attempt_month', c.variables)
                    self.assertNotIn(f'sed_{name}_request_pending', target['variables'])
                    c.run('sed_set_mode_assisted')
                    c.run(f'sed_run_{name}_approval', target)
                    expected = 0 if readings.get('in_default') or readings.get(
                        'construction_queue_num_queued_private_levels') else 1
                    self.assertEqual(len(c.constructions), expected)
                    self.assertNotIn('sed_auto_last_attempt_month', c.variables)

    def test_auto_month_limit_survives_empty_queue_mode_changes_and_reenable(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.readings['construction_queue_num_queued_government_levels'] = 0
                c.run('sed_set_mode_automatic')
                c.run('sed_run_' + name + '_approval', target)
                self.assertEqual(len(c.constructions), 1)
                marker = c.variables['sed_auto_last_attempt_month']
                # A second state remains eligible after the first queued project is removed.
                other = state(-2 if name == 'railway' else 0, buildings=[producer.copy()])
                c.states.append(other)
                c.readings['construction_queue_num_queued_government_levels'] = 0
                for mode in ('manual', 'assisted', 'automatic'):
                    c.run('sed_set_mode_' + mode)
                c.run('sed_run_' + name + '_approval', other)
                c.run('sed_auto_apply_monthly')
                self.assertEqual(len(c.constructions), 1)
                self.assertEqual(c.variables['sed_auto_action_status'], 16)
                self.assertTrue(self.auto_panel_shown(c, 'current_month_limit'))
                self.assertFalse(self.auto_panel_shown(c, 'current_clear'))
                c.run('sed_disable_country')
                self.assertEqual(c.variables, {'sed_schema_version': 1,
                                               'sed_auto_last_attempt_month': marker})
                c.run('sed_enable_country')
                c.run('sed_set_mode_automatic')
                c.run('sed_auto_apply_monthly')
                self.assertEqual(len(c.constructions), 1)
                self.assertEqual(c.variables['sed_auto_action_status'], 16)

    def test_failed_auto_attempt_consumes_month_but_manual_approval_is_available(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.readings['construction_queue_num_queued_government_levels'] = 0
                c.run('sed_set_mode_automatic')
                c.construction_accepted = False
                c.run('sed_run_' + name + '_approval', target)
                self.assertEqual(len(c.constructions), 1)
                self.assertNotIn(f'sed_{name}_request_pending', target['variables'])
                marker = c.variables['sed_auto_last_attempt_month']
                c.construction_accepted = True
                c.run('sed_run_' + name + '_approval', target)
                self.assertEqual(len(c.constructions), 1)
                c.run('sed_set_mode_assisted')
                self.assertTrue(c.condition(child(self.definitions[f'sed_{name}_ready_sgui'],
                                                   'is_shown'), target))
                c.run('sed_run_' + name + '_approval', target)
                self.assertEqual(len(c.constructions), 2)
                self.assertEqual(c.variables['sed_auto_last_attempt_month'], marker)

    def test_auto_month_limit_reads_live_calendar_and_releases_after_year_rollover(self):
        for name in ACTION_NAMES:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.readings.update(year=1840, month=11,
                                  construction_queue_num_queued_government_levels=0)
                c.run('sed_set_mode_automatic')
                c.run('sed_run_' + name + '_approval', target)
                self.assertEqual(c.variables['sed_auto_last_attempt_month'], 1840 * 12 + 11)
                stale_diagnostic_month = c.variables['sed_month_key']
                other = state(-2 if name == 'railway' else 0, buildings=[producer.copy()])
                c.states.append(other)
                c.readings.update(year=1841, month=0,
                                  construction_queue_num_queued_government_levels=0)
                # No diagnostic refresh: the safety check must not use a stale sampled date.
                c.run('sed_run_' + name + '_approval', other)
                self.assertEqual(len(c.constructions), 2)
                self.assertEqual(c.variables['sed_auto_last_attempt_month'], 1841 * 12)
                self.assertEqual(c.variables['sed_month_key'], stale_diagnostic_month)

    def test_validator_rejects_cleanup_that_resets_automatic_month_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in outputs().items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            path = root / 'common/scripted_effects/sed_effects.txt'
            text = path.read_text(encoding='utf-8-sig').replace(
                'sed_disable_country = {',
                'sed_disable_country = {\n remove_variable = sed_auto_last_attempt_month', 1)
            path.write_text(text, encoding='utf-8-sig')
            errors = validate(root=root)
            self.assertTrue(any('monthly safety marker' in error for error in errors))

    def test_producer_and_sector_infrastructure_guard_revalidates_old_cards(self):
        for name in ACTION_NAMES[1:]:
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.run('sed_refresh_diagnostics')
                self.assertIn(target, c.variable_lists[f'sed_{name}_candidates'])
                target['infrastructure_delta'] = -1
                gui = self.definitions[f'sed_approve_{name}_sgui']
                self.assertFalse(c.condition(child(gui, 'is_valid'), target))
                notice = self.definitions[f'sed_{name}_infrastructure_blocked_sgui']
                self.assertTrue(c.condition(child(notice, 'is_shown'), target))
                c.execute(child(gui, 'effect'), target)
                self.assertEqual(c.constructions, [])
                c.run('sed_refresh_diagnostics')
                self.assertNotIn(f'sed_{name}_candidates', c.variable_lists)
                self.assertEqual(c.variables[f'sed_{name}_infrastructure_states'], 1)
                target['infrastructure_delta'] = 0
                self.assertTrue(c.condition(child(gui, 'is_valid'), target))
                self.assertFalse(c.condition(child(notice, 'is_shown'), target))
                c.execute(child(gui, 'effect'), target)
                self.assertEqual(len(c.constructions), 1)
        # A negative balance still permits the railway action intended to relieve it.
        c, target, producer = self.card_fixture('railway')
        c.readings['construction_queue_num_queued_government_levels'] = 0
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [{'building': 'building_railway', 'state': target}])

    def test_auto_supply_skips_infrastructure_deficit_without_consuming_month(self):
        for item in SUPPLY_TARGETS:
            name = item['good']
            with self.subTest(action=name):
                c, target, producer = self.card_fixture(name)
                c.readings['construction_queue_num_queued_government_levels'] = 0
                target['infrastructure_delta'] = -2
                c.run('sed_set_mode_automatic')
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.constructions, [])
                self.assertEqual(c.variables['sed_auto_action_status'], 2)
                self.assertNotIn('sed_auto_last_attempt_month', c.variables)
                healthy = state(0, buildings=[producer.copy()])
                c.states.append(healthy)
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.constructions, [{'building': item['building'], 'state': healthy}])
                self.assertNotIn(f'sed_{name}_request_pending', target['variables'])

    def test_construction_infrastructure_rejections_are_disjoint_and_reset(self):
        c = self.country(num_queued_government_constructions=3)
        ignored = state(-4, buildings=[construction_sector()])
        ignored['variables']['sed_construction_ignored'] = True
        eligible = state(0, buildings=[construction_sector()])
        c.states = [ignored, eligible,
                    state(-1, buildings=[construction_sector()]),
                    state(-2, buildings=[construction_sector(failed_hires=True)]),
                    state(-3, incorporated=False, buildings=[construction_sector()])]
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_construction_sector_states'], 5)
        reasons = ('ignored', 'not_ready', 'blocked', 'infrastructure')
        for reason in reasons:
            self.assertEqual(c.variables[f'sed_construction_{reason}_states'], 1, reason)
        self.assertEqual(c.variable_lists['sed_construction_candidates'], [eligible])
        c.states = []
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_construction_infrastructure_states'], 0)
        self.assertNotIn('sed_construction_candidates', c.variable_lists)

    def test_activation_collects_real_supplied_readings(self):
        c = self.country(gdp=12345, total_population=500, average_sol=13.25)
        self.assertEqual(c.variables['sed_gdp'], 12345)
        self.assertEqual(c.variables['sed_sol'], 13.25)
        self.assertEqual(c.variables['sed_gdp_per_capita'], 24.69)
        self.assertEqual(c.journals_added, 1)
        self.assertEqual(c.variables['sed_last_month'], 1)
        self.assertEqual(c.variables['sed_growth_available'], 0)

    def test_zero_population_credit_and_surplus_have_explicit_unavailable_states(self):
        c = self.country(total_population=0, credit=0, net_total_income=0)
        for name in ['per_capita', 'debt_share', 'reserve_weeks']:
            self.assertEqual(c.variables['sed_' + name + '_available'], 0)

    def test_reserve_coverage_is_scale_invariant_and_excludes_credit(self):
        small = self.country(gold_reserves=1000, net_total_income=-100, credit=1e9)
        large = self.country(gold_reserves=1e6, net_total_income=-1e5, credit=0)
        self.assertEqual(small.variables['sed_reserve_weeks'], 10)
        self.assertEqual(large.variables['sed_reserve_weeks'], 10)
        self.assertEqual(small.variables['sed_reserve_weeks_available'], 1)

    def test_negative_reserves_do_not_produce_negative_coverage(self):
        c = self.country(gold_reserves=-50, net_total_income=-100, in_default=True)
        self.assertEqual(c.variables['sed_reserve_weeks'], 0)
        self.assertEqual(c.variables['sed_in_default'], 1)

    def test_growth_requires_another_month_and_retains_baseline_on_repeat_refresh(self):
        c = self.country(gdp=10000)
        c.readings['gdp'] = 11000
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_growth_available'], 0)
        c.readings['month'] = 1
        c.run('sed_refresh_diagnostics')
        self.assertAlmostEqual(c.variables['sed_growth'], 0.1)
        self.assertEqual(c.variables['sed_growth_months'], 1)
        c.readings['gdp'] = 12000
        c.run('sed_refresh_diagnostics')
        self.assertAlmostEqual(c.variables['sed_growth'], 0.2)
        self.assertEqual(c.variables['sed_previous_gdp'], 10000)
        self.assertEqual(c.variables['sed_anchor_gdp'], 11000)

    def test_growth_after_gap_reports_actual_months_and_handles_year_rollover(self):
        c = self.country(year=1836, month=11, gdp=10000)
        c.readings.update(year=1837, month=2, gdp=8000)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_growth_months'], 3)
        self.assertAlmostEqual(c.variables['sed_growth'], -0.2)
        self.assertEqual(c.variables['sed_last_month'], 3)

    def test_zero_gdp_baseline_never_divides_by_zero(self):
        c = self.country(gdp=0)
        c.readings.update(month=1, gdp=100)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_growth_available'], 0)

    def test_state_and_building_counts_are_not_employment_estimates(self):
        c = self.country()
        c.states = [
            {'infrastructure_delta': -2, 'market_access': 0.8, 'buildings': [
                {'level': 1, 'building_has_goods_shortage': True, 'occupancy': 0.5, 'has_failed_hires': True},
                {'level': 0, 'building_has_goods_shortage': True, 'occupancy': 0, 'has_failed_hires': True}]},
            {'infrastructure_delta': 5, 'market_access': 1, 'buildings': [
                {'level': 4, 'building_has_goods_shortage': False, 'occupancy': 1, 'has_failed_hires': False}]}]
        c.run('sed_refresh_diagnostics')
        expected = {'states': 2, 'infrastructure_short_states': 1, 'low_access_states': 1,
                    'shortage_buildings': 1, 'understaffed_buildings': 1, 'hiring_failure_buildings': 1}
        for name, count in expected.items():
            self.assertEqual(c.variables['sed_' + name], count)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_shortage_buildings'], 1)

    def test_manual_schedule_suspends_monthly_reads_but_explicit_refresh_works(self):
        c = self.country(gdp=10000)
        c.execute(child(self.definitions['sed_manual_updates_sgui'], 'effect'), c.readings)
        c.readings.update(gdp=20000, month=1)
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_gdp'], 10000)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_gdp'], 20000)
        self.assertEqual(c.journals_added, 1)

    def test_monthly_schedule_resumes_and_updates_immediately(self):
        c = self.country()
        c.variables.pop('sed_monthly_refresh')
        c.readings.update(gdp=20000)
        c.execute(child(self.definitions['sed_monthly_updates_sgui'], 'effect'), c.readings)
        self.assertEqual(c.variables['sed_gdp'], 20000)
        c.readings.update(month=1, gdp=21000)
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_gdp'], 21000)
        self.assertEqual(c.journals_added, 1)

    def test_disable_cleans_every_runtime_variable_and_never_reactivates(self):
        c = self.country()
        for name in country_variables():
            c.variables.setdefault(name, 123)
        pending = state()
        pending['variables'].update({name: 123 for name in STATE_VARIABLES})
        c.states = [pending]
        c.variable_lists['sed_railway_candidates'] = [pending]
        c.variable_lists['sed_construction_candidates'] = [pending]
        c.run('sed_disable_country')
        # Seeded snapshots are restored before the Director's own state is removed.
        from tools.coordination import OPTIONS, ADVISOR_POLICY_OPTIONS
        foreign_options = [option for _, option, _ in OPTIONS] + [option for _, option in ADVISOR_POLICY_OPTIONS]
        expected = {'sed_schema_version': 1, **{option: 123 for option in foreign_options}}
        self.assertEqual(c.variables, expected)
        self.assertEqual(pending['variables'], {})
        self.assertNotIn('sed_railway_candidates', c.variable_lists)
        self.assertNotIn('sed_construction_candidates', c.variable_lists)
        c.run('sed_monthly_update')
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables, expected)
        c.active_journal = False  # The engine's JE outcome is outside this harness.
        c.run('sed_enable_country')
        self.assertEqual(c.variables['sed_growth_available'], 0)

    def test_nonplayer_country_never_gets_periodic_reads(self):
        c = self.country()
        c.readings.update(is_player=False, gdp=20000)
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_gdp'], 10000)

    def test_railway_candidate_requires_deficit_operation_and_free_queue(self):
        c = self.country()
        cases = {
            'eligible': (state(-2, buildings=[railway()]), True),
            'no_deficit': (state(0, buildings=[railway()]), False),
            'unincorporated': (state(-2, incorporated=False, buildings=[railway()]), False),
            'understaffed': (state(-2, buildings=[railway(occupancy=0.79)]), False),
            'failed_hires': (state(-2, buildings=[railway(failed_hires=True)]), False),
            'goods_shortage': (state(-2, buildings=[railway(shortage=True)]), False),
            'queued_expansion': (state(-2, buildings=[railway(queued_levels=1)]), False),
            'cannot_construct': (state(-2, can_construct=False, buildings=[railway()]), False),
            'no_railway': (state(-2), False),
        }
        for name, (target, expected) in cases.items():
            with self.subTest(name):
                self.assertEqual(
                    c.condition(c.definitions['sed_railway_candidate_eligible'], target), expected)

    def test_candidate_refresh_ranks_by_deficit_and_limits_results(self):
        states = [state(-1, buildings=[railway()]),
                  state(-9, buildings=[railway()]),
                  state(-3, buildings=[railway()]),
                  state(-5, buildings=[railway()]),
                  state(2, buildings=[railway()])]
        c = self.country()
        c.states = states
        c.run('sed_refresh_railway_candidates')
        self.assertEqual(c.variable_lists['sed_railway_candidates'],
                         [states[1], states[3], states[2]])

    def test_railway_rejection_counts_use_one_primary_reason(self):
        states = [state(1, buildings=[railway()]),
                  state(-1),
                  state(-2, buildings=[railway(occupancy=0.5)]),
                  state(-3, incorporated=False, buildings=[railway()]),
                  state(-4, can_construct=False, buildings=[railway()]),
                  state(-5, buildings=[railway()])]
        c = self.country()
        c.states = states
        c.run('sed_refresh_railway_candidates')
        self.assertEqual(c.variables['sed_railway_deficit_states'], 5)
        self.assertEqual(c.variables['sed_railway_no_railway_states'], 1)
        self.assertEqual(c.variables['sed_railway_not_ready_states'], 1)
        self.assertEqual(c.variables['sed_railway_blocked_states'], 2)
        self.assertEqual(c.variable_lists['sed_railway_candidates'], [states[-1]])
        self.assertEqual(
            c.variables['sed_railway_deficit_states'],
            c.variables['sed_railway_no_railway_states']
            + c.variables['sed_railway_not_ready_states']
            + c.variables['sed_railway_blocked_states'] + 1)

    def test_railway_rejection_counts_reset_between_readings(self):
        c = self.country()
        c.states = [state(-1), state(-2, buildings=[railway(occupancy=0.5)])]
        c.run('sed_refresh_railway_candidates')
        self.assertEqual(c.variables['sed_railway_deficit_states'], 2)
        c.states = [state(-1)]
        c.run('sed_refresh_railway_candidates')
        self.assertEqual(c.variables['sed_railway_deficit_states'], 1)
        self.assertEqual(c.variables['sed_railway_not_ready_states'], 0)

    def test_pending_request_stays_while_queued_and_clears_when_resolved(self):
        target = state(-2, buildings=[railway(queued_levels=1)])
        target['variables']['sed_railway_request_pending'] = True
        c = self.country()
        c.states = [target]
        c.run('sed_refresh_railway_candidates')
        self.assertTrue(target['variables']['sed_railway_request_pending'])
        self.assertNotIn('sed_railway_candidates', c.variable_lists)

        target['buildings'][0]['level_after_queued_constructions'] = 1
        c.run('sed_refresh_railway_candidates')
        self.assertNotIn('sed_railway_request_pending', target['variables'])
        self.assertEqual(c.variable_lists['sed_railway_candidates'], [target])

    def test_empty_opportunity_messages_distinguish_no_deficit_from_filters(self):
        c = self.country()

        def shown(name):
            block = next(entry.value for entry in self.definitions[name]
                         if entry.key == 'is_shown')
            return c.condition(block, c.country_scope())

        no_deficit = 'sed_no_infrastructure_opportunity_visible_sgui'
        filtered = 'sed_no_railway_candidate_visible_sgui'
        breakdown = 'sed_railway_breakdown_visible_sgui'
        recommendations = 'sed_recommendations_visible_sgui'
        c.variables['sed_infrastructure_short_states'] = 0
        self.assertTrue(shown(no_deficit))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(breakdown))
        self.assertFalse(shown(recommendations))
        c.variables['sed_infrastructure_short_states'] = 2
        self.assertFalse(shown(no_deficit))
        self.assertTrue(shown(filtered))
        self.assertTrue(shown(breakdown))
        c.variable_lists['sed_railway_candidates'] = [state()]
        self.assertFalse(shown(no_deficit))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(breakdown))
        self.assertTrue(shown(recommendations))

    def test_railway_approval_revalidates_every_guard(self):
        c = self.country()
        target = state(-2, buildings=[railway()])
        valid = lambda: c.condition(c.definitions['sed_railway_approval_valid'], target)
        self.assertTrue(valid())
        guards = {
            'enabled': ('variables', {'sed_enabled': None}),
            'default': ('readings', {'in_default': True}),
            'private_queue': ('readings', {'construction_queue_num_queued_private_levels': 1}),
        }
        for name, (area, value) in guards.items():
            with self.subTest(name):
                if area == 'variables':
                    original = dict(c.variables)
                    c.variables.clear()
                    self.assertFalse(valid())
                    c.variables.update(original)
                else:
                    original = {field: c.readings[field] for field in value}
                    c.readings.update(value)
                    self.assertFalse(valid())
                    c.readings.update(original)
        target['variables']['sed_railway_request_pending'] = True
        self.assertFalse(valid())
        del target['variables']['sed_railway_request_pending']
        target['buildings'][0]['level_after_queued_constructions'] = 2
        self.assertFalse(valid())

    def test_approved_railway_queues_one_level_and_marks_request(self):
        c = self.country()
        target = state(-2, buildings=[railway()])
        c.states = [target]
        c.run('sed_refresh_railway_candidates')
        c.run('sed_run_railway_approval', target)
        self.assertEqual(c.constructions,
                         [{'building': 'building_railway', 'state': target}])
        self.assertEqual(c.variables['sed_railway_action_status'], 1)
        self.assertTrue(target['variables']['sed_railway_request_pending'])
        self.assertNotIn('sed_queue_levels_before', c.variables)

    def test_failed_queue_insertion_is_reported_without_retry_or_pending_state(self):
        c = self.country()
        c.construction_accepted = False
        target = state(-2, buildings=[railway()])
        c.states = [target]
        c.run('sed_run_railway_approval', target)
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_railway_action_status'], 2)
        self.assertNotIn('sed_railway_request_pending', target['variables'])

    def test_invalid_approval_does_not_touch_the_construction_queue(self):
        c = self.country(in_default=True)
        target = state(-2, buildings=[railway()])
        c.states = [target]
        c.run('sed_run_railway_approval', target)
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_railway_action_status'], 0)
        self.assertNotIn('sed_railway_request_pending', target['variables'])

    def test_state_variables_are_separate_from_the_country_cleanup_registry(self):
        self.assertEqual(set(runtime_variables()) - set(country_variables()),
                         set(STATE_VARIABLES))

    def test_construction_candidate_requires_staffed_sector_and_free_queue(self):
        c = self.country()
        cases = {
            'eligible': (state(0, buildings=[construction_sector()]), True),
            'pending': (state(0, buildings=[construction_sector()]), False),
            'no_sector': (state(0), False),
            'unincorporated': (state(0, incorporated=False,
                                    buildings=[construction_sector()]), False),
            'understaffed': (state(0, buildings=[construction_sector(occupancy=0.89)]), False),
            'failed_hires': (state(0, buildings=[construction_sector(failed_hires=True)]), False),
            'goods_shortage': (state(0, buildings=[construction_sector(shortage=True)]), False),
            'queued_expansion': (state(0, buildings=[construction_sector(queued_levels=1)]), False),
            'cannot_construct': (state(0, can_construct=False,
                                       buildings=[construction_sector()]), False),
        }
        for name, (target, expected) in cases.items():
            with self.subTest(name):
                if name == 'pending':
                    target['variables']['sed_construction_request_pending'] = True
                self.assertEqual(
                    c.condition(c.definitions['sed_construction_candidate_eligible'], target),
                    expected)

    def test_construction_refresh_requires_queue_and_picks_most_populous_state(self):
        states = [state(0, population=500, buildings=[construction_sector()]),
                  state(0, population=5000, buildings=[construction_sector()]),
                  state(0, population=2000, buildings=[construction_sector()])]
        c = self.country()
        c.states = states
        c.run('sed_refresh_construction_candidates')
        self.assertNotIn('sed_construction_candidates', c.variable_lists)
        c.readings['num_queued_government_constructions'] = 3
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variable_lists['sed_construction_candidates'], [states[1]])

    def test_construction_rejection_counts_use_one_primary_reason(self):
        states = [state(0),
                  state(0, buildings=[construction_sector(occupancy=0.5)]),
                  state(0, incorporated=False, buildings=[construction_sector()]),
                  state(0, can_construct=False, buildings=[construction_sector()]),
                  state(0, buildings=[construction_sector()])]
        c = self.country(num_queued_government_constructions=3)
        c.states = states
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_construction_sector_states'], 4)
        self.assertEqual(c.variables['sed_construction_not_ready_states'], 1)
        self.assertEqual(c.variables['sed_construction_blocked_states'], 2)
        self.assertEqual(c.variable_lists['sed_construction_candidates'], [states[-1]])
        self.assertEqual(
            c.variables['sed_construction_sector_states'],
            c.variables['sed_construction_not_ready_states']
            + c.variables['sed_construction_blocked_states'] + 1)

    def test_construction_rejection_counts_reset_between_readings(self):
        c = self.country(num_queued_government_constructions=3)
        c.states = [state(0), state(0, buildings=[construction_sector(occupancy=0.5)])]
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_construction_sector_states'], 1)
        self.assertEqual(c.variables['sed_construction_not_ready_states'], 1)
        c.states = [state(0)]
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_construction_sector_states'], 0)
        self.assertEqual(c.variables['sed_construction_not_ready_states'], 0)

    def test_construction_pending_clears_when_queue_resolves(self):
        target = state(0, buildings=[construction_sector(queued_levels=1)])
        target['variables']['sed_construction_request_pending'] = True
        c = self.country(num_queued_government_constructions=3)
        c.states = [target]
        c.run('sed_refresh_construction_candidates')
        self.assertTrue(target['variables']['sed_construction_request_pending'])
        self.assertNotIn('sed_construction_candidates', c.variable_lists)
        target['buildings'][0]['level_after_queued_constructions'] = 1
        c.run('sed_refresh_construction_candidates')
        self.assertNotIn('sed_construction_request_pending', target['variables'])
        self.assertEqual(c.variable_lists['sed_construction_candidates'], [target])

    def test_construction_approval_revalidates_queue_and_budget_guards(self):
        c = self.country(num_queued_government_constructions=3)
        target = state(0, buildings=[construction_sector()])

        def valid():
            return c.condition(c.definitions['sed_construction_approval_valid'], target)

        self.assertTrue(valid())
        guards = {
            'queue': ('readings', 'num_queued_government_constructions', 2),
            'default': ('readings', 'in_default', True),
            'private_queue': ('readings', 'construction_queue_num_queued_private_levels', 1),
        }
        for name, (area, field, value) in guards.items():
            with self.subTest(name):
                original = c.readings[field]
                c.readings[field] = value
                self.assertFalse(valid())
                c.readings[field] = original
        original = dict(c.variables)
        c.variables.clear()
        self.assertFalse(valid())
        c.variables.update(original)
        target['variables']['sed_construction_request_pending'] = True
        self.assertFalse(valid())
        del target['variables']['sed_construction_request_pending']
        target['buildings'][0]['level_after_queued_constructions'] = 2
        self.assertFalse(valid())

    def test_blocked_buttons_name_the_first_failing_guard(self):
        for action, factory in [
                ('railway', lambda: state(-2, buildings=[railway()])),
                ('construction', lambda: state(0, buildings=[construction_sector()]))]:
            with self.subTest(action=action):
                c = self.country(num_queued_government_constructions=3)
                target = factory()
                guards = ['queue', 'private', 'default']
                if action == 'railway':
                    guards.remove('queue')

                def is_shown(name, target=target, c=c):
                    block = next(entry.value for entry in self.definitions[name]
                                 if entry.key == 'is_shown')
                    return c.condition(block, target)

                def assert_only(expected):
                    for guard in guards:
                        self.assertEqual(
                            is_shown(f'sed_{action}_blocked_{guard}_sgui'),
                            guard == expected, guard)

                assert_only(None)
                cases = {
                    'queue': ('num_queued_government_constructions', 2),
                    'private': ('construction_queue_num_queued_private_levels', 1),
                    'default': ('in_default', True),
                }
                for guard in guards:
                    with self.subTest(guard=guard):
                        field, value = cases[guard]
                        original = c.readings[field]
                        c.readings[field] = value
                        assert_only(guard)
                        c.readings[field] = original
                # Cascading: an earlier failing guard wins over later ones.
                c.readings.update(
                    in_default=True,
                    construction_queue_num_queued_private_levels=1)
                assert_only('private')
                # Ineligible states name no guard.
                ineligible = state(-2, buildings=[])
                self.assertFalse(any(
                    c.condition(next(entry.value for entry in self.definitions[name]
                                     if entry.key == 'is_shown'), ineligible)
                    for name in [f'sed_{action}_blocked_{g}_sgui' for g in guards]))

    def test_approved_construction_sector_queues_one_level_and_marks_request(self):
        c = self.country(num_queued_government_constructions=3)
        target = state(0, buildings=[construction_sector()])
        c.states = [target]
        c.run('sed_refresh_construction_candidates')
        c.run('sed_run_construction_approval', target)
        self.assertEqual(c.constructions,
                         [{'building': 'building_construction_sector', 'state': target}])
        self.assertEqual(c.variables['sed_construction_action_status'], 1)
        self.assertTrue(target['variables']['sed_construction_request_pending'])
        self.assertNotIn('sed_queue_levels_before', c.variables)

    def test_failed_construction_queue_insertion_is_reported_without_retry(self):
        c = self.country(num_queued_government_constructions=3)
        c.construction_accepted = False
        target = state(0, buildings=[construction_sector()])
        c.states = [target]
        c.run('sed_run_construction_approval', target)
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_construction_action_status'], 2)
        self.assertNotIn('sed_construction_request_pending', target['variables'])

    def test_construction_empty_messages_follow_queue_pressure(self):
        c = self.country()

        def shown(name):
            block = next(entry.value for entry in self.definitions[name]
                         if entry.key == 'is_shown')
            return c.condition(block, c.country_scope())

        short = 'sed_no_construction_queue_visible_sgui'
        filtered = 'sed_no_construction_candidate_visible_sgui'
        breakdown = 'sed_construction_breakdown_visible_sgui'
        recommendations = 'sed_construction_recommendations_visible_sgui'
        c.readings['num_queued_government_constructions'] = 2
        self.assertTrue(shown(short))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(breakdown))
        self.assertFalse(shown(recommendations))
        c.readings['num_queued_government_constructions'] = 3
        self.assertFalse(shown(short))
        self.assertTrue(shown(filtered))
        self.assertTrue(shown(breakdown))
        c.variable_lists['sed_construction_candidates'] = [state()]
        self.assertFalse(shown(short))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(breakdown))
        self.assertTrue(shown(recommendations))

    def test_repository_passes_reference_and_action_boundary_checks(self):
        self.assertEqual(validate(), [])

    def test_validator_rejects_foreign_state_and_missing_localization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in outputs().items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            path = root / 'common/scripted_effects/sed_effects.txt'
            path.write_text(path.read_text(encoding='utf-8-sig').replace(
                'remove_variable = sed_balance', 'remove_variable = advisor_enabled'), encoding='utf-8-sig')
            path = root / 'localization/english/sed_l_english.yml'
            path.write_text(path.read_text(encoding='utf-8-sig').replace(' sed_refresh:0 ', ' removed_key:0 '), encoding='utf-8-sig')
            errors = validate(root=root)
            self.assertTrue(any('Foreign variable removed' in error for error in errors))
            self.assertTrue(any('Localization key sets differ' in error for error in errors))

    def test_validator_rejects_action_building_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, data in outputs().items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            path = root / 'common/scripted_effects/sed_effects.txt'
            text = path.read_text(encoding='utf-8-sig').replace(
                ' start_building_construction = building_railway',
                ' start_building_construction = building_construction_sector')
            path.write_text(text, encoding='utf-8-sig')
            errors = validate(root=root)
            self.assertTrue(any('declared building level' in error for error in errors))

    def test_release_has_correct_layout_and_no_research_or_saves(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = package(Path(directory) / 'sed.zip')
            with zipfile.ZipFile(archive) as release:
                names = release.namelist()
                self.assertIn('Smart Economy Director.mod', names)
                self.assertIn('Smart Economy Director/descriptor.mod', names)
                self.assertIn('Smart Economy Director/.metadata/metadata.json', names)
                self.assertTrue(all(name.startswith('Smart Economy Director') for name in names))
                self.assertFalse(any(name.endswith('.v3') or '/docs/' in name or '/tests/' in name for name in names))


if __name__ == '__main__':
    unittest.main()
