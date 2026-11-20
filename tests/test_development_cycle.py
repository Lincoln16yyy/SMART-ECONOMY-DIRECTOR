"""Testes sintéticos das quatro melhorias mecânicas; não emula a engine."""
import copy
import unittest
from script_harness import Country, building, state
from test_diagnostics import script_definitions
from tools.production_methods import PROFILES


def economy(income=10000, debt=0, gold=100000):
    c = Country(script_definitions(), principal=debt, credit=200000,
                net_total_income=income, net_fixed_income=income, gold_reserves=gold,
                construction_queue_num_queued_government_levels=0)
    camp = building('building_logging_camp', earnings=500, weekly_profit=450)
    camp['production_methods'] = [group['method'] for group in PROFILES['building_logging_camp']]
    # Make the wage reference explicit in the supported reading shape.
    camp['weekly_profit'] = 450
    c.states = [state(population=200000, buildings=[camp],
                      can_construct=['building_logging_camp', 'building_construction_sector'])]
    c.run('sed_enable_country')
    c.run('sed_set_mode_automatic')
    return c, camp


class FirstSectorTests(unittest.TestCase):
    def test_founds_first_sector_with_sustainable_wages_and_inputs(self):
        c, _ = economy()
        c.run('sed_auto_apply_monthly')
        self.assertEqual([p['building'] for p in c.constructions], ['building_construction_sector'])
        self.assertEqual(c.states[0]['variables']['sed_construction_intent_level'], 0)
        self.assertIn('sed_first_sector_pending', c.states[0]['variables'])
        self.assertEqual(c.variables['sed_build_budget_project_points'], 25)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        c.readings['month'] = 1
        c.run('sed_refresh_diagnostics')
        self.assertIn('sed_construction_request_pending', c.states[0]['variables'])

    def test_first_sector_precedes_discretionary_university(self):
        c, _ = economy()
        c.readings.update(country_innovation=0, max_innovation=50)
        c.states[0]['can_construct_building'].append('building_university')
        c.market_goods['paper'] = dict(market_goods_buy_orders=0, market_goods_sell_orders=100, market_goods_has_goods_shortage=False)
        c.run('sed_refresh_diagnostics')
        self.assertTrue(c.condition(c.definitions['sed_university_ready'], c.country_scope()))
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions[0]['building'], 'building_construction_sector')
        self.assertEqual(c.variables['sed_build_budget_project_points'], 25)

    def test_low_income_does_not_buy_a_permanent_expense(self):
        c, _ = economy(income=100)
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('building_construction_sector', [p['building'] for p in c.constructions])

    def test_first_sector_waits_for_missing_fabric(self):
        c, _ = economy()
        c.market_goods['fabric'].update(market_goods_buy_orders=100, market_goods_sell_orders=0)
        c.run('sed_refresh_national_plan')
        self.assertFalse(c.condition(c.definitions['sed_first_sector_available'], c.country_scope()))

    def test_existing_or_foreign_queued_sector_is_not_founded_again(self):
        c, _ = economy()
        c.states[0]['buildings'].append(building('building_construction_sector', level=0, queued_levels=1))
        self.assertFalse(c.condition(c.definitions['sed_first_sector_available'], c.country_scope()))

    def test_no_wage_sample_prevents_unpriced_payroll(self):
        c, camp = economy()
        camp['earnings'] = camp['weekly_profit'] = 0
        c.run('sed_refresh_national_plan')
        self.assertFalse(c.condition(c.definitions['sed_first_sector_available'], c.country_scope()))

    def test_first_sector_can_be_cash_funded_with_debt_but_not_in_crisis(self):
        c, _ = economy(debt=50000, gold=0)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions[0]['building'], 'building_construction_sector')
        c, _ = economy(debt=170000, gold=0)
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('building_construction_sector', [p['building'] for p in c.constructions])

    def test_first_sector_yields_in_manual_private_and_paused_modes(self):
        for mode in ('manual', 'assisted'):
            c, _ = economy();c.run('sed_set_mode_'+mode)
            self.assertFalse(c.condition(c.definitions['sed_first_sector_available'], c.country_scope()))
        for reading in ('construction_queue_num_queued_private_levels', 'is_construction_paused'):
            c, _ = economy();c.readings[reading] = 1
            self.assertFalse(c.condition(c.definitions['sed_first_sector_available'], c.country_scope()))


