"""Trade Center fallback; script simulation, not engine evidence."""
import unittest

from tools.build_mod import outputs
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class TradeCenterTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        # A paper shortage no local producer can answer: the state has no paper
        # mill, cannot host one (no labor) and accepts the Trade Center building.
        self.c.states = [state(population=0)]
        self.c.market_goods['paper'] = dict(market_goods_has_goods_shortage=True,
                                            market_goods_buy_orders=100,
                                            market_goods_sell_orders=40)
        # The executor guard in the real game is budget-aware; the harness does
        # not set spendable-build budget by default, so the direct-direct path
        # falls through to status 14 (no branch matched) once any supply branch
        # was already skipped. Mirror the budget-known guard so the fallback is
        # reachable without patching the harness.
        self.c.variables['sed_build_budget_known'] = 1
        self.c.variables['sed_build_budget_weekly'] = 50
        self.c.variables['sed_build_budget_required_gold'] = 100

    def test_automatic_founds_a_trade_center_when_no_local_producer_is_eligible(self):
        c = self.c
        self.assertFalse(any(c.condition(c.definitions['sed_paper_candidate_eligible'], target)
                             for target in c.states))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual([item.get('building') for item in c.constructions], ['building_trade_center'])
        self.assertEqual(c.variables['sed_trade_center_action_status'], 1)
        self.assertEqual(c.states[0]['variables'].get('sed_trade_center_intent_level'), 0)
        self.assertIn('sed_trade_center_request_pending', c.states[0]['variables'])

    def test_expanding_an_existing_trade_center_reads_its_level(self):
        c = self.c
        c.states[0]['buildings'].append(building('building_trade_center', level=2))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.states[0]['variables'].get('sed_trade_center_intent_level'), 2)
        self.assertEqual(c.variables.get('sed_trade_center_intents'), 1)

    def test_isolationism_blocks_the_fallback(self):
        c = self.c
        c.readings['laws'] = ['law_isolationism']
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual([item.get('building') for item in c.constructions], [])
        self.assertNotIn('sed_trade_center_action_status', c.variables)

    def test_monthly_review_records_completion_from_the_level(self):
        c = self.c
        c.states[0]['buildings'].append(building('building_trade_center', level=1))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        c.states[0]['buildings'][0]['level_after_queued_constructions'] = 2
        c.run('sed_refresh_trade_center')
        self.assertIn('sed_trade_center_request_pending', c.states[0]['variables'])
        c.states[0]['buildings'][0]['level'] = 2
        c.run('sed_refresh_trade_center')
        self.assertNotIn('sed_trade_center_request_pending', c.states[0]['variables'])
        self.assertEqual(c.variables.get('sed_trade_center_completed'), 1)
        self.assertEqual(c.variables.get('sed_trade_center_result'), 1)

    def test_budget_reserves_the_trade_center_points_without_a_ranked_project(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.run('sed_refresh_national_plan')
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_project_points'], 100)

    def test_a_good_with_a_waiting_producer_does_not_buy_capacity(self):
        # No paper mill exists, which is what the fallback answers; once a mill is
        # present the shortage belongs to the normal supply lane, never the market.
        c = self.c
        c.states[0]['population'] = 200000
        c.states[0]['buildings'].append(building('building_paper_mill'))
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('sed_trade_center_action_status', c.variables)

    def test_panel_text_explains_the_fallback_limits(self):
        english = outputs()['localization/english/sed_l_english.yml'].decode('utf-8-sig')
        self.assertIn('does not open a route', english)
        self.assertIn('Trade Center', english)


if __name__ == '__main__':
    unittest.main()
