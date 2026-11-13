"""Core input growth lane; script simulation only."""
import unittest

from tools.build_mod import outputs
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class CoreGrowthTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.c.states = [state(population=60000)]
        self.c.variables['sed_build_budget_known'] = 1
        self.c.variables['sed_build_budget_weekly'] = 50
        self.c.variables['sed_build_budget_required_gold'] = 100

    def add_logging_camp(self, level=1, queued_levels=0):
        camp = building('building_logging_camp', level=level, queued_levels=queued_levels)
        camp['production_methods'] = ['pm_simple_forestry']
        self.c.states[0]['buildings'].append(camp)
        return camp

    def test_a_healthy_economy_keeps_expanding_a_core_input(self):
        # Treasury positive, nothing scarce and nothing above base price: the
        # plan has no priority, but the executor should not idle.
        c = self.c
        self.add_logging_camp()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_count'], 0)
        self.assertEqual([item.get('building') for item in c.constructions],
                         ['building_logging_camp'])
        self.assertEqual(c.variables['sed_auto_action_status'], 1)
        self.assertEqual(c.states[0]['variables'].get('sed_wood_intent_level'), 1)
        self.assertIn('sed_wood_request_pending', c.states[0]['variables'])

    def test_a_missing_good_without_a_host_site_leaves_the_month_to_growth(self):
        # Paraguay-like deadlock: a good is scarce and has no producer, but no
        # state can host the industry (no deposit, technology or land). The plan
        # waits on goal 5; the growth lane must not wait with it forever.
        c = self.c
        self.add_logging_camp()
        c.market_goods['grain'] = {'market_goods_has_goods_shortage': True,
                                    'market_goods_buy_orders': 100, 'market_goods_sell_orders': 0}
        c.states[0]['variables']['sed_grain_ignored'] = 1
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_missing_grain'], 1)
        self.assertEqual(c.variables['sed_plan_goal'], 5)
        self.assertTrue(c.condition(c.definitions['sed_develop_core'], c.country_scope()))
        self.assertTrue(c.constructions)

    def test_a_missing_good_with_a_host_site_keeps_the_growth_lane_waiting(self):
        c = self.c
        self.add_logging_camp()
        c.market_goods['grain'] = {'market_goods_has_goods_shortage': True,
                                    'market_goods_buy_orders': 100, 'market_goods_sell_orders': 0}
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 2)
        self.assertEqual([item.get('building') for item in c.constructions],
                         ['building_wheat_farm'])
        self.assertNotIn('building_logging_camp',
                         [item.get('building') for item in c.constructions])

    def test_no_building_means_no_founding_from_the_growth_lane(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_a_good_cheaper_than_base_is_not_expanded(self):
        c = self.c
        self.add_logging_camp()
        c.market_goods['wood']['market_goods_cheaper'] = True
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_civic_goals_keep_their_own_executor(self):
        c = self.c
        self.add_logging_camp()
        c.readings['bureaucracy'] = -10
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 6)
        self.assertEqual([item.get('building') for item in c.constructions],
                         ['building_government_administration'])

    def test_private_queue_blocks_the_growth_lane(self):
        c = self.c
        self.add_logging_camp()
        c.readings['construction_queue_num_queued_private_levels'] = 1
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_auto_action_status'], 11)

    def test_the_monthly_limit_keeps_one_level_per_month(self):
        c = self.c
        self.add_logging_camp()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_action_status'], 16)

    def test_a_queued_level_waits_for_the_queue(self):
        c = self.c
        self.add_logging_camp(queued_levels=1)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_budget_reserves_the_logging_camp_points(self):
        c = self.c
        self.add_logging_camp()
        c.run('sed_set_mode_automatic')
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_project_points'], 200)

    def add_construction_sector(self, level=1, queued_levels=0):
        # The sector's own methods give the material budget its capacity; without
        # them the budget stays unknown and the executor guard blocks everything.
        sector = building('building_construction_sector', level=level, queued_levels=queued_levels)
        sector['production_methods'] = ['pm_wooden_buildings']
        self.c.states[0]['buildings'].append(sector)
        return sector

    def test_a_long_public_queue_buys_a_sector_level(self):
        c = self.c
        self.add_construction_sector()
        c.readings['construction_queue_government_duration'] = 20
        # The material guard requires gold for the queue weeks the income does
        # not cover; a country able to pay a 20-week queue holds that treasure.
        c.readings['gold_reserves'] = 400000
        c.readings['principal'] = 0
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual([item.get('building') for item in c.constructions],
                         ['building_construction_sector'])
        self.assertEqual(c.states[0]['variables'].get('sed_construction_intent_level'), 1)

    def test_a_short_queue_does_not_buy_a_sector_level(self):
        c = self.c
        self.add_construction_sector()
        c.readings['construction_queue_government_duration'] = 5
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_a_sector_level_already_queued_waits(self):
        c = self.c
        self.add_construction_sector(queued_levels=1)
        c.readings['construction_queue_government_duration'] = 20
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_panel_does_not_promise_new_buildings(self):
        # The growth lane expands only existing buildings; the supply panel text
        # must not claim otherwise.
        en = outputs()['localization/english/sed_l_english.yml'].decode('utf-8-sig')
        self.assertIn('This version only expands existing buildings.', en)


if __name__ == '__main__':
    unittest.main()
