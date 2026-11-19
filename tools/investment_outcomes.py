"""Observe levels between reviews; builder identity is not available in script."""

TARGETS = {
    'wood': ('building_logging_camp', 'wood'),
    'iron': ('building_iron_mine', 'iron'),
    'tools': ('building_tooling_workshop', 'tools'),
    'paper': ('building_paper_mill', 'paper'),
    'food': ('building_food_industry', 'groceries'),
    'clothes': ('building_textile_mill', 'clothes'),
}
COUNTRY_VARIABLES = ['sed_outcome_staff', 'sed_outcome_inputs', 'sed_outcome_market',
                     'sed_outcome_observed', 'sed_outcome_month']
STATE_VARIABLES = [f'sed_outcome_{name}_{field}' for name in TARGETS
                   for field in ('level', 'pending')]


def effects():
    parts = ['''sed_outcome_review = {
 if = { limit = {
  NOT = { has_variable = sed_outcome_month var:sed_outcome_month = sed_live_month_key }
 }
  set_variable = { name = sed_outcome_month value = sed_live_month_key }
  set_variable = { name = sed_outcome_staff value = 0 }
  set_variable = { name = sed_outcome_inputs value = 0 }
  set_variable = { name = sed_outcome_market value = 0 }
  set_variable = { name = sed_outcome_observed value = 0 }
  every_scope_state = {
''']
    for name, (building, good) in TARGETS.items():
        level = f'sed_outcome_{name}_level'
        pending = f'sed_outcome_{name}_pending'
        parts.append(f'''   if = {{ limit = {{ has_building = {building} }}
    if = {{ limit = {{ has_variable = {level} b:{building}.level > var:{level} }}
     set_variable = {{ name = {pending} value = yes }}
    }}
    set_variable = {{ name = {level} value = b:{building}.level }}
    if = {{ limit = {{ has_variable = {pending} }}
     root = {{ change_variable = {{ name = sed_outcome_observed add = 1 }} }}
     if = {{ limit = {{ b:{building} = {{ OR = {{ occupancy < 0.8 has_failed_hires = yes }} }} }}
      root = {{ change_variable = {{ name = sed_outcome_staff add = 1 }} }}
     }}
     if = {{ limit = {{ b:{building} = {{ building_has_goods_shortage = yes }} }}
      root = {{ change_variable = {{ name = sed_outcome_inputs add = 1 }} }}
     }}
     if = {{ limit = {{ owner = {{ market = {{ mg:{good} ?= {{
      market_goods_sell_orders > market_goods_buy_orders market_goods_cheaper = yes
     }} }} }} }}
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
            'Expansões observadas desde a revisão anterior (madeira, ferro, ferramentas, papel, alimentos e roupas): ' +
            value('outcome_observed', '0') + '. Contratação limitada: ' + value('outcome_staff', '0') +
            '; falta de insumos: ' + value('outcome_inputs', '0') + '; oferta excedente e preço baixo: ' +
            value('outcome_market', '0') + '. O nível observado pode incluir obras de qualquer construtor.',
            'Observed expansions since the previous review (wood, iron, tools, paper, food and clothes): ' +
            value('outcome_observed', '0') + '. Staffing constrained: ' + value('outcome_staff', '0') +
            '; input shortages: ' + value('outcome_inputs', '0') + '; excess supply and low price: ' +
            value('outcome_market', '0') + '. Observed levels can come from any builder.'),
        'sed_outcome_wait': (
            'A diversificação do Advisor aguarda recuperação das expansões recentes. Confira contratação, insumos e compradores. Prioridades econômicas urgentes continuam avaliadas.',
            'Advisor diversification waits for recent expansions to recover. Review staffing, inputs and buyers. Urgent economic priorities remain under review.'),
    }
