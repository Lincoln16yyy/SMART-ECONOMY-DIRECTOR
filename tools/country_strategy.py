"""Preferências limitadas por porte, trabalhadores e fornecedores observados."""
try:
    from . import input_forecast, investment_outcomes, labor, planning
except ImportError:
    import input_forecast, investment_outcomes, labor, planning


LOCAL = input_forecast.LOCAL_GOODS


def triggers(items, variants):
    parts = []
    for item in items:
        good = item['good']
        if good in planning.MILITARY_INDUSTRY_GOODS: continue
        for variant in variants(item):
            b = variant['building']; name = b.removeprefix('building_')
            checks, used = [], []
            for g in input_forecast.building_goods(b):
                amount = input_forecast.amount_name(b,g)
                startup = input_forecast.amount_name(b,g,founding=True)
                unused = f'OR = {{ AND = {{ has_building = {b} {amount} <= 0 }} AND = {{ NOT = {{ has_building = {b} }} {startup} <= 0 }} }}'
                used.append(f'NOT = {{ {unused} }}')
                producers = []
                for producer, outputs in investment_outcomes.OUTPUTS.items():
                    methods = outputs.get(g, [])
                    if not methods: continue
                    active = ' '.join('has_active_production_method = '+m for m in methods)
                    producers.append(f'AND = {{ has_building = {producer} b:{producer} = {{ level > 0 occupancy >= 0.8 building_has_goods_shortage = no OR = {{ {active} }} }} }}')
                supply = 'OR = { '+' '.join(producers)+' }' if producers else 'always = no'
                # Local electricity/transport require a producer in this state.
                if g not in LOCAL: supply = f'owner = {{ any_scope_state = {{ {supply} }} }}'
                checks.append(f' OR = {{ {unused} {supply} }}')
            parts.append(f'sed_strategy_{name}_domestic_inputs = {{\n OR = {{ '+ ' '.join(used or ['always = no'])+' }\n'+'\n'.join(checks)+'\n}\n')
    return ''.join(parts)


def values(items, variants, costs):
    parts = []
    for item in items:
        good = item['good']
        if good in planning.MILITARY_INDUSTRY_GOODS: continue
        vs = variants(item)
        # Use the same preferred supplier as approval and the return estimate.
        supported, labor_ready = [], []
        for v in vs:
            name=v['building'].removeprefix('building_')
            gate=f'sed_{good}_{name}_preferred_supplier' if len(vs)>1 else f'sed_{good}_{name}_investment_eligible'
            supported.append(f'AND = {{ {gate} = yes sed_strategy_{name}_domestic_inputs = yes }}')
            labor_ready.append(f'AND = {{ {gate} = yes sed_state_labor_available >= {labor.REQUIREMENTS[v["building"]]*2:g} }}')
        small_bonus = ''' if = { limit = { owner = { total_population <= 1000000 } } add = 0.2 }''' if costs[good]<=400 else ''
        industry_bonus = f''' if = {{ limit = {{ OR = {{ {' '.join(labor_ready)} }} }} add = 0.15 }}''' if costs[good]>=600 else ''
        living_bonus = ''' if = { limit = { owner = { OR = { average_sol < 10 sed_coord_advisor_sol_pressure = yes } } } add = 0.2 }''' if good in ('grain','groceries','clothes') else ''
        parts.append(f'''sed_strategy_{good}_factor = {{ value = 1
{small_bonus}
{industry_bonus}
{living_bonus}
 if = {{ limit = {{ OR = {{ {' '.join(supported)} }} }} add = 0.2 }}
 # Déficit de oferta do mercado não é uma medida de importação do país.
 add = {{ value = 0 owner = {{ market = {{ mg:{good} ?= {{
  if = {{ limit = {{ market_goods_buy_orders > 0 }}
   add = {{ value = market_goods_buy_orders subtract = market_goods_sell_orders
    divide = market_goods_buy_orders min = 0 max = 1 multiply = 0.2 }}
  }}
 }} }} }} }}
 min = 1 max = 1.75
}}
''')
    return ''.join(parts)
