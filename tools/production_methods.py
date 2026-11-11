"""Generate initial configurations and bounded upgrades for player industries."""
import json
from pathlib import Path

try:
    from . import input_forecast
except ImportError:
    import input_forecast

DATA = Path(__file__).resolve().parents[1] / 'data'
PROFILES = json.loads((DATA / 'founding_production_methods.json').read_text())
ECONOMICS = json.loads((DATA / 'founding_method_economics.json').read_text())
EMPLOYMENT = json.loads((DATA / 'employment_profiles.json').read_text())
COUNTRY_VARIABLES = ['sed_pm_upgrade_status']


def state_variables(targets):
    return ([f"sed_{item['good']}_found_pm_pending" for item in targets]
            + ['sed_pm_upgrade_score', 'sed_pm_upgrade_choice', 'sed_pm_upgrade_levels']
            + ['sed_pm_cooldown_' + building.removeprefix('building_') for building in PROFILES])


def material_margin(profile):
    prices = ECONOMICS['prices']
    revenue = sum(amount * prices[good] for good, amount in profile['outputs'].items())
    inputs = sum(amount * prices[good] for good, amount in profile['inputs'].items())
    return revenue * 0.75 - inputs * 1.25


def weighted_jobs(building, method):
    """Wage-weighted employment per level of one vanilla production method."""
    return EMPLOYMENT['buildings'].get(building, {}).get(method, {}).get('weighted_jobs', 0)


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
    return '\n'.join(result) + '''
 }
}
sed_begin_pm_input_reservations = {
 if = { limit = { NOT = { has_variable = sed_pm_inputs_month var:sed_pm_inputs_month = sed_live_month_key } }
  sed_clear_pm_input_reservations = yes
  set_variable = { name = sed_pm_inputs_month value = sed_live_month_key }
 }
 sed_refresh_input_readings = yes
}
'''


def reserve_input(good, amount):
    variable = f'sed_pm_reserved_{good}'
    margin = f'sed_input_local_margin_{good}' if good in input_forecast.LOCAL_GOODS else f'sed_input_market_margin_{good}'
    changes = f'''set_variable = {{ name = {variable} value = {{ value = 0 if = {{ limit = {{ has_variable = {variable} }} add = var:{variable} }} add = {amount} }} }}
        set_variable = {{ name = {margin} value = {{ value = var:{margin} subtract = {amount} }} }}'''
    if good not in input_forecast.LOCAL_GOODS:
        changes = changes.replace('var:sed_pm_upgrade_levels', 'prev.var:sed_pm_upgrade_levels')
        changes = 'owner = { ' + changes + ' }'
    return changes


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
        reservations.append('        ' + reserve_input(good, f'{stressed:g}'))
    commands = '\n'.join(f'''       if = {{ limit = {{ b:{building} = {{ NOT = {{ has_active_production_method = {method} }} }} }}
        activate_production_method = {{ building_type = {building} production_method = {method} }}
       }}''' for method in methods)
    confirmed = ' '.join(f'has_active_production_method = {method}' for method in methods)
    input_checks = '\n'.join(inputs)
    reservation_commands = '\n'.join(reservations)
    labor_guard = 'sed_state_labor_pool >= sed_state_labor_committed'
    baseline = [group['method'] for group in PROFILES[building]]
    if methods == baseline:
        jobs = ECONOMICS['buildings'][building][methods[0]]['workers']
        main_methods = ' '.join(
            f'has_active_production_method = {method}'
            for method, profile in ECONOMICS['buildings'][building].items()
            if profile['workers'] >= jobs)
        auxiliaries = ' '.join(f'has_active_production_method = {method}' for method in methods[1:])
        # A tracked startup may remain partially staffed. Returning its main PM
        # to basic does not add jobs when its auxiliary groups are already basic.
        labor_guard = f'OR = {{ {labor_guard} b:{building} = {{ {auxiliaries} OR = {{ {main_methods} }} }} }}'
    return f'''    else_if = {{ limit = {{ has_building = {building}
     {labor_guard}
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
  sed_begin_pm_input_reservations = yes
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
     owner = {{ OR = {{ has_variable = advisor_pm_balance_enabled has_variable = advisor_labor_auto_enabled }} }}
     AND = {{ NOT = {{ has_building = {building} }} NOT = {{ has_variable = sed_{good}_request_pending }} }}
     AND = {{ has_building = {building} b:{building} = {{ OR = {{ level > 1 level_after_queued_constructions > 1 }} }} }}
    }} }} remove_variable = {marker} }}''')
            for methods in configurations(building, good):
                result.append(configuration_branch(building, methods, marker))
            result.append('   }')
    return '\n'.join(result) + '\n  }\n }\n}\n' + reservation_effects()


