"""Military-economic assessment regressions; synthetic script execution."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country


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


if __name__ == '__main__':
    unittest.main()
