"""Initial configuration of newly founded, single-level Director industries."""
import json
from pathlib import Path

try:
    from . import input_forecast
except ImportError:
    import input_forecast

PROFILES = json.loads((Path(__file__).resolve().parents[1] / 'data/founding_production_methods.json').read_text())


def state_variables(targets):
    return [f"sed_{item['good']}_found_pm_pending" for item in targets]


def effects(targets, variants):
    result = ['''sed_configure_founded_industries = {
 if = { limit = {
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  NOT = { has_variable = sed_mode_manual }
  NOT = { has_variable = sed_mode_assisted }
 }
  sed_refresh_input_readings = yes
  every_scope_state = {
''']
    for item in targets:
        good = item['good']
        marker = f'sed_{good}_found_pm_pending'
        for index, variant in enumerate(variants(item), 1):
            building = variant['building']
            methods = [profile['method'] for profile in PROFILES[building]]
            activation = '\n'.join(
                f'''       OR = {{ b:{building} = {{ has_active_production_method = {method} }}
        can_activate_production_method = {{ building_type = {building} production_method = {method} }}
       }}'''
                for method in methods)
            inputs = []
            reservations = []
            for good_input in input_forecast.building_goods(building):
                amount = sum(input_forecast.PROFILES[building].get(method, {}).get(good_input, 0)
                             for method in methods)
                if amount > 0:
                    inputs.append(f'       sed_input_headroom_{good_input} >= {amount * 1.25:g}')
                    if good_input in input_forecast.LOCAL_GOODS:
                        variable = f'sed_input_local_margin_{good_input}'
                        reservations.append(f'        set_variable = {{ name = {variable} value = {{ value = var:{variable} subtract = {amount * 1.25:g} }} }}')
                    else:
                        variable = f'sed_input_market_margin_{good_input}'
                        reservations.append(f'        owner = {{ set_variable = {{ name = {variable} value = {{ value = var:{variable} subtract = {amount * 1.25:g} }} }} }}')
            commands = '\n'.join(f'''       if = {{ limit = {{ b:{building} = {{ NOT = {{ has_active_production_method = {method} }} }} }}
        activate_production_method = {{ building_type = {building} production_method = {method} }}
       }}''' for method in methods)
            input_checks = '\n'.join(inputs)
            reservation_commands = '\n'.join(reservations)
            confirmed = ' '.join(f'has_active_production_method = {method}' for method in methods)
            result.append(f'''   if = {{ limit = {{ has_variable = {marker} var:{marker} = {index} }}
    if = {{ limit = {{ OR = {{
     has_variable = sed_{good}_ignored is_incorporated = no
     AND = {{ NOT = {{ has_building = {building} }} NOT = {{ has_variable = sed_{good}_request_pending }} }}
     AND = {{ has_building = {building} b:{building} = {{ OR = {{ level > 1 level_after_queued_constructions > 1 }} }} }}
    }} }} remove_variable = {marker} }}
    else_if = {{ limit = {{ has_building = {building}
     sed_state_labor_pool >= sed_state_labor_committed
{activation}
{input_checks}
    }}
     if = {{ limit = {{ NOT = {{ b:{building} = {{ {confirmed} }} }} }}
{commands}
{reservation_commands}
     }}
     if = {{ limit = {{ b:{building} = {{ {confirmed} }} }} remove_variable = {marker} }}
    }}
   }}''')
    return '\n'.join(result) + '\n  }\n }\n}\n'
