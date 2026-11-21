"""Conservative public-building operating reference using catalogued inputs/payroll."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
PROFILES = json.loads((DATA / 'public_upkeep.json').read_text())
VARIABLES = [f'sed_upkeep_{name}_{field}' for name in PROFILES
             for field in ('cost', 'known', 'materials', 'jobs')]


def effects():
    parts = ['sed_refresh_public_upkeep = {']
    for name, data in PROFILES.items():
        building = data['building']
        # Each group uses the highest technology-available reference, rather than
        # charging a starting country for end-game methods it cannot use.
        for field in ('materials', 'jobs'):
            parts.append(f' set_variable = {{ name = sed_upkeep_{name}_{field} value = {{ value = 0')
            for group in data['groups']:
                parts.append('  add = { value = 0')
                for method, spec in group.items():
                    amount = spec['materials' if field == 'materials' else 'weighted_jobs']
                    tech = ' '.join('has_technology_researched = ' + t for t in spec['technologies'])
                    parts.append(f'   min = {{ value = 0 if = {{ limit = {{ {tech} }} add = {amount:g} }} }}')
                parts.append('  }')
            parts.append(' } }')
        parts.append(f''' set_variable = {{ name = sed_upkeep_{name}_known value = 0 }}
 set_variable = {{ name = sed_upkeep_{name}_cost value = var:sed_upkeep_{name}_materials }}
 if = {{ limit = {{ has_variable = sed_investment_wage_known var:sed_investment_wage_known = 1 }}
  change_variable = {{ name = sed_upkeep_{name}_cost add = {{
   value = var:sed_investment_wage_unit multiply = var:sed_upkeep_{name}_jobs multiply = 1.25
  }} }}
  set_variable = {{ name = sed_upkeep_{name}_known value = 1 }}
 }}
 every_scope_state = {{
  limit = {{ has_building = {building} b:{building} = {{ level > 0 occupancy >= 0.5 earnings >= weekly_profit }} }}
  owner = {{
   set_variable = {{ name = sed_upkeep_{name}_cost value = {{
    value = var:sed_upkeep_{name}_cost
    min = {{ value = prev.b:{building}.earnings subtract = prev.b:{building}.weekly_profit
     divide = prev.b:{building}.level divide = prev.b:{building}.occupancy
     multiply = 1.25 add = var:sed_upkeep_{name}_materials }}
   }} }}
   set_variable = {{ name = sed_upkeep_{name}_known value = 1 }}
  }}
 }}
''')
    return '\n'.join(parts) + '\n}\n'


def triggers():
    return '\n'.join(f'''sed_upkeep_{name}_safe = {{
 OR = {{
  AND = {{ has_variable = sed_upkeep_{name}_known var:sed_upkeep_{name}_known = 1
   net_total_income >= var:sed_upkeep_{name}_cost }}
  AND = {{ NOT = {{ has_variable = sed_upkeep_{name}_known var:sed_upkeep_{name}_known = 1 }}
   net_total_income > 0 principal <= 0
   gold_reserves >= {{ value = sed_fixed_expenses_value multiply = 12 }} }}
 }}
}}
''' for name in PROFILES)
