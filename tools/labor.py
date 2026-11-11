"""Conservative state labor reference for existing-producer expansions.

Requirements are verified maximum employment sums by production-method group
in local vanilla. They intentionally ignore automation savings. The demographic
pool is a proxy, with half of peasants counted and no qualification forecast.
"""
import json
from pathlib import Path

REQUIREMENTS = json.loads((Path(__file__).resolve().parents[1] / 'data/labor_requirements.json').read_text())
STATE_VARIABLES = ['sed_labor_pool', 'sed_labor_committed', 'sed_labor_available']


def values(founding_projects=()):
    result = ['''# State scope; demographic proxy rather than a worker count from the engine.
sed_state_labor_pool = {
 value = state_population min = 0
 multiply = { value = 0.25 add = modifier:state_working_adult_ratio_add min = 0.05 max = 1 }
 multiply = {
  value = state_unemployment_rate min = 0 max = 1
  add = { value = "pop_type_percent_state(pop_type:peasants)" min = 0 max = 1 multiply = 0.5 }
  max = 1
 }
}
sed_state_labor_committed = {
 value = 0
''']
    for building, workers in REQUIREMENTS.items():
        result.append(f''' if = {{ limit = {{ has_building = {building} }}
  add = {{ value = b:{building}.level_after_queued_constructions
   subtract = {{ value = b:{building}.level multiply = {{ value = b:{building}.occupancy min = 0 max = 1 }} }}
   min = 0 multiply = {workers}
  }}
 }}''')
    for action, variant, building in founding_projects:
        variant_gate = f'var:sed_{action}_intent_variant = {variant}' if variant else ''
        result.append(f''' if = {{ limit = {{
  NOT = {{ has_building = {building} }}
  has_variable = sed_{action}_request_pending
  var:sed_{action}_intent_level = 0
{variant_gate}
 }} add = {REQUIREMENTS[building]} }}''')
    result.append('''}
sed_state_labor_available = {
 value = sed_state_labor_pool subtract = sed_state_labor_committed min = 0
}
''')
    return '\n'.join(result)


def effects():
    return '''sed_refresh_labor_readings = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  every_scope_state = {
   set_variable = { name = sed_labor_pool value = sed_state_labor_pool }
   set_variable = { name = sed_labor_committed value = sed_state_labor_committed }
   set_variable = { name = sed_labor_available value = sed_state_labor_available }
  }
 }
}
'''
