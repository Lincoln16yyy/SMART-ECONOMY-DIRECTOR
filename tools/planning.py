"""Generate a bounded national plan from observable readings, not a return model."""

from textwrap import indent

RANKS = (1, 2, 3)
MILITARY_GOODS = (
    ('small_arms', 'armas leves', 'small arms'),
    ('artillery', 'artilharia', 'artillery'),
    ('ammunition', 'munição', 'ammunition'),
    ('manowars', 'navios de guerra à vela', 'sailing warships'),
    ('ironclads', 'navios de guerra blindados', 'ironclads'),
)
MILITARY_INDUSTRY_GOODS = ('small_arms', 'artillery', 'ammunition')
COUNTRY_VARIABLES = ['sed_plan_count', 'sed_plan_goal', 'sed_fiscal_status',
                     'sed_plan_year', 'sed_plan_month', 'sed_plan_missing_count',
                     'sed_plan_waiting', 'sed_reserve_floor', 'sed_reserve_required',
                     'sed_reserve_spare', 'sed_reserve_runway', 'sed_military_posture', 'sed_military_at_war',
                     'sed_military_shortage_count', 'sed_investment_best_output',
                     'sed_investment_nonnegative_only'] + [f'sed_military_short_{good}' for good, _, _ in MILITARY_GOODS]
STATE_VARIABLES = ['sed_plan_score', 'sed_plan_type']


def country_variables(actions):
    supply = [name for name in actions if name not in ('railway', 'construction')]
    pressure = [f'sed_plan_pressure_{name}' for name in supply]
    missing = [f'sed_plan_missing_{name}' for name in supply]
    months = [f'sed_{name}_short_months' for name in supply]
    meta = [f'sed_{name}_meta_year' for name in supply]
    streak = [f'sed_{name}_{field}' for name in supply for field in ('goal_streak', 'meta_since')]
    streak.append('sed_prev_year')
    samples = [f'sed_{name}_short_sample_month' for name in supply]
    return (COUNTRY_VARIABLES + pressure + missing + months + meta + streak + samples
            + ['sed_short_sample_gap'])


def state_variables(actions):
    return STATE_VARIABLES + [f'sed_plan_{name}_{field}' for name in actions
                             for field in ('rank', 'score')] + [
        f'sed_plan_{name}_{field}' for name in actions if name not in ('railway', 'construction')
        for field in ('margin', 'output')]


def lists(actions):
    return [f'sed_plan_{rank}_{name}' for rank in RANKS for name in actions]


TAX_LEVELS = ('very_low', 'low', 'medium', 'high', 'very_high')


def policy_step(effect, level, month_marker, previous_index):
    prefix = month_marker.removesuffix('_change_month')
    return (f'set_variable = {{ name = {month_marker} value = sed_live_month_key }} '
            f'set_variable = {{ name = {prefix}_from value = {previous_index} }} '
            f'set_variable = {{ name = {prefix}_to value = {TAX_LEVELS.index(level) + 1} }} '
            f'set_variable = {{ name = {prefix}_year value = year }} '
            f'set_variable = {{ name = {prefix}_month value = {{ value = month add = 1 }} }} '
            f'{effect} = {level}')


