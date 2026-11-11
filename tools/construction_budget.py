"""Material stress benchmark from verified vanilla construction methods.

This is a deliberately conservative reference, not an engine expense forecast.
It charges the next project's potential points at the highest active method's
material cost, capped by the sectors' level/occupancy material reference,
with a 75% price stress. Existing wages and completed-factory
operating costs are outside this incremental material benchmark.
"""
import json
from pathlib import Path

QUEUED_COSTS = json.loads((Path(__file__).resolve().parents[1] / 'data/queued_building_costs.json').read_text())
BASE_PRICES = {'wood': 20, 'fabric': 20, 'iron': 40, 'tools': 40,
               'steel': 50, 'glass': 40, 'explosives': 50,
               'electricity': 30, 'copper': 40}
PROFILES = (
    ('pm_wooden_buildings', 2, {'fabric': 25, 'wood': 75}),
    ('pm_iron_frame_buildings', 5, {'wood': 40, 'fabric': 20, 'iron': 50, 'tools': 10}),
    ('pm_steel_frame_buildings', 10, {'steel': 50, 'glass': 40, 'explosives': 10, 'tools': 20}),
    ('pm_arc_welded_buildings', 15, {'steel': 50, 'glass': 40, 'explosives': 20,
                                  'tools': 30, 'electricity': 40, 'copper': 10}),
)
# Vanilla required_construction values per level, in construction points.
# Every action has a single cost category across its producer variants.
PROJECT_POINTS = {
    'railway': 800, 'construction': 25,
    'wood': 200, 'iron': 400, 'coal': 400, 'grain': 200, 'fabric': 200,
    'tools': 600, 'groceries': 600, 'clothes': 600,
    'small_arms': 600, 'artillery': 600, 'ammunition': 800,
}
VARIABLES = ['sed_build_budget_known', 'sed_build_budget_points',
             'sed_build_budget_point_cost', 'sed_build_budget_weekly',
             'sed_build_budget_required_gold', 'sed_build_budget_material_capacity',
             'sed_build_budget_project_points', 'sed_build_budget_project_weeks',
             'sed_build_budget_project_materials', 'sed_build_budget_queue_levels_known',
             'sed_build_budget_queue_points', 'sed_build_budget_queue_weeks',
             'sed_build_budget_queue_levels_unknown', 'sed_build_budget_funding_weeks',
             'sed_build_budget_active_points']


