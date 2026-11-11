"""General startup forecasts use one verified basic configuration per industry."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state
from tools import input_forecast


class StartupInputTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions())
        self.c.run('sed_enable_country')
        self.target = state()
        self.c.states = [self.target]
        self.c.run('sed_set_mode_automatic')
        self.c.readings['technologies'] = sorted({tech for groups in input_forecast.FOUNDING_GROUPS.values()
                                                 for group in groups for techs in group.values() for tech in techs})

    def test_every_supported_industry_uses_only_its_basic_configuration(self):
        for kind, groups in input_forecast.STARTUP_METHODS.items():
            for good in input_forecast.building_goods(kind):
                with self.subTest(building=kind, good=good):
                    expected = sum(input_forecast.PROFILES[kind].get(group['method'], {}).get(good, 0)
                                   for group in groups)
                    self.assertEqual(self.c.number(input_forecast.amount_name(kind, good, founding=True), self.target), expected)

    def test_external_pm_manager_retains_the_broader_forecast(self):
        self.c.variables['advisor_pm_balance_enabled'] = True
        self.assertEqual(self.c.number('sed_founding_input_paper_mill_sulfur', self.target), 10)
        self.c.variables.pop('advisor_pm_balance_enabled')
        self.assertEqual(self.c.number('sed_founding_input_paper_mill_sulfur', self.target), 0)

    def test_assisted_founding_retains_the_conservative_forecast(self):
        self.c.run('sed_set_mode_assisted')
        self.assertEqual(self.c.number('sed_founding_input_paper_mill_sulfur', self.target), 10)

    def test_paper_can_start_with_advanced_technology_and_no_sulfur(self):
        from test_paper import PaperTests

        scenario = PaperTests()
        scenario.setUp()
        c = scenario.c
        c.readings['technologies'] = ['mechanical_tools', 'chemical_bleaching', 'watertube_boiler']
        scenario.target['state_population'] = 18400
        for good in ['sulfur', 'dye', 'coal', 'tools']:
            c.market_goods[good] = dict(market_goods_buy_orders=0, market_goods_sell_orders=0,
                                      market_goods_has_goods_shortage=False)
        scenario.automatic()
        self.assertEqual([order['building'] for order in c.constructions], ['building_paper_mill'])
        c.run('sed_refresh_input_readings')
        self.assertEqual(c.number('sed_input_pending_sulfur', scenario.target), 0)
        self.assertEqual(c.number('sed_input_pending_wood', scenario.target), 37.5)

    def test_partially_staffed_startup_returns_to_basic_without_extra_jobs(self):
        producer = building('building_paper_mill', occupancy=0.2)
        producer['production_methods'] = ['pm_sulfite_pulping', 'pm_automation_disabled']
        self.target['buildings'] = [producer]
        self.target['state_population'] = 18400
        self.c.run('sed_set_mode_automatic')
        self.target['variables']['sed_paper_found_pm_pending'] = 1
        self.c.market_goods['sulfur'] = dict(market_goods_buy_orders=10, market_goods_sell_orders=0,
                                           market_goods_has_goods_shortage=True)
        self.c.run('sed_configure_founded_industries')
        self.assertIn('pm_pulp_pressing', producer['production_methods'])
        self.assertNotIn('sed_paper_found_pm_pending', self.target['variables'])

    def test_disabling_automation_still_requires_enough_workers(self):
        producer = building('building_paper_mill', occupancy=0.2)
        producer['production_methods'] = ['pm_sulfite_pulping', 'pm_rotary_valve_engine_building_paper_mill']
        self.target['buildings'] = [producer]
        self.target['state_population'] = 18400
        self.c.run('sed_set_mode_automatic')
        self.target['variables']['sed_paper_found_pm_pending'] = 1
        self.c.market_goods['sulfur'] = dict(market_goods_buy_orders=10, market_goods_sell_orders=0,
                                           market_goods_has_goods_shortage=True)
        self.c.run('sed_configure_founded_industries')
        self.assertIn('pm_sulfite_pulping', producer['production_methods'])
        self.assertIn('sed_paper_found_pm_pending', self.target['variables'])
