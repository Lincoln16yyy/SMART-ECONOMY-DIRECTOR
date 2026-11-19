"""Follow confirmed Director projects until staffing and inputs recover."""

COUNTRY_VARIABLES = ['sed_follow_staff', 'sed_follow_inputs']
STATE_VARIABLES = ['sed_follow_' + good for good in ('wood', 'iron', 'tools')]


def effects():
    targets = (('wood', 'building_logging_camp'), ('iron', 'building_iron_mine'),
               ('tools', 'building_tooling_workshop'))
    parts = ['''sed_follow_projects = {
 set_variable = { name = sed_follow_staff value = 0 }
 set_variable = { name = sed_follow_inputs value = 0 }
 every_scope_state = {
''']
    for good, building in targets:
        parts.append(f'''  if = {{ limit = {{
   has_variable = sed_{good}_intent_level has_building = {building}
   b:{building}.level > var:sed_{good}_intent_level
  }}
   set_variable = {{ name = sed_follow_{good} value = yes }}
  }}
  if = {{ limit = {{ has_variable = sed_follow_{good} }}
   if = {{ limit = {{ NOT = {{ has_building = {building} }} }}
    remove_variable = sed_follow_{good}
   }}
   else_if = {{ limit = {{ b:{building} = {{
    occupancy >= 0.8 has_failed_hires = no building_has_goods_shortage = no
   }} }}
    remove_variable = sed_follow_{good}
   }}
   else = {{
    if = {{ limit = {{ b:{building} = {{ OR = {{ occupancy < 0.8 has_failed_hires = yes }} }} }}
     root = {{ change_variable = {{ name = sed_follow_staff add = 1 }} }}
    }}
    if = {{ limit = {{ b:{building} = {{ building_has_goods_shortage = yes }} }}
     root = {{ change_variable = {{ name = sed_follow_inputs add = 1 }} }}
    }}
   }}
  }}
''')
    parts.append(' }\n}\n')
    return ''.join(parts)