class PerformanceTests(unittest.TestCase):
    def prepare(self, accepted=True):
        c, camp = economy(income=2000)
        c.states[0]['can_construct_building'] = ['building_logging_camp']
        c.construction_accepted = accepted
        c.run('sed_auto_apply_monthly')
        return c, camp, c.states[0]['variables']

    def finish(self, c, camp, profit=200):
        camp.update(level=2, level_after_queued_constructions=2, earnings=1000, weekly_profit=profit)
        c.readings.update(month=1, construction_queue_num_queued_government_levels=0)
        c.run('sed_review_project_performance')

    def test_grace_period_and_per_level_profit_wages(self):
        c, camp, v = self.prepare();self.assertIn('sed_perf_wood_tracking', v)
        self.finish(c, camp)
        c.readings['month'] = 3;c.run('sed_review_project_performance')
        self.assertNotIn('sed_perf_wood_known', v)
        c.readings['month'] = 4;c.run('sed_review_project_performance')
        self.assertEqual(v['sed_perf_wood_actual'], 100)
        self.assertEqual(v['sed_perf_wood_wages'], 400)
        self.assertEqual(c.variables['sed_perf_evaluated'], 1)
        c.run('sed_review_project_performance')
        self.assertEqual(c.variables['sed_perf_evaluated'], 1)

    def test_negative_return_blocks_repetition_and_recovers_on_new_sample(self):
        c, camp, v = self.prepare();self.finish(c, camp, profit=-20)
        c.readings['month'] = 4;c.run('sed_review_project_performance')
        self.assertTrue(c.condition(c.definitions['sed_perf_wood_blocked'], c.states[0]))
        self.assertFalse(c.condition(c.definitions['sed_growth_wood_candidate'], c.states[0]))
        camp['weekly_profit'] = 1000;c.readings['month'] = 5;c.run('sed_review_project_performance')
        self.assertFalse(c.condition(c.definitions['sed_perf_wood_blocked'], c.states[0]))

    def test_underperformance_reduces_score(self):
        c, camp, v = self.prepare();self.finish(c, camp, profit=100)
        c.readings['month'] = 4;c.run('sed_review_project_performance')
        self.assertLess(v['sed_perf_wood_actual'], v['sed_perf_wood_expected']*0.5)
        self.assertEqual(c.lookup('sed_perf_wood_factor', c.states[0]), .5)

    def test_quote_is_taken_before_engine_queue_mutation(self):
        c, camp = economy(income=2000)
        c.states[0]['can_construct_building'] = ['building_logging_camp']
        c.mutate_queue_levels = True
        c.run('sed_auto_apply_monthly')
        v = c.states[0]['variables']
        self.assertEqual(camp['level_after_queued_constructions'], 2)
        self.assertGreater(v['sed_perf_wood_expected'], 0)
        self.assertNotIn('sed_perf_wood_quote', v)

    def test_failed_insertion_has_no_performance_claim(self):
        c, _, v = self.prepare(accepted=False)
        self.assertNotIn('sed_perf_wood_tracking', v)

    def test_unstaffed_or_subsidized_plant_has_no_profit_verdict(self):
        for key, value in [('occupancy', .2), ('is_subsidized', True)]:
            c, camp, v = self.prepare();self.finish(c, camp, profit=-100)
            camp[key] = value;c.readings['month'] = 4;c.run('sed_review_project_performance')
            self.assertNotIn('sed_perf_wood_known', v)

    def test_simulated_reload_preserves_target_and_completion_date(self):
        c, camp, v = self.prepare();self.finish(c, camp)
        saved = copy.deepcopy(c)
        saved.readings['month'] = 4;saved.run('sed_review_project_performance')
        self.assertEqual(saved.states[0]['variables']['sed_perf_wood_actual'], 100)
        saved.run('sed_disable_country')
        self.assertFalse(any(k.startswith('sed_perf_') for k in saved.states[0]['variables']))


