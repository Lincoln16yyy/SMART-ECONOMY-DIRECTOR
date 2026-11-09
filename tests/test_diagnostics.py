import tempfile
from pathlib import Path
import unittest
import zipfile

from tools.build_mod import ROOT, outputs, runtime_variables
from tools.package_mod import package
from tools.pdx_script import parse, child
from tools.validate import validate
from script_harness import Country


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
        for name in runtime_variables():
            c.variables.setdefault(name, 123)
        c.run('sed_disable_country')
        self.assertEqual(c.variables, {'sed_schema_version': 1})
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