def upgrades(targets, variants):
    result = []
    for item in targets:
        good = item['good']
        for variant in variants(item):
            building = variant['building']
            profiles = ECONOMICS['buildings'][building]
            for current, before in profiles.items():
                for target, after in profiles.items():
                    gain = material_margin(after) - material_margin(before)
                    preserves_outputs = all(after['outputs'].get(output, 0) >= amount
                                            for output, amount in before['outputs'].items()
                                            if output != good)
                    if (after['outputs'].get(good, 0) > before['outputs'].get(good, 0)
                            and after['workers'] <= before['workers'] and preserves_outputs
                            and material_margin(after) > 0 and gain > 0):
                        wage_delta = weighted_jobs(building, target) - weighted_jobs(building, current)
                        result.append((good, building, current, target, gain, wage_delta))
    return result


def recoveries(targets, variants):
    result = []
    for item in targets:
        good = item['good']
        for variant in variants(item):
            building = variant['building']
            profiles = ECONOMICS['buildings'][building]
            for current, before in profiles.items():
                for target, after in profiles.items():
                    output = after['outputs'].get(good, 0)
                    removes_input = any(amount > 0 and after['inputs'].get(input_good, 0) == 0
                                     for input_good, amount in before['inputs'].items())
                    no_new_inputs = all(amount <= before['inputs'].get(input_good, 0)
                                        for input_good, amount in after['inputs'].items())
                    preserves_outputs = all(after['outputs'].get(other, 0) >= amount
                                            for other, amount in before['outputs'].items() if other != good)
                    if (current != target and output > 0
                            and after['workers'] <= before['workers'] and material_margin(after) > 0
                            and removes_input
                            and no_new_inputs and preserves_outputs):
                        saving = sum((amount - after['inputs'].get(input_good, 0)) * ECONOMICS['prices'][input_good]
                                     for input_good, amount in before['inputs'].items())
                        wage_delta = weighted_jobs(building, target) - weighted_jobs(building, current)
                        result.append((good, building, current, target, saving, wage_delta))
    return result


def actual_input_shortage(good):
    if good in input_forecast.LOCAL_GOODS:
        return f'sg:{good} ?= {{ state_goods_consumption > {{ value = state_goods_production min = 0 multiply = 2 }} }}'
    return f'owner = {{ market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} }}'


def recovery_constraints(building, current, target, good):
    before = ECONOMICS['buildings'][building][current]['inputs']
    after = ECONOMICS['buildings'][building][target]['inputs']
    removed = '\n'.join('  ' + actual_input_shortage(good) for good, amount in before.items()
                        if amount > 0 and after.get(good, 0) == 0)
    lost_output = max(0, ECONOMICS['buildings'][building][current]['outputs'].get(good, 0)
                      - ECONOMICS['buildings'][building][target]['outputs'].get(good, 0))
    output_value = 'sed_supplier_' + building.removeprefix('building_') + '_output'
    result = [f' {output_value} > 0', f' {output_value} >= {lost_output * 2:g}', ' OR = {', removed, ' }']
    for input_good in input_forecast.building_goods(building):
        reduction = before.get(input_good, 0) - after.get(input_good, 0)
        result.append(f''' NOT = {{
  {input_forecast.amount_name(building, input_good)} > {reduction:g}
  {actual_input_shortage(input_good)}
 }}''')
    return '\n'.join(result)


def upgrade_inputs(building, current, target):
    profiles = ECONOMICS['buildings'][building]
    before, after = profiles[current]['inputs'], profiles[target]['inputs']
    return {good: amount - before.get(good, 0) for good, amount in after.items()
            if amount > before.get(good, 0)}


def upgrade_triggers(targets, variants, recovery=False):
    result = ['''sed_pm_upgrade_month_limit_reached = {
 has_variable = sed_pm_upgrade_last_attempt_month
 var:sed_pm_upgrade_last_attempt_month = sed_live_month_key
}''']
    pairs = recoveries(targets, variants) if recovery else upgrades(targets, variants)
    prefix = 'sed_pm_recovery' if recovery else 'sed_pm_upgrade'
    if recovery:
        result = []
    for index, (good, building, current, target, gain, wage_delta) in enumerate(pairs, 1):
        cooldown = 'sed_pm_cooldown_' + building.removeprefix('building_')
        technologies = ' '.join(f'has_technology_researched = {tech}'
                                for tech in ECONOMICS['buildings'][building][target]['technologies'])
        inputs = '\n'.join(f''' sed_input_headroom_{input_good} >= {{
  value = {amount * 1.25:g} multiply = b:{building}.level
 }}''' for input_good, amount in upgrade_inputs(building, current, target).items())
        cooldown_guard = '' if recovery else f' OR = {{ NOT = {{ has_variable = {cooldown} }} var:{cooldown} <= sed_live_month_key }}'
        demand_guard = '' if recovery else f'''  OR = {{ market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }}
   has_variable = sed_input_priority_{good}
  }}'''
        operation_guard = ('occupancy >= 0.5 building_has_goods_shortage = yes' if recovery
                           else 'occupancy >= 0.9 has_failed_hires = no building_has_goods_shortage = no')
        if recovery:
            inputs = recovery_constraints(building, current, target, good)
        site_guard = f'NOT = {{ has_variable = sed_{good}_ignored }}' if recovery else f'sed_{good}_candidate_site = yes'
        queue_guard = '' if recovery else 'level_after_queued_constructions <= level'
        result.append(f'''{prefix}_{index}_eligible = {{
 {site_guard}
 NOT = {{ has_variable = sed_{good}_found_pm_pending }}
{cooldown_guard}
 owner = {{
{demand_guard}
  {technologies}
 }}
 has_building = {building}
 b:{building} = {{
  level > 0 {operation_guard}
  {queue_guard}
  has_active_production_method = {current}
 }}
 can_activate_production_method = {{ building_type = {building} production_method = {target} }}
{inputs}
}}''')
    rendered = '\n'.join(result)
    return '\n'.join(line.rstrip() for line in rendered.splitlines()) + '\n'