def effects(founding_projects=()):
    methods = ' '.join(f'has_active_production_method = {method}' for method, _, _ in PROFILES)
    result = ['''sed_refresh_direct_budget = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  set_variable = { name = sed_build_budget_known value = 1 }
  set_variable = { name = sed_build_budget_point_cost value = 0 }
  set_variable = { name = sed_build_budget_points value = {
   value = modifier:country_construction_add min = 0
   max = { value = modifier:country_max_weekly_construction_progress_add min = 0 }
  } }
''']
    for method, points, inputs in PROFILES:
        cost = sum(BASE_PRICES[good] * amount for good, amount in inputs.items()) * 1.75 / points
        result.append(f'''  if = {{ limit = {{ any_scope_state = {{ has_building = building_construction_sector
   b:building_construction_sector = {{ level > 0 occupancy > 0 has_active_production_method = {method} }}
  }} }}
   set_variable = {{ name = sed_build_budget_point_cost value = {{ value = var:sed_build_budget_point_cost min = {cost:.6f} }} }}
  }}''')
    result.append(f'''  if = {{ limit = {{ any_scope_state = {{ has_building = building_construction_sector
   b:building_construction_sector = {{ level > 0 occupancy > 0 NOT = {{ OR = {{ {methods} }} }} }}
  }} }} set_variable = {{ name = sed_build_budget_known value = 0 }} }}''')
    result.append('''  set_variable = { name = sed_build_budget_material_capacity value = {
   value = 0
   every_scope_state = {
    limit = { has_building = building_construction_sector
     b:building_construction_sector = { level > 0 occupancy > 0 }
    }
''')
    for method, _, inputs in PROFILES:
        cost = sum(BASE_PRICES[good] * amount for good, amount in inputs.items()) * 1.75
        result.append(f'''    if = {{ limit = {{ b:building_construction_sector = {{ has_active_production_method = {method} }} }}
     add = {{ value = b:building_construction_sector.level
      multiply = {{ value = b:building_construction_sector.occupancy min = 0 max = 1 }}
      multiply = {cost:g}
     }}
    }}''')
    result.append('''   }
  } }
  set_variable = { name = sed_build_budget_active_points value = {
   value = modifier:country_construction_add min = 0
   max = { value = construction_queue_num_queued_government_levels min = 0 add = 1
    multiply = { value = modifier:country_max_weekly_construction_progress_add min = 0 }
   }
  } }
  set_variable = { name = sed_build_budget_weekly value = {
   value = var:sed_build_budget_active_points multiply = var:sed_build_budget_point_cost
   max = var:sed_build_budget_material_capacity
  } }
  # Duration and full material reference for the plan's first priority.
  set_variable = { name = sed_build_budget_project_points value = 0 }
''')
    for action, points in PROJECT_POINTS.items():
        result.append(f'''  if = {{ limit = {{ var:sed_build_budget_project_points = 0
   any_scope_state = {{ has_variable = sed_plan_{action}_rank var:sed_plan_{action}_rank = 1 }} }}
   set_variable = {{ name = sed_build_budget_project_points value = {points} }}
  }}''')
    for field in ('levels_known', 'points'):
        result.append(f'''  set_variable = {{ name = sed_build_budget_queue_{field} value = 0 }}
  if = {{ limit = {{ construction_queue_num_queued_government_levels > 0 }}
   set_variable = {{ name = sed_build_budget_queue_{field} value = {{
    value = 0 every_scope_state = {{ limit = {{ }}
''')
        for building, points in QUEUED_COSTS.items():
            multiplier = points if field == 'points' else 1
            result.append(f'''     if = {{ limit = {{ has_building = {building} }}
      add = {{ value = b:{building}.level_after_queued_constructions subtract = b:{building}.level min = 0 multiply = {multiplier} }}
     }}''')
        for action, variant, building in founding_projects:
            variant_gate = f'var:sed_{action}_intent_variant = {variant}' if variant else ''
            points = QUEUED_COSTS[building] if field == 'points' else 1
            result.append(f'''     if = {{ limit = {{
      NOT = {{ has_building = {building} }}
      has_variable = sed_{action}_request_pending var:sed_{action}_intent_level = 0
{variant_gate}
     }} add = {points} }}''')
        result.append('    }\n   } }\n  }')
    result.append(f'''  set_variable = {{ name = sed_build_budget_queue_levels_unknown value = {{
   value = construction_queue_num_queued_government_levels
   subtract = var:sed_build_budget_queue_levels_known min = 0
  }} }}
  set_variable = {{ name = sed_build_budget_queue_points value = {{
   value = var:sed_build_budget_queue_points
   add = {{ value = var:sed_build_budget_queue_levels_unknown multiply = {max(QUEUED_COSTS.values())} }}
   max = {{ value = construction_queue_num_queued_government_levels min = 0 multiply = {max(QUEUED_COSTS.values())} }}
  }} }}
  set_variable = {{ name = sed_build_budget_queue_weeks value = 0 }}
  if = {{ limit = {{ modifier:country_construction_add > 0 }}
   set_variable = {{ name = sed_build_budget_queue_weeks value = {{
    value = var:sed_build_budget_queue_points divide = modifier:country_construction_add
   }} }}
  }}
''')
    result.append('''  set_variable = { name = sed_build_budget_project_weeks value = 0 }
  set_variable = { name = sed_build_budget_project_materials value = {
   value = var:sed_build_budget_project_points multiply = var:sed_build_budget_point_cost
  } }
  if = { limit = { var:sed_build_budget_project_points > 0 var:sed_build_budget_points > 0 }
   set_variable = { name = sed_build_budget_project_weeks value = {
    value = var:sed_build_budget_project_points divide = var:sed_build_budget_points
   } }
  }
  set_variable = { name = sed_build_budget_funding_weeks value = {
   value = var:sed_build_budget_project_weeks add = var:sed_build_budget_queue_weeks add = 4 min = 26
  } }
  set_variable = { name = sed_build_budget_required_gold value = {
   value = fixed_expenses min = 0 multiply = 4
   add = { value = var:sed_build_budget_weekly subtract = net_total_income min = 0
    multiply = var:sed_build_budget_funding_weeks
   }
  } }
 }
}
''')
    return '\n'.join(result)


def triggers():
    return '''sed_direct_budget_safe = {
 has_variable = sed_build_budget_known var:sed_build_budget_known = 1
 has_variable = sed_build_budget_weekly
 modifier:country_construction_add > 0
 modifier:country_max_weekly_construction_progress_add > 0
 OR = {
  net_total_income >= var:sed_build_budget_weekly
  AND = { principal <= 0 gold_reserves >= var:sed_build_budget_required_gold }
 }
}
'''
