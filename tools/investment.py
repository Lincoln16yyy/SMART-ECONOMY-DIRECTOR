"""Per-level material references for supply investments in the existing catalog."""
try:
    from . import input_forecast, production_methods
except ImportError:
    import input_forecast
    import production_methods

PRICES = production_methods.ECONOMICS['prices']
COUNTRY_VARIABLES = [f'sed_investment_market_{good}_{bound}' for good in PRICES
                     for bound in ('lower', 'upper')]
STATE_VARIABLES = [f'sed_investment_local_{good}_{bound}' for good in PRICES
                   for bound in ('lower', 'upper')]


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
    return '\n'.join(result) + '\n  }\n }\n}\n'


def values(targets, variants):
    result = [price_values()]
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
        for field in ('margin', 'output'):
            result.append(f'sed_investment_{good}_{field} = {{\n value = 0')
            for supplier in suppliers:
                name = supplier['building'].removeprefix('building_')
                preferred = 'preferred_supplier' if len(suppliers) > 1 else 'investment_eligible'
                result.append(f' if = {{ limit = {{ sed_{good}_{name}_{preferred} = yes }} add = sed_investment_{name}_{field} }}')
            result.append('}')
    return '\n'.join(result) + '\n'
