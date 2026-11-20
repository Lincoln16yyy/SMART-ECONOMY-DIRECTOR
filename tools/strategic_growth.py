"""Civilian investment across the verified supply catalog; no external mutations."""
try:
    from . import planning
except ImportError:
    import planning


def targets(items):
    return [item for item in items if item['good'] not in planning.MILITARY_INDUSTRY_GOODS]


def triggers(items):
    parts = ['''sed_growth_ready = {
 is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
 NOT = { has_variable = sed_mode_manual } NOT = { has_variable = sed_mode_assisted }
 NOT = { in_default = yes } sed_direct_fiscal_safe = yes
 construction_queue_num_queued_government_levels = 0
 construction_queue_government_duration <= 0
 has_variable = sed_plan_count var:sed_plan_count = 0
 construction_queue_num_queued_private_levels = 0 is_construction_paused = no
 NOT = { sed_outcome_growth_wait = yes }
 OR = { NOT = { has_variable = sed_plan_waiting } var:sed_plan_waiting = 0 }
}
sed_growth_takeover = {
 sed_growth_ready = yes
 OR = {
  NOT = { has_variable = sed_coord_advisor_known }
  AND = { has_variable = sed_watch_idle var:sed_watch_idle >= 2 }
  AND = { has_variable = advisor_auto_construction_status var:advisor_auto_construction_status = 4 }
 }
 any_scope_state = { sed_growth_site = yes }
}
''']
    goods = []
    for item in targets(items):
        good = item['good']; goods.append(good)
        parts.append(f'''sed_growth_{good}_candidate = {{
 owner = {{ sed_growth_ready = yes
  market = {{ mg:{good} ?= {{ market_goods_buy_orders > 0
   NOT = {{ market_goods_cheaper > 0 }} }} }}
 }}
 sed_{good}_candidate_site = yes
 sed_{good}_supplier_available = yes
 NOT = {{ has_variable = sed_follow_{good} }}
 sed_investment_{good}_output > 0
 sed_investment_{good}_return > 0
 # Do not found an entire level for a negligible market.
 sed_growth_{good}_demand >= {{ value = sed_investment_{good}_output multiply = 0.5 }}
}}
''')
    parts.append('sed_growth_site = { OR = { ' + ' '.join(f'sed_growth_{g}_candidate = yes' for g in goods) + ' } }\n')
    return '\n' + ''.join(parts)


def values(items, costs):
    parts = []
    for item in targets(items):
        good = item['good']
        parts.append(f'''sed_growth_{good}_demand = {{ value = 0
 owner = {{ market = {{ mg:{good} ?= {{ add = market_goods_buy_orders }} }} }}
}}
sed_growth_{good}_score = {{ value = 0
 if = {{ limit = {{ sed_growth_{good}_candidate = yes }}
  add = {{ value = sed_investment_{good}_return divide = {costs[good]} multiply = 100 }}
  # Diversifying into the first national producer breaks ties toward new industry.
  if = {{ limit = {{ sed_{good}_found_site = yes }}
   add = {{ value = sed_investment_{good}_return divide = {costs[good]} multiply = 50 }}
  }}
  add = {{ value = sed_site_readiness multiply = 0.000001 }}
 }}
}}
''')
    parts.append('sed_growth_best_score = { value = 0\n' + ''.join(
        f' min = sed_growth_{i["good"]}_score\n' for i in targets(items)) + '}\n')
    return ''.join(parts)


def branch(items):
    body = []
    for index, item in enumerate(targets(items)):
        good = item['good']
        body.append(f'''   {'if' if index == 0 else 'else_if'} = {{ limit = {{
    sed_growth_{good}_candidate = yes sed_growth_{good}_score >= sed_growth_best_score
   }} sed_run_{good}_approval = yes }}''')
    return '''  else_if = { limit = { any_scope_state = { sed_growth_site = yes } }
   ordered_scope_state = {
    limit = { sed_growth_site = yes }
    order_by = sed_growth_best_score max = 1 check_range_bounds = no
''' + '\n'.join(body) + '\n   }\n  }\n'
