"""Military-economic assessment regressions; synthetic script execution."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state
from tools.build_mod import SUPPLY_TARGETS


class MilitaryEconomyTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def test_normal_plan_entry_reads_costs_war_and_market_shortages(self):
        c = self.c
        c.readings.update(military_expenses=40, military_expenses_share=0.2, is_at_war=True)
        c.market_goods['small_arms'] = dict(market_goods_buy_orders=100,
                                           market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_expenses'], 40)
        self.assertEqual(c.variables['sed_military_share'], 0.2)
        self.assertEqual(c.variables['sed_military_at_war'], 1)
        self.assertEqual(c.variables['sed_military_shortage_count'], 1)
        self.assertEqual(c.variables['sed_military_posture'], 2)
        self.assertEqual(c.constructions, [])

    def test_absent_goods_and_zero_demand_do_not_create_shortages(self):
        c = self.c
        c.readings['military_expenses'] = 40
        c.market_goods['artillery'] = dict(market_goods_buy_orders=0,
                                          market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_shortage_count'], 0)
        self.assertEqual(c.variables['sed_military_posture'], 1)

    def test_crisis_overrides_shortage_without_hiding_supply_warning(self):
        c = self.c
        c.readings.update(military_expenses=40, net_total_income=-100, gold_reserves=0)
        c.market_goods['ammunition'] = dict(market_goods_buy_orders=100,
                                           market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_posture'], 3)
        self.assertEqual(c.variables['sed_military_short_ammunition'], 1)
        self.assertEqual(c.variables['sed_plan_goal'], 4)

    def test_modernization_assessment_requires_reserves_and_no_debt_or_shortages(self):
        c = self.c
        c.readings.update(military_expenses=40, principal=0, gold_reserves=600)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_posture'], 4)
        c.readings['gold_reserves'] = 599
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_posture'], 1)
        c.readings.update(gold_reserves=1000, principal=1)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_posture'], 1)
        c.readings.update(principal=0, net_fixed_income=-1)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_posture'], 3)

    def test_new_readings_clear_resolved_shortages_and_war_flag(self):
        c = self.c
        c.readings.update(military_expenses=40, is_at_war=True)
        for good in ('small_arms', 'artillery', 'ammunition', 'manowars', 'ironclads'):
            c.market_goods[good] = dict(market_goods_buy_orders=100,
                                        market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_shortage_count'], 5)
        c.market_goods.clear()
        c.readings['is_at_war'] = False
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_shortage_count'], 0)
        self.assertEqual(c.variables['sed_military_at_war'], 0)
        self.assertTrue(all(c.variables['sed_military_short_' + good] == 0
                            for good in ('small_arms', 'artillery', 'ammunition', 'manowars', 'ironclads')))

    def test_zero_military_spending_does_not_infer_national_need_from_market(self):
        c = self.c
        c.market_goods['ironclads'] = dict(market_goods_buy_orders=100,
                                          market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_military_shortage_count'], 1)
        self.assertEqual(c.variables['sed_military_posture'], 0)

    def test_assessment_is_read_only_and_cleans_up_on_disable(self):
        c = self.c
        c.readings.update(military_expenses=40, is_at_war=True)
        before = dict(c.readings)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.readings, before)
        self.assertEqual(c.constructions, [])
        c.run('sed_disable_country')
        self.assertFalse(any(k.startswith('sed_military_') for k in c.variables))

    def producer(self, good):
        c = self.c
        item = next(item for item in SUPPLY_TARGETS if item['good'] == good)
        producer = building(item['building'])
        producer['production_methods'] = [item['methods'][0]]
        target = state(buildings=[producer])
        c.states.append(target)
        c.readings['military_expenses'] = 40
        c.market_goods[good] = dict(market_goods_buy_orders=100, market_goods_sell_orders=40,
                                    market_goods_has_goods_shortage=True)
        return target, producer

    def test_all_three_industries_can_expand_once_through_assisted_approval(self):
        for good in ('small_arms', 'artillery', 'ammunition'):
            with self.subTest(good=good):
                self.setUp()
                c = self.c
                target, producer = self.producer(good)
                c.run('sed_refresh_diagnostics')
                c.run('sed_run_' + good + '_approval', target)
                self.assertEqual(c.constructions, [{'building': producer['building'], 'state': target}])
                self.assertIn('sed_' + good + '_request_pending', target['variables'])
                c.run('sed_run_' + good + '_approval', target)
                self.assertEqual(len(c.constructions), 1)

    def test_shared_market_shortage_without_spending_does_not_create_military_plan(self):
        c = self.c
        target, _ = self.producer('small_arms')
        c.readings['military_expenses'] = 0
        c.run('sed_refresh_national_plan')
        self.assertEqual(target['variables']['sed_plan_small_arms_rank'], 0)
        self.assertEqual(c.variables['sed_plan_missing_small_arms'], 0)
        self.assertEqual(c.variables['sed_plan_count'], 0)
        c.states.clear()
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_missing_count'], 0)
        self.assertNotIn('sed_small_arms_short_months', c.variables)

    def test_positive_demand_is_revalidated_before_military_approval(self):
        c = self.c
        target, _ = self.producer('ammunition')
        c.run('sed_refresh_diagnostics')
        c.market_goods['ammunition']['market_goods_buy_orders'] = 0
        c.run('sed_run_ammunition_approval', target)
        self.assertEqual(c.constructions, [])

    def test_military_expansion_rejects_staff_inputs_and_unverified_methods(self):
        for field, invalid in (('occupancy', 0.5), ('has_failed_hires', True),
                               ('building_has_goods_shortage', True), ('production_methods', [])):
            with self.subTest(field=field):
                self.setUp()
                c = self.c
                target, producer = self.producer('artillery')
                producer[field] = invalid
                c.run('sed_refresh_diagnostics')
                c.run('sed_run_artillery_approval', target)
                self.assertEqual(c.constructions, [])

    def test_war_bonus_changes_priority_without_bypassing_civilian_candidates(self):
        c = self.c
        military, _ = self.producer('small_arms')
        item = next(item for item in SUPPLY_TARGETS if item['good'] == 'grain')
        farm = building(item['building'])
        farm['production_methods'] = [item['methods'][0]]
        civilian = state(buildings=[farm])
        c.states.append(civilian)
        c.market_goods['grain'] = dict(market_goods_buy_orders=100, market_goods_sell_orders=40,
                                       market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        self.assertEqual(civilian['variables']['sed_plan_grain_rank'], 1)
        c.readings['is_at_war'] = True
        c.run('sed_refresh_national_plan')
        self.assertEqual(military['variables']['sed_plan_small_arms_rank'], 1)
        self.assertEqual(civilian['variables']['sed_plan_grain_rank'], 2)

    def test_direct_automatic_military_execution_obeys_fiscal_protection(self):
        c = self.c
        self.producer('small_arms')
        c.readings.update(net_total_income=-100, gold_reserves=0)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        c.readings.update(net_total_income=100, gold_reserves=1000)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.constructions[0]['building'], 'building_arms_industry')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)

    def test_coordinated_military_priority_uses_one_direct_executor(self):
        c = self.c
        self.producer('ammunition')
        c.variables['advisor_enabled'] = True
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 11)
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.constructions[0]['building'], 'building_munition_plant')
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)

    def test_military_request_result_and_new_state_are_cleaned_on_disable(self):
        c = self.c
        target, producer = self.producer('small_arms')
        c.run('sed_run_small_arms_approval', target)
        producer['level'] += 1
        producer['level_after_queued_constructions'] = producer['level']
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_small_arms_completed'], 1)
        c.run('sed_disable_country')
        self.assertFalse(any('small_arms' in key for key in c.variables))
        self.assertFalse(any('small_arms' in key for key in target['variables']))


if __name__ == '__main__':
    unittest.main()
