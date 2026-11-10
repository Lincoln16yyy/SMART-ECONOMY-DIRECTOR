"""Generate a bounded national plan from observable readings, not a return model."""

RANKS = (1, 2, 3)
COUNTRY_VARIABLES = ['sed_plan_count', 'sed_plan_goal', 'sed_fiscal_status',
                     'sed_plan_year', 'sed_plan_month', 'sed_plan_missing_count']
STATE_VARIABLES = ['sed_plan_score', 'sed_plan_type']


def country_variables(actions):
    supply = [name for name in actions if name not in ('railway', 'construction')]
    pressure = [f'sed_plan_pressure_{name}' for name in supply]
    missing = [f'sed_plan_missing_{name}' for name in supply]
    months = [f'sed_{name}_short_months' for name in supply]
    meta = [f'sed_{name}_meta_year' for name in supply]
    samples = [f'sed_{name}_short_sample_month' for name in supply]
    return COUNTRY_VARIABLES + pressure + missing + months + meta + samples + ['sed_short_sample_gap']


def state_variables(actions):
    return STATE_VARIABLES + [f'sed_plan_{name}_{field}' for name in actions
                             for field in ('rank', 'score')]


def lists(actions):
    return [f'sed_plan_{rank}_{name}' for rank in RANKS for name in actions]


TAX_LEVELS = ('very_low', 'low', 'medium', 'high', 'very_high')


def policy_step(effect, level, month_marker):
    return (f'set_variable = {{ name = {month_marker} value = sed_live_month_key }} '
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
            raise_steps.append(f'   {branch} = {{ limit = {{ tax_level = {level} }} {policy_step('set_tax_level', TAX_LEVELS[index], 'sed_tax_last_change_month')} }}')
        if index > 2:
            branch = 'if' if index == 3 else 'else_if'
            lower_steps.append(f'   {branch} = {{ limit = {{ tax_level = {level} }} {policy_step('set_tax_level', TAX_LEVELS[index - 2], 'sed_tax_last_change_month')} }}')
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
    gold_reserves >= { value = fixed_expenses min = 0 multiply = 12 }
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
            cut_steps.append(f'   {branch} = {{ limit = {{ government_wage_level = {level} }} {policy_step('set_government_wage_level', previous, 'sed_wage_last_change_month')} }}')
        if index < 3:
            branch = 'if' if index == 1 else 'else_if'
            raise_steps.append(f'   {branch} = {{ limit = {{ government_wage_level = {level} }} {policy_step('set_government_wage_level', TAX_LEVELS[index], 'sed_wage_last_change_month')} }}')
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
    gold_reserves >= { value = fixed_expenses min = 0 multiply = 12 }
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


def triggers():
    return '''sed_tax_month_limit_reached = {
 has_variable = sed_tax_last_change_month
 var:sed_tax_last_change_month = sed_live_month_key
}

sed_wage_month_limit_reached = {
 has_variable = sed_wage_last_change_month
 var:sed_wage_last_change_month = sed_live_month_key
}

# Initial proportional policy; not an incremental cost estimate.
sed_auto_fiscal_safe = {
 net_total_income >= 0
 net_fixed_income >= 0
 gold_reserves >= { value = fixed_expenses min = 0 multiply = 4 }
 OR = {
  principal <= 0
  AND = { credit > 0 principal <= { value = credit multiply = 0.75 } }
 }
}

# Keep a reserve floor plus six months of the currently observed deficit.
sed_coord_reserve_drawdown_safe = {
 net_fixed_income >= 0
 net_total_income < 0
 principal <= 0
 gold_reserves >= {
  value = fixed_expenses min = 0 multiply = 12
  add = { value = net_total_income multiply = -26 }
 }
}

sed_coord_fiscal_safe = {
 OR = { sed_auto_fiscal_safe = yes AND = { has_variable = sed_coord_advisor_known sed_coord_reserve_drawdown_safe = yes } }
}
'''


def effects(actions, buildings):
    supply = [name for name in actions if name not in ('railway', 'construction')]
    result = ['''sed_refresh_national_plan = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
  set_variable = { name = sed_plan_count value = 0 }
  set_variable = { name = sed_plan_missing_count value = 0 }
  set_variable = { name = sed_plan_goal value = 0 }
  set_variable = { name = sed_plan_year value = year }
  set_variable = { name = sed_plan_month value = { value = month add = 1 } }
  set_variable = { name = sed_fiscal_status value = 1 }
  if = { limit = { in_default = yes } set_variable = { name = sed_fiscal_status value = 4 } }
  else_if = {
   limit = { OR = {
    AND = { net_total_income < 0 gold_reserves < { value = net_total_income multiply = -4 } }
    AND = { principal > 0 OR = { credit <= 0 principal > { value = credit multiply = 0.9 } } }
   } }
   set_variable = { name = sed_fiscal_status value = 3 }
  }
  else_if = { limit = { sed_coord_reserve_drawdown_safe = yes } set_variable = { name = sed_fiscal_status value = 5 } }
  else_if = { limit = { NOT = { sed_auto_fiscal_safe = yes } } set_variable = { name = sed_fiscal_status value = 2 } }
''']
    for name in lists(actions):
        result.append(f'  clear_variable_list = {name}')
    for name in supply:
        producers = ' '.join(f'has_building = {building}' for building in buildings[name])
        result.append(f'''  set_variable = {{ name = sed_plan_missing_{name} value = 0 }}
  if = {{ limit = {{
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
  if = {{ limit = {{ market = {{ mg:{name} ?= {{ market_goods_has_goods_shortage = yes }} }} }}
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
    set_variable = {{ name = sed_{name}_meta_year value = year }}
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
    if = {{ limit = {{ owner = {{ has_variable = sed_{name}_meta_year var:sed_{name}_meta_year = year }} }} add = 25 }}'''
        result.append(f'''   if = {{ limit = {{ {eligibility} }}
    set_variable = {{ name = sed_plan_{name}_score value = {{ {score} }} }}
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
            result.append(f'''   if = {{ limit = {{ var:sed_plan_type = {index} }}
    set_variable = {{ name = sed_plan_{name}_rank value = {rank} }}
    owner = {{
     add_to_variable_list = {{ name = sed_plan_{rank}_{name} target = prev }}
     change_variable = {{ name = sed_plan_count add = 1 }}
     {goal_update}
    }}
   }}''')
        result.append('  }')
    result.append('''  if = { limit = { var:sed_plan_count = 0 var:sed_plan_missing_count > 0 } set_variable = { name = sed_plan_goal value = 5 } }
  if = { limit = { var:sed_plan_goal = 0 sed_coord_fiscal_safe = yes } set_variable = { name = sed_plan_goal value = 8 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } bureaucracy < 0 } set_variable = { name = sed_plan_goal value = 6 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } any_scope_state = { is_incorporated = yes tax_capacity_usage > tax_capacity } } set_variable = { name = sed_plan_goal value = 7 } }
  if = { limit = { OR = { var:sed_plan_goal = 0 var:sed_plan_goal = 8 } any_scope_state = { sg:electricity ?= { state_goods_pricier >= 0.2 } } } set_variable = { name = sed_plan_goal value = 9 } }
  if = { limit = { OR = { var:sed_fiscal_status = 3 var:sed_fiscal_status = 4 } } set_variable = { name = sed_plan_goal value = 4 } }
 }
}
''')
    return '\n'.join(line.rstrip() for block in result for line in block.splitlines()) + '\n'