class DebtStrategyTests(unittest.TestCase):
    def test_debt_regimes_follow_cashflow_and_credit(self):
        for debt, balance, expected in [(0,100,0), (5000,-10,1), (5000,100,2), (170000,100,3)]:
            c, _ = economy(income=balance, debt=debt)
            c.run('sed_refresh_debt_strategy')
            self.assertEqual(c.variables['sed_debt_stage'], expected)
        c.readings['in_default'] = True;c.run('sed_refresh_debt_strategy')
        self.assertEqual(c.variables['sed_debt_stage'], 4)

    def test_two_real_months_of_rising_debt_prioritize_repayment(self):
        c, _ = economy(debt=5000, gold=0)
        c.run('sed_refresh_debt_strategy')
        for month, principal in [(1,5200),(2,5400)]:
            c.readings.update(month=month, principal=principal)
            c.run('sed_refresh_debt_strategy');c.run('sed_refresh_debt_strategy')
        self.assertEqual(c.variables['sed_debt_rising_months'], 2)
        self.assertEqual(c.variables['sed_debt_stage'], 3)
        self.assertFalse(c.condition(c.definitions['sed_growth_ready'], c.country_scope()))
        c.readings.update(month=3, principal=5000);c.run('sed_refresh_debt_strategy')
        self.assertEqual(c.variables['sed_debt_stage'], 2)

    def test_skipped_month_does_not_prove_consecutive_deterioration(self):
        c, _ = economy(debt=5000)
        c.readings.update(month=3, principal=8000);c.run('sed_refresh_debt_strategy')
        self.assertEqual(c.variables['sed_debt_rising_months'], 0)

    def test_debt_observer_does_not_change_taxes_wages_or_money(self):
        c, _ = economy(debt=5000)
        before = {k:c.readings[k] for k in ('principal','gold_reserves','tax_level','government_wage_level')}
        c.run('sed_refresh_debt_strategy')
        self.assertEqual(before, {k:c.readings[k] for k in before})


    def test_simulated_reload_keeps_trend_and_restores_fiscal_snapshots(self):
        c, _ = economy(debt=5000, gold=0)
        c.readings.update(month=1, principal=5200);c.run('sed_refresh_debt_strategy')
        loaded = copy.deepcopy(c)
        loaded.readings.update(month=2, principal=5400);loaded.run('sed_refresh_debt_strategy')
        self.assertEqual(loaded.variables['sed_debt_rising_months'], 2)
        loaded.readings.update(net_total_income=-100, net_fixed_income=-100)
        loaded.run('sed_auto_apply_monthly')
        self.assertEqual(loaded.readings['tax_level'], 'high')
        self.assertEqual(loaded.readings['government_wage_level'], 'low')
        reloaded = copy.deepcopy(loaded);reloaded.run('sed_set_mode_manual')
        self.assertEqual(reloaded.readings['tax_level'], 'medium')
        self.assertEqual(reloaded.readings['government_wage_level'], 'medium')
        self.assertEqual(reloaded.readings['principal'], 5400)
        self.assertEqual(reloaded.readings['gold_reserves'], 0)

    def test_catalog_migration_clears_old_receipt_only_once(self):
        c, _ = economy()
        c.variables.pop('sed_development_schema')
        c.variables.update(sed_last_build_action=17, sed_last_build_year=1840)
        c.run('sed_refresh_calendar')
        self.assertNotIn('sed_last_build_action', c.variables)
        c.variables['sed_last_build_action'] = 25
        c.run('sed_refresh_calendar')
        self.assertEqual(c.variables['sed_last_build_action'], 25)


class AdvancedChainTests(unittest.TestCase):
    def test_steel_shortage_builds_suppliers_before_unfed_steel_mill(self):
        c = Country(script_definitions(), principal=0, gold_reserves=100000,
                    net_total_income=10000, net_fixed_income=10000,
                    construction_queue_num_queued_government_levels=0)
        c.states = [state(population=200000, can_construct=['building_steel_mill','building_iron_mine','building_coal_mine'])]
        for good in ('steel','iron','coal'):
            c.market_goods[good] = dict(market_goods_buy_orders=100,market_goods_sell_orders=0,
                                       market_goods_has_goods_shortage=good=='steel')
        c.run('sed_enable_country');c.run('sed_set_mode_automatic');c.run('sed_auto_apply_monthly')
        self.assertIn('sed_input_priority_iron',c.variables)
        self.assertIn('sed_input_priority_coal',c.variables)
        self.assertEqual(len(c.constructions),1)
        self.assertIn(c.constructions[0]['building'],['building_iron_mine','building_coal_mine'])
