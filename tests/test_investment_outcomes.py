import unittest
from script_harness import Country, building, state
from test_diagnostics import script_definitions


class InvestmentOutcomeTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), principal=0, net_total_income=1000,
                         gold_reserves=100000)
        self.c.run('sed_enable_country')

    def test_new_external_building_is_observed_after_baseline(self):
        c = self.c
        site = state()
        c.states = [site]
        c.readings['month'] = 1
        c.run('sed_outcome_review')
        mill = building('building_paper_mill', occupancy=0.3, shortage=True)
        site['buildings'].append(mill)
        c.readings['month'] = 2
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_observed'], 1)
        self.assertEqual(c.variables['sed_outcome_staff'], 1)
        self.assertEqual(c.variables['sed_outcome_inputs'], 1)
        mill.update(occupancy=1, building_has_goods_shortage=False)
        c.readings['month'] = 3
        c.run('sed_outcome_review')
        self.assertNotIn('sed_outcome_paper_pending', site['variables'])

    def test_market_pressure_persists_until_buyers_recover(self):
        c = self.c
        mill = building('building_paper_mill')
        site = state(buildings=[mill])
        c.states = [site]
        c.readings['month'] = 1
        c.run('sed_outcome_review')
        mill['level'] = 2
        c.market_goods['paper'] = dict(market_goods_sell_orders=200,
                                       market_goods_buy_orders=100, market_goods_cheaper=True, market_goods_has_goods_shortage=False)
        c.readings['month'] = 2
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_market'], 1)
        c.variables.update(advisor_enabled=True)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.variables['sed_coord_executor'], 0)
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)
        c.market_goods['paper']['market_goods_cheaper'] = False
        c.readings['month'] = 3
        c.run('sed_outcome_review')
        c.run('sed_coord_sync')
        self.assertEqual(c.variables['sed_coord_executor'], 1)

    def test_repeated_review_does_not_erase_the_current_month(self):
        c = self.c
        c.variables['sed_outcome_staff'] = 3
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_staff'], 3)
        c.run('sed_disable_country')
        self.assertNotIn('sed_outcome_staff', c.variables)