def tax_policy_effects():
    """One reviewed tax step per monthly review; the original level is restored."""
    snapshot = []
    for index, level in enumerate(TAX_LEVELS, 1):
        branch = 'if' if index == 1 else 'else_if'
        snapshot.append(f'''  {branch} = {{ limit = {{ tax_level = {level} }}
   set_variable = {{ name = sed_tax_level_saved value = {index} }}
  }}''')
    raise_steps = []
    lower_steps = []
    restore_steps = []
    for index, level in enumerate(TAX_LEVELS, 1):
        if index < len(TAX_LEVELS):
            branch = 'if' if index == 1 else 'else_if'
            raise_steps.append(f'   {branch} = {{ limit = {{ tax_level = {level} }} {policy_step('set_tax_level', TAX_LEVELS[index], 'sed_tax_last_change_month', index)} }}')
        if index > 2:
            branch = 'if' if index == 3 else 'else_if'
            lower_steps.append(f'   {branch} = {{ limit = {{ tax_level = {level} }} {policy_step('set_tax_level', TAX_LEVELS[index - 2], 'sed_tax_last_change_month', index)} }}')
        branch = 'if' if index == 1 else 'else_if'
        restore_steps.append(f'  {branch} = {{ limit = {{ var:sed_tax_level_saved = {index} }} set_tax_level = {level} }}')
    return '''# Country scope. TAX_LEVELS is ordered: very_low, low, medium, high, very_high.
# Snapshot before the first change so leaving Automatic or disabling can restore.
sed_tax_policy_save = {
 if = {
  limit = { is_player = yes NOT = { has_variable = sed_tax_level_saved } }
''' + '\n'.join(snapshot) + '''
 }
}

sed_apply_fiscal_policy = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
   has_variable = sed_fiscal_status
   NOT = { has_variable = sed_mode_manual }
   NOT = { has_variable = sed_mode_assisted }
   NOT = { sed_tax_month_limit_reached = yes }
  }
  if = {
   limit = { OR = { var:sed_fiscal_status = 2 var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 } }
   sed_tax_policy_save = yes
''' + '\n'.join(raise_steps) + '''
  }
  else_if = {
   limit = { OR = { var:sed_fiscal_status = 1 var:sed_fiscal_status = 5 }
    gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 12 }
    principal <= 0
    net_total_income > 0
   }
   sed_tax_policy_save = yes
''' + '\n'.join(lower_steps) + '''
  }
 }
}

sed_restore_fiscal_policy = {
 if = {
  limit = { is_player = yes has_variable = sed_tax_level_saved }
''' + '\n'.join(restore_steps) + '''
  remove_variable = sed_tax_level_saved
 }
}
'''


def wage_policy_effects():
    """Cut government wages in crisis, restore them with fiscal health."""
    snapshot = []
    cut_steps = []
    raise_steps = []
    restore_steps = []
    for index, level in enumerate(TAX_LEVELS, 1):
        branch = 'if' if index == 1 else 'else_if'
        snapshot.append(f'''  {branch} = {{ limit = {{ government_wage_level = {level} }}
   set_variable = {{ name = sed_gov_wage_saved value = {index} }}
  }}''')
        if index > 2:
            previous = TAX_LEVELS[index - 2]
            branch = 'if' if index == 3 else 'else_if'
            cut_steps.append(f'   {branch} = {{ limit = {{ government_wage_level = {level} }} {policy_step('set_government_wage_level', previous, 'sed_wage_last_change_month', index)} }}')
        if index < 3:
            branch = 'if' if index == 1 else 'else_if'
            raise_steps.append(f'   {branch} = {{ limit = {{ government_wage_level = {level} }} {policy_step('set_government_wage_level', TAX_LEVELS[index], 'sed_wage_last_change_month', index)} }}')
        branch = 'if' if index == 1 else 'else_if'
        restore_steps.append(f'  {branch} = {{ limit = {{ var:sed_gov_wage_saved = {index} }} set_government_wage_level = {level} }}')
    return '''# Country scope; civilian government wages only, one step per monthly review.
sed_wage_policy_save = {
 if = {
  limit = { is_player = yes NOT = { has_variable = sed_gov_wage_saved } }
''' + '\n'.join(snapshot) + '''
 }
}

sed_apply_wage_policy = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
   has_variable = sed_fiscal_status
   NOT = { has_variable = sed_mode_manual }
   NOT = { has_variable = sed_mode_assisted }
   NOT = { sed_wage_month_limit_reached = yes }
  }
  if = {
   limit = { OR = { var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 } }
   sed_wage_policy_save = yes
''' + '\n'.join(cut_steps) + '''
  }
  else_if = {
   limit = { OR = { var:sed_fiscal_status = 1 var:sed_fiscal_status = 5 }
    gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 12 }
    principal <= 0
    net_total_income > 0
   }
   sed_wage_policy_save = yes
''' + '\n'.join(raise_steps) + '''
  }
 }
}

sed_restore_wage_policy = {
 if = {
  limit = { is_player = yes has_variable = sed_gov_wage_saved }
''' + '\n'.join(restore_steps) + '''
  remove_variable = sed_gov_wage_saved
 }
}
'''


