"""Observe levels between reviews; builder identity is not available in script."""

import json
from pathlib import Path

OUTPUTS = json.loads((Path(__file__).resolve().parents[1] / 'data/outcome_goods.json').read_text())
LEGACY_KEYS = {
    'building_logging_camp': 'wood', 'building_iron_mine': 'iron',
    'building_tooling_workshop': 'tools', 'building_paper_mill': 'paper',
    'building_food_industry': 'food', 'building_textile_mill': 'clothes',
}
TARGETS = {LEGACY_KEYS.get(building, building.removeprefix('building_')): (building, goods)
           for building, goods in OUTPUTS.items()}
INPUTS = json.loads((Path(__file__).resolve().parents[1] / 'data/outcome_inputs.json').read_text())
INPUT_GOODS = sorted({good for inputs in INPUTS.values() for good in inputs if good not in {'electricity', 'transportation', 'services'}})
COUNTRY_VARIABLES = ['sed_problem_state', 'sed_problem_type', 'sed_problem_good', 'sed_outcome_hiring','sed_outcome_staff', 'sed_outcome_inputs', 'sed_outcome_market',
                     'sed_outcome_observed', 'sed_outcome_month', 'sed_outcome_workers']
STATE_VARIABLES = [f'sed_outcome_{name}_{field}' for name in TARGETS
                   for field in ('level', 'pending', 'since')]


def effects():
    parts = ['''sed_outcome_review = {
 sed_refresh_calendar = yes
 if = { limit = {
  NOT = { has_variable = sed_outcome_month var:sed_outcome_month = var:sed_calendar_month_key }
 }
  set_variable = { name = sed_outcome_month value = var:sed_calendar_month_key }
  set_variable = { name = sed_outcome_staff value = 0 }
  set_variable = { name = sed_outcome_inputs value = 0 }
  set_variable = { name = sed_outcome_market value = 0 }
  set_variable = { name = sed_outcome_observed value = 0 }
  set_variable = { name = sed_outcome_workers value = 0 }
  remove_variable = sed_problem_state
  remove_variable = sed_problem_type
  remove_variable = sed_problem_good
  set_variable = { name = sed_outcome_hiring value = 0 }
  every_scope_state = {
''']
    for index, (name, (building, goods)) in enumerate(TARGETS.items(), 1):
        market_conditions = ' '.join(
            f'AND = {{ b:{building} = {{ OR = {{ ' +
            ' '.join(f'has_active_production_method = {method}' for method in methods) +
            f' }} }} owner = {{ market = {{ mg:{good} ?= {{ market_goods_sell_orders > market_goods_buy_orders market_goods_cheaper = yes }} }} }} }}'
            for good, methods in goods.items() if good not in {'electricity', 'transportation', 'services'})
        market_conditions = f'OR = {{ {market_conditions} }}' if market_conditions else 'always = no'
        level = f'sed_outcome_{name}_level'
        pending = f'sed_outcome_{name}_pending'
        since = f'sed_outcome_{name}_since'
        missing = []
        for good, methods in INPUTS[building].items():
            if good not in INPUT_GOODS:
                continue
            active = ' '.join(f'has_active_production_method = {method}' for method in methods)
            missing.append(f'''     if = {{ limit = {{
      owner = {{ NOT = {{ has_variable = sed_problem_good }} market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} }}
      b:{building} = {{ OR = {{ {active} }} }}
     }}
      root = {{ set_variable = {{ name = sed_problem_good value = {INPUT_GOODS.index(good) + 1} }} }}
     }}''')

        parts.append(f'''   if = {{ limit = {{ has_building = {building} }}
    if = {{ limit = {{ has_variable = {level} b:{building}.level > var:{level} }}
     set_variable = {{ name = {pending} value = yes }}
     set_variable = {{ name = {since} value = owner.var:sed_calendar_month_key }}
    }}
    set_variable = {{ name = {level} value = b:{building}.level }}
    if = {{ limit = {{ has_variable = {pending} }}
     if = {{ limit = {{ NOT = {{ has_variable = {since} }} }}
      set_variable = {{ name = {since} value = owner.var:sed_calendar_month_key }}
     }}
     root = {{ change_variable = {{ name = sed_outcome_observed add = 1 }} }}
     if = {{ limit = {{ b:{building} = {{ OR = {{ occupancy < 0.8 has_failed_hires = yes }} }} }}
      root = {{ change_variable = {{ name = sed_outcome_hiring add = 1 }} }}
      if = {{ limit = {{ owner.var:sed_calendar_month_key >= {{ value = var:{since} add = 3 }} }}
       root = {{ change_variable = {{ name = sed_outcome_staff add = 1 }} }}
       if = {{ limit = {{ sed_state_labor_available < 1000 }}
        root = {{ change_variable = {{ name = sed_outcome_workers add = 1 }} }}
       }}
      }}
     }}
     if = {{ limit = {{ b:{building} = {{ building_has_goods_shortage = yes }} }}
      root = {{ change_variable = {{ name = sed_outcome_inputs add = 1 }} }}
     }}
     if = {{ limit = {{
      owner = {{ NOT = {{ has_variable = sed_problem_type }} }}
      b:{building} = {{ OR = {{ occupancy < 0.8 has_failed_hires = yes building_has_goods_shortage = yes }} }}
     }}
      root = {{
       set_variable = {{ name = sed_problem_state value = prev }}
       set_variable = {{ name = sed_problem_type value = {index} }}
      }}
{chr(10).join(missing)}
     }}
     if = {{ limit = {{ {market_conditions} }}
      root = {{ change_variable = {{ name = sed_outcome_market add = 1 }} }}
     }}
     else_if = {{ limit = {{ b:{building} = {{
      occupancy >= 0.8 has_failed_hires = no building_has_goods_shortage = no
     }} }}
      remove_variable = {pending}
     }}
    }}
   }}
   else = {{
    set_variable = {{ name = {level} value = 0 }}
    remove_variable = {pending}
   }}
''')
    return ''.join(parts) + '  }\n }\n}\n'


