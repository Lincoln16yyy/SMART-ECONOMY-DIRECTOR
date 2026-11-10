"""Version-specific option adapter tests; not cross-mod engine integration."""
import tempfile
from pathlib import Path
import unittest

from tools.build_mod import outputs, SUPPLY_TARGETS
from tools.coordination import OPTIONS, ADVISOR_POLICY_OPTIONS, SUPPLY_POLICY_OPTIONS
from tools.validate import validate
from test_diagnostics import script_definitions
from script_harness import Country, railway, state, building


class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.original = {option: value for (_, option, _), value in zip(OPTIONS, (1, 0, 25, 11, 3, 100, 6))}
        self.c.variables.update(self.original)
        self.c.variables['advisor_enabled'] = True
        self.c.states = [state(-12, buildings=[railway()])]

    def external(self):
        return {option: self.c.variables[option] for _, option, _ in OPTIONS if option in self.c.variables}

    def test_automatic_takes_control_and_chooses_only_supply_railways(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        self.assertIn('sed_coord_active', c.variables)
        self.assertEqual(self.external(), {'zw_var_scsab_construct_railway': 1})
        self.assertEqual(c.variables['sed_coord_executor'], 2)
        self.assertEqual(c.constructions, [])
        self.assertEqual(len(c.scheduled_events), 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 18)
        self.assertEqual(c.constructions, [])
        self.assertNotIn('sed_auto_last_attempt_month', c.variables)
        c.run('sed_run_railway_approval', c.states[0])
        self.assertEqual(c.constructions, [])  # Never run both own and delegated executor.

    def test_repeated_enable_or_automatic_does_not_overwrite_original_options(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        saved = {name: value for name, value in c.variables.items() if name.startswith('sed_coord_saved_')}
        c.run('sed_coord_enable')
        c.run('sed_set_mode_automatic')
        self.assertEqual({name: value for name, value in c.variables.items() if name.startswith('sed_coord_saved_')}, saved)
        c.run('sed_coord_restore')
        self.assertEqual(self.external(), self.original)
        c.run('sed_coord_restore')
        self.assertEqual(self.external(), self.original)

    def test_manual_assisted_and_disable_restore_exact_values(self):
        for action in ('sed_set_mode_manual', 'sed_set_mode_assisted', 'sed_disable_country'):
            with self.subTest(action=action):
                c = self.c
                c.run('sed_set_mode_automatic')
                c.run(action)
                self.assertEqual(self.external(), self.original)
                self.assertNotIn('sed_coord_active', c.variables)
                self.assertFalse(any(k.startswith('sed_coord_saved_') for k in c.variables))
                if action == 'sed_disable_country':
                    c.run('sed_enable_country')

    def test_missing_original_options_remain_absent_after_restore(self):
        c = self.c
        for _, option, _ in OPTIONS:
            c.variables.pop(option, None)
        c.variables['zw_var_scsab_gov_admin_for_institution'] = 2
        c.run('sed_set_mode_automatic')
        self.assertEqual(self.external(), {'zw_var_scsab_construct_railway': 1})
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.external(), {})
        self.assertTrue(c.variables['advisor_enabled'])

    def test_critical_fiscal_readings_pause_both_builders_then_recover(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.readings['net_total_income'] = -100
        c.run('sed_monthly_update')
        self.assertEqual(self.external(), {})
        self.assertEqual(c.variables['sed_coord_executor'], 0)
        self.assertEqual(c.constructions, [])
        c.readings['net_total_income'] = 100
        c.run('sed_monthly_update')
        self.assertEqual(self.external(), {'zw_var_scsab_construct_railway': 1})
        c.readings['is_construction_paused'] = True
        c.run('sed_monthly_update')
        self.assertEqual(self.external(), {})

    def test_no_producer_shortage_delegates_to_advisor_and_preserves_unrelated_options(self):
        c = self.c
        c.states.clear()
        c.market_goods['grain'] = {'market_goods_has_goods_shortage': True,
                                    'market_goods_buy_orders': 100, 'market_goods_sell_orders': 0}
        unrelated = {'advisor_pm_balance_enabled': 1, 'advisor_labor_auto_enabled': 1,
                     'zw_var_expand_building_food': 0, 'gora_auto_export_enabled': 1}
        c.variables.update(unrelated)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_plan_goal'], 5)
        self.assertEqual(c.variables['sed_plan_missing_grain'], 1)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        for key, value in unrelated.items():
            self.assertEqual(c.variables[key], value)
        self.assertEqual(c.constructions, [])

    def test_supply_chain_fallback_only_enables_chains_and_preserves_zero_value(self):
        c = self.c
        c.variables.pop('advisor_enabled')
        c.variables.pop('advisor_auto_construction_enabled')
        c.states.clear()
        c.market_goods['tools'] = {'market_goods_has_goods_shortage': True}
        c.run('sed_set_mode_automatic')
        self.assertEqual(self.external(), {'zw_var_expand_building': 0})
        self.assertEqual(c.variables['sed_coord_executor'], 3)
        c.run('sed_coord_restore')
        expected = {k: v for k, v in self.original.items() if k != 'advisor_auto_construction_enabled'}
        self.assertEqual(self.external(), expected)

    def test_aroai_unknown_adapter_does_not_enable_another_concurrent_builder(self):
        c = self.c
        c.variables['aroai_autobuild'] = 1
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_executor'], 5)
        self.assertEqual(self.external(), {})
        self.assertEqual(c.variables['aroai_autobuild'], 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_player_activation_guards_and_unknown_tools(self):
        c = self.c
        c.readings['is_player'] = False
        c.run('sed_coord_enable')
        self.assertEqual(self.external(), self.original)
        self.assertNotIn('sed_coord_active', c.variables)
        c.readings['is_player'] = True
        c.run('sed_disable_country')
        c.run('sed_coord_enable')
        self.assertEqual(self.external(), self.original)
        self.assertNotIn('sed_coord_active', c.variables)

    def test_administration_power_and_growth_goals_select_their_domain_only(self):
        c = self.c
        c.states = [state()]
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})
        c.readings['bureaucracy'] = -10
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_plan_goal'], 6)
        self.assertEqual(self.external(), {'zw_var_scsab_gov_admin': 1})
        c.readings['bureaucracy'] = 0
        c.states[0].update(tax_capacity_usage=200, tax_capacity=100)
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_plan_goal'], 7)
        self.assertEqual(self.external(), {'zw_var_scsab_gov_admin_for_tax': 1})
        c.states[0].update(tax_capacity_usage=100, tax_capacity=100,
                           state_goods={'electricity': {'state_goods_pricier': 0.3}})
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_plan_goal'], 9)
        self.assertEqual(self.external(), {'zw_var_scsab_construct_power_plant': 1})
        c.states[0]['state_goods']['electricity']['state_goods_pricier'] = 0.19
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})

    def test_manual_diagnostic_schedule_does_not_disable_coordination_reviews(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.variables.pop('sed_monthly_refresh')
        c.readings['net_total_income'] = -100
        c.run('sed_monthly_update')
        self.assertEqual(self.external(), {})
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.external(), self.original)

    def test_sync_refuses_conflicting_manual_mode_and_does_not_override_options(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        before = self.external()
        c.variables['sed_mode_manual'] = 1
        c.readings['net_total_income'] = -100
        c.run('sed_coord_sync')
        self.assertEqual(self.external(), before)

    def advisor_policy(self):
        return {option: self.c.variables[option] for _, option in ADVISOR_POLICY_OPTIONS
                if option in self.c.variables}

    def test_growth_applies_balanced_budget_and_restores_all_original_policy_values(self):
        c = self.c
        c.states.clear()
        originals = {option: index + 4 for index, (_, option) in enumerate(ADVISOR_POLICY_OPTIONS)}
        c.variables.update(originals)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 1)
        self.assertEqual(self.advisor_policy(), {})
        saved = {k: v for k, v in c.variables.items() if k.startswith('sed_coord_saved_')}
        c.run('sed_coord_sync')
        self.assertEqual({k: v for k, v in c.variables.items() if k.startswith('sed_coord_saved_')}, saved)
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.advisor_policy(), originals)
        self.assertEqual(self.external(), self.original)

    def test_essentials_and_debt_choose_different_advisor_objectives(self):
        c = self.c
        c.states.clear()
        c.market_goods['grain'] = {'market_goods_has_goods_shortage': True}
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 2)
        self.assertEqual(self.advisor_policy(), {'advisor_setting_sc_goal_sol': True})
        c.readings['principal'] = 500
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 3)
        self.assertEqual(self.advisor_policy(), {'advisor_setting_sc_goal_treasury': True,
                                                'advisor_setting_treasury_off': True})
        c.readings['principal'] = 499
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 2)
        c.run('sed_disable_country')
        self.assertEqual(self.advisor_policy(), {})

    def test_legacy_active_coordination_captures_policy_before_first_write(self):
        c = self.c
        c.run('sed_set_mode_automatic')  # Railways selected, no Advisor authorization.
        for name, _ in ADVISOR_POLICY_OPTIONS:
            c.variables.pop('sed_coord_saved_' + name, None)
        c.variables.pop('sed_coord_policy_saved', None)
        original = {'advisor_setting_borrow': 7, 'advisor_setting_sc_goal_sol': 3}
        c.variables.update(original)
        c.states.clear()
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 1)
        self.assertEqual(self.advisor_policy(), {})
        c.run('sed_set_mode_manual')
        self.assertEqual(self.advisor_policy(), original)

    def test_legacy_release_without_new_policy_snapshot_preserves_policy(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.variables.pop('sed_coord_policy_saved', None)
        original = {'advisor_setting_borrow': 7, 'advisor_setting_sc_goal_sol': 3}
        c.variables.update(original)
        c.run('sed_set_mode_manual')
        self.assertEqual(self.advisor_policy(), original)

    def test_supply_executor_does_not_change_advisor_policy(self):
        c = self.c
        original = {'advisor_setting_borrow': 2, 'advisor_setting_treasury_off': 5}
        c.variables.update(original)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_executor'], 2)
        self.assertEqual(self.advisor_policy(), original)
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 0)

    def test_reserve_funded_construction_keeps_advisor_authorized_until_floor(self):
        c = self.c
        c.states.clear()
        c.readings.update(net_total_income=-10, net_fixed_income=100,
                          fixed_expenses=50, gold_reserves=860, principal=0)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_fiscal_status'], 5)
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})
        c.readings['gold_reserves'] = 859
        c.run('sed_monthly_update')
        self.assertEqual(c.variables['sed_coord_executor'], 0)
        self.assertEqual(self.external(), {})
        c.readings['gold_reserves'] = 1000
        c.readings['principal'] = 1
        c.run('sed_monthly_update')
        self.assertEqual(self.external(), {})
        self.assertEqual(c.constructions, [])

    def test_reserve_drawdown_routes_infrastructure_to_advisor_and_not_supply(self):
        c = self.c
        c.readings.update(net_total_income=-10, net_fixed_income=100,
                          fixed_expenses=50, gold_reserves=860, principal=0)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_plan_goal'], 1)
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})
        c.run('sed_set_mode_assisted')
        c.variables.pop('advisor_enabled')
        c.variables.pop('advisor_auto_construction_enabled')
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_executor'], 0)
        self.assertEqual(self.external(), {})

    def test_specific_goals_use_only_the_matching_supply_routine(self):
        for goal, option, executor in (
            (6, 'zw_var_scsab_gov_admin', 6),
            (7, 'zw_var_scsab_gov_admin_for_tax', 7),
            (9, 'zw_var_scsab_construct_power_plant', 8),
            (3, 'zw_var_more_construction_sectors', 4),
        ):
            with self.subTest(goal=goal):
                self.setUp()
                c = self.c
                c.run('sed_set_mode_automatic')
                c.variables['sed_plan_goal'] = goal
                c.run('sed_coord_sync')
                self.assertEqual(c.variables['sed_coord_executor'], executor)
                self.assertEqual(self.external(), {option: 1})

    def test_specific_goal_without_supply_waits_and_restores_original_options(self):
        for goal in (6, 7, 9):
            with self.subTest(goal=goal):
                self.setUp()
                c = self.c
                c.run('sed_set_mode_automatic')
                c.variables.pop('sed_coord_supply_known')
                c.variables['sed_plan_goal'] = goal
                c.run('sed_coord_sync')
                self.assertEqual(c.variables['sed_coord_executor'], 9)
                self.assertEqual(self.external(), {})
                c.run('sed_set_mode_assisted')
                self.assertEqual(self.external(), self.original)

    def test_tax_shortfall_without_supply_records_unavailable_execution(self):
        c = self.c
        c.states = [state(tax_capacity_usage=200, tax_capacity=100)]
        c.run('sed_set_mode_automatic')
        c.variables.pop('sed_coord_supply_known')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 7)
        self.assertEqual(c.variables['sed_coord_executor'], 9)
        self.assertEqual(c.variables['sed_auto_review_status'], 19)
        self.assertEqual(self.external(), {})
        c.variables['sed_coord_supply_known'] = True
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 7)
        self.assertEqual(c.variables['sed_auto_review_status'], 18)
        self.assertEqual(self.external(), {'zw_var_scsab_gov_admin_for_tax': 1})

    def test_fiscally_blocked_coordination_does_not_report_delegation(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.readings['net_total_income'] = -100
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 17)
        self.assertEqual(self.external(), {})

    def test_waiting_queue_suspends_delegation_and_resumes_after_cancellation(self):
        c = self.c
        rail = c.states[0]['buildings'][0]
        rail['level_after_queued_constructions'] = rail['level'] + 1
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_waiting'], 1)
        self.assertEqual(c.variables['sed_coord_executor'], 10)
        self.assertEqual(c.variables['sed_auto_review_status'], 20)
        self.assertEqual(self.external(), {})
        rail['level_after_queued_constructions'] = rail['level']
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_waiting'], 0)
        self.assertEqual(c.variables['sed_coord_executor'], 2)
        self.assertEqual(c.variables['sed_auto_review_status'], 18)
        self.assertEqual(self.external(), {'zw_var_scsab_construct_railway': 1})

    def test_reserve_funded_queue_pauses_then_resumes_without_cancelling_projects(self):
        c = self.c
        c.states.clear()
        c.readings.update(net_total_income=-10, net_fixed_income=100,
                          fixed_expenses=50, gold_reserves=860, principal=0,
                          construction_queue_num_queued_government_levels=1)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_fiscal_status'], 5)
        self.assertEqual(c.variables['sed_coord_executor'], 12)
        self.assertEqual(c.variables['sed_auto_review_status'], 21)
        self.assertEqual(self.external(), {})
        self.assertEqual(c.readings['construction_queue_num_queued_government_levels'], 1)
        c.readings['construction_queue_num_queued_government_levels'] = 0
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        self.assertEqual(self.external(), {'advisor_auto_construction_enabled': 1})
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.external(), self.original)

    def test_healthy_growth_with_queue_retains_previous_advisor_route(self):
        c = self.c
        c.states.clear()
        c.readings['construction_queue_num_queued_government_levels'] = 1
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_executor'], 1)

    def test_reserve_funded_private_queue_does_not_impose_public_queue_pause(self):
        c = self.c
        c.states.clear()
        c.readings.update(net_total_income=-10, fixed_expenses=50,
                          gold_reserves=860, principal=0,
                          construction_queue_num_queued_private_levels=3)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_executor'], 1)

    def test_diagnostic_refresh_synchronizes_executor_without_building_or_rewriting_review(self):
        c = self.c
        c.states.clear()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        review = {key: value for key, value in c.variables.items() if key.startswith('sed_auto_review_')}
        c.readings.update(net_total_income=-10, fixed_expenses=50, gold_reserves=860,
                          principal=0, construction_queue_num_queued_government_levels=1)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_coord_executor'], 12)
        self.assertEqual(self.external(), {})
        self.assertEqual(c.constructions, [])
        self.assertEqual({key: value for key, value in c.variables.items() if key in review}, review)
        c.readings['gold_reserves'] = 859
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_coord_executor'], 0)
        c.readings.update(net_total_income=100, gold_reserves=1000)
        c.run('sed_refresh_diagnostics')
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        self.assertEqual(c.constructions, [])

    def direct_supply_fixture(self):
        c = self.c
        item = next(item for item in SUPPLY_TARGETS if item['good'] == 'wood')
        producer = building(item['building'])
        producer['production_methods'] = [item['methods'][0]]
        target = state(buildings=[producer])
        c.states = [target]
        c.market_goods['wood'] = dict(market_goods_buy_orders=100, market_goods_sell_orders=20,
                                     market_goods_has_goods_shortage=True)
        c.run('sed_set_mode_automatic')
        return target, producer

    def test_coordinated_direct_supply_queues_the_ranked_target_and_restores_options(self):
        c = self.c
        target, _ = self.direct_supply_fixture()
        self.assertEqual(c.variables['sed_coord_executor'], 11)
        self.assertEqual(self.external(), {})
        self.assertEqual(c.constructions, [])  # Selecting a mode only selects the executor.
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [{'building': 'building_logging_camp', 'state': target}])
        self.assertEqual(c.variables['sed_auto_review_status'], 1)
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.external(), self.original)

    def test_coordinated_direct_supply_keeps_month_limit_after_modes_are_toggled(self):
        c = self.c
        _, producer = self.direct_supply_fixture()
        c.run('sed_auto_apply_monthly')
        c.states.append(state(buildings=[producer.copy()]))
        c.readings['construction_queue_num_queued_government_levels'] = 0
        c.run('sed_set_mode_assisted')
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        self.assertEqual(c.variables['sed_auto_review_status'], 16)

    def test_coordinated_direct_supply_waits_for_either_queue_to_clear(self):
        for queue in ('construction_queue_num_queued_government_levels',
                      'construction_queue_num_queued_private_levels'):
            with self.subTest(queue=queue):
                self.setUp()
                c = self.c
                self.direct_supply_fixture()
                c.readings[queue] = 1
                c.run('sed_auto_apply_monthly')
                self.assertEqual(c.constructions, [])
                self.assertEqual(self.external(), {})
                self.assertEqual(c.variables['sed_auto_review_status'], 11)
                c.readings[queue] = 0
                c.run('sed_auto_apply_monthly')
                self.assertEqual(len(c.constructions), 1)

    def test_stale_coordinated_target_and_competing_switch_are_revalidated(self):
        c = self.c
        target, producer = self.direct_supply_fixture()
        producer['building_has_goods_shortage'] = True
        c.run('sed_auto_run_direct')
        self.assertEqual(c.constructions, [])
        producer['building_has_goods_shortage'] = False
        c.variables['advisor_auto_construction_enabled'] = True
        c.run('sed_auto_run_direct')
        self.assertEqual(c.constructions, [])
        c.variables.pop('advisor_auto_construction_enabled')
        c.run('sed_auto_run_direct')
        self.assertEqual(c.constructions, [{'building': 'building_logging_camp', 'state': target}])

    def test_coordinated_approval_cannot_build_a_different_type_in_the_ranked_state(self):
        c = self.c
        target, _ = self.direct_supply_fixture()
        item = next(item for item in SUPPLY_TARGETS if item['good'] == 'iron')
        iron = building(item['building'])
        iron['production_methods'] = [item['methods'][0]]
        target['buildings'].append(iron)
        c.market_goods['iron'] = dict(market_goods_buy_orders=100, market_goods_sell_orders=90,
                                     market_goods_has_goods_shortage=True)
        c.run('sed_refresh_national_plan')
        c.run('sed_coord_sync')
        self.assertEqual(target['variables']['sed_plan_wood_rank'], 1)
        c.run('sed_run_iron_approval', target)
        self.assertEqual(c.constructions, [])
        c.run('sed_run_wood_approval', target)
        self.assertEqual(len(c.constructions), 1)

    def test_coordinated_direct_execution_rejects_fiscal_failure_and_mode_conflicts(self):
        for readings, variables in (({'net_total_income': -100, 'gold_reserves': 0}, {}),
                                    ({}, {'sed_mode_manual': True}),
                                    ({}, {'sed_mode_assisted': True}),
                                    ({'is_player': False}, {})):
            with self.subTest(readings=readings, variables=variables):
                self.setUp()
                c = self.c
                self.direct_supply_fixture()
                c.readings.update(readings)
                c.variables.update(variables)
                c.run('sed_auto_run_direct')
                self.assertEqual(c.constructions, [])

    def test_direct_failure_consumes_attempt_and_never_claims_delegation(self):
        c = self.c
        self.direct_supply_fixture()
        c.construction_accepted = False
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 15)
        self.assertEqual(len(c.constructions), 1)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_auto_review_status'], 16)
        self.assertEqual(len(c.constructions), 1)

    def test_aroai_blocks_direct_supply_even_when_priority_is_eligible(self):
        c = self.c
        self.direct_supply_fixture()
        c.variables['aroai_autobuild'] = True
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 5)
        self.assertEqual(c.variables['sed_auto_review_status'], 13)
        self.assertEqual(c.constructions, [])
        self.assertEqual(self.external(), {})

    def supply_policy(self):
        return {option: self.c.variables[option] for _, option in SUPPLY_POLICY_OPTIONS
                if option in self.c.variables}

    def test_supply_policy_is_bounded_and_restores_all_original_values(self):
        c = self.c
        originals = {option: index for index, (_, option) in enumerate(SUPPLY_POLICY_OPTIONS)}
        c.variables.update(originals)
        c.run('sed_set_mode_automatic')
        expected = {'zw_var_develop_incorporated_states': True,
                    'zw_var_ip_incorporated': True}
        self.assertEqual(self.supply_policy(), expected)
        c.run('sed_monthly_update')
        self.assertEqual(self.supply_policy(), expected)
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.supply_policy(), originals)
        self.assertFalse(any(k.startswith('sed_coord_saved_supply_') for k in c.variables))

    def test_supply_policy_restores_absent_options_on_disable(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        self.assertEqual(len(self.supply_policy()), 2)
        c.run('sed_disable_country')
        self.assertEqual(self.supply_policy(), {})
        self.assertNotIn('sed_coord_supply_policy_saved', c.variables)

    def test_legacy_coordination_captures_new_policy_once_before_mutation(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.variables.pop('sed_coord_supply_policy_saved')
        for name, option in SUPPLY_POLICY_OPTIONS:
            c.variables.pop('sed_coord_saved_supply_' + name, None)
            c.variables.pop(option, None)
        originals = {'zw_var_scsab_gov_admin_for_institution': 35,
                     'zw_var_ip_incorporated': 0}
        c.variables.update(originals)
        c.run('sed_coord_sync')
        c.run('sed_coord_sync')
        c.run('sed_set_mode_manual')
        self.assertEqual(self.supply_policy(), originals)

    def test_legacy_release_without_new_snapshot_preserves_supply_policy(self):
        c = self.c
        c.run('sed_set_mode_automatic')
        c.variables.pop('sed_coord_supply_policy_saved')
        original = {'zw_var_scsab_gov_admin_for_institution': 35}
        for _, option in SUPPLY_POLICY_OPTIONS:
            c.variables.pop(option, None)
        c.variables.update(original)
        c.run('sed_set_mode_manual')
        self.assertEqual(self.supply_policy(), original)

    def test_advisor_only_does_not_modify_supply_policy(self):
        c = self.c
        for _, option, _ in OPTIONS:
            if option != 'advisor_auto_construction_enabled':
                c.variables.pop(option, None)
        c.states.clear()
        c.variables['zw_var_ip_incorporated'] = 0
        c.run('sed_set_mode_automatic')
        self.assertNotIn('sed_coord_supply_policy_saved', c.variables)
        self.assertEqual(self.supply_policy(), {'zw_var_ip_incorporated': 0})
        c.run('sed_set_mode_assisted')
        self.assertEqual(self.supply_policy(), {'zw_var_ip_incorporated': 0})

    def test_validator_rejects_broadened_coordinated_direct_authority(self):
        for filename, old, new in (
            ('common/scripted_triggers/sed_triggers.txt',
             'var:sed_coord_executor = 11', 'var:sed_coord_executor = 1'),
            ('common/scripted_triggers/sed_triggers.txt',
             ' sed_direct_budget_safe = yes\n}', ' # material guard removed\n}'),
            ('common/scripted_effects/sed_effects.txt',
             'sed_auto_run_direct = {\n sed_refresh_direct_budget = yes', 'sed_auto_run_direct = {'),
            ('common/scripted_triggers/sed_triggers.txt',
             'var:sed_plan_wood_rank = 1 }', 'var:sed_plan_wood_rank >= 1 }'),
            ('common/scripted_effects/sed_effects.txt',
             'limit = { sed_auto_executor_safe = yes }', 'limit = { always = yes }'),
        ):
            with self.subTest(filename=filename, old=old), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                for name, data in outputs().items():
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                target = root / filename
                text = target.read_text(encoding='utf-8-sig')
                self.assertIn(old, text)
                target.write_text(text.replace(old, new, 1), encoding='utf-8-sig')
                errors = validate(root)
                self.assertTrue(any('authority' in error or 'safety guard' in error
                                    or 'first-ranked target' in error or 'material budget' in error for error in errors), errors)

    def test_validator_rejects_foreign_write_outside_adapter_and_unlisted_option(self):
        for replacement in (
            ('sed_coord_sync = {', 'sed_bad_adapter = {'),
            ('remove_variable = zw_var_expand_building', 'remove_variable = unrelated_mod_variable'),
        ):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                for name, data in outputs().items():
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                effect = root / 'common/scripted_effects/sed_effects.txt'
                text = effect.read_text(encoding='utf-8-sig').replace(*replacement, 1)
                effect.write_text(text, encoding='utf-8-sig')
                errors = validate(root)
                self.assertTrue(any('Foreign variable' in e for e in errors), errors)


if __name__ == '__main__':
    unittest.main()