def military_wage_policy_effects():
    """Reduce structural peacetime deficits and recover only the captured wage."""
    snapshots = []
    cuts = []
    recoveries = []
    restores = []
    for index, level in enumerate(TAX_LEVELS, 1):
        branch = 'if' if index == 1 else 'else_if'
        snapshots.append(f'  {branch} = {{ limit = {{ military_wage_level = {level} }} set_variable = {{ name = sed_military_wage_saved value = {index} }} }}')
        restores.append(f'  {branch} = {{ limit = {{ var:sed_military_wage_saved = {index} }} set_military_wage_level = {level} }}')
        if index > 2:
            branch = 'if' if index == 3 else 'else_if'
            step = policy_step('set_military_wage_level', TAX_LEVELS[index - 2],
                               'sed_military_wage_last_change_month', index)
            cuts.append(f'   {branch} = {{ limit = {{ military_wage_level = {level} }} sed_save_military_wage = yes {step} }}')
        if index < len(TAX_LEVELS):
            branch = 'if' if index == 1 else 'else_if'
            readiness = 'sed_military_readiness_required = yes' if index < 3 else ''
            step = policy_step('set_military_wage_level', TAX_LEVELS[index],
                               'sed_military_wage_last_change_month', index)
            recoveries.append(f'''   {branch} = {{ limit = {{
    military_wage_level = {level}
    var:sed_military_wage_saved > {index}
    OR = {{ sed_military_wage_recovery_affordable = yes {readiness} }}
   }} {step} }}''')
    return '''sed_save_military_wage = {
 if = { limit = { is_player = yes NOT = { has_variable = sed_military_wage_saved } }
''' + '\n'.join(snapshots) + '''
 }
}

sed_apply_military_wage_policy = {
 if = { limit = {
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  has_variable = sed_fiscal_status
  NOT = { has_variable = sed_mode_manual }
  NOT = { has_variable = sed_mode_assisted }
  NOT = { sed_military_wage_month_limit_reached = yes }
 }
  if = { limit = {
   OR = { var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 }
   net_fixed_income < 0 military_expenses > 0
   NOT = { sed_military_readiness_required = yes }
  }
''' + '\n'.join(cuts) + '''
  }
  else_if = { limit = { has_variable = sed_military_wage_saved }
''' + '\n'.join(recoveries) + '''
  }
 }
}

sed_restore_military_wage_policy = {
 if = { limit = { is_player = yes has_variable = sed_military_wage_saved }
''' + '\n'.join(restores) + '''
  remove_variable = sed_military_wage_saved
 }
}
'''


def triggers():
    return '''sed_military_wage_month_limit_reached = {
 has_variable = sed_military_wage_last_change_month
 var:sed_military_wage_last_change_month = sed_live_month_key
}

sed_military_readiness_required = {
 OR = { is_at_war = yes is_diplomatic_play_committed_participant = yes
  is_diplomatic_play_initiator = yes is_diplomatic_play_target = yes
  is_diplomatic_play_undecided_participant = yes any_military_formation = { is_mobilized = yes } }
}

sed_military_wage_recovery_affordable = {
 net_total_income > 0
 net_fixed_income >= 0
 net_total_income >= { value = military_expenses min = 0 multiply = 0.5 }
 principal <= 0
 gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 12 }
}

sed_tax_month_limit_reached = {
 has_variable = sed_tax_last_change_month
 var:sed_tax_last_change_month = sed_live_month_key
}

sed_wage_month_limit_reached = {
 has_variable = sed_wage_last_change_month
 var:sed_wage_last_change_month = sed_live_month_key
}

# Initial proportional policy; not an incremental cost estimate.
# Uma leitura saudavel mantem o piso de quatro semanas de despesas fixas.
# Um deficit operacional sem divida e financiado por ouro quando as reservas
# cobrem seis semanas de despesas fixas. O custo da obra em si continua na
# guarda de orcamento, que ja projeta o deficit da fila e do projeto.
sed_auto_fiscal_safe = {
 OR = {
  AND = {
   net_total_income >= 0
   net_fixed_income >= 0
   gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 4 }
   OR = {
    principal <= 0
    AND = { credit > 0 principal <= { value = credit multiply = 0.75 } }
   }
  }
  AND = {
   net_total_income < 0
   net_fixed_income >= 0
   principal <= 0
   gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 6 }
  }
 }
}

sed_direct_fiscal_safe = {
 sed_auto_fiscal_safe = yes
}

sed_coord_fiscal_safe = {
 sed_auto_fiscal_safe = yes
}
'''


