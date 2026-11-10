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

    def test_grain_alternative_producer_is_planned_and_queued(self):
        maize = building('building_maize_farm')
        maize['production_methods'] = ['pm_simple_farming']
        target = state(buildings=[maize])
        self.c.states.append(target)
        self.c.market_goods['grain'] = dict(market_goods_has_goods_shortage=True,
                                            market_goods_buy_orders=100,
                                            market_goods_sell_orders=0)
        c = self.c
        c.run('sed_refresh_national_plan')
        self.assertEqual(self.ranked(), [(1, 'grain', target)])
        self.assertEqual(c.variables['sed_plan_missing_grain'], 0)
        c.run('sed_set_mode_assisted')
        c.run('sed_run_grain_approval', target)
        self.assertEqual(c.constructions, [dict(building='building_maize_farm', state=target)])

    def test_alternative_producer_absent_from_rejection_counts_when_eligible(self):
        ranch = building('building_livestock_ranch')
        ranch['production_methods'] = ['pm_simple_ranch']
        target = state(buildings=[ranch])
        self.c.states.append(target)
        self.c.market_goods['fabric'] = dict(market_goods_has_goods_shortage=True)
        c = self.c
        c.run('sed_refresh_supply_candidates')
        self.assertEqual(c.variables['sed_fabric_producer_states'], 1)
        for reason in ('understaffed_states', 'hiring_states', 'input_states', 'method_states',
                       'permission_states', 'infrastructure_states'):
            self.assertEqual(c.variables['sed_fabric_' + reason], 0, reason)
        self.assertEqual(c.variable_lists['sed_fabric_candidates'], [target])

    def test_persistent_shortage_defines_an_annual_industrial_goal(self):
        grain = self.producer('grain', buy=100, sell=30)
        c = self.c
        visible = c.definitions['sed_meta_grain_visible_sgui']
        for expected_months in (1, 2):
            c.run('sed_refresh_national_plan')
            self.assertEqual(c.variables['sed_grain_short_months'], expected_months)
            self.assertFalse(c.condition(child(visible, 'is_shown'), c.country_scope()))
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 3)
        self.assertEqual(c.variables['sed_grain_meta_year'], 1836)
        self.assertTrue(c.condition(child(visible, 'is_shown'), c.country_scope()))
        # A cleared shortage removes the counter but the annual goal lasts to January.
        c.market_goods.clear()
        c.run('sed_refresh_national_plan')
        self.assertNotIn('sed_grain_short_months', c.variables)
        self.assertTrue(c.condition(child(visible, 'is_shown'), c.country_scope()))
        c.readings['year'] = 1837
        self.assertFalse(c.condition(child(visible, 'is_shown'), c.country_scope()))

    def test_annual_goal_keeps_priority_over_a_newer_higher_gap(self):
        grain = self.producer('grain', buy=100, sell=40)
        clothes = self.producer('clothes', buy=100, sell=30)
        self.c.market_goods['clothes']['market_goods_has_goods_shortage'] = False
        c = self.c
        for _ in range(3):
            c.run('sed_refresh_national_plan')
        self.assertEqual([x[1] for x in self.ranked()], ['grain'])
        self.c.market_goods['clothes']['market_goods_has_goods_shortage'] = True
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_pressure_grain'], 60)
        self.assertEqual(c.variables['sed_plan_pressure_clothes'], 70)
        self.assertEqual(c.variables['sed_clothes_short_months'], 1)
        self.assertEqual(grain['variables']['sed_plan_grain_score'], 185)
        self.assertEqual(clothes['variables']['sed_plan_clothes_score'], 170)
        self.assertEqual([x[1] for x in self.ranked()], ['grain', 'clothes'])
        self.assertEqual([x[2] for x in self.ranked()], [grain, clothes])

    def test_disable_clears_shortage_counters_and_annual_goal(self):
        self.producer('grain')
        c = self.c
        for _ in range(3):
            c.run('sed_refresh_national_plan')
        c.run('sed_disable_country')
        self.assertNotIn('sed_grain_short_months', c.variables)
        self.assertNotIn('sed_grain_meta_year', c.variables)

    def test_automatic_fiscal_policy_raises_tax_and_restores_on_mode_change(self):
        c = self.c
        c.readings['gold_reserves'] = 100  # Status 2: reserves under four weeks.
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_fiscal_status'], 2)
        self.assertEqual(c.readings['tax_level'], 'high')
        self.assertEqual(c.variables['sed_tax_level_saved'], 3)
        c.run('sed_set_mode_assisted')
        self.assertEqual(c.readings['tax_level'], 'medium')
        self.assertNotIn('sed_tax_level_saved', c.variables)

    def test_fiscal_policy_caps_at_very_high_and_disable_restores(self):
        c = self.c
        c.readings['gold_reserves'] = 100
        c.run('sed_set_mode_automatic')
        for _ in range(3):
            c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'very_high')
        self.assertEqual(c.tax_changes, ['high', 'very_high'])
        c.run('sed_disable_country')
        self.assertEqual(c.readings['tax_level'], 'medium')
        self.assertNotIn('sed_tax_level_saved', c.variables)

    def test_fiscal_policy_lowers_one_step_only_when_healthy(self):
        c = self.c
        c.readings.update(principal=0, gold_reserves=1000, net_total_income=100)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_fiscal_status'], 1)
        self.assertEqual(c.readings['tax_level'], 'low')
        c.readings['principal'] = 1
        c.run('sed_set_mode_manual')
        self.assertEqual(c.readings['tax_level'], 'medium')
        c.readings['gold_reserves'] = 100
        c.run('sed_set_mode_assisted')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'medium')
        self.assertNotIn('sed_tax_level_saved', c.variables)

    def test_wage_policy_cuts_in_crisis_to_floor_and_restores(self):
        c = self.c
        c.readings.update(gold_reserves=100, net_total_income=-100)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_fiscal_status'], 3)
        self.assertEqual(c.readings['government_wage_level'], 'low')
        self.assertEqual(c.variables['sed_gov_wage_saved'], 3)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.wage_changes, ['low'])
        c.run('sed_set_mode_manual')
        self.assertEqual(c.readings['government_wage_level'], 'medium')
        self.assertNotIn('sed_gov_wage_saved', c.variables)

    def test_wage_policy_raises_with_health_up_to_medium(self):
        c = self.c
        c.readings.update(government_wage_level='low', principal=0,
                          net_total_income=100, gold_reserves=1000)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['government_wage_level'], 'medium')
        self.assertEqual(c.variables['sed_gov_wage_saved'], 2)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.wage_changes, ['medium'])
        c.run('sed_disable_country')
        self.assertEqual(c.readings['government_wage_level'], 'low')

    def test_wage_policy_stays_put_under_caution(self):
        c = self.c
        c.readings.update(gold_reserves=100, net_total_income=100)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_fiscal_status'], 2)
        self.assertEqual(c.readings['tax_level'], 'high')
        self.assertEqual(c.wage_changes, [])
        self.assertNotIn('sed_gov_wage_saved', c.variables)

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