def upgrade_effects(targets, variants, recovery=False):
    pairs = recoveries(targets, variants) if recovery else upgrades(targets, variants)
    prefix = 'sed_pm_recovery' if recovery else 'sed_pm_upgrade'
    effect_name = 'sed_recover_existing_industry' if recovery else 'sed_modernize_existing_industry'
    result = ['''__EFFECT_NAME__ = {
 if = { limit = {
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  NOT = { has_variable = sed_mode_manual }
  NOT = { has_variable = sed_mode_assisted }
  NOT = { sed_pm_upgrade_month_limit_reached = yes }
  NOT = { sed_auto_month_limit_reached = yes }
  NOT = { in_default = yes }
  NOT = { has_variable = aroai_autobuild }
  NOT = { has_variable = advisor_pm_balance_enabled }
  NOT = { has_variable = advisor_labor_auto_enabled }
  OR = { has_variable = sed_coord_active NOT = { sed_competing_builder_configured = yes } }
 }
  sed_begin_pm_input_reservations = yes
  every_scope_state = {
   set_variable = { name = sed_pm_upgrade_score value = 0 }
   set_variable = { name = sed_pm_upgrade_choice value = 0 }
''']
    for index, (good, building, current, target, gain, wage_delta) in enumerate(pairs, 1):
        score = (f'{{ value = {gain:g} multiply = b:{building}.level multiply = b:{building}.occupancy')
        if wage_delta > 0:
            # Only a change that adds wage-weighted employment needs the observed unit.
            score += (f'\n     if = {{ limit = {{ has_variable = sed_investment_wage_known var:sed_investment_wage_known = 1 }}\n'
                      f'      subtract = {{ value = {wage_delta:g} multiply = b:{building}.level'
                      f' multiply = b:{building}.occupancy multiply = var:sed_investment_wage_unit }} }}')
        score += ' }'
        result.append(f'''   if = {{ limit = {{ {prefix}_{index}_eligible = yes var:sed_pm_upgrade_score < {score} }}
    set_variable = {{ name = sed_pm_upgrade_score value = {score} }}
    set_variable = {{ name = sed_pm_upgrade_choice value = {index} }}
   }}''')
    result.append('''  }
  ordered_scope_state = {
   limit = { var:sed_pm_upgrade_score > 0 }
   order_by = { value = var:sed_pm_upgrade_score }
   max = 1 check_range_bounds = no
''')
    for index, (good, building, current, target, gain, wage_delta) in enumerate(pairs, 1):
        branch = 'if' if index == 1 else 'else_if'
        cooldown = 'sed_pm_cooldown_' + building.removeprefix('building_')
        reserves = '\n'.join('     ' + reserve_input(input_good,
                                f'{{ value = {amount * 1.25:g} multiply = var:sed_pm_upgrade_levels }}')
                             for input_good, amount in upgrade_inputs(building, current, target).items())
        result.append(f'''   {branch} = {{ limit = {{ var:sed_pm_upgrade_choice = {index} {prefix}_{index}_eligible = yes }}
    set_variable = {{ name = sed_pm_upgrade_levels value = b:{building}.level }}
    owner = {{
     set_variable = {{ name = sed_pm_upgrade_last_attempt_month value = sed_live_month_key }}
     set_variable = {{ name = sed_pm_upgrade_status value = 2 }}
     sed_record_auto_attempt = yes
     if = {{ limit = {{ has_variable = sed_coord_active }} sed_coord_sync = yes }}
    }}
    activate_production_method = {{ building_type = {building} production_method = {target} }}
{reserves}
    if = {{ limit = {{ b:{building} = {{ has_active_production_method = {target} }} }}
     set_variable = {{ name = {cooldown} value = {{ value = sed_live_month_key add = 3 }} }}
     owner = {{ set_variable = {{ name = sed_pm_upgrade_status value = {3 if recovery else 1} }} }}
    }}
    remove_variable = sed_pm_upgrade_levels
   }}''')
    script = '\n'.join(result) + '\n  }\n }\n}\n'
    if recovery:
        script = script.replace('  NOT = { in_default = yes }\n', '')
    return script.replace('__EFFECT_NAME__', effect_name)
