"""Last-resort expansion of the core inputs in a healthy economy.

The national plan only creates demand for a good when the market is short, when
the price is at least 20% above base, or when the good blocks another expansion
(`sed_<good>_supply_demand` in tools/build_mod.py). With everything balanced the
plan ends with zero priorities and the automatic executor idles -- which is
exactly what happened in a healthy Paraguay: positive treasury, nothing scarce,
no construction for months.

The stress used for the reference return (75% of revenue, 125% of inputs) is
negative for most industries at base prices, so waiting for a positive margin is
not enough either. This module adds a bounded growth lane for the three inputs
every economy needs first -- wood, iron and tools -- as the last branch of the
direct dispatcher, after the ranked targets, the civic goals and the Trade
Center fallback.

Scope of the lane:
- expansion only: a building of that type must already exist, so the country is
  not planting industry from scratch here (the scarcity lane already founds);
- only when `sed_develop_core` holds: automatic mode, fiscally safe, no default,
  non-negative bureaucracy, no state over tax capacity, no dear local power and
  no good without a producer -- those cases keep their own executor;
- not while the good is cheaper than base (`market_goods_cheaper`);
- occupancy >= 50%, no failed hires, no level already queued, labor reserved and
  the input forecast safe;
- one level per month, under the same direct-execution guards.
"""

try:
    from . import labor
except ImportError:
    import labor

TARGETS = (
    {'good': 'wood', 'building': 'building_logging_camp', 'variant': 'logging_camp'},
    {'good': 'iron', 'building': 'building_iron_mine', 'variant': 'iron_mine'},
    {'good': 'tools', 'building': 'building_tooling_workshop', 'variant': 'tooling_workshop'},
)


# The construction sector is the throttle of every other expansion. Vanilla
# charges only construction_cost_construction_sector (25 points,
# common/script_values/building_values.txt) and the plan only ranks it when the
# public queue already holds three projects, so a long queue never buys capacity.
# `construction_queue_government_duration` (weeks, country scope) is the gate
# here: with a queue of 12+ weeks a new sector level pays for itself.
CONSTRUCTION_BUILDING = 'building_construction_sector'
CONSTRUCTION_QUEUE_WEEKS = 12


def triggers():
    parts = [f'''# State scope. Growth expansion of the construction sector while the public
# queue is long; a level already queued waits for the queue.
sed_core_construction_eligible = {{
 is_incorporated = yes
 infrastructure_delta >= 0
 can_construct_building = {CONSTRUCTION_BUILDING}
 has_building = {CONSTRUCTION_BUILDING}
 NOT = {{ has_variable = sed_construction_ignored }}
 NOT = {{ has_variable = sed_construction_request_pending }}
 b:{CONSTRUCTION_BUILDING} = {{
  level_after_queued_constructions <= level
  occupancy >= 0.5
  has_failed_hires = no
 }}
 owner = {{ sed_develop_core = yes }}
 owner = {{ construction_queue_government_duration >= {CONSTRUCTION_QUEUE_WEEKS} }}
}}

sed_core_construction_approval_valid = {{
 sed_core_construction_eligible = yes
 owner = {{
  is_player = yes
  has_variable = sed_enabled
  NOT = {{ in_default = yes }}
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }}
}}''']
    for item in TARGETS:
        good, building, variant = item['good'], item['building'], item['variant']
        parts.append(f'''# State scope. Growth expansion of {good}: the building must already exist.
sed_core_{good}_eligible = {{
 is_incorporated = yes
 infrastructure_delta >= 0
 can_construct_building = {building}
 has_building = {building}
 NOT = {{ has_variable = sed_{good}_ignored }}
 NOT = {{ has_variable = sed_{good}_request_pending }}
 b:{building} = {{
  level_after_queued_constructions <= level
  occupancy >= 0.5
  has_failed_hires = no
 }}
 owner = {{ sed_develop_core = yes }}
 owner = {{ NOT = {{ market = {{ mg:{good} ?= {{ market_goods_cheaper = yes }} }} }} }}
 sed_state_labor_available >= {labor.REQUIREMENTS[building]}
 sed_input_{variant}_safe = yes
 sed_investment_{variant}_output > 0
}}

sed_core_{good}_approval_valid = {{
 sed_core_{good}_eligible = yes
 owner = {{
  is_player = yes
  has_variable = sed_enabled
  NOT = {{ in_default = yes }}
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }}
}}''')
    return '\n'.join(parts)


def effects():
    parts = [f'''# State scope. Queue one sector level under the growth lane.
sed_run_core_construction_approval = {{
 owner = {{ if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic }} sed_refresh_direct_budget = yes }} }}
 if = {{
  limit = {{ sed_core_construction_approval_valid = yes }}
  owner = {{
   set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }}
  }}
  owner = {{ sed_record_auto_attempt = yes }}
  set_variable = {{ name = sed_construction_intent_level value = b:{CONSTRUCTION_BUILDING}.level }}
  start_building_construction = {CONSTRUCTION_BUILDING}
  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_construction_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_mode_automatic }}
     set_variable = {{ name = sed_auto_action_status value = 1 }}
    }}
    prev = {{ set_variable = {{ name = sed_construction_request_pending value = yes }} }}
   }}
   else = {{
    set_variable = {{ name = sed_construction_action_status value = 2 }}
    prev = {{ remove_variable = sed_construction_intent_level }}
   }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}''']
    for item in TARGETS:
        good, building = item['good'], item['building']
        parts.append(f'''# State scope. Queue one public level under the growth lane. Reuses the ledger
# variables of the good, so the monthly reconciliation already covers it.
sed_run_core_{good}_approval = {{
 owner = {{ if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic }} sed_refresh_direct_budget = yes }} }}
 if = {{
  limit = {{ sed_core_{good}_approval_valid = yes }}
  owner = {{
   set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }}
  }}
  owner = {{ sed_record_auto_attempt = yes }}
  set_variable = {{ name = sed_{good}_intent_level value = b:{building}.level }}
  set_variable = {{ name = sed_{good}_intent_variant value = 1 }}
  start_building_construction = {building}
  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_{good}_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_mode_automatic }}
     set_variable = {{ name = sed_auto_action_status value = 1 }}
    }}
    if = {{ limit = {{ has_variable = sed_{good}_intents }}
     change_variable = {{ name = sed_{good}_intents add = 1 }}
    }}
    else = {{ set_variable = {{ name = sed_{good}_intents value = 1 }} }}
    prev = {{ set_variable = {{ name = sed_{good}_request_pending value = yes }} }}
   }}
   else = {{
    set_variable = {{ name = sed_{good}_action_status value = 2 }}
    prev = {{
     remove_variable = sed_{good}_intent_level
     remove_variable = sed_{good}_intent_variant
    }}
   }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}''')
    return '\n'.join(parts)
