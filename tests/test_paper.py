"""Paper supply scenarios reproduce a missing industry with idle free construction."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state
from tools import production_methods


class PaperTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(),
                         construction_queue_num_queued_government_levels=0,
                         num_queued_government_constructions=0,
                         gold_reserves=176000, net_total_income=745,
                         net_fixed_income=745, fixed_expenses=1220, principal=0)
        self.c.run('sed_enable_country')
        self.target = state(population=318000)
        self.c.states = [self.target]
        self.c.market_goods['paper'] = dict(market_goods_has_goods_shortage=True,
                                           market_goods_buy_orders=5, market_goods_sell_orders=0)
        self.c.variables['advisor_enabled'] = True

    def automatic(self):
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')

    def test_missing_paper_mill_is_founded_using_free_capacity(self):
        self.automatic()
        self.assertEqual(self.c.variables['sed_coord_executor'], 11)
        self.assertEqual(self.c.constructions,
                         [dict(building='building_paper_mill', state=self.target)])
        self.assertEqual(self.c.variables['sed_build_budget_project_points'], 600)
        self.assertNotIn('advisor_auto_construction_enabled', self.c.variables)
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(len(self.c.constructions), 1)

    def test_small_shortage_can_start_with_partial_staffing(self):
        self.target['state_population'] = 18400
        self.automatic()
        self.assertEqual(len(self.c.constructions), 1)
        self.c.run('sed_refresh_diagnostics')
        self.assertGreaterEqual(self.target['variables']['sed_labor_committed'], 5000)
        self.assertEqual(self.target['variables']['sed_labor_available'], 0)

    def test_partial_staffing_must_cover_shortage_with_margin(self):
        self.target['state_population'] = 18400
        self.c.market_goods['paper']['market_goods_buy_orders'] = 20
        self.automatic()
        self.assertEqual(self.c.constructions, [])

    def test_existing_paper_mill_can_expand(self):
        mill = building('building_paper_mill')
        mill['production_methods'] = ['pm_pulp_pressing', 'pm_automation_disabled']
        self.target['buildings'].append(mill)
        self.automatic()
        self.assertEqual(self.c.constructions,
                         [dict(building='building_paper_mill', state=self.target)])

    def test_wood_bottleneck_is_planned_before_paper(self):
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=False,
                                          market_goods_buy_orders=80, market_goods_sell_orders=40)
        camp = building('building_logging_camp')
        camp['production_methods'] = ['pm_simple_forestry']
        self.target['buildings'].append(camp)
        self.automatic()
        self.assertIn('sed_input_priority_wood', self.c.variables)
        self.assertEqual(self.c.constructions,
                         [dict(building='building_logging_camp', state=self.target)])

    def test_insufficient_labor_prevents_paper_founding(self):
        self.target['state_population'] = 1
        self.automatic()
        self.assertEqual(self.c.constructions, [])

    def test_paper_baseline_and_advanced_methods_match_vanilla(self):
        groups = production_methods.PROFILES['building_paper_mill']
        self.assertEqual([group['method'] for group in groups],
                         ['pm_pulp_pressing', 'pm_automation_disabled'])
        baseline = production_methods.ECONOMICS['buildings']['building_paper_mill']['pm_pulp_pressing']
        self.assertEqual(baseline['inputs'], {'wood': 30})
        self.assertEqual(baseline['outputs'], {'paper': 40})
        self.assertEqual(baseline['workers'], 5000)
