"""Power plant executor for plan goal 9.

The national plan sets goal 9 when an incorporated state sees local electricity
at least 20% above its base price (`tools/planning.py`). Until now that goal was
only served by the Supply Chain adapter (`zw_var_scsab_construct_power_plant`):
with no external tool detected, the direct executor had no action for it.

Vanilla 1.15 makes this building the natural answer. In
`common/buildings/06_urban_center.txt` it declares no `can_build_*`
restriction, unlocks with `electrical_generation`, requires
`construction_cost_medium` (400 points, `data/queued_building_costs.json` and
`common/script_values/building_values.txt`) and its `ai_value` says the country
needs one level everywhere as the prerequisite for electricity production
methods. `can_construct_building` enforces the technology and the city type,
so a country without the technology simply has no eligible state.

The executor is deliberately narrow: one level per month, only for goal 9, only
in an incorporated state with non-negative infrastructure whose local
electricity is expensive, one level at a time per state, and always under the
direct-execution guards (private queue, pause, fiscal, material budget and
monthly attempt limit).
"""

VARIABLES = ['sed_power_action_status', 'sed_power_intent_level',
             'sed_power_request_pending', 'sed_power_intents',
             'sed_power_completed', 'sed_power_abandoned',
             'sed_power_result', 'sed_power_result_month']

BUILDING = 'building_power_plant'
POINTS = 400


def triggers():
    return f'''# Country scope. Goal 9 is computed by the national plan.
sed_power_needed = {{
 has_variable = sed_plan_goal
 var:sed_plan_goal = 9
}}

# State scope. Local electricity must be dear where the plant goes; the plan
# uses the same reading to set the goal.
sed_power_candidate_eligible = {{
 is_incorporated = yes
 infrastructure_delta >= 0
 can_construct_building = {BUILDING}
 NOT = {{ has_variable = sed_power_request_pending }}
 owner = {{ sed_power_needed = yes }}
 sg:electricity ?= {{ state_goods_pricier >= 0.2 }}
 OR = {{
  NOT = {{ has_building = {BUILDING} }}
  b:{BUILDING} = {{
   level_after_queued_constructions <= level
   occupancy >= 0.5
   has_failed_hires = no
  }}
 }}
}}

sed_power_approval_valid = {{
 sed_power_candidate_eligible = yes
 owner = {{
  is_player = yes
  has_variable = sed_enabled
  NOT = {{ in_default = yes }}
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }}
}}
'''


def effects():
    return f'''# State scope. Queue one public level and record the intent for the monthly
# review; only a queue count increase confirms the insertion.
sed_run_power_approval = {{
 owner = {{ if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic }} sed_refresh_direct_budget = yes }} }}
 if = {{
  limit = {{ sed_power_approval_valid = yes }}
  owner = {{
   set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }}
  }}
  owner = {{ sed_record_auto_attempt = yes }}
  if = {{ limit = {{ has_building = {BUILDING} }}
   set_variable = {{ name = sed_power_intent_level value = b:{BUILDING}.level }}
  }}
  else = {{ set_variable = {{ name = sed_power_intent_level value = 0 }} }}
  start_building_construction = {BUILDING}
  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_power_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_power_intents }}
     change_variable = {{ name = sed_power_intents add = 1 }}
    }}
    else = {{ set_variable = {{ name = sed_power_intents value = 1 }} }}
    prev = {{ set_variable = {{ name = sed_power_request_pending value = yes }} }}
   }}
   else = {{
    set_variable = {{ name = sed_power_action_status value = 2 }}
    prev = {{ remove_variable = sed_power_intent_level }}
   }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}

# Completion is inferred from the queue leaving and the level rising.
sed_refresh_power = {{
 if = {{ limit = {{ is_player = yes has_variable = sed_enabled }}
  every_scope_state = {{
   if = {{
    limit = {{ has_variable = sed_power_request_pending
     OR = {{
      NOT = {{ has_building = {BUILDING} }}
      b:{BUILDING} = {{ level_after_queued_constructions <= level }}
     }}
    }}
    if = {{ limit = {{ has_variable = sed_power_intent_level
     has_building = {BUILDING} b:{BUILDING}.level > var:sed_power_intent_level }}
     owner = {{
      if = {{ limit = {{ has_variable = sed_power_completed }}
       change_variable = {{ name = sed_power_completed add = 1 }}
      }}
      else = {{ set_variable = {{ name = sed_power_completed value = 1 }} }}
      set_variable = {{ name = sed_power_result value = 1 }}
      set_variable = {{ name = sed_power_result_month value = sed_live_month_key }}
     }}
    }}
    else_if = {{ limit = {{ has_variable = sed_power_intent_level }}
     owner = {{
      if = {{ limit = {{ has_variable = sed_power_abandoned }}
       change_variable = {{ name = sed_power_abandoned add = 1 }}
      }}
      else = {{ set_variable = {{ name = sed_power_abandoned value = 1 }} }}
      set_variable = {{ name = sed_power_result value = 2 }}
      set_variable = {{ name = sed_power_result_month value = sed_live_month_key }}
     }}
    }}
    remove_variable = sed_power_intent_level
    remove_variable = sed_power_request_pending
   }}
  }}
 }}
}}
'''
