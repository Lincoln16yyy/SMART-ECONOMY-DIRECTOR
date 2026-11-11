"""Observed weekly wage bill used by the investment reference."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state

LOGGING_BASE = ['pm_simple_forestry', 'pm_no_hardwood', 'pm_no_equipment', 'pm_road_carts']


class InvestmentWageTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def producer(self, methods=None, **kwargs):
        result = building('building_logging_camp', **kwargs)
        result['production_methods'] = list(methods or LOGGING_BASE)
        return result

    def refresh(self, *states):
        self.c.states = list(states)
        self.c.run('sed_refresh_investment_prices')

    def unit(self, target):
        return target['variables'].get('sed_investment_wage_unit')

    def known(self, target):
        return target['variables'].get('sed_investment_wage_known')

    def test_observed_weekly_wage_bill_sets_the_unit_and_the_return(self):
        sample = state(buildings=[self.producer(earnings=4800, weekly_profit=1800)])
        other = state()
        self.refresh(sample, other)
        self.assertEqual(self.c.variables['sed_investment_wage_unit'], 0.5)
        self.assertEqual(self.unit(other), 0.5)
        self.assertEqual(self.c.number('sed_investment_logging_camp_margin', other), 450)
        self.assertEqual(self.c.number('sed_investment_logging_camp_return', other), -2550)

    def test_active_methods_scale_the_forecast(self):
        sample = state(buildings=[self.producer(earnings=4800, weekly_profit=1800)])
        wood = state(buildings=[self.producer(['pm_saw_mills', 'pm_no_hardwood',
                                               'pm_no_equipment', 'pm_road_carts'],
                                              earnings=4800, weekly_profit=1800)])
        self.refresh(sample, wood)
        self.assertEqual(self.c.number('sed_investment_logging_camp_weighted_jobs', wood), 6250)
        self.assertEqual(self.c.number('sed_investment_logging_camp_margin', wood), 650)
        self.assertEqual(self.c.number('sed_investment_logging_camp_return', wood), -2350)

    def test_unhealthy_or_unpriced_samples_leave_the_material_reference(self):
        for kwargs in (dict(subsidized=True), dict(shortage=True), dict(failed_hires=True),
                       dict(occupancy=0.7),
                       dict(earnings=0, weekly_profit=0),
                       dict(earnings=100, weekly_profit=200)):
            with self.subTest(kwargs=kwargs):
                readings = dict(earnings=4800, weekly_profit=1800)
                readings.update(kwargs)
                sample = state(buildings=[self.producer(**readings)])
                other = state()
                self.refresh(sample, other)
                self.assertEqual(self.known(other), 0)
                self.assertEqual(self.c.number('sed_investment_logging_camp_return', other), 450)

    def test_unrecognized_production_method_excludes_the_sample(self):
        sample = state(buildings=[self.producer(['pm_saw_mills', 'pm_no_hardwood',
                                                 'pm_no_equipment', 'pm_unknown_transport'],
                                                earnings=4800, weekly_profit=1800)])
        other = state()
        self.refresh(sample, other)
        self.assertEqual(self.known(other), 0)

    def test_state_sample_overrides_the_country_unit(self):
        cheap = state(buildings=[self.producer(earnings=4800, weekly_profit=2400)])
        dear = state(buildings=[self.producer(earnings=4800, weekly_profit=1800)])
        other = state()
        self.refresh(cheap, dear, other)
        self.assertEqual(self.unit(cheap), 0.4)
        self.assertEqual(self.unit(dear), 0.5)
        self.assertEqual(self.unit(other), 0.45)
        self.assertEqual(self.c.number('sed_investment_logging_camp_return', other), -2250)

    def test_wage_aware_return_changes_the_preferred_grain_supplier(self):
        sample = state(buildings=[self.producer(earnings=1300, weekly_profit=1000)])
        wheat = building('building_wheat_farm')
        wheat['production_methods'] = ['pm_simple_farming', 'pm_no_secondary', 'pm_tools_disabled']
        rice = building('building_rice_farm')
        rice['production_methods'] = ['pm_simple_farming_building_rice_farm', 'pm_no_secondary',
                                      'pm_tools_disabled']
        target = state(buildings=[wheat, rice])
        self.refresh(sample, target)
        self.assertEqual(self.unit(target), 0.05)
        self.assertGreater(self.c.number('sed_investment_rice_farm_margin', target),
                           self.c.number('sed_investment_wheat_farm_margin', target))
        self.assertTrue(self.c.condition(
            self.c.definitions['sed_grain_wheat_farm_preferred_supplier'], target))
        self.assertEqual(self.c.number('sed_investment_grain_return', target), 0)

    def test_disable_clears_wage_readings(self):
        target = state(buildings=[self.producer(earnings=4800, weekly_profit=1800)])
        self.refresh(target)
        self.assertEqual(self.known(target), 1)
        self.c.run('sed_disable_country')
        self.assertFalse(any(name.startswith('sed_investment_wage_')
                             for name in self.c.variables))
        self.assertFalse(any(name.startswith('sed_investment_wage_')
                             for name in target['variables']))


if __name__ == '__main__':
    unittest.main()
