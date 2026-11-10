"""National planning policy scenarios; script simulation, not engine evidence."""
import unittest

from tools.build_mod import ACTION_NAMES, SUPPLY_TARGETS
from tools.pdx_script import child, parse, walk
from test_diagnostics import script_definitions
from script_harness import Country, building, railway, state


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def producer(self, good, target=None, buy=100, sell=40):
        item = next(x for x in SUPPLY_TARGETS if x['good'] == good)
        b = building(item['building'])
        b['production_methods'] = [item['methods'][0]]
        if target is None:
            target = state()
            self.c.states.append(target)
        target['buildings'].append(b)
        self.c.market_goods[good] = dict(market_goods_has_goods_shortage=True,
                                        market_goods_buy_orders=buy,
                                        market_goods_sell_orders=sell)
        return target

    def ranked(self):
        result = []
        for rank in (1, 2, 3):
            for name in ACTION_NAMES:
                for target in self.c.variable_lists.get(f'sed_plan_{rank}_{name}', []):
                    result.append((rank, name, target))
        return result

    def test_severity_overrides_previous_fixed_type_order_and_drives_executor(self):
        wood = self.producer('wood', buy=100, sell=50)
        grain = self.producer('grain', buy=100, sell=0)
        self.c.states.append(state(-5, buildings=[railway()]))
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual([x[1] for x in self.ranked()], ['grain', 'wood', 'railway'])
        self.assertEqual(self.c.constructions[0]['state'], grain)
        self.assertEqual(self.c.constructions[0]['building'], 'building_wheat_farm')
        self.assertEqual(self.c.variables['sed_plan_goal'], 2)
        self.assertEqual(self.c.variables['sed_auto_review_status'], 1)

    def test_exactly_three_global_pairs_even_when_one_state_has_several_types(self):
        target = self.producer('grain', buy=100, sell=0)
        self.producer('clothes', target, buy=100, sell=10)
        self.producer('tools', target, buy=100, sell=20)
        self.producer('wood', target, buy=100, sell=30)
        self.c.run('sed_refresh_national_plan')
        self.assertEqual([x[1] for x in self.ranked()], ['grain', 'clothes', 'tools'])
        self.assertTrue(all(x[2] is target for x in self.ranked()))
        self.assertEqual(self.c.variables['sed_plan_count'], 3)
        self.assertEqual(target['variables']['sed_plan_wood_rank'], 0)

    def test_filters_run_before_scores_and_ignored_targets_do_not_rank(self):
        invalid = self.producer('grain', buy=100, sell=0)
        invalid['buildings'][0]['has_failed_hires'] = True
        ignored = self.producer('clothes', buy=100, sell=0)
        ignored['variables']['sed_clothes_ignored'] = True
        good = self.producer('wood', buy=100, sell=40)
        self.c.run('sed_refresh_national_plan')
        self.assertEqual(self.ranked(), [(1, 'wood', good)])

    def test_supply_gap_is_relative_clamped_and_zero_orders_are_safe(self):
        self.producer('grain', buy=100, sell=25)
        self.c.run('sed_refresh_national_plan')
        self.assertEqual(self.c.variables['sed_plan_pressure_grain'], 75)
        self.c.market_goods['grain'].update(market_goods_buy_orders=10000,
                                           market_goods_sell_orders=2500)
        self.c.run('sed_refresh_national_plan')
        self.assertEqual(self.c.variables['sed_plan_pressure_grain'], 75)
        for buy, sell in [(0, 20), (100, 150)]:
            self.c.market_goods['grain'].update(market_goods_buy_orders=buy,
                                               market_goods_sell_orders=sell)
            self.c.run('sed_refresh_national_plan')
            self.assertEqual(self.c.variables['sed_plan_pressure_grain'], 0)

    def test_infrastructure_severity_and_goal_use_current_readings(self):
        small = state(-5, buildings=[railway()])
        large = state(-70, buildings=[railway()])
        self.c.states = [small, large]
        self.c.run('sed_refresh_national_plan')
        self.assertIs(self.ranked()[0][2], large)
        self.assertEqual(self.c.variables['sed_plan_goal'], 1)
        large['infrastructure_delta'] = 0
        small['infrastructure_delta'] = 0
        self.c.run('sed_refresh_national_plan')
        self.assertEqual(self.ranked(), [])
        self.assertEqual(self.c.variables['sed_plan_goal'], 8)
        self.assertEqual(self.c.variables['sed_plan_count'], 0)

    def test_fiscal_policy_scale_invariance_boundaries_and_unknown_credit(self):
        for scale in (0.01, 1, 1000):
            with self.subTest(scale=scale):
                c = self.c
                c.readings.update(net_total_income=scale, net_fixed_income=scale,
                                  fixed_expenses=10 * scale, gold_reserves=40 * scale,
                                  principal=75 * scale, credit=100 * scale)
                self.assertTrue(c.condition(c.definitions['sed_auto_fiscal_safe'], c.country_scope()))
                c.readings['gold_reserves'] = 39.99 * scale
                self.assertFalse(c.condition(c.definitions['sed_auto_fiscal_safe'], c.country_scope()))
                c.readings.update(gold_reserves=40 * scale, principal=75.01 * scale)
                self.assertFalse(c.condition(c.definitions['sed_auto_fiscal_safe'], c.country_scope()))
        c.readings.update(principal=1, credit=0)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_fiscal_status'], 3)
        c.readings.update(principal=0, credit=0, fixed_expenses=0, gold_reserves=0)
        self.assertTrue(c.condition(c.definitions['sed_auto_fiscal_safe'], c.country_scope()))

    def test_fiscal_block_revalidates_effect_and_leaves_assisted_approval(self):
        target = self.producer('grain')
        c = self.c
        c.run('sed_set_mode_automatic')
        for readings in ({'net_total_income': -1}, {'net_fixed_income': -1},
                         {'gold_reserves': 199}, {'principal': 751}):
            with self.subTest(readings=readings):
                baseline = c.readings.copy()
                c.readings.update(readings)
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.variables['sed_auto_review_status'], 17)
                c.run('sed_run_grain_approval', target)
                self.assertEqual(c.constructions, [])
                self.assertNotIn('sed_auto_last_attempt_month', c.variables)
                c.readings = baseline
        c.readings['net_total_income'] = -1
        c.run('sed_set_mode_assisted')
        c.run('sed_run_grain_approval', target)
        self.assertEqual(len(c.constructions), 1)

    def test_fiscal_crisis_and_default_objectives_do_not_fake_tax_actions(self):
        self.producer('grain')
        for readings, status in [({'net_total_income': -100, 'gold_reserves': 399}, 3),
                                 ({'in_default': True}, 4)]:
            self.c.readings.update(readings)
            self.c.run('sed_refresh_national_plan')
            self.assertEqual(self.c.variables['sed_fiscal_status'], status)
            self.assertEqual(self.c.variables['sed_plan_goal'], 4)
            self.assertEqual(self.c.constructions, [])

    def test_plan_rebuilds_after_external_change_mode_and_cleanup(self):
        target = self.producer('grain')
        c = self.c
        c.run('sed_refresh_diagnostics')
        self.assertEqual(self.ranked(), [(1, 'grain', target)])
        c.run('sed_set_mode_manual')
        c.market_goods.clear()
        c.run('sed_refresh_diagnostics')
        self.assertEqual(self.ranked(), [])
        c.run('sed_disable_country')
        self.assertFalse(any(k.startswith('sed_plan_') for k in c.variables))
        self.assertFalse(any(k.startswith('sed_plan_') for k in target['variables']))
        self.assertFalse(any(k.startswith('sed_plan_') for k in c.variable_lists))

    def test_only_populated_rank_lists_are_visible_in_the_main_plan(self):
        self.producer('grain')
        c = self.c
        c.run('sed_refresh_national_plan')
        visible = []
        for rank in (1, 2, 3):
            for name in ACTION_NAMES:
                gui = c.definitions[f'sed_plan_{rank}_{name}_visible_sgui']
                if c.condition(child(gui, 'is_shown'), c.country_scope()):
                    visible.append((rank, name))
        self.assertEqual(visible, [(1, 'grain')])
        c.market_goods.clear()
        c.run('sed_refresh_national_plan')
        self.assertFalse(c.condition(child(c.definitions['sed_plan_1_grain_visible_sgui'],
                                           'is_shown'), c.country_scope()))

    def test_reserve_drawdown_guard_scales_and_rejects_operating_deficit(self):
        c = self.c
        for scale in (0.01, 1, 1000):
            with self.subTest(scale=scale):
                c.readings.update(net_total_income=-10 * scale, net_fixed_income=100 * scale,
                                  fixed_expenses=50 * scale, gold_reserves=860 * scale,
                                  principal=0)
                self.assertTrue(c.condition(c.definitions['sed_coord_reserve_drawdown_safe'], c.country_scope()))
                self.assertFalse(c.condition(c.definitions['sed_auto_fiscal_safe'], c.country_scope()))
                c.readings['net_fixed_income'] = -1
                self.assertFalse(c.condition(c.definitions['sed_coord_reserve_drawdown_safe'], c.country_scope()))

    def test_queue_wait_preserves_plan_but_never_calls_constructor(self):
        self.producer('grain')
        c = self.c
        c.readings['construction_queue_num_queued_government_levels'] = 1
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_count'], 1)
        self.assertEqual(c.variables['sed_auto_review_status'], 11)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)


if __name__ == '__main__':
    unittest.main()
