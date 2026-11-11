"""Per-level material references for supply investments in the existing catalog."""
import json
from pathlib import Path

try:
    from . import input_forecast, production_methods
except ImportError:
    import input_forecast
    import production_methods

EMPLOYMENT = json.loads((Path(__file__).resolve().parents[1] / 'data/employment_profiles.json').read_text())
WAGE_VARIABLES = [f'sed_investment_wage_{field}' for field in ('cost', 'jobs', 'unit', 'known')]
PRICES = production_methods.ECONOMICS['prices']
COUNTRY_VARIABLES = [f'sed_investment_market_{good}_{bound}' for good in PRICES
                     for bound in ('lower', 'upper')] + WAGE_VARIABLES
STATE_VARIABLES = [f'sed_investment_local_{good}_{bound}' for good in PRICES
                   for bound in ('lower', 'upper')] + WAGE_VARIABLES


def price_adjustments(scope, base, bound):
    if scope == 'market':
        return f''' if = {{ limit = {{ market_goods_pricier > 0 }} add = {{ value = market_goods_pricier multiply = {base:g} }} }}
 if = {{ limit = {{ market_goods_cheaper > 0 }} subtract = {{ value = market_goods_cheaper multiply = {base:g} }} }}'''
    result = []
    if bound == 'lower':
        result.append(f' if = {{ limit = {{ state_goods_cheaper > 0 }} subtract = {base * 0.1:g} }}')
    else:
        result.append(f' if = {{ limit = {{ state_goods_pricier > 0 }} add = {base * 0.1:g} }}')
    previous = 0
    for threshold in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75):
        change = base * (threshold - previous)
        result.append(f' if = {{ limit = {{ {scope}_goods_pricier >= {threshold:g} }} add = {change:g} }}')
        result.append(f' if = {{ limit = {{ {scope}_goods_cheaper >= {threshold:g} }} subtract = {change:g} }}')
        previous = threshold
    return '\n'.join(result)


def price_values():
    result = []
    for good, base in PRICES.items():
        for bound, factor in [('lower', 0.75), ('upper', 1.25)]:
            market = price_adjustments('market', base, bound)
            local = price_adjustments('state', base, bound)
            present = f'sg:{good} ?= {{ state_goods_production >= 0 }}'
            result.append(f'''sed_investment_market_price_{good}_{bound} = {{
 value = {base * factor:g}
 market ?= {{ mg:{good} ?= {{
{market}
 }} }}
 min = 0
 max = {base * 2:g}
}}
sed_investment_observed_price_{good}_{bound} = {{
 value = 0
 if = {{ limit = {{ {present} }}
  add = {base * factor:g}
  sg:{good} ?= {{
{local}
  }}
 }}
 if = {{ limit = {{ NOT = {{ {present} }} }} add = owner.var:sed_investment_market_{good}_{bound} }}
 min = 0
 max = {base * 2:g}
}}
sed_investment_price_{good}_{bound} = {{
 value = 0
 if = {{ limit = {{ has_variable = sed_investment_local_{good}_{bound} }} add = var:sed_investment_local_{good}_{bound} }}
 if = {{ limit = {{ NOT = {{ has_variable = sed_investment_local_{good}_{bound} }} }} add = sed_investment_observed_price_{good}_{bound} }}
}}''')
    return '\n'.join(result) + '\n'


def employment_values():
    result = []
    for building, methods in EMPLOYMENT['buildings'].items():
        name = building.removeprefix('building_')
        result.append(f'sed_investment_{name}_weighted_jobs = {{\n value = 0')
        for method, profile in methods.items():
            amount = profile['weighted_jobs']
            if amount:
                result.append(f' if = {{ limit = {{ b:{building} = {{ has_active_production_method = {method} }} }} add = {amount:g} }}')
        result.append(' min = 0\n}')
    return '\n'.join(result) + '\n'


def wage_effects():
    """Observed weekly wage bill per weighted job.

    Vanilla shows earnings as weekly value added next to wages
    (`TOOLTIP_BUILDING_HEALTH_WORLD`, `EARNINGS_BREAKDOWN`), so
    earnings minus weekly_profit is the building's weekly wage bill.
    """
    result = ['''sed_refresh_investment_wages = {
 set_variable = { name = sed_investment_wage_cost value = 0 }
 set_variable = { name = sed_investment_wage_jobs value = 0 }
 set_variable = { name = sed_investment_wage_unit value = 0 }
 set_variable = { name = sed_investment_wage_known value = 0 }
 every_scope_state = {
  set_variable = { name = sed_investment_wage_cost value = 0 }
  set_variable = { name = sed_investment_wage_jobs value = 0 }''']
    for building, groups in production_methods.PROFILES.items():
        name = building.removeprefix('building_')
        known = '\n'.join('    OR = { ' + ' '.join(f'has_active_production_method = {method}'
                                                for method in group['alternatives']) + ' }'
                          for group in groups)
        result.append(f'''  if = {{ limit = {{ has_building = {building}
   b:{building} = {{ level > 0 occupancy >= 0.8 has_failed_hires = no
    building_has_goods_shortage = no is_subsidized = no earnings > 0
{known}
    weekly_profit <= earnings
   }}
   sed_investment_{name}_weighted_jobs > 0
  }}
   change_variable = {{ name = sed_investment_wage_cost add = {{
    value = b:{building}.earnings subtract = b:{building}.weekly_profit min = 0
   }} }}
   change_variable = {{ name = sed_investment_wage_jobs add = {{
    value = sed_investment_{name}_weighted_jobs
    multiply = b:{building}.level multiply = b:{building}.occupancy
   }} }}
  }}''')
    result.append('''  owner = {
   change_variable = { name = sed_investment_wage_cost add = prev.var:sed_investment_wage_cost }
   change_variable = { name = sed_investment_wage_jobs add = prev.var:sed_investment_wage_jobs }
  }
 }
 if = { limit = { var:sed_investment_wage_jobs > 0 }
  set_variable = { name = sed_investment_wage_unit value = {
   value = var:sed_investment_wage_cost divide = var:sed_investment_wage_jobs
  } }
  set_variable = { name = sed_investment_wage_known value = 1 }
 }
 every_scope_state = {
  set_variable = { name = sed_investment_wage_known value = owner.var:sed_investment_wage_known }
  set_variable = { name = sed_investment_wage_unit value = owner.var:sed_investment_wage_unit }
  if = { limit = { var:sed_investment_wage_jobs > 0 }
   set_variable = { name = sed_investment_wage_unit value = {
    value = var:sed_investment_wage_cost divide = var:sed_investment_wage_jobs
   } }
   set_variable = { name = sed_investment_wage_known value = 1 }
  }
 }
}
''')
    return '\n'.join(result)



