"""Funda o primeiro setor apenas com caixa e insumos verificados."""
try:
    from . import public_upkeep
except ImportError:
    import public_upkeep

STATE_VARIABLES = ['sed_first_sector_pending']
PROFILES = public_upkeep.PROFILES['construction']['groups']
GOODS = sorted({g for group in PROFILES for spec in group.values() for g in spec['inputs']})


def values():
    result = []
    for good in GOODS:
        result.append(f'sed_first_sector_input_{good} = {{ value = 0')
        for group in PROFILES:
            for spec in group.values():
                amount = spec['inputs'].get(good, 0)
                tech = ' '.join('has_technology_researched = ' + t for t in spec['technologies'])
                result.append(f' min = {{ value = 0 if = {{ limit = {{ {tech} }} add = {amount:g} }} }}')
        result.append('}')
    return '\n'.join(result)+'\n'


def triggers():
    inputs = '\n'.join(f''' NOT = {{ owner = {{ sed_first_sector_input_{g} > 0 }}
  sed_input_headroom_{g} < {{ value = 0 owner = {{ add = sed_first_sector_input_{g} }} multiply = 1.25 }} }}''' for g in GOODS)
    return '''sed_first_sector_available = {
 is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
 NOT = { has_variable = sed_mode_manual } NOT = { has_variable = sed_mode_assisted }
 NOT = { in_default = yes } sed_direct_fiscal_safe = yes
 NOT = { sed_debt_discretionary_blocked = yes }
 has_variable = sed_plan_count var:sed_plan_count = 0
 NOT = { sed_civic_direct_available = yes }
 NOT = { any_scope_state = { has_building = building_construction_sector } }
 NOT = { any_scope_state = { has_variable = sed_construction_request_pending } }
 construction_queue_num_queued_private_levels = 0 is_construction_paused = no
 has_variable = sed_upkeep_construction_known var:sed_upkeep_construction_known = 1
 net_total_income >= { value = var:sed_upkeep_construction_cost multiply = 1.25 }
 OR = {
  AND = { principal <= 0 gold_reserves >= { value = sed_fixed_expenses_value
   add = var:sed_upkeep_construction_cost multiply = 4 } }
  AND = { sed_debt_growth_safe = yes credit >= { value = principal add = {
   value = sed_fixed_expenses_value add = var:sed_upkeep_construction_cost multiply = 4 } } }
 }
 OR = {
  AND = { construction_queue_government_duration >= 12
   has_variable = sed_build_budget_queue_levels_unknown var:sed_build_budget_queue_levels_unknown = 0 }
  AND = { construction_queue_num_queued_government_levels = 0
   modifier:country_construction_add <= 15 any_scope_state = { sed_growth_site = yes } }
 }
 any_scope_state = { sed_first_sector_site = yes }
}
sed_first_sector_site = {
 is_incorporated = yes infrastructure_delta >= 0
 can_construct_building = building_construction_sector
 NOT = { has_variable = sed_construction_ignored }
 sed_state_labor_available >= 1000
''' + inputs + '\n}\n'


def effects():
    return '''sed_follow_first_sector = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  every_scope_state = {
   limit = { has_variable = sed_first_sector_pending }
   if = { limit = { has_building = building_construction_sector
    b:building_construction_sector = { level > 0 } }
    remove_variable = sed_first_sector_pending
   }
   else_if = { limit = { NOT = { has_variable = sed_construction_request_pending } }
    remove_variable = sed_first_sector_pending
   }
  }
 }
}
'''


def branch():
    return '''  else_if = { limit = { sed_first_sector_available = yes }
   ordered_scope_state = {
    limit = { sed_first_sector_site = yes }
    order_by = sed_site_readiness max = 1 check_range_bounds = no
    sed_run_core_construction_approval = yes
   }
  }
'''
