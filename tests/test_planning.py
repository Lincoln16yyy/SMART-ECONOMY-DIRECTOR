"""National planning policy scenarios; script simulation, not engine evidence."""
import unittest
import tempfile
from pathlib import Path

from tools.build_mod import ACTION_NAMES, SUPPLY_TARGETS, outputs
from tools.pdx_script import child, parse, walk
from tools.validate import validate
from test_diagnostics import script_definitions
from script_harness import Country, building, construction_sector, railway, state


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def test_tax_goal_requires_an_incorporated_state(self):
        c = self.c
        target = state(incorporated=False, tax_capacity_usage=200, tax_capacity=100)
        c.states = [target]
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        target['is_incorporated'] = True
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 7)
        target['tax_capacity'] = 200
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 8)

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

    def test_queued_railway_keeps_goal_until_cancellation_or_completion(self):
        c = self.c
        rail = railway(queued_levels=1)
        target = state(-10, buildings=[rail])
        c.states = [target]
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 1)
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        self.assertEqual(c.variables['sed_plan_count'], 0)
        rail['level_after_queued_constructions'] = rail['level']
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 1)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        self.assertEqual(c.variables['sed_plan_count'], 1)
        target['infrastructure_delta'] = 5
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)

    def test_queued_supply_waits_only_for_verified_output_and_current_shortage(self):
        c = self.c
        target = self.producer('fabric')
        producer = target['buildings'][0]
        producer['level_after_queued_constructions'] = 2
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 2)
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        producer['production_methods'] = []
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        producer['production_methods'] = ['default_building_cotton_plantation']
        c.market_goods['fabric']['market_goods_has_goods_shortage'] = False
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_waiting'], 0)

    def test_other_eligible_priority_takes_over_from_queued_bottleneck(self):
        c = self.c
        c.states = [state(-10, buildings=[railway(queued_levels=1)])]
        self.producer('grain')
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 2)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        self.assertEqual(self.ranked()[0][1], 'grain')

    def test_queued_administration_waits_only_in_an_affected_incorporated_state(self):
        c = self.c
        admin = building('building_government_administration', queued_levels=1)
        target = state(tax_capacity_usage=200, tax_capacity=100, buildings=[admin])
        c.states = [target]
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 7)
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        target['tax_capacity'] = 200
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        c.readings['bureaucracy'] = -10
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 6)
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        target['is_incorporated'] = False
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_waiting'], 0)

    def test_power_waiting_requires_queued_plant_in_the_expensive_state(self):
        c = self.c
        plant = building('building_power_plant', queued_levels=1)
        expensive = state(state_goods={'electricity': {'state_goods_pricier': 0.3}})
        cheap = state(buildings=[plant])
        c.states = [expensive, cheap]
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 9)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        expensive['buildings'] = [plant]
        cheap['buildings'] = []
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        expensive['state_goods']['electricity']['state_goods_pricier'] = 0.1
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)

    def test_fiscal_crisis_overrides_waiting_construction(self):
        c = self.c
        c.states = [state(-10, buildings=[railway(queued_levels=1)])]
        c.readings.update(net_total_income=-100, gold_reserves=0)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_plan_goal'], 4)
        self.assertEqual(c.variables['sed_plan_waiting'], 0)

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
            c.readings['month'] = expected_months - 1
            c.run('sed_refresh_national_plan')
            self.assertEqual(c.variables['sed_grain_short_months'], expected_months)
            self.assertFalse(c.condition(child(visible, 'is_shown'), c.country_scope()))
        c.readings['month'] = 2
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
        for month in range(3):
            c.readings['month'] = month
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
        for month in range(3):
            c.readings['month'] = month
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

    def test_fiscal_commands_record_date_and_levels_without_rewriting_on_noop(self):
        c = self.c
        c.readings.update(gold_reserves=0, net_total_income=-100, month=4,
                          tax_level='medium', government_wage_level='medium')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        for policy, expected_to in (('tax', 4), ('wage', 2)):
            self.assertEqual(c.variables[f'sed_{policy}_last_from'], 3)
            self.assertEqual(c.variables[f'sed_{policy}_last_to'], expected_to)
            self.assertEqual(c.variables[f'sed_{policy}_last_year'], 1836)
            self.assertEqual(c.variables[f'sed_{policy}_last_month'], 5)
        receipt = {k: v for k, v in c.variables.items()
                   if k.startswith(('sed_tax_last_', 'sed_wage_last_'))}
        c.run('sed_auto_apply_monthly')
        self.assertEqual({k: v for k, v in c.variables.items() if k in receipt}, receipt)
        c.run('sed_set_mode_assisted')
        self.assertEqual(c.variables['sed_tax_last_to'], 4)
        self.assertEqual(c.variables['sed_wage_last_to'], 2)
        c.run('sed_disable_country')
        self.assertNotIn('sed_tax_last_from', c.variables)
        self.assertNotIn('sed_wage_last_from', c.variables)
        self.assertIn('sed_tax_last_change_month', c.variables)
        self.assertIn('sed_wage_last_change_month', c.variables)

    def test_fiscal_commands_at_limits_do_not_fabricate_history(self):
        c = self.c
        c.readings.update(gold_reserves=0, net_total_income=-100,
                          tax_level='very_high', government_wage_level='low')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('sed_tax_last_from', c.variables)
        self.assertNotIn('sed_wage_last_from', c.variables)

    def test_fiscal_policy_caps_at_very_high_and_disable_restores(self):
        c = self.c
        c.readings['gold_reserves'] = 100
        c.run('sed_set_mode_automatic')
        for month in range(3):
            c.readings['month'] = month
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

    def test_shortage_samples_ignore_repeated_refreshes_and_reset_across_gaps(self):
        self.producer('grain')
        c = self.c
        for _ in range(8):
            c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 1)
        self.assertNotIn('sed_grain_meta_year', c.variables)
        c.readings['month'] = 1
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 2)
        c.readings['month'] = 3
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 1)
        self.assertNotIn('sed_grain_meta_year', c.variables)
        for month in (4, 5):
            c.readings['month'] = month
            c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_meta_year'], 1836)

    def test_shortage_legacy_counters_without_dates_do_not_create_a_goal(self):
        self.producer('grain')
        c = self.c
        c.variables['sed_grain_short_months'] = 100
        c.variables['sed_grain_meta_year'] = 1836
        c.variables.pop('sed_grain_short_sample_month', None)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 1)
        self.assertNotIn('sed_grain_meta_year', c.variables)
        c.readings.update(year=1836, month=11)
        c.run('sed_refresh_national_plan')
        c.readings.update(year=1837, month=0)
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_short_months'], 2)
        c.readings['month'] = 1
        c.run('sed_refresh_national_plan')
        self.assertEqual(c.variables['sed_grain_meta_year'], 1837)

    def test_tax_changes_once_per_month_across_mode_changes_and_reactivation(self):
        c = self.c
        c.readings['gold_reserves'] = 100
        c.run('sed_set_mode_automatic')
        for _ in range(4):
            c.run('sed_auto_apply_monthly')
        self.assertEqual(c.tax_changes, ['high'])
        marker = c.variables['sed_tax_last_change_month']
        c.run('sed_set_mode_assisted')
        self.assertEqual(c.readings['tax_level'], 'medium')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'medium')
        c.run('sed_disable_country')
        self.assertEqual(c.variables['sed_tax_last_change_month'], marker)
        c.run('sed_enable_country')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'medium')
        c.readings['month'] = 1
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'high')

    def test_healthy_tax_policy_stops_at_low_and_keeps_month_available_at_floor(self):
        c = self.c
        c.readings.update(principal=0, gold_reserves=1000, tax_level='low')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'low')
        self.assertEqual(c.tax_changes, [])
        self.assertNotIn('sed_tax_last_change_month', c.variables)
        c.readings['gold_reserves'] = 100
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['tax_level'], 'medium')

    def test_wages_change_once_per_calendar_month_and_restore_original_level(self):
        c = self.c
        c.readings.update(government_wage_level='very_high', gold_reserves=100,
                          net_total_income=-100, year=1836, month=11)
        c.run('sed_set_mode_automatic')
        for _ in range(4):
            c.run('sed_auto_apply_monthly')
        self.assertEqual(c.wage_changes, ['high'])
        c.run('sed_set_mode_manual')
        self.assertEqual(c.readings['government_wage_level'], 'very_high')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['government_wage_level'], 'very_high')
        c.readings.update(year=1837, month=0)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['government_wage_level'], 'high')
        c.run('sed_disable_country')
        self.assertEqual(c.readings['government_wage_level'], 'very_high')
        self.assertIn('sed_wage_last_change_month', c.variables)

    def test_conflicting_manual_mode_blocks_tax_and_wage_effects(self):
        c = self.c
        c.readings.update(gold_reserves=100, net_total_income=-100)
        c.run('sed_refresh_national_plan')
        c.variables.update(sed_mode_automatic=1, sed_mode_manual=1)
        c.run('sed_apply_fiscal_policy')
        c.run('sed_apply_wage_policy')
        self.assertEqual(c.tax_changes, [])
        self.assertEqual(c.wage_changes, [])

    def test_tracked_grain_request_does_not_wait_for_another_variant_queue(self):
        target = self.producer('grain')
        wheat = target['buildings'][0]
        rye = building('building_rye_farm', queued_levels=1)
        rye['production_methods'] = ['pm_simple_farming']
        target['buildings'].append(rye)
        c = self.c
        c.run('sed_run_grain_approval', target)
        wheat['level_after_queued_constructions'] = wheat['level']
        c.run('sed_refresh_supply_candidates')
        self.assertNotIn('sed_grain_request_pending', target['variables'])
        self.assertEqual(c.variables['sed_grain_abandoned'], 1)
        self.assertEqual(c.variables['sed_grain_intents'], 1)

    def test_destroyed_tracked_producer_closes_request_without_fabricating_completion(self):
        target = self.producer('grain')
        c = self.c
        c.run('sed_run_grain_approval', target)
        target['buildings'].clear()
        c.run('sed_refresh_supply_candidates')
        self.assertNotIn('sed_grain_request_pending', target['variables'])
        self.assertEqual(c.variables['sed_grain_abandoned'], 1)
        self.assertNotIn('sed_grain_completed', c.variables)

    def test_validator_rejects_fiscal_monthly_guard_bypass_and_marker_cleanup(self):
        for policy, marker in [('tax', 'sed_tax_last_change_month'),
                               ('wage', 'sed_wage_last_change_month')]:
            with self.subTest(policy=policy), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, data in outputs().items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                path = root / 'common/scripted_effects/sed_effects.txt'
                text = path.read_text(encoding='utf-8-sig').replace(
                    f'NOT = {{ sed_{policy}_month_limit_reached = yes }}', '', 1)
                text = text.replace('sed_disable_country = {',
                                    f'sed_disable_country = {{\n remove_variable = {marker}', 1)
                path.write_text(text, encoding='utf-8-sig')
                errors = validate(root)
                self.assertTrue(any('monthly or mode exclusion' in error for error in errors))
                self.assertTrue(any('monthly safety marker' in error for error in errors))

    def test_supply_book_records_completed_and_abandoned_outcomes(self):
        target = self.producer('grain')
        building = target['buildings'][0]
        c = self.c
        c.run('sed_set_mode_assisted')
        c.run('sed_run_grain_approval', target)
        self.assertEqual(target['variables']['sed_grain_intent_level'], 1)
        self.assertEqual(target['variables']['sed_grain_intent_variant'], 1)
        self.assertEqual(c.variables['sed_grain_intents'], 1)
        building['level_after_queued_constructions'] = 2
        c.run('sed_refresh_supply_candidates')
        self.assertIn('sed_grain_request_pending', target['variables'])
        building['level'] = 2
        c.run('sed_refresh_supply_candidates')
        self.assertNotIn('sed_grain_request_pending', target['variables'])
        self.assertEqual(c.variables['sed_grain_completed'], 1)
        self.assertEqual(c.variables['sed_grain_result'], 1)
        self.assertNotIn('sed_grain_intent_level', target['variables'])
        # A request that leaves the queue without a higher level is abandoned.
        c.run('sed_run_grain_approval', target)
        building['level_after_queued_constructions'] = 3
        c.run('sed_refresh_supply_candidates')
        building['level_after_queued_constructions'] = 2
        c.run('sed_refresh_supply_candidates')
        self.assertEqual(c.variables['sed_grain_abandoned'], 1)
        self.assertEqual(c.variables['sed_grain_result'], 2)
        self.assertEqual(c.variables['sed_grain_intents'], 2)

    def test_railway_and_sector_books_record_outcomes(self):
        target = state(-5, buildings=[railway()])
        sector = state(buildings=[construction_sector()])
        self.c.states.extend([target, sector])
        c = self.c
        c.readings['num_queued_government_constructions'] = 3
        c.run('sed_set_mode_assisted')
        c.run('sed_run_railway_approval', target)
        self.assertEqual(target['variables']['sed_railway_intent_level'], 1)
        self.assertEqual(c.variables['sed_railway_intents'], 1)
        c.run('sed_run_construction_approval', sector)
        self.assertEqual(sector['variables']['sed_construction_intent_level'], 1)
        self.assertEqual(c.variables['sed_construction_intents'], 1)
        target['buildings'][0]['level_after_queued_constructions'] = 2
        sector['buildings'][0]['level_after_queued_constructions'] = 2
        c.run('sed_refresh_railway_candidates')
        c.run('sed_refresh_construction_candidates')
        self.assertIn('sed_railway_request_pending', target['variables'])
        self.assertIn('sed_construction_request_pending', sector['variables'])
        target['buildings'][0]['level'] = 2
        sector['buildings'][0]['level_after_queued_constructions'] = 1
        c.run('sed_refresh_railway_candidates')
        c.run('sed_refresh_construction_candidates')
        self.assertEqual(c.variables['sed_railway_completed'], 1)
        self.assertEqual(c.variables['sed_railway_result'], 1)
        self.assertEqual(c.variables['sed_construction_abandoned'], 1)
        self.assertEqual(c.variables['sed_construction_result'], 2)
        self.assertNotIn('sed_railway_intent_level', target['variables'])
        self.assertNotIn('sed_construction_intent_level', sector['variables'])

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