def triggers():
    return '''sed_outcome_growth_wait = {
 has_variable = sed_plan_goal var:sed_plan_goal = 8
 OR = {
  AND = { has_variable = sed_outcome_staff var:sed_outcome_staff > 0 }
  AND = { has_variable = sed_outcome_inputs var:sed_outcome_inputs > 0 }
  AND = { has_variable = sed_outcome_market var:sed_outcome_market > 0 }
 }
}
'''


def localization(value):
    return {
        'sed_outcome_summary': (
            'Expansões acompanhadas nos setores catalogados: ' +
            value('outcome_observed', '0') + '. Contratação limitada após três meses: ' + value('outcome_staff', '0') +
            '; falta de insumos: ' + value('outcome_inputs', '0') + '; oferta excedente e preço baixo: ' +
            value('outcome_market', '0') + '; pouca mão de obra disponível: ' + value('outcome_workers', '0') + '. O nível observado pode incluir obras de qualquer construtor.',
            'Expansions tracked across catalogued sectors: ' +
            value('outcome_observed', '0') + '. Staffing constrained after three months: ' + value('outcome_staff', '0') +
            '; input shortages: ' + value('outcome_inputs', '0') + '; excess supply and low price: ' +
            value('outcome_market', '0') + '; low available labor: ' + value('outcome_workers', '0') + '. Observed levels can come from any builder.'),
        'sed_outcome_labor': (
            'Há expansões com contratação limitada e pouca mão de obra estimada. A coordenação habilitou a automação de trabalhadores do Economy Advisor, sujeita aos filtros dele. Confira o resultado no painel de métodos.',
            'Some expansions have staffing problems and low estimated labor. Coordination enabled the Economy Advisor labor automation under its own filters. Check the production-method panel for the result.'),
        'sed_outcome_wait': (
            'A diversificação do Advisor aguarda recuperação das expansões recentes. Confira contratação, insumos e compradores. Prioridades econômicas urgentes continuam avaliadas.',
            'Advisor diversification waits for recent expansions to recover. Review staffing, inputs and buyers. Urgent economic priorities remain under review.'),
    }
