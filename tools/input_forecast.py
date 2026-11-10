"""Project full-level input demand from verified active vanilla methods.

Current supply is held fixed and queued output is not credited. A 25% demand
stress covers part of the uncertainty, without modeling prices, trade changes,
throughput modifiers or future production-method changes.
"""
import json
from pathlib import Path

PROFILES = json.loads((Path(__file__).resolve().parents[1] / 'data/input_profiles.json').read_text())
LOCAL_GOODS = {'electricity', 'transportation', 'services'}
GOODS = sorted({good for methods in PROFILES.values() for goods in methods.values() for good in goods})
LABELS_PT = {
    'coal': 'carvão', 'copper': 'cobre', 'dye': 'corantes', 'electricity': 'eletricidade',
    'engines': 'motores', 'explosives': 'explosivos', 'fabric': 'tecido',
    'fertilizer': 'fertilizante', 'fish': 'peixe', 'glass': 'vidro', 'grain': 'cereais',
    'hardwood': 'madeira de lei', 'iron': 'ferro', 'lead': 'chumbo', 'meat': 'carne',
    'oil': 'petróleo', 'rubber': 'borracha', 'silk': 'seda', 'steel': 'aço',
    'sugar': 'açúcar', 'tools': 'ferramentas', 'transportation': 'transporte', 'wood': 'madeira',
}
MARKET_GOODS = [good for good in GOODS if good not in LOCAL_GOODS]
COUNTRY_VARIABLES = ['sed_input_market_margin_' + good for good in MARKET_GOODS]
STATE_VARIABLES = ['sed_input_local_margin_' + good for good in sorted(LOCAL_GOODS & set(GOODS))]


def amount_name(building, good):
    return 'sed_input_' + building.removeprefix('building_') + '_' + good


def building_goods(building):
    return sorted({good for inputs in PROFILES[building].values() for good in inputs})


def values():
    result = []
    for building, methods in PROFILES.items():
        for good in building_goods(building):
            result.append(f'{amount_name(building, good)} = {{\n value = 0')
            for method, inputs in methods.items():
                if good in inputs:
                    result.append(f' if = {{ limit = {{ b:{building} = {{ has_active_production_method = {method} }} }} add = {inputs[good]} }}')
            result.append(' min = 0\n}')
    for good in GOODS:
        result.append(f'sed_input_pending_{good} = {{\n value = 0')
        for building in PROFILES:
            if good in building_goods(building):
                result.append(f''' if = {{ limit = {{ has_building = {building} }}
  add = {{ value = {amount_name(building, good)}
   multiply = {{ value = b:{building}.level_after_queued_constructions
    subtract = {{ value = b:{building}.level multiply = {{ value = b:{building}.occupancy min = 0 max = 1 }} }}
    min = 0
   }}
   multiply = 1.25
  }}
 }}''')
        result.append('}')
        if good in LOCAL_GOODS:
            result.append(f'''sed_input_local_headroom_{good} = {{
 value = 0
 sg:{good} ?= {{ add = {{ value = state_goods_production min = 0 multiply = 2 subtract = {{ value = state_goods_consumption min = 0 }} }} }}
 subtract = sed_input_pending_{good}
}}
sed_input_headroom_{good} = {{
 value = 0
 if = {{ limit = {{ has_variable = sed_input_local_margin_{good} }} add = var:sed_input_local_margin_{good} }}
 if = {{ limit = {{ NOT = {{ has_variable = sed_input_local_margin_{good} }} }} add = sed_input_local_headroom_{good} }}
}}''')
        else:
            result.append(f'''sed_input_country_headroom_{good} = {{
 value = 0
 market ?= {{ mg:{good} ?= {{ add = {{ value = market_goods_sell_orders min = 0 multiply = 2 subtract = {{ value = market_goods_buy_orders min = 0 }} }} }} }}
 subtract = {{ value = 0 every_scope_state = {{ limit = {{ }} add = sed_input_pending_{good} }} }}
}}
sed_input_headroom_{good} = {{ value = owner.var:sed_input_market_margin_{good} }}''')
    return '\n'.join(result) + '\n'


def blocked_input(building, good):
    amount = amount_name(building, good)
    return f""" {amount} > 0
     sed_input_headroom_{good} < {{ value = {amount} multiply = 1.25 }}"""


def triggers():
    result = []
    for building in PROFILES:
        name = building.removeprefix('building_')
        result.append(f'sed_input_{name}_safe = {{')
        for good in building_goods(building):
            result.append(f''' NOT = {{
 {blocked_input(building, good)}
 }}''')
        result.append('}')
    return '\n'.join(result) + '\n'


def effects():
    result = ['sed_refresh_input_readings = {\n if = { limit = { is_player = yes has_variable = sed_enabled }']
    for good in MARKET_GOODS:
        result.append(f'  set_variable = {{ name = sed_input_market_margin_{good} value = sed_input_country_headroom_{good} }}')
    result.append('  every_scope_state = {')
    for good in sorted(LOCAL_GOODS & set(GOODS)):
        result.append(f'   set_variable = {{ name = sed_input_local_margin_{good} value = sed_input_local_headroom_{good} }}')
    result.append('  }\n  sed_refresh_input_priorities = yes\n }\n}\n')
    return '\n'.join(result)