def effects(actions, dependencies, buildings):
    supply = [name for name in actions if name not in ('railway', 'construction')]
    result = ['''sed_refresh_national_plan = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
  sed_refresh_investment_prices = yes
  sed_refresh_input_readings = yes
  set_variable = { name = sed_plan_count value = 0 }
  set_variable = { name = sed_plan_missing_count value = 0 }
  set_variable = { name = sed_plan_goal value = 0 }
  set_variable = { name = sed_plan_waiting value = 0 }
  set_variable = { name = sed_plan_year value = year }
  set_variable = { name = sed_prev_year value = { value = year subtract = 1 } }
  set_variable = { name = sed_plan_month value = { value = month add = 1 } }
  set_variable = { name = sed_reserve_floor value = { value = sed_fixed_expenses_value min = 0 multiply = 4 } }
  set_variable = { name = sed_reserve_required value = { value = var:sed_reserve_floor } }
  if = { limit = { net_total_income < 0 }
   set_variable = { name = sed_reserve_required value = { value = sed_fixed_expenses_value min = 0 multiply = 6 } }
  }
  set_variable = { name = sed_reserve_spare value = { value = gold_reserves subtract = var:sed_reserve_required min = 0 } }
  set_variable = { name = sed_reserve_runway value = 0 }
  if = { limit = { net_total_income < 0 }
   set_variable = { name = sed_reserve_runway value = { value = var:sed_reserve_spare divide = { value = net_total_income multiply = -1 } } }
  }
  set_variable = { name = sed_fiscal_status value = 1 }
  if = { limit = { in_default = yes } set_variable = { name = sed_fiscal_status value = 4 } }
  else_if = {
   limit = { OR = {
    AND = { net_total_income < 0 gold_reserves < { value = net_total_income multiply = -4 } }
    AND = { principal > 0 OR = { credit <= 0 principal > { value = credit multiply = 0.9 } } }
   } }
   set_variable = { name = sed_fiscal_status value = 3 }
  }
  else_if = { limit = { sed_auto_fiscal_safe = yes net_total_income < 0 } set_variable = { name = sed_fiscal_status value = 5 } }
  else_if = { limit = { NOT = { sed_auto_fiscal_safe = yes } } set_variable = { name = sed_fiscal_status value = 2 } }
''']
    for name in lists(actions):
        result.append(f'  clear_variable_list = {name}')
    for name in supply:
        producers = ' '.join(f'has_building = {building}' for building in buildings[name])
        military_demand = (f'military_expenses > 0 market = {{ mg:{name} ?= {{ market_goods_buy_orders > 0 }} }}'
                           if name in MILITARY_INDUSTRY_GOODS else '')
        result.append(f'''  set_variable = {{ name = sed_plan_missing_{name} value = 0 }}
  if = {{ limit = {{
   {military_demand}
   market = {{ mg:{name} ?= {{ market_goods_has_goods_shortage = yes }} }}
   NOT = {{ any_scope_state = {{ OR = {{ {producers} }} }} }}
  }}
   set_variable = {{ name = sed_plan_missing_{name} value = 1 }}
   change_variable = {{ name = sed_plan_missing_count add = 1 }}
  }}''')
        # Optional numeric scopes are used by vanilla ip5_je_values.txt.
        result.append(f'''  set_variable = {{ name = sed_plan_pressure_{name} value = {{
   value = 0
   market ?= {{ mg:{name} ?= {{
    if = {{ limit = {{ market_goods_buy_orders > 0 }}
     add = {{ value = market_goods_buy_orders subtract = market_goods_sell_orders
      divide = market_goods_buy_orders min = 0 max = 1 multiply = 100 }}
    }}
   }} }}
  }} }}''')
        # Observe distinct calendar months. Repeated refreshes do not age a goal.
        # Old counters without a sample date cannot prove consecutive months.
        result.append(f'''  if = {{ limit = {{ NOT = {{ has_variable = sed_{name}_short_sample_month }} }}
   remove_variable = sed_{name}_short_months
   remove_variable = sed_{name}_meta_year
  }}
  if = {{ limit = {{ {military_demand} market = {{ mg:{name} ?= {{ market_goods_has_goods_shortage = yes }} }} }}
   if = {{ limit = {{ NOT = {{ has_variable = sed_{name}_short_sample_month var:sed_{name}_short_sample_month = sed_live_month_key }} }}
    set_variable = {{ name = sed_short_sample_gap value = 0 }}
    if = {{ limit = {{ has_variable = sed_{name}_short_sample_month }}
     set_variable = {{ name = sed_short_sample_gap value = {{ value = sed_live_month_key subtract = var:sed_{name}_short_sample_month }} }}
    }}
    if = {{ limit = {{ var:sed_short_sample_gap = 1 has_variable = sed_{name}_short_months }}
     change_variable = {{ name = sed_{name}_short_months add = 1 }}
    }}
    else = {{ set_variable = {{ name = sed_{name}_short_months value = 1 }} }}
    remove_variable = sed_short_sample_gap
   }}
   else_if = {{ limit = {{ NOT = {{ has_variable = sed_{name}_short_months }} }}
    set_variable = {{ name = sed_{name}_short_months value = 1 }}
   }}
   if = {{ limit = {{ var:sed_{name}_short_months >= 3 }}
    if = {{ limit = {{ NOT = {{ has_variable = sed_{name}_meta_year }} }}
     set_variable = {{ name = sed_{name}_meta_year value = year }}
     set_variable = {{ name = sed_{name}_goal_streak value = 1 }}
     set_variable = {{ name = sed_{name}_meta_since value = year }}
    }}
    else_if = {{ limit = {{ var:sed_{name}_meta_year < year }}
     # Consecutive annual goals form a multi-year goal; a skipped year restarts it.
     if = {{ limit = {{ var:sed_{name}_meta_year = var:sed_prev_year }}
      change_variable = {{ name = sed_{name}_goal_streak add = 1 }}
      set_variable = {{ name = sed_{name}_goal_streak value = {{ value = var:sed_{name}_goal_streak max = 5 }} }}
     }}
     else = {{
      set_variable = {{ name = sed_{name}_goal_streak value = 1 }}
      set_variable = {{ name = sed_{name}_meta_since value = year }}
     }}
     set_variable = {{ name = sed_{name}_meta_year value = year }}
    }}
   }}
  }}
  else = {{ remove_variable = sed_{name}_short_months }}
  set_variable = {{ name = sed_{name}_short_sample_month value = sed_live_month_key }}''')
    result.append('  every_scope_state = {')
    for name in actions:
        result.append(f'   set_variable = {{ name = sed_plan_{name}_rank value = 0 }}')
        result.append(f'   set_variable = {{ name = sed_plan_{name}_score value = 0 }}')
        eligibility = f'sed_{name}_candidate_eligible = yes'
        if name == 'construction':
            eligibility += ' owner = { num_queued_government_constructions >= 3 }'
        if name == 'railway':
            score = 'value = infrastructure_delta multiply = -1 max = 100 add = 100'
        elif name == 'construction':
            score = 'value = 40'
        else:
            bonus = 20 if name in ('grain', 'groceries', 'clothes') else 10
            score = f'''value = owner.var:sed_plan_pressure_{name} add = {80 + bonus}
    if = {{ limit = {{ owner = {{ has_variable = sed_{name}_meta_year var:sed_{name}_meta_year = year }} }} add = 25 }}
    if = {{ limit = {{ owner = {{ has_variable = sed_{name}_goal_streak var:sed_{name}_goal_streak >= 2 }} }} add = 15 }}'''
            if name in dependencies:
                score += f'\n    if = {{ limit = {{ owner = {{ has_variable = sed_input_priority_{name} }} }} add = 75 }}'
            if name in MILITARY_INDUSTRY_GOODS:
                score += '\n    if = { limit = { owner = { is_at_war = yes } } add = 20 }'
        result.append(f'''   if = {{ limit = {{ {eligibility} }}
    set_variable = {{ name = sed_plan_{name}_score value = {{ {score} }} }}
   }}''')
        if name not in ('railway', 'construction'):
            result.append(f'''   set_variable = {{ name = sed_plan_{name}_margin value = 0 }}
   set_variable = {{ name = sed_plan_{name}_output value = 0 }}
   if = {{ limit = {{ var:sed_plan_{name}_score > 0 }}
    set_variable = {{ name = sed_plan_{name}_margin value = sed_investment_{name}_return }}
    set_variable = {{ name = sed_plan_{name}_output value = sed_investment_{name}_output }}
   }}''')
    result.append('  }')
    # Recompute the best unselected pair in each state, select the best state,
    # then repeat. Allows three different building types in the same state.
    for rank in RANKS:
        result.append('''  every_scope_state = {
   set_variable = { name = sed_plan_score value = 0 }
   set_variable = { name = sed_plan_type value = 0 }''')
        for index, name in enumerate(actions, 1):
            result.append(f'''   if = {{ limit = {{ var:sed_plan_{name}_rank = 0 var:sed_plan_{name}_score > var:sed_plan_score }}
    set_variable = {{ name = sed_plan_score value = var:sed_plan_{name}_score }}
    set_variable = {{ name = sed_plan_type value = {index} }}
   }}''')
        result.append('''  }
  ordered_scope_state = {
   limit = { var:sed_plan_score > 0 }
   order_by = { value = var:sed_plan_score }
   max = 1
   check_range_bounds = no''')
        for index, name in enumerate(actions, 1):
            goal_update = ''
            if rank == 1:
                goal = {'railway': 1, 'construction': 3}.get(name, 2)
                goal_update = f'set_variable = {{ name = sed_plan_goal value = {goal} }}'
            assign_rank = f'''set_variable = {{ name = sed_plan_{name}_rank value = {rank} }}
owner = {{
 add_to_variable_list = {{ name = sed_plan_{rank}_{name} target = prev }}
 change_variable = {{ name = sed_plan_count add = 1 }}
 {goal_update}
}}'''
            if name not in ('railway', 'construction'):
                # Preserve the chosen national objective, then compare its unranked suppliers.
                assign_rank = f'''if = {{
 limit = {{ owner = {{ has_variable = sed_mode_automatic }} }}
 owner = {{
  remove_variable = sed_investment_nonnegative_only
  if = {{ limit = {{ any_scope_state = {{ var:sed_plan_{name}_score > 0 var:sed_plan_{name}_rank = 0 var:sed_plan_{name}_margin >= 0 }} }}
   set_variable = {{ name = sed_investment_nonnegative_only value = yes }}
  }}
  ordered_scope_state = {{
   limit = {{ var:sed_plan_{name}_score > 0 var:sed_plan_{name}_rank = 0
    OR = {{ owner = {{ NOT = {{ has_variable = sed_investment_nonnegative_only }} }} var:sed_plan_{name}_margin >= 0 }}
   }}
   order_by = {{ value = var:sed_plan_{name}_output }}
   max = 1 check_range_bounds = no
   owner = {{ set_variable = {{ name = sed_investment_best_output value = prev.var:sed_plan_{name}_output }} }}
  }}
  ordered_scope_state = {{
   limit = {{ var:sed_plan_{name}_score > 0 var:sed_plan_{name}_rank = 0
    var:sed_plan_{name}_output = owner.var:sed_investment_best_output
    OR = {{ owner = {{ NOT = {{ has_variable = sed_investment_nonnegative_only }} }} var:sed_plan_{name}_margin >= 0 }}
   }}
   order_by = {{ value = var:sed_plan_{name}_margin }}
   max = 1 check_range_bounds = no
{indent(assign_rank, '   ')}
  }}
  remove_variable = sed_investment_best_output
  remove_variable = sed_investment_nonnegative_only
 }}
}}
else = {{
{indent(assign_rank, ' ')}
}}'''
            result.append(f'''   if = {{ limit = {{ var:sed_plan_type = {index} }}
{indent(assign_rank, '    ')}
   }}''')
        result.append('  }')
    result.append('''  if = { limit = { var:sed_plan_goal = 0 any_scope_state = {
   is_incorporated = yes infrastructure_delta < 0 NOT = { has_variable = sed_railway_ignored } has_building = building_railway
   b:building_railway = { level_after_queued_constructions > level }
  } }
   set_variable = { name = sed_plan_goal value = 1 }
   set_variable = { name = sed_plan_waiting value = 1 }
  }''')
    for name in supply:
        military_demand = (f'military_expenses > 0 market = {{ mg:{name} ?= {{ market_goods_buy_orders > 0 }} }}'
                           if name in MILITARY_INDUSTRY_GOODS else '')
        demand = f'market = {{ mg:{name} ?= {{ market_goods_has_goods_shortage = yes }} }}'
        if name in dependencies:
            demand = f'OR = {{ {demand} has_variable = sed_input_priority_{name} }}'
        result.append(f'''  if = {{ limit = {{ var:sed_plan_goal = 0 {military_demand}
   {demand}
   any_scope_state = {{ is_incorporated = yes NOT = {{ has_variable = sed_{name}_ignored }} sed_{name}_queued_supply = yes }}
  }}
   set_variable = {{ name = sed_plan_goal value = 2 }}
   set_variable = {{ name = sed_plan_waiting value = 1 }}
  }}''')
    result.append('''  if = { limit = { var:sed_plan_goal = 0 var:sed_plan_missing_count > 0 } set_variable = { name = sed_plan_goal value = 5 } }
  if = { limit = { var:sed_plan_goal = 0 sed_coord_fiscal_safe = yes } set_variable = { name = sed_plan_goal value = 8 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } bureaucracy < 0 } set_variable = { name = sed_plan_goal value = 6 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } any_scope_state = { is_incorporated = yes tax_capacity_usage > tax_capacity } } set_variable = { name = sed_plan_goal value = 7 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } any_scope_state = { sg:electricity ?= { state_goods_pricier >= 0.2 } } } set_variable = { name = sed_plan_goal value = 9 } }
  if = { limit = {
   OR = {
    AND = { var:sed_plan_goal = 6 any_scope_state = { is_incorporated = yes has_building = building_government_administration b:building_government_administration = { level_after_queued_constructions > level } } }
    AND = { var:sed_plan_goal = 7 any_scope_state = { is_incorporated = yes tax_capacity_usage > tax_capacity has_building = building_government_administration b:building_government_administration = { level_after_queued_constructions > level } } }
    AND = { var:sed_plan_goal = 9 any_scope_state = { is_incorporated = yes sg:electricity ?= { state_goods_pricier >= 0.2 } has_building = building_power_plant b:building_power_plant = { level_after_queued_constructions > level } } }
   }
  } set_variable = { name = sed_plan_waiting value = 1 } }
  if = { limit = { OR = { var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 } }
   set_variable = { name = sed_plan_goal value = 4 }
   set_variable = { name = sed_plan_waiting value = 0 }
  }
  sed_refresh_labor_readings = yes
  sed_refresh_direct_budget = yes
  sed_refresh_military_plan = yes
 }
}
''')
    return '\n'.join(line.rstrip() for block in result for line in block.splitlines()) + '\n'


