"""Explicit reversible adapters for verified external construction switches.

These are version-specific option adapters, not public mod APIs. Do not call
external effects or alter unrelated production/political/financial options.
"""
OPTIONS = (
    ('advisor', 'advisor_auto_construction_enabled', 1),
    ('chains', 'zw_var_expand_building', 0),
    ('sectors', 'zw_var_more_construction_sectors', 5),
    ('railways', 'zw_var_scsab_construct_railway', 1),
    ('power', 'zw_var_scsab_construct_power_plant', 1),
    ('admin', 'zw_var_scsab_gov_admin', 10),
    ('tax', 'zw_var_scsab_gov_admin_for_tax', 1),
)
ADVISOR_POLICY_OPTIONS = (
    ('goal_sol', 'advisor_setting_sc_goal_sol'),
    ('goal_treasury', 'advisor_setting_sc_goal_treasury'),
    ('treasury_off', 'advisor_setting_treasury_off'),
    ('borrow', 'advisor_setting_borrow'),
)
# Retained settings identify a previously configured Supply Chain even when
# all construction switches are off. Avoid optional foreign journal IDs.
SUPPLY_HINTS = (
    'zw_var_scsab_gov_admin_for_institution', 'zw_var_added_constructions',
    'zw_var_labor_threshold', 'zw_var_more_construction_sectors_gold_reserves',
    'zw_var_develop_incorporated_states',
)
VARIABLES = ['sed_coord_active', 'sed_coord_supply_known', 'sed_coord_advisor_known',
             'sed_coord_executor', 'sed_coord_advisor_policy', 'sed_coord_policy_saved'] + [f'sed_coord_saved_{name}' for name, _, _ in OPTIONS] + [f'sed_coord_saved_{name}' for name, _ in ADVISOR_POLICY_OPTIONS]


def enable_option(name):
    _, option, default = next(x for x in OPTIONS if x[0] == name)
    return f'''if = {{ limit = {{ has_variable = sed_coord_saved_{name} }}
 set_variable = {{ name = {option} value = var:sed_coord_saved_{name} }}
}}
else = {{ set_variable = {{ name = {option} value = {default} }} }}'''


