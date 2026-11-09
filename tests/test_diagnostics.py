import tempfile
from pathlib import Path
import unittest
import zipfile

from tools.build_mod import ROOT, country_variables, outputs, runtime_variables
from tools.package_mod import package
from tools.pdx_script import parse, child
from tools.validate import validate
from script_harness import Country, construction_sector, railway, state


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
        pending['variables']['sed_railway_request_pending'] = 123
        pending['variables']['sed_construction_request_pending'] = 123
        c.states = [pending]
        c.variable_lists['sed_railway_candidates'] = [pending]
        c.variable_lists['sed_construction_candidates'] = [pending]
        c.run('sed_disable_country')
        self.assertEqual(c.variables, {'sed_schema_version': 1})
        self.assertEqual(pending['variables'], {})
        self.assertNotIn('sed_railway_candidates', c.variable_lists)
        self.assertNotIn('sed_construction_candidates', c.variable_lists)
        c.run('sed_monthly_update')
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables, {'sed_schema_version': 1})
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
        recommendations = 'sed_recommendations_visible_sgui'
        c.variables['sed_infrastructure_short_states'] = 0
        self.assertTrue(shown(no_deficit))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(recommendations))
        c.variables['sed_infrastructure_short_states'] = 2
        self.assertFalse(shown(no_deficit))
        self.assertTrue(shown(filtered))
        c.variable_lists['sed_railway_candidates'] = [state()]
        self.assertFalse(shown(no_deficit))
        self.assertFalse(shown(filtered))
        self.assertTrue(shown(recommendations))

    def test_railway_approval_revalidates_every_guard(self):
        c = self.country()
        target = state(-2, buildings=[railway()])
        valid = lambda: c.condition(c.definitions['sed_railway_approval_valid'], target)
        self.assertTrue(valid())
        guards = {
            'enabled': ('variables', {'sed_enabled': None}),
            'paused': ('readings', {'is_game_paused': False}),
            'default': ('readings', {'in_default': True}),
            'negative_balance': ('readings', {'net_total_income': -1}),
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
                    original = c.readings[name] if name in c.readings else None
                    c.readings.update(value)
                    self.assertFalse(valid())
                    c.readings.update({name: original})
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
        c = self.country(is_game_paused=False)
        target = state(-2, buildings=[railway()])
        c.states = [target]
        c.run('sed_run_railway_approval', target)
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_railway_action_status'], 0)
        self.assertNotIn('sed_railway_request_pending', target['variables'])

    def test_state_variables_are_separate_from_the_country_cleanup_registry(self):
        self.assertEqual(set(runtime_variables()) - set(country_variables()),
                         {'sed_railway_request_pending',
                          'sed_construction_request_pending'})

    def test_construction_candidate_requires_staffed_sector_and_free_queue(self):
        c = self.country()
        cases = {
            'eligible': (state(-2, buildings=[construction_sector()]), True),
            'pending': (state(-2, buildings=[construction_sector()]), False),
            'no_sector': (state(-2), False),
            'unincorporated': (state(-2, incorporated=False,
                                    buildings=[construction_sector()]), False),
            'understaffed': (state(-2, buildings=[construction_sector(occupancy=0.89)]), False),
            'failed_hires': (state(-2, buildings=[construction_sector(failed_hires=True)]), False),
            'goods_shortage': (state(-2, buildings=[construction_sector(shortage=True)]), False),
            'queued_expansion': (state(-2, buildings=[construction_sector(queued_levels=1)]), False),
            'cannot_construct': (state(-2, can_construct=False,
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
        states = [state(-1, population=500, buildings=[construction_sector()]),
                  state(-1, population=5000, buildings=[construction_sector()]),
                  state(-1, population=2000, buildings=[construction_sector()])]
        c = self.country()
        c.states = states
        c.run('sed_refresh_construction_candidates')
        self.assertNotIn('sed_construction_candidates', c.variable_lists)
        c.readings['num_queued_government_constructions'] = 3
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variable_lists['sed_construction_candidates'], [states[1]])

    def test_construction_pending_clears_when_queue_resolves(self):
        target = state(-2, buildings=[construction_sector(queued_levels=1)])
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
        target = state(-2, buildings=[construction_sector()])

        def valid():
            return c.condition(c.definitions['sed_construction_approval_valid'], target)

        self.assertTrue(valid())
        guards = {
            'queue': ('readings', 'num_queued_government_constructions', 2),
            'paused': ('readings', 'is_game_paused', False),
            'default': ('readings', 'in_default', True),
            'negative_balance': ('readings', 'net_total_income', -1),
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

    def test_approved_construction_sector_queues_one_level_and_marks_request(self):
        c = self.country(num_queued_government_constructions=3)
        target = state(-2, buildings=[construction_sector()])
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
        target = state(-2, buildings=[construction_sector()])
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
        recommendations = 'sed_construction_recommendations_visible_sgui'
        c.readings['num_queued_government_constructions'] = 2
        self.assertTrue(shown(short))
        self.assertFalse(shown(filtered))
        self.assertFalse(shown(recommendations))
        c.readings['num_queued_government_constructions'] = 3
        self.assertFalse(shown(short))
        self.assertTrue(shown(filtered))
        c.variable_lists['sed_construction_candidates'] = [state()]
        self.assertFalse(shown(short))
        self.assertFalse(shown(filtered))
        self.assertTrue(shown(recommendations))


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
