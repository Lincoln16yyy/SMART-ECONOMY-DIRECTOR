"""Government administration executor for plan goals 6 and 7.

The national plan already sets goal 6 when national bureaucracy is negative and
goal 7 when an incorporated state uses more tax capacity than it has
(`tools/planning.py`). Until now those goals were only served by the Supply
Chain adapter: with no external tool detected, the direct executor had no action
for them and the monthly review ended with "nothing eligible".

Vanilla 1.15 makes this building the natural answer. In
`common/buildings/07_government.txt` it declares no `can_build_*` restriction,
requires `construction_cost_very_low` (100 points, see
`common/script_values/building_values.txt`) and its own `should_auto_expand`
reads the same bureaucracy and tax-capacity signals the plan uses.

The executor is deliberately narrow: one level per month, only in an
incorporated state with non-negative infrastructure that the engine accepts for
the building, only for goals 6 and 7, only when the building is not already
waiting for a queued level, and always under the direct-execution guards
(private queue, pause, fiscal, material budget and monthly attempt limit).
Goal 9 (power plant) remains delegated to the Supply Chain adapter.
"""

VARIABLES = ['sed_admin_action_status', 'sed_admin_intent_level',
             'sed_admin_request_pending', 'sed_admin_intents',
             'sed_admin_completed', 'sed_admin_abandoned',
             'sed_admin_result', 'sed_admin_result_month']

BUILDING = 'building_government_administration'
POINTS = 100


def triggers():
    return f'''# Country scope. Goals 6 and 7 are computed by the national plan.
sed_admin_needed = {{
 has_variable = sed_plan_goal
 OR = {{
  var:sed_plan_goal = 6
  var:sed_plan_goal = 7
 }}
}}

# State scope. Goal 7 only acts in a state that actually exceeds its tax
# capacity; goal 6 accepts any incorporated state that can host the building.
sed_admin_candidate_eligible = {{
 is_incorporated = yes
 infrastructure_delta >= 0
 can_construct_building = {BUILDING}
 NOT = {{ has_variable = sed_admin_request_pending }}
 owner = {{ sed_admin_needed = yes }}
 OR = {{
  NOT = {{ owner = {{ var:sed_plan_goal = 7 }} }}
  tax_capacity_usage > tax_capacity
 }}
 OR = {{
  NOT = {{ has_building = {BUILDING} }}
  b:{BUILDING} = {{
   level_after_queued_constructions <= level
   occupancy >= 0.5
   has_failed_hires = no
  }}
 }}
}}

sed_admin_approval_valid = {{
 sed_admin_candidate_eligible = yes
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
sed_run_admin_approval = {{
 owner = {{ if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic }} sed_refresh_direct_budget = yes }} }}
 if = {{
  limit = {{ sed_admin_approval_valid = yes }}
  owner = {{
   set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }}
  }}
  owner = {{ sed_record_auto_attempt = yes }}
  if = {{ limit = {{ has_building = {BUILDING} }}
   set_variable = {{ name = sed_admin_intent_level value = b:{BUILDING}.level }}
  }}
  else = {{ set_variable = {{ name = sed_admin_intent_level value = 0 }} }}
  start_building_construction = {BUILDING}
  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_admin_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_admin_intents }}
     change_variable = {{ name = sed_admin_intents add = 1 }}
    }}
    else = {{ set_variable = {{ name = sed_admin_intents value = 1 }} }}
    prev = {{ set_variable = {{ name = sed_admin_request_pending value = yes }} }}
   }}
   else = {{
    set_variable = {{ name = sed_admin_action_status value = 2 }}
    prev = {{ remove_variable = sed_admin_intent_level }}
   }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}

# Completion is inferred from the queue leaving and the level rising.
sed_refresh_admin = {{
 if = {{ limit = {{ is_player = yes has_variable = sed_enabled }}
  every_scope_state = {{
   if = {{
    limit = {{ has_variable = sed_admin_request_pending
     OR = {{
      NOT = {{ has_building = {BUILDING} }}
      b:{BUILDING} = {{ level_after_queued_constructions <= level }}
     }}
    }}
    if = {{ limit = {{ has_variable = sed_admin_intent_level
     has_building = {BUILDING} b:{BUILDING}.level > var:sed_admin_intent_level }}
     owner = {{
      if = {{ limit = {{ has_variable = sed_admin_completed }}
       change_variable = {{ name = sed_admin_completed add = 1 }}
      }}
      else = {{ set_variable = {{ name = sed_admin_completed value = 1 }} }}
      set_variable = {{ name = sed_admin_result value = 1 }}
      set_variable = {{ name = sed_admin_result_month value = sed_live_month_key }}
     }}
    }}
    else_if = {{ limit = {{ has_variable = sed_admin_intent_level }}
     owner = {{
      if = {{ limit = {{ has_variable = sed_admin_abandoned }}
       change_variable = {{ name = sed_admin_abandoned add = 1 }}
      }}
      else = {{ set_variable = {{ name = sed_admin_abandoned value = 1 }} }}
      set_variable = {{ name = sed_admin_result value = 2 }}
      set_variable = {{ name = sed_admin_result_month value = sed_live_month_key }}
     }}
    }}
    remove_variable = sed_admin_intent_level
    remove_variable = sed_admin_request_pending
   }}
  }}
 }}
}}
'''
