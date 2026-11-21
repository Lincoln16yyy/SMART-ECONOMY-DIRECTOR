"""Compara previsões próprias com médias observadas após a contratação.

Lucro por nível não prova o retorno causal da expansão marginal. Só avalia
prédios sem subsídio após três meses da conclusão.
"""
VARIABLES = ['sed_perf_month', 'sed_perf_evaluated', 'sed_perf_loss_count', 'sed_perf_under_count']
FIELDS = ('quote', 'tracking', 'target', 'variant', 'expected', 'completed_month', 'known', 'actual', 'wages')


def state_variables(items):
    return [f'sed_perf_{i["good"]}_{f}' for i in items for f in FIELDS]


def capture(good):
    return f'''     if = {{ limit = {{ owner = {{ has_variable = sed_mode_automatic }} has_variable = sed_perf_{good}_quote }}
      set_variable = {{ name = sed_perf_{good}_tracking value = yes }}
      set_variable = {{ name = sed_perf_{good}_target value = {{ value = var:sed_{good}_intent_level add = 1 }} }}
      set_variable = {{ name = sed_perf_{good}_variant value = var:sed_{good}_intent_variant }}
      set_variable = {{ name = sed_perf_{good}_expected value = var:sed_perf_{good}_quote }}
      remove_variable = sed_perf_{good}_completed_month
      remove_variable = sed_perf_{good}_known
     }}
     remove_variable = sed_perf_{good}_quote'''


def effects(items, variants):
    parts = ['''sed_review_project_performance = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  sed_refresh_calendar = yes
  if = { limit = { NOT = { has_variable = sed_perf_month var:sed_perf_month = var:sed_calendar_month_key } }
   set_variable = { name = sed_perf_month value = var:sed_calendar_month_key }
   set_variable = { name = sed_perf_evaluated value = 0 }
   set_variable = { name = sed_perf_loss_count value = 0 }
   set_variable = { name = sed_perf_under_count value = 0 }
   every_scope_state = {
''']
    for item in items:
        g = item['good']; pre = f'sed_perf_{g}_'
        parts.append(f'    if = {{ limit = {{ has_variable = {pre}tracking has_variable = {pre}variant has_variable = {pre}target }}')
        for index, v in enumerate(variants(item), 1):
            b = v['building']
            parts.append(f'''     {'if' if index==1 else 'else_if'} = {{ limit = {{ var:{pre}variant = {index} }}
      if = {{ limit = {{ has_building = {b} b:{b}.level >= var:{pre}target }}
       if = {{ limit = {{ NOT = {{ has_variable = {pre}completed_month }} }}
        set_variable = {{ name = {pre}completed_month value = owner.var:sed_calendar_month_key }}
       }}
       # Do not treat an unstaffed or subsidized building as a measured return.
       if = {{ limit = {{
        owner.var:sed_calendar_month_key >= {{ value = var:{pre}completed_month add = 3 }}
        b:{b} = {{ level > 0 occupancy >= 0.8 has_failed_hires = no
         building_has_goods_shortage = no is_subsidized = no earnings >= weekly_profit }}
       }}
        set_variable = {{ name = {pre}known value = yes }}
        set_variable = {{ name = {pre}actual value = {{ value = b:{b}.weekly_profit divide = b:{b}.level }} }}
        set_variable = {{ name = {pre}wages value = {{ value = b:{b}.earnings
         subtract = b:{b}.weekly_profit divide = b:{b}.level min = 0 }} }}
        owner = {{ change_variable = {{ name = sed_perf_evaluated add = 1 }} }}
        if = {{ limit = {{ var:{pre}actual < 0 }}
         owner = {{ change_variable = {{ name = sed_perf_loss_count add = 1 }} }}
        }}
        else_if = {{ limit = {{ has_variable = {pre}expected var:{pre}expected > 0
         var:{pre}actual < {{ value = var:{pre}expected multiply = 0.5 }} }}
         owner = {{ change_variable = {{ name = sed_perf_under_count add = 1 }} }}
        }}
       }}
       else = {{ remove_variable = {pre}known }}
      }}
      else_if = {{ limit = {{ owner = {{ construction_queue_num_queued_government_levels = 0 }} }}
       remove_variable = {pre}tracking
       remove_variable = {pre}known
      }}
     }}''')
        parts.append('    }')
    parts.append('   }\n  }\n }\n}\n')
    return '\n'.join(parts)


def triggers(items):
    return '\n'.join(f'''sed_perf_{i['good']}_blocked = {{
 has_variable = sed_perf_{i['good']}_known
 has_variable = sed_perf_{i['good']}_actual var:sed_perf_{i['good']}_actual < 0
}}''' for i in items)+'\n'


def values(items):
    return '\n'.join(f'''sed_perf_{i['good']}_factor = {{ value = 1
 if = {{ limit = {{ has_variable = sed_perf_{i['good']}_known
  has_variable = sed_perf_{i['good']}_expected var:sed_perf_{i['good']}_expected > 0
  has_variable = sed_perf_{i['good']}_actual
  var:sed_perf_{i['good']}_actual < {{ value = var:sed_perf_{i['good']}_expected multiply = 0.5 }}
 }} subtract = 0.5 }}
}}''' for i in items)+'\n'
