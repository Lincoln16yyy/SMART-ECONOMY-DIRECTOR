"""Material stress benchmark from verified vanilla construction methods.

This is a deliberately conservative reference, not an engine expense forecast.
It charges the next project's potential points at the highest active method's
material cost, capped by the sectors' level/occupancy material reference,
with a 75% price stress. Existing wages and completed-factory
operating costs are outside this incremental material benchmark.
"""
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
VARIABLES = ['sed_build_budget_known', 'sed_build_budget_points',
             'sed_build_budget_point_cost', 'sed_build_budget_weekly',
             'sed_build_budget_required_gold', 'sed_build_budget_material_capacity']


def effects():
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
  set_variable = { name = sed_build_budget_weekly value = {
   value = var:sed_build_budget_points multiply = var:sed_build_budget_point_cost
   max = var:sed_build_budget_material_capacity
  } }
  set_variable = { name = sed_build_budget_required_gold value = {
   value = fixed_expenses min = 0 multiply = 4
   add = { value = var:sed_build_budget_weekly subtract = net_total_income min = 0 multiply = 26 }
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
