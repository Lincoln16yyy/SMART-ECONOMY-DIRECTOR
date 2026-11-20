"""Uma obra pública junto da fila privada, apenas com reservas verificáveis."""
try:
    from . import production_methods, input_forecast, labor, investment_outcomes, planning, construction_budget
except ImportError:
    import production_methods, input_forecast, labor, investment_outcomes, planning, construction_budget

VARIABLES = ['sed_parallel_direct_pending']

SUPPORTED = sorted(set(production_methods.PROFILES) & set(input_forecast.PROFILES) & set(labor.REQUIREMENTS))


def values():
    parts = ['sed_parallel_visible_levels = { value = 0 every_scope_state = { limit = { }']
    for building in SUPPORTED:
        known = ' '.join('OR = { '+' '.join('has_active_production_method = '+m for m in group['alternatives'])+' }'
                         for group in production_methods.PROFILES[building])
        parts.append(f''' if = {{ limit = {{ has_building = {building} b:{building} = {{ {known} }} }}
  add = {{ value = b:{building}.level_after_queued_constructions subtract = b:{building}.level min = 0 }}
 }}''')
    parts.append(' } }\n')
    parts.append('sed_parallel_all_visible_levels = { value = 0 every_scope_state = { limit = { }')
    for building in construction_budget.QUEUED_COSTS:
        parts.append(f''' if = {{ limit = {{ has_building = {building} }}
  add = {{ value = b:{building}.level_after_queued_constructions subtract = b:{building}.level min = 0 }}
 }}''')
    parts.append(' } }\n')
    return '\n'.join(parts)


def triggers(items):
    parts = ['''sed_private_parallel_capacity_safe = {
 is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
 NOT = { has_variable = sed_mode_manual } NOT = { has_variable = sed_mode_assisted }
 NOT = { in_default = yes } NOT = { sed_debt_discretionary_blocked = yes }
 is_construction_paused = no
 construction_queue_num_queued_government_levels = 0
 construction_queue_num_queued_private_levels > 0
 modifier:country_max_weekly_construction_progress_add > 0
 # Reserva o teto semanal de cada nível privado e de um novo projeto público.
 modifier:country_construction_add >= { value = construction_queue_num_queued_private_levels
  add = 1 multiply = modifier:country_max_weekly_construction_progress_add }
 sed_parallel_all_visible_levels = construction_queue_num_queued_private_levels
 sed_parallel_visible_levels = sed_parallel_all_visible_levels
 modifier:country_private_construction_allocation_mult >= 0
 modifier:country_private_construction_allocation_mult < 1
 sed_parallel_public_allocation >= modifier:country_max_weekly_construction_progress_add
 net_fixed_income >= 0 net_total_income > 0
 has_variable = sed_build_budget_known var:sed_build_budget_known = 1
 has_variable = sed_build_budget_weekly
 net_total_income >= { value = var:sed_build_budget_weekly multiply = 1.25 }
 NOT = { sed_civic_direct_available = yes }
}
''']
    for item in items:
        good = item['good']
        if good in planning.MILITARY_INDUSTRY_GOODS:continue
        queued=[]
        for b, outputs in investment_outcomes.OUTPUTS.items():
            methods=outputs.get(good,[])
            if not methods:continue
            active=' '.join('has_active_production_method = '+m for m in methods)
            queued.append(f'AND = {{ has_building = {b} b:{b} = {{ level_after_queued_constructions > level OR = {{ {active} }} }} }}')
        parts.append(f'''sed_parallel_{good}_not_duplicated = {{
 NOT = {{ any_scope_state = {{ OR = {{ has_variable = sed_{good}_request_pending {' '.join(queued)} }} }} }}
}}
''')
    return ''.join(parts)


def allocation_value():
    return '''sed_parallel_public_allocation = {
 value = 1 subtract = { value = modifier:country_private_construction_allocation_mult min = 0 max = 1 }
 multiply = { value = modifier:country_construction_add min = 0 }
}
'''


def effects():
    return '''sed_refresh_parallel_ownership = {
 if = { limit = { is_player = yes has_variable = sed_enabled
  has_variable = sed_parallel_direct_pending construction_queue_num_queued_government_levels = 0 }
  remove_variable = sed_parallel_direct_pending
 }
}
'''