def military_effects():
    result = ["""# Country scope; read-only military-economic assessment.
sed_refresh_military_plan = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  set_variable = { name = sed_military_expenses value = military_expenses }
  set_variable = { name = sed_military_share value = military_expenses_share }
  set_variable = { name = sed_military_at_war value = 0 }
  if = { limit = { is_at_war = yes } set_variable = { name = sed_military_at_war value = 1 } }
  set_variable = { name = sed_military_shortage_count value = 0 }
  set_variable = { name = sed_military_posture value = 0 }
"""]
    for good, _, _ in MILITARY_GOODS:
        result.append(f"""  set_variable = {{ name = sed_military_short_{good} value = 0 }}
  if = {{ limit = {{ market = {{ mg:{good} ?= {{ market_goods_buy_orders > 0 market_goods_has_goods_shortage = yes }} }} }}
   set_variable = {{ name = sed_military_short_{good} value = 1 }}
   change_variable = {{ name = sed_military_shortage_count add = 1 }}
  }}""")
    result.append("""  if = { limit = { military_expenses > 0 }
   set_variable = { name = sed_military_posture value = 1 }
   if = { limit = { var:sed_military_shortage_count > 0 }
    set_variable = { name = sed_military_posture value = 2 }
   }
   if = { limit = { OR = { var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 net_fixed_income < 0 } }
    set_variable = { name = sed_military_posture value = 3 }
   }
   else_if = { limit = { var:sed_military_shortage_count = 0
    sed_auto_fiscal_safe = yes principal <= 0 net_total_income > 0
    gold_reserves >= { value = sed_fixed_expenses_value min = 0 multiply = 12 }
   } set_variable = { name = sed_military_posture value = 4 } }
  }
 }
}
""")
    return '\n'.join(result)