def effects():
    result = ['''sed_refresh_investment_prices = {
 if = { limit = { is_player = yes has_variable = sed_enabled }''']
    for good in PRICES:
        for bound in ('lower', 'upper'):
            result.append(f'  set_variable = {{ name = sed_investment_market_{good}_{bound} value = sed_investment_market_price_{good}_{bound} }}')
    result.append('  every_scope_state = {')
    for good in PRICES:
        for bound in ('lower', 'upper'):
            result.append(f'   set_variable = {{ name = sed_investment_local_{good}_{bound} value = sed_investment_observed_price_{good}_{bound} }}')
    return '\n'.join(result) + '\n  }\n  sed_refresh_investment_wages = yes\n }\n}\n' + wage_effects()


def values(targets, variants):
    result = [price_values(), employment_values()]
    outputs = production_methods.ECONOMICS['all_outputs']
    for item in targets:
        good = item['good']
        suppliers = variants(item)
        for supplier in suppliers:
            building = supplier['building']
            name = building.removeprefix('building_')
            methods = outputs[building]
            output_goods = sorted({output for amounts in methods.values() for output in amounts})
            baseline = [group['method'] for group in production_methods.PROFILES[building]]
            baseline_outputs = {output: max(0, sum(methods.get(method, {}).get(output, 0) for method in baseline))
                                for output in output_goods}
            baseline_inputs = {input_good: sum(input_forecast.PROFILES[building].get(method, {}).get(input_good, 0)
                                               for method in baseline)
                               for input_good in input_forecast.building_goods(building)}
            for output in output_goods:
                result.append(f'sed_investment_{name}_output_{output} = {{\n value = 0')
                for method, amounts in methods.items():
                    if output in amounts:
                        result.append(f' if = {{ limit = {{ b:{building} = {{ has_active_production_method = {method} }} }} add = {amounts[output]:g} }}')
                result.append(' min = 0\n}')
            result.append(f'''sed_investment_{name}_margin = {{
 value = 0
 if = {{ limit = {{ NOT = {{ has_building = {building} }} }}
''')
            for output, amount in baseline_outputs.items():
                result.append(f'  add = {{ value = {amount:g} multiply = sed_investment_price_{output}_lower }}')
            for input_good, amount in baseline_inputs.items():
                result.append(f'  subtract = {{ value = {amount:g} multiply = sed_investment_price_{input_good}_upper }}')
            result.append(f''' }}
 if = {{ limit = {{ has_building = {building} }}
''')
            for output in output_goods:
                result.append(f'  add = {{ value = sed_investment_{name}_output_{output} multiply = sed_investment_price_{output}_lower }}')
            for input_good in input_forecast.building_goods(building):
                result.append(f'  subtract = {{ value = {input_forecast.amount_name(building, input_good)} multiply = sed_investment_price_{input_good}_upper }}')
            result.append(' }\n}')
            result.append(f'''sed_investment_{name}_output = {{
 value = 0
 if = {{ limit = {{ NOT = {{ has_building = {building} }} }} add = {baseline_outputs.get(good, 0):g} }}
 if = {{ limit = {{ has_building = {building} }} add = sed_investment_{name}_output_{good} }}
}}''')
            weighted_jobs = sum(EMPLOYMENT['buildings'][building][method]['weighted_jobs'] for method in baseline)
            result.append(f'''sed_investment_{name}_return = {{
 value = sed_investment_{name}_margin
 if = {{ limit = {{ has_variable = sed_investment_wage_known var:sed_investment_wage_known = 1 }}
  if = {{ limit = {{ NOT = {{ has_building = {building} }} }}
   subtract = {{ value = {max(0, weighted_jobs):g} multiply = var:sed_investment_wage_unit }}
  }}
  if = {{ limit = {{ has_building = {building} }}
   subtract = {{ value = sed_investment_{name}_weighted_jobs multiply = var:sed_investment_wage_unit }}
  }}
 }}
}}''')
        for field in ('margin', 'output', 'return'):
            result.append(f'sed_investment_{good}_{field} = {{\n value = 0')
            for supplier in suppliers:
                name = supplier['building'].removeprefix('building_')
                preferred = 'preferred_supplier' if len(suppliers) > 1 else 'investment_eligible'
                result.append(f' if = {{ limit = {{ sed_{good}_{name}_{preferred} = yes }} add = sed_investment_{name}_{field} }}')
            result.append('}')
    return '\n'.join(result) + '\n'