def effects():
    snapshot = '\n'.join(f'''  if = {{ limit = {{ has_variable = {option} }}
   set_variable = {{ name = sed_coord_saved_{name} value = var:{option} }}
  }}''' for name, option, _ in OPTIONS)
    remove = '\n'.join(f'  remove_variable = {option}' for _, option, _ in OPTIONS)
    restore = '\n'.join(f'''  if = {{ limit = {{ has_variable = sed_coord_saved_{name} }}
   set_variable = {{ name = {option} value = var:sed_coord_saved_{name} }}
  }}
  else = {{ remove_variable = {option} }}''' for name, option, _ in OPTIONS)
    policy_snapshot = '\n'.join(f'''  if = {{ limit = {{ has_variable = {option} }}
   set_variable = {{ name = sed_coord_saved_{name} value = var:{option} }}
  }}''' for name, option in ADVISOR_POLICY_OPTIONS)
    policy_restore = '\n'.join(f'''   if = {{ limit = {{ has_variable = sed_coord_saved_{name} }}
    set_variable = {{ name = {option} value = var:sed_coord_saved_{name} }}
   }}
   else = {{ remove_variable = {option} }}''' for name, option in ADVISOR_POLICY_OPTIONS)
    cleanup = '\n'.join('  remove_variable = ' + name for name in VARIABLES)
    supply_options = [option for name, option, _ in OPTIONS if name != 'advisor']
    supply = ' '.join('has_variable = ' + option for option in supply_options + list(SUPPLY_HINTS))
    # No foreign write is permitted outside these two checked effects.
    return f'''sed_coord_capture_advisor_policy = {{
 if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_coord_active
  has_variable = sed_coord_advisor_known NOT = {{ has_variable = sed_coord_policy_saved }} }}
{policy_snapshot}
  set_variable = {{ name = sed_coord_policy_saved value = yes }}
 }}
}}

sed_coord_enable = {{
 if = {{
  limit = {{ is_player = yes has_variable = sed_enabled NOT = {{ has_variable = sed_coord_active }} }}
{snapshot}
  if = {{ limit = {{ OR = {{ has_variable = advisor_enabled has_variable = advisor_auto_construction_enabled }} }} set_variable = {{ name = sed_coord_advisor_known value = yes }} }}
  if = {{ limit = {{ OR = {{ {supply} }} }} set_variable = {{ name = sed_coord_supply_known value = yes }} }}
  set_variable = {{ name = sed_coord_active value = yes }}
  sed_coord_capture_advisor_policy = yes
  remove_variable = sed_mode_manual
  remove_variable = sed_mode_assisted
  set_variable = {{ name = sed_mode_automatic value = yes }}
  set_variable = {{ name = sed_auto_action_status value = 0 }}
  sed_schedule_auto_event = yes
  sed_refresh_national_plan = yes
  sed_coord_sync = yes
 }}
}}

sed_coord_restore = {{
 if = {{ limit = {{ is_player = yes has_variable = sed_coord_active }}
{restore}
  if = {{ limit = {{ has_variable = sed_coord_policy_saved }}
{policy_restore}
  }}
{cleanup}
 }}
}}

sed_coord_sync = {{
 if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic NOT = {{ has_variable = sed_mode_manual }} NOT = {{ has_variable = sed_mode_assisted }} has_variable = sed_coord_active }}
{remove}
  set_variable = {{ name = sed_coord_executor value = 0 }}
  set_variable = {{ name = sed_coord_advisor_policy value = 0 }}
  if = {{ limit = {{ has_variable = aroai_autobuild }} set_variable = {{ name = sed_coord_executor value = 5 }} }}
  else_if = {{ limit = {{ sed_coord_fiscal_safe = yes NOT = {{ in_default = yes }} is_construction_paused = no }}
   if = {{ limit = {{ var:sed_plan_goal = 1 has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes }}
    {enable_option('railways')}
    set_variable = {{ name = sed_coord_executor value = 2 }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes var:sed_plan_goal = 6 }}
    {enable_option('admin')}
    set_variable = {{ name = sed_coord_executor value = 6 }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes var:sed_plan_goal = 7 }}
    {enable_option('tax')}
    set_variable = {{ name = sed_coord_executor value = 7 }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes var:sed_plan_goal = 9 }}
    {enable_option('power')}
    set_variable = {{ name = sed_coord_executor value = 8 }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_advisor_known OR = {{ var:sed_plan_goal = 1 var:sed_plan_goal = 2 var:sed_plan_goal = 3 var:sed_plan_goal = 5 var:sed_plan_goal = 6 var:sed_plan_goal = 7 var:sed_plan_goal = 8 var:sed_plan_goal = 9 }} }}
    {enable_option('advisor')}
    set_variable = {{ name = sed_coord_executor value = 1 }}
    sed_coord_capture_advisor_policy = yes
    remove_variable = advisor_setting_sc_goal_sol
    remove_variable = advisor_setting_sc_goal_treasury
    remove_variable = advisor_setting_treasury_off
    remove_variable = advisor_setting_borrow
    set_variable = {{ name = sed_coord_advisor_policy value = 1 }}
    if = {{ limit = {{ principal > 0 credit > 0 principal >= {{ value = credit multiply = 0.5 }} }}
     set_variable = {{ name = advisor_setting_sc_goal_treasury value = yes }}
     set_variable = {{ name = advisor_setting_treasury_off value = yes }}
     set_variable = {{ name = sed_coord_advisor_policy value = 3 }}
    }}
    else_if = {{ limit = {{ OR = {{
     any_scope_state = {{ OR = {{ var:sed_plan_grain_rank = 1 var:sed_plan_groceries_rank = 1 var:sed_plan_clothes_rank = 1 }} }}
     AND = {{ var:sed_plan_goal = 5 OR = {{ var:sed_plan_missing_grain = 1 var:sed_plan_missing_groceries = 1 var:sed_plan_missing_clothes = 1 }} }}
    }} }}
     set_variable = {{ name = advisor_setting_sc_goal_sol value = yes }}
     set_variable = {{ name = sed_coord_advisor_policy value = 2 }}
    }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes OR = {{ var:sed_plan_goal = 2 var:sed_plan_goal = 5 var:sed_plan_goal = 8 }} }}
    {enable_option('chains')}
    set_variable = {{ name = sed_coord_executor value = 3 }}
   }}
   else_if = {{ limit = {{ has_variable = sed_coord_supply_known sed_auto_fiscal_safe = yes var:sed_plan_goal = 3 }}
    {enable_option('sectors')}
    set_variable = {{ name = sed_coord_executor value = 4 }}
   }}
  }}
 }}
}}
'''


def triggers():
    option_names = [option for _, option, _ in OPTIONS] + list(SUPPLY_HINTS)
    options = '\n'.join('  has_variable = ' + option for option in option_names)
    return ('sed_coord_tools_available = {\n OR = {\n  has_variable = advisor_enabled\n'
            + options + '\n }\n}\n')
