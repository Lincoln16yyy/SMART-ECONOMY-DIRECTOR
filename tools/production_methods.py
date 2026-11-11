"""Choose an initial production configuration for tracked Director foundations."""
import json
from pathlib import Path

try:
    from . import input_forecast
except ImportError:
    import input_forecast

DATA = Path(__file__).resolve().parents[1] / 'data'
PROFILES = json.loads((DATA / 'founding_production_methods.json').read_text())
ECONOMICS = json.loads((DATA / 'founding_method_economics.json').read_text())


def state_variables(targets):
    return [f"sed_{item['good']}_found_pm_pending" for item in targets]


def material_margin(profile):
    prices = ECONOMICS['prices']
    revenue = sum(amount * prices[good] for good, amount in profile['outputs'].items())
    inputs = sum(amount * prices[good] for good, amount in profile['inputs'].items())
    return revenue * 0.75 - inputs * 1.25


def configurations(building, good):
    baseline = [group['method'] for group in PROFILES[building]]
    profiles = ECONOMICS['buildings'][building]
    reference = profiles[baseline[0]]
    alternatives = [method for method, profile in profiles.items()
                    if profile['outputs'].get(good, 0) > reference['outputs'].get(good, 0)
                    and profile['workers'] <= reference['workers']
                    and material_margin(profile) > max(0, material_margin(reference))]
    alternatives.sort(key=lambda method: material_margin(profiles[method]), reverse=True)
    return [[method, *baseline[1:]] for method in alternatives] + [baseline]


def reservation_effects():
    result = ['sed_clear_pm_input_reservations = {\n remove_variable = sed_pm_inputs_month']
    for good in input_forecast.MARKET_GOODS:
        result.append(f' set_variable = {{ name = sed_pm_reserved_{good} value = 0 }}')
    result.append(' every_scope_state = {')
    for good in sorted(input_forecast.LOCAL_GOODS & set(input_forecast.GOODS)):
        result.append(f'  set_variable = {{ name = sed_pm_reserved_{good} value = 0 }}')
    return '\n'.join(result) + '\n }\n}\n'


def configuration_branch(building, methods, marker):
    activation = '\n'.join(
        f'''       OR = {{ b:{building} = {{ has_active_production_method = {method} }}
        can_activate_production_method = {{ building_type = {building} production_method = {method} }}
       }}''' for method in methods)
    technologies = ' '.join(f'has_technology_researched = {tech}'
                            for tech in ECONOMICS['buildings'][building][methods[0]]['technologies'])
    inputs = []
    reservations = []
    for good in input_forecast.building_goods(building):
        amount = sum(input_forecast.PROFILES[building].get(method, {}).get(good, 0) for method in methods)
        if amount <= 0:
            continue
        stressed = amount * 1.25
        inputs.append(f'       sed_input_headroom_{good} >= {stressed:g}')
        variable = f'sed_pm_reserved_{good}'
        margin = f'sed_input_local_margin_{good}' if good in input_forecast.LOCAL_GOODS else f'sed_input_market_margin_{good}'
        changes = f'''set_variable = {{ name = {variable} value = {{ value = 0 if = {{ limit = {{ has_variable = {variable} }} add = var:{variable} }} add = {stressed:g} }} }}
        set_variable = {{ name = {margin} value = {{ value = var:{margin} subtract = {stressed:g} }} }}'''
        if good not in input_forecast.LOCAL_GOODS:
            changes = 'owner = { ' + changes + ' }'
        reservations.append('        ' + changes)
    commands = '\n'.join(f'''       if = {{ limit = {{ b:{building} = {{ NOT = {{ has_active_production_method = {method} }} }} }}
        activate_production_method = {{ building_type = {building} production_method = {method} }}
       }}''' for method in methods)
    confirmed = ' '.join(f'has_active_production_method = {method}' for method in methods)
    input_checks = '\n'.join(inputs)
    reservation_commands = '\n'.join(reservations)
    return f'''    else_if = {{ limit = {{ has_building = {building}
     sed_state_labor_pool >= sed_state_labor_committed
     owner = {{ {technologies} }}
{activation}
{input_checks}
    }}
     if = {{ limit = {{ NOT = {{ b:{building} = {{ {confirmed} }} }} }}
{commands}
{reservation_commands}
     }}
     if = {{ limit = {{ b:{building} = {{ {confirmed} }} }} remove_variable = {marker} }}
    }}'''


def effects(targets, variants):
    result = ['''sed_configure_founded_industries = {
 if = { limit = {
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  NOT = { has_variable = sed_mode_manual }
  NOT = { has_variable = sed_mode_assisted }
 }
  if = { limit = { NOT = { has_variable = sed_pm_inputs_month var:sed_pm_inputs_month = sed_live_month_key } }
   sed_clear_pm_input_reservations = yes
   set_variable = { name = sed_pm_inputs_month value = sed_live_month_key }
  }
  sed_refresh_input_readings = yes
  every_scope_state = {
''']
    for item in targets:
        good = item['good']
        marker = f'sed_{good}_found_pm_pending'
        for index, variant in enumerate(variants(item), 1):
            building = variant['building']
            result.append(f'''   if = {{ limit = {{ has_variable = {marker} var:{marker} = {index} }}
    if = {{ limit = {{ OR = {{
     has_variable = sed_{good}_ignored is_incorporated = no
     AND = {{ NOT = {{ has_building = {building} }} NOT = {{ has_variable = sed_{good}_request_pending }} }}
     AND = {{ has_building = {building} b:{building} = {{ OR = {{ level > 1 level_after_queued_constructions > 1 }} }} }}
    }} }} remove_variable = {marker} }}''')
            for methods in configurations(building, good):
                result.append(configuration_branch(building, methods, marker))
            result.append('   }')
    return '\n'.join(result) + '\n  }\n }\n}\n' + reservation_effects()
