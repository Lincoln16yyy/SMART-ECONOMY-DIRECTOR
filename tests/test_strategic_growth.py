import unittest
from script_harness import Country, state, building, construction_sector
from test_diagnostics import script_definitions
from tools import strategic_growth, public_upkeep
from tools.build_mod import SUPPLY_TARGETS, variants


class StrategicGrowthTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), principal=0, net_total_income=2000,
                         net_fixed_income=2000, gold_reserves=100000,
                         construction_queue_num_queued_government_levels=0)
        for item in strategic_growth.targets(SUPPLY_TARGETS):
            self.c.market_goods.setdefault(item['good'], dict(market_goods_buy_orders=1000,
                market_goods_sell_orders=1000, market_goods_has_goods_shortage=False))
        self.c.run('sed_enable_country')
        self.c.run('sed_set_mode_automatic')
        self.c.states = [state()]
        self.c.run('sed_refresh_national_plan')

    def test_founds_first_industry_without_market_shortage(self):
        c = self.c
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertIn(c.constructions[0]['building'],
                      [v['building'] for i in strategic_growth.targets(SUPPLY_TARGETS) for v in variants(i)])
        self.assertEqual(c.variables['sed_auto_action_status'], 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)

    def test_empty_market_does_not_justify_growth(self):
        c = self.c
        for good in c.market_goods.values():
            good.update(market_goods_buy_orders=0, market_goods_sell_orders=0)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_low_prices_block_growth(self):
        c = self.c
        for good in c.market_goods.values():
            good['market_goods_cheaper'] = 0.5
        self.assertFalse(c.condition(c.definitions['sed_growth_site'], c.states[0]))

    def test_advisor_budget_block_triggers_viable_direct_alternative(self):
        c = self.c
        c.variables.update(advisor_enabled=True, advisor_auto_construction_status=4)
        c.run('sed_coord_enable')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 11)
        self.assertEqual(len(c.constructions), 1)
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)

    def test_manual_and_assisted_do_not_start_growth(self):
        c = self.c
        for mode in ('manual', 'assisted'):
            c.run('sed_set_mode_' + mode)
            self.assertFalse(c.condition(c.definitions['sed_growth_site'], c.states[0]))

    def test_debt_with_no_gold_and_cash_surplus_can_invest(self):
        c = self.c
        c.readings.update(principal=5000, credit=20000, gold_reserves=0)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertTrue(c.condition(c.definitions['sed_debt_growth_safe'], c.country_scope()))

    def test_debt_crisis_deficit_and_insufficient_credit_remain_blocked(self):
        c = self.c
        for principal, credit, balance, default in (
            (17000, 20000, 2000, False), (5000, 20000, -10, False),
            (5000, 20000, 2000, True), (1, 100, 2000, False)):
            with self.subTest(principal=principal, credit=credit, balance=balance):
                c.readings.update(principal=principal, credit=credit,
                                  gold_reserves=0, net_total_income=balance, in_default=default)
                c.run('sed_refresh_direct_budget')
                self.assertFalse(c.condition(c.definitions['sed_debt_growth_safe'], c.country_scope()))

    def test_debt_investment_requires_stressed_materials_plus_buffer(self):
        c = self.c
        sector = construction_sector(); sector['production_methods'] = ['pm_wooden_buildings']
        c.states[0]['buildings'].append(sector)
        c.readings.update(principal=5000, credit=100000, gold_reserves=0)
        c.run('sed_refresh_direct_budget')
        materials = c.variables['sed_build_budget_weekly']
        self.assertGreater(materials, 0)
        c.readings['net_total_income'] = materials * 1.25 - 1
        self.assertFalse(c.condition(c.definitions['sed_debt_growth_safe'], c.country_scope()))
        c.readings['net_total_income'] = materials * 1.25
        self.assertTrue(c.condition(c.definitions['sed_debt_growth_safe'], c.country_scope()))

    def test_private_queue_and_pause_keep_ownership(self):
        c = self.c
        for reading in ('construction_queue_num_queued_private_levels', 'is_construction_paused'):
            c.readings[reading] = 1
            self.assertFalse(c.condition(c.definitions['sed_growth_takeover'], c.country_scope()))
            c.readings[reading] = 0

    def test_public_upkeep_uses_available_technologies(self):
        c = self.c
        c.run('sed_refresh_public_upkeep')
        early = c.variables['sed_upkeep_admin_cost']
        techs = {t for data in public_upkeep.PROFILES.values() for g in data['groups']
                 for spec in g.values() for t in spec['technologies']}
        c.readings['technologies'] = list(techs)
        c.run('sed_refresh_public_upkeep')
        self.assertGreater(c.variables['sed_upkeep_admin_cost'], early)

    def test_each_catalogued_civilian_producer_can_be_founded(self):
        for item in strategic_growth.targets(SUPPLY_TARGETS):
            for variant in variants(item):
                with self.subTest(building=variant['building']):
                    self.setUp()
                    c = self.c
                    c.states[0]['can_construct_building'] = [variant['building']]
                    c.run('sed_auto_apply_monthly')
                    self.assertEqual([p['building'] for p in c.constructions], [variant['building']])
                    self.assertEqual(c.states[0]['variables']['sed_' + item['good'] + '_intent_level'], 0)

    def test_budget_reserves_the_selected_growth_project(self):
        from tools.construction_budget import PROJECT_POINTS
        c = self.c
        c.run('sed_refresh_direct_budget')
        points = c.variables['sed_build_budget_project_points']
        c.run('sed_auto_apply_monthly')
        selected = c.constructions[0]['building']
        good = next(item['good'] for item in strategic_growth.targets(SUPPLY_TARGETS)
                    if selected in [v['building'] for v in variants(item)])
        self.assertEqual(points, PROJECT_POINTS[good])

    def test_growth_releases_back_to_advisor_after_confirmed_insertion(self):
        c = self.c
        c.variables.update(advisor_enabled=True, advisor_auto_construction_status=4)
        c.run('sed_coord_enable')
        c.run('sed_auto_apply_monthly')
        c.run('sed_coord_sync')
        self.assertNotEqual(c.variables['sed_coord_executor'], 11)
        self.assertIn('advisor_auto_construction_enabled', c.variables)

    def test_founding_with_no_workers_is_rejected(self):
        c = self.c
        c.states = [state(population=1, state_unemployment_rate=0,
                          **{'pop_type_percent_state(pop_type:peasants)': 0})]
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
