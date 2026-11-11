"""Per-level material references for supply investments in the existing catalog."""
try:
    from . import input_forecast, production_methods
except ImportError:
    import input_forecast
    import production_methods


def values(targets, variants):
    result = []
    prices = production_methods.ECONOMICS['prices']
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
            baseline_margin = (sum(amount * prices[output] * 0.75 for output, amount in baseline_outputs.items())
                               - sum(amount * prices[input_good] * 1.25 for input_good, amount in baseline_inputs.items()))
            for output in output_goods:
                result.append(f'sed_investment_{name}_output_{output} = {{\n value = 0')
                for method, amounts in methods.items():
                    if output in amounts:
                        result.append(f' if = {{ limit = {{ b:{building} = {{ has_active_production_method = {method} }} }} add = {amounts[output]:g} }}')
                result.append(' min = 0\n}')
            result.append(f'''sed_investment_{name}_margin = {{
 value = 0
 if = {{ limit = {{ NOT = {{ has_building = {building} }} }} add = {baseline_margin:g} }}
 if = {{ limit = {{ has_building = {building} }}
''')
            for output in output_goods:
                result.append(f'  add = {{ value = sed_investment_{name}_output_{output} multiply = {prices[output] * 0.75:g} }}')
            for input_good in input_forecast.building_goods(building):
                result.append(f'  subtract = {{ value = {input_forecast.amount_name(building, input_good)} multiply = {prices[input_good] * 1.25:g} }}')
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
