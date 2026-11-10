"""Build the diagnostics and approved-action prototype. Game files use UTF-8 BOM."""

import argparse
import json
from pathlib import Path

try:
    from . import planning, coordination, construction_budget
except ImportError:
    import planning, coordination, construction_budget

ROOT = Path(__file__).resolve().parents[1]
METRICS = json.loads((ROOT / 'data/metrics.json').read_text())
VERSION = '0.6.18'
# Observed country options; this registry also drives the live explanation.
COMPETING_BUILDERS = (
    ('advisor', 'advisor_auto_construction_enabled', 'Economy Advisor: construção automática', 'Economy Advisor: automatic construction'),
    ('chains', 'zw_var_expand_building', 'Supply Chain: cadeias produtivas', 'Supply Chain: production chains'),
    ('sectors', 'zw_var_more_construction_sectors', 'Supply Chain: setores de construção', 'Supply Chain: construction sectors'),
    ('railways', 'zw_var_scsab_construct_railway', 'Supply Chain: ferrovias', 'Supply Chain: railways'),
    ('power', 'zw_var_scsab_construct_power_plant', 'Supply Chain: energia', 'Supply Chain: power plants'),
    ('admin', 'zw_var_scsab_gov_admin', 'Supply Chain: administração geral', 'Supply Chain: general administration'),
    ('tax', 'zw_var_scsab_gov_admin_for_tax', 'Supply Chain: administração tributária', 'Supply Chain: tax administration'),
    ('aroai', 'aroai_autobuild', 'ARoAI: construção automática', 'ARoAI: automatic construction'),
)
SUPPLY_TARGETS = [
    {'good': 'wood', 'building': 'building_logging_camp', 'methods': ['pm_electric_saw_mills', 'pm_saw_mills', 'pm_simple_forestry'], 'label_pt': 'madeira', 'label_en': 'wood', 'building_pt': 'acampamento madeireiro', 'building_en': 'logging camp'},
    {'good': 'iron', 'building': 'building_iron_mine', 'methods': ['pm_atmospheric_engine_pump_building_iron_mine', 'pm_condensing_engine_pump_building_iron_mine', 'pm_diesel_pump_building_iron_mine', 'pm_dynamite_building_iron_mine', 'pm_nitroglycerin_building_iron_mine', 'pm_picks_and_shovels_building_iron_mine'], 'label_pt': 'ferro', 'label_en': 'iron', 'building_pt': 'mina de ferro', 'building_en': 'iron mine'},
    {'good': 'coal', 'building': 'building_coal_mine', 'methods': ['pm_atmospheric_engine_pump_building_coal_mine', 'pm_condensing_engine_pump_building_coal_mine', 'pm_diesel_pump_building_coal_mine', 'pm_dynamite_building_coal_mine', 'pm_nitroglycerin_building_coal_mine', 'pm_picks_and_shovels_building_coal_mine'], 'label_pt': 'carvão', 'label_en': 'coal', 'building_pt': 'mina de carvão', 'building_en': 'coal mine'},
    {'good': 'grain', 'building': 'building_wheat_farm', 'methods': ['pm_chemical_fertilizer', 'pm_fertilization', 'pm_herring_meal_farming', 'pm_simple_farming', 'pm_soil_enriching_farming'], 'label_pt': 'cereais', 'label_en': 'grain', 'building_pt': 'fazenda de trigo', 'building_en': 'wheat farm',
     'alternatives': [
         {'building': 'building_rye_farm', 'methods': ['pm_chemical_fertilizer', 'pm_fertilization', 'pm_simple_farming', 'pm_soil_enriching_farming'], 'building_pt': 'fazenda de centeio', 'building_en': 'rye farm'},
         {'building': 'building_rice_farm', 'methods': ['pm_chemical_fertilizer_building_rice_farm', 'pm_fertilization_building_rice_farm', 'pm_herring_meal_farming_building_rice_farm', 'pm_simple_farming_building_rice_farm', 'pm_soil_enriching_farming_building_rice_farm'], 'building_pt': 'fazenda de arroz', 'building_en': 'rice farm'},
         {'building': 'building_maize_farm', 'methods': ['pm_chemical_fertilizer', 'pm_fertilization', 'pm_simple_farming', 'pm_soil_enriching_farming'], 'building_pt': 'fazenda de milho', 'building_en': 'maize farm'},
         {'building': 'building_millet_farm', 'methods': ['pm_chemical_fertilizer', 'pm_fertilization', 'pm_simple_farming', 'pm_soil_enriching_farming'], 'building_pt': 'fazenda de milhete', 'building_en': 'millet farm'},
     ]},
    {'good': 'fabric', 'building': 'building_cotton_plantation', 'methods': ['automatic_irrigation_building_cotton_plantation', 'default_building_cotton_plantation', 'slave_exploitation_cotton', 'worker_exploitation_cotton'], 'label_pt': 'tecido', 'label_en': 'fabric', 'building_pt': 'plantação de algodão', 'building_en': 'cotton plantation',
     'alternatives': [
         {'building': 'building_livestock_ranch', 'methods': ['pm_intensive_grazing_ranch', 'pm_sheep_farms', 'pm_simple_ranch'], 'building_pt': 'fazenda de gado', 'building_en': 'livestock ranch'},
     ]},
    {'good': 'tools', 'building': 'building_tooling_workshop', 'methods': ['pm_crude_tools', 'pm_pig_iron', 'pm_rubber_grips', 'pm_steel'], 'label_pt': 'ferramentas', 'label_en': 'tools', 'building_pt': 'oficina de ferramentas', 'building_en': 'tooling workshop'},
    {'good': 'groceries', 'building': 'building_food_industry', 'methods': ['pm_bakery', 'pm_baking_powder', 'pm_cannery', 'pm_cannery_fish', 'pm_sweeteners', 'pm_vacuum_canning', 'pm_vacuum_canning_principle_3'], 'label_pt': 'mantimentos', 'label_en': 'groceries', 'building_pt': 'indústria alimentícia', 'building_en': 'food industry'},
    {'good': 'clothes', 'building': 'building_textile_mill', 'methods': ['pm_dye_workshops', 'pm_electric_sewing_machines', 'pm_handsewn_clothes', 'pm_sewing_machines'], 'label_pt': 'roupas', 'label_en': 'clothes', 'building_pt': 'fábrica têxtil', 'building_en': 'textile mill'},
    {'good': 'small_arms', 'building': 'building_arms_industry', 'methods': ['pm_muskets', 'pm_rifles', 'pm_repeaters', 'pm_bolt_action_rifles'], 'label_pt': 'armas leves', 'label_en': 'small arms', 'building_pt': 'indústria de armas', 'building_en': 'arms industry'},
    {'good': 'artillery', 'building': 'building_artillery_foundry', 'methods': ['pm_cannons', 'pm_bronze_cannons', 'pm_smoothbores', 'pm_bronze_smoothbores', 'pm_breech_loaders', 'pm_recoiled_barrels'], 'label_pt': 'artilharia', 'label_en': 'artillery', 'building_pt': 'fundição de artilharia', 'building_en': 'artillery foundry'},
    {'good': 'ammunition', 'building': 'building_munition_plant', 'methods': ['pm_percussion_caps', 'pm_explosive_shells'], 'label_pt': 'munição', 'label_en': 'ammunition', 'building_pt': 'fábrica de munição', 'building_en': 'munition plant'},
]
PERSISTENT_VARIABLES = ['sed_schema_version', 'sed_auto_last_attempt_month',
                        'sed_tax_last_change_month', 'sed_wage_last_change_month']


def variants(item):
    """Primary producer plus verified alternatives for the same market good."""
    return [{'building': item['building'], 'methods': item['methods'],
             'building_pt': item['building_pt'], 'building_en': item['building_en']}] + item.get('alternatives', [])


def variant_id(variant):
    return variant['building'].removeprefix('building_')


def variant_methods(variant, indent='  '):
    return '\n'.join(f'{indent}has_active_production_method = {method}'
                      for method in variant['methods'])
ACTION_NAMES = ('railway', 'construction') + tuple(item['good'] for item in SUPPLY_TARGETS)
IGNORED_VARIABLES = [f'sed_{name}_ignored' for name in ACTION_NAMES]
SUPPLY_DIAGNOSTICS = ('producer_states', 'ignored_states', 'pending_states', 'unincorporated_states',
                      'understaffed_states', 'hiring_states', 'input_states',
                      'method_states', 'permission_states', 'infrastructure_states')
STATE_VARIABLES = ['sed_railway_request_pending', 'sed_construction_request_pending',
                   'sed_railway_intent_level', 'sed_construction_intent_level'] + [
    f"sed_{item['good']}_request_pending" for item in SUPPLY_TARGETS] + IGNORED_VARIABLES + [
    f"sed_{item['good']}_{field}" for item in SUPPLY_TARGETS
    for field in ('intent_level', 'intent_variant')]
STATE_VARIABLES += planning.state_variables(ACTION_NAMES)
EXTRA_VARIABLES = '''sed_last_year sed_last_month sed_month_key sed_in_default
sed_gdp_per_capita sed_per_capita_available sed_debt_share sed_debt_share_available
sed_reserve_weeks sed_reserve_weeks_available sed_states sed_infrastructure_short_states
sed_low_access_states sed_shortage_buildings sed_understaffed_buildings
sed_hiring_failure_buildings sed_anchor_month sed_anchor_gdp sed_previous_month
sed_previous_gdp sed_growth sed_growth_months sed_growth_available
sed_railway_action_status sed_construction_action_status
sed_railway_ignored_states sed_construction_ignored_states
sed_railway_deficit_states sed_railway_no_railway_states
sed_railway_not_ready_states sed_railway_blocked_states
sed_construction_sector_states sed_construction_not_ready_states
sed_construction_blocked_states sed_construction_infrastructure_states
sed_queue_levels_before'''.split() + [
    'sed_mode_manual', 'sed_mode_assisted', 'sed_mode_automatic',
    'sed_auto_action_status', 'sed_auto_event_pending', 'sed_details_visible',
    'sed_tax_level_saved', 'sed_gov_wage_saved',
    *[f'sed_{policy}_last_{field}' for policy in ('tax', 'wage')
      for field in ('from', 'to', 'year', 'month')],
    'sed_auto_review_status', 'sed_auto_review_year', 'sed_auto_review_month',
    *[f"sed_{item['good']}_action_status" for item in SUPPLY_TARGETS],
    *[f"sed_{item['good']}_{field}" for item in SUPPLY_TARGETS
      for field in ('intents', 'completed', 'abandoned', 'result', 'result_month')],
    *[f"sed_{name}_{field}" for name in ('railway', 'construction')
      for field in ('intents', 'completed', 'abandoned', 'result', 'result_month')],
    *[f"sed_{item['good']}_{reason}" for item in SUPPLY_TARGETS
      for reason in SUPPLY_DIAGNOSTICS],
]


EXTRA_VARIABLES += planning.country_variables(ACTION_NAMES) + coordination.VARIABLES + construction_budget.VARIABLES


def runtime_variables():
    return ['sed_enabled', 'sed_monthly_refresh'] + [
        'sed_' + metric['id'] for metric in METRICS] + EXTRA_VARIABLES + STATE_VARIABLES


def country_variables():
    return ['sed_enabled', 'sed_monthly_refresh'] + [
        'sed_' + metric['id'] for metric in METRICS] + EXTRA_VARIABLES


def supply_effects():
    result = ['''sed_ensure_mode_default = {
 if = {
  limit = { NOT = { OR = { has_variable = sed_mode_manual has_variable = sed_mode_assisted has_variable = sed_mode_automatic } } }
  sed_set_mode_assisted = yes
 }
}

# Country scope; the persistent marker is written before an automatic attempt.
sed_record_auto_attempt = {
 if = {
  limit = { has_variable = sed_mode_automatic }
  set_variable = { name = sed_auto_last_attempt_month value = { value = year multiply = 12 add = month } }
 }
}

sed_refresh_supply_candidates = {''']
    for item in SUPPLY_TARGETS:
        good = item['good']
        vs = variants(item)
        primary = vs[0]['building']
        any_present = ' '.join(f'has_building = {variant["building"]}' for variant in vs)
        any_queued = ' '.join(
            f'AND = {{ has_building = {variant["building"]} b:{variant["building"]} = {{ level_after_queued_constructions > level }} }}'
            for variant in vs)
        tracked_queued = ' '.join(
            f'AND = {{ var:sed_{good}_intent_variant = {index} has_building = {variant["building"]} '
            f'b:{variant["building"]} = {{ level_after_queued_constructions > level }} }}'
            for index, variant in enumerate(vs, 1))
        request_queued = (f'OR = {{ AND = {{ has_variable = sed_{good}_intent_variant '
                          f'OR = {{ {tracked_queued} }} }} '
                          f'AND = {{ NOT = {{ has_variable = sed_{good}_intent_variant }} '
                          f'OR = {{ {any_queued} }} }} }}')
        reset = '\n'.join(f' set_variable = {{ name = sed_{good}_{reason} value = 0 }}'
                          for reason in SUPPLY_DIAGNOSTICS)
        breakdown = f'''  if = {{
   limit = {{ OR = {{ {any_present} }} }}
   root = {{ change_variable = {{ name = sed_{good}_producer_states add = 1 }} }}
  }}
  if = {{ limit = {{ sed_{good}_candidate_eligible = yes }} }}
'''
        for variant in vs:
            building = variant['building']
            methods = ' '.join(f'has_active_production_method = {method}' for method in variant['methods'])
            reasons = [
                ('ignored_states', f'has_variable = sed_{good}_ignored'),
                ('pending_states', f'OR = {{ has_variable = sed_{good}_request_pending b:{building} = {{ level_after_queued_constructions > level }} }}'),
                ('unincorporated_states', 'NOT = { is_incorporated = yes }'),
                ('understaffed_states', f'b:{building} = {{ OR = {{ level <= 0 occupancy < 0.8 }} }}'),
                ('hiring_states', f'b:{building} = {{ has_failed_hires = yes }}'),
                ('input_states', f'b:{building} = {{ building_has_goods_shortage = yes }}'),
                ('method_states', f'b:{building} = {{ NOT = {{ OR = {{ {methods} }} }} }}'),
                ('permission_states', f'NOT = {{ can_construct_building = {building} }}'),
                ('infrastructure_states', 'infrastructure_delta < 0'),
            ]
            breakdown += f'''  else_if = {{
   limit = {{ has_building = {building} }}
'''
            for index, (reason, condition) in enumerate(reasons):
                branch = 'if' if index == 0 else 'else_if'
                breakdown += f'''   {branch} = {{
    limit = {{ {condition} }}
    root = {{ change_variable = {{ name = sed_{good}_{reason} add = 1 }} }}
   }}
'''
            breakdown += '  }'
        outcome = '''   if = {
    limit = { has_variable = sed_''' + good + '''_intent_variant has_variable = sed_''' + good + '''_intent_level }
'''
        for index, variant in enumerate(vs, 1):
            branch = 'if' if index == 1 else 'else_if'
            outcome += f'''    {branch} = {{
     limit = {{ var:sed_{good}_intent_variant = {index}
      has_building = {variant['building']}
      b:{variant['building']}.level > var:sed_{good}_intent_level
     }}
     sed_{good}_record_completed = yes
    }}
'''
        outcome += f'''    else = {{ sed_{good}_record_abandoned = yes }}
   }}'''
        result.extend([
            reset,
            f' clear_variable_list = sed_{good}_candidates',
            f''' every_scope_state = {{
  if = {{
   limit = {{ has_variable = sed_{good}_request_pending
    NOT = {{ {request_queued} }}
   }}
{outcome}
   remove_variable = sed_{good}_request_pending
  }}
{breakdown}
 }}''',
            f''' if = {{
  limit = {{ is_player = yes has_variable = sed_enabled
   market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }}
  }}
  ordered_scope_state = {{
   limit = {{ sed_{good}_candidate_eligible = yes }}
   order_by = {{ value = state_population multiply = -1 }}
   max = 3
   check_range_bounds = no
   root = {{ add_to_variable_list = {{ name = sed_{good}_candidates target = prev }} }}
  }}
 }}''',
        ])
    result.append('}')
    for item in SUPPLY_TARGETS:
        good = item['good']
        vs = variants(item)
        enqueue = ''
        for index, variant in enumerate(vs):
            branch = 'if' if index == 0 else 'else_if'
            enqueue += f'''  {branch} = {{
   limit = {{ sed_{good}_{variant_id(variant)}_eligible = yes }}
   # Baseline level before queuing; the monthly review compares it after the queue.
   set_variable = {{ name = sed_{good}_intent_level value = b:{variant['building']}.level }}
   set_variable = {{ name = sed_{good}_intent_variant value = {index + 1} }}
   start_building_construction = {variant['building']}
  }}
'''
        result.append(f'''sed_run_{good}_approval = {{
 owner = {{ if = {{ limit = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic }} sed_refresh_direct_budget = yes }} }}
 if = {{
  limit = {{ sed_{good}_approval_valid = yes }}
  owner = {{ set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }} }}
  owner = {{ sed_record_auto_attempt = yes }}
{enqueue}  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_{good}_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_mode_automatic }} set_variable = {{ name = sed_auto_action_status value = 1 }} }}
    if = {{ limit = {{ has_variable = sed_{good}_intents }}
     change_variable = {{ name = sed_{good}_intents add = 1 }}
    }}
    else = {{ set_variable = {{ name = sed_{good}_intents value = 1 }} }}
    prev = {{ set_variable = {{ name = sed_{good}_request_pending value = yes }} }}
   }}
   else = {{
    set_variable = {{ name = sed_{good}_action_status value = 2 }}
    prev = {{
     remove_variable = sed_{good}_intent_level
     remove_variable = sed_{good}_intent_variant
    }}
   }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}''')
        record = []
        for outcome, code in (('completed', 1), ('abandoned', 2)):
            record.append(f'''sed_{good}_record_{outcome} = {{
 owner = {{
  if = {{ limit = {{ has_variable = sed_{good}_{outcome} }}
   change_variable = {{ name = sed_{good}_{outcome} add = 1 }}
  }}
  else = {{ set_variable = {{ name = sed_{good}_{outcome} value = 1 }} }}
  set_variable = {{ name = sed_{good}_result value = {code} }}
  set_variable = {{ name = sed_{good}_result_month value = sed_live_month_key }}
 }}
 remove_variable = sed_{good}_intent_level
 remove_variable = sed_{good}_intent_variant
}}''')
        result.extend(record)
    mode_actions = []
    for mode in ('manual', 'assisted', 'automatic'):
        other_modes = [value for value in ('manual', 'assisted', 'automatic') if value != mode]
        cleanup = '\n'.join(f' remove_variable = sed_mode_{value}' for value in other_modes)
        release = ' sed_coord_restore = yes\n sed_restore_fiscal_policy = yes\n sed_restore_wage_policy = yes\n' if mode != 'automatic' else ''
        takeover = ''
        if mode == 'automatic':
            takeover = ' if = { limit = { has_variable = sed_enabled NOT = { has_variable = sed_coord_active } sed_coord_tools_available = yes } sed_coord_enable = yes }\n'
        mode_actions.append(f'''sed_set_mode_{mode} = {{
{release} remove_variable = sed_mode_{mode}{cleanup}
 set_variable = {{ name = sed_mode_{mode} value = yes }}
 set_variable = {{ name = sed_auto_action_status value = 0 }}
{takeover} if = {{ limit = {{ has_variable = sed_mode_automatic }} sed_schedule_auto_event = yes }}
}}''')
    result.extend(mode_actions)
    result.append('''sed_schedule_auto_event = {
 if = {
  limit = { has_variable = sed_mode_automatic NOT = { has_variable = sed_auto_event_pending } }
  set_variable = { name = sed_auto_event_pending value = yes }
  trigger_event = { id = sed_pulse.1 days = 23 }
 }
}''')
    result.append('''sed_auto_apply_monthly = {
 sed_refresh_national_plan = yes
 sed_apply_fiscal_policy = yes
 sed_apply_wage_policy = yes
 set_variable = { name = sed_auto_action_status value = 2 }
 if = {
  limit = { has_variable = sed_coord_active }
  sed_coord_sync = yes
  if = { limit = { var:sed_coord_executor = 11 } sed_auto_run_direct = yes }
  else = {
   set_variable = { name = sed_auto_action_status value = 18 }
   if = { limit = { var:sed_coord_executor = 12 } set_variable = { name = sed_auto_action_status value = 21 } }
   else_if = { limit = { var:sed_coord_executor = 10 } set_variable = { name = sed_auto_action_status value = 20 } }
   else_if = { limit = { var:sed_coord_executor = 9 } set_variable = { name = sed_auto_action_status value = 19 } }
   else_if = { limit = { var:sed_coord_executor = 5 } set_variable = { name = sed_auto_action_status value = 13 } }
   else_if = { limit = { var:sed_coord_executor = 0 }
    set_variable = { name = sed_auto_action_status value = 2 }
    if = { limit = { NOT = { sed_coord_fiscal_safe = yes } } set_variable = { name = sed_auto_action_status value = 17 } }
   }
  }
 }
 else = { sed_auto_run_direct = yes }
 # Store the actual result after either direct execution or delegation.
 set_variable = { name = sed_auto_review_status value = var:sed_auto_action_status }
 set_variable = { name = sed_auto_review_year value = year }
 set_variable = { name = sed_auto_review_month value = { value = month add = 1 } }
}

sed_auto_run_direct = {
 sed_refresh_direct_budget = yes
 if = {
  limit = { sed_auto_executor_safe = yes }
''')
    choices = [('railway', 'sed_railway_candidate_eligible')]
    choices.extend((item['good'], f"sed_{item['good']}_candidate_eligible") for item in SUPPLY_TARGETS)
    for index, (name, eligibility) in enumerate(choices):
        start = 'if' if index == 0 else 'else_if'
        order = 'infrastructure_delta' if name == 'railway' else 'state_population'
        direction = ' multiply = -1'
        result.append(f'''  {start} = {{
   limit = {{ any_scope_state = {{ {eligibility} = yes var:sed_plan_{name}_rank = 1 }} }}
   ordered_scope_state = {{
    limit = {{ {eligibility} = yes var:sed_plan_{name}_rank = 1 }}
    order_by = {{ value = {order}{direction} }}
    max = 1
    check_range_bounds = no
    # A candidate was selected; only confirmed insertion changes this to success.
    owner = {{ set_variable = {{ name = sed_auto_action_status value = 15 }} }}
    sed_run_{name}_approval = yes
   }}
  }}''')
    result.append(''' }
 else_if = { limit = { in_default = yes } set_variable = { name = sed_auto_action_status value = 10 } }
 else_if = { limit = { sed_auto_month_limit_reached = yes } set_variable = { name = sed_auto_action_status value = 16 } }
 else_if = { limit = { OR = { construction_queue_num_queued_government_levels > 0 construction_queue_num_queued_private_levels > 0 } } set_variable = { name = sed_auto_action_status value = 11 } }
 else_if = { limit = { is_construction_paused = yes } set_variable = { name = sed_auto_action_status value = 12 } }
 else_if = { limit = { sed_competing_builder_configured = yes } set_variable = { name = sed_auto_action_status value = 13 } }
 else_if = { limit = { NOT = { sed_auto_fiscal_safe = yes } } set_variable = { name = sed_auto_action_status value = 17 } }
 else_if = { limit = { NOT = { sed_direct_budget_safe = yes } } set_variable = { name = sed_auto_action_status value = 22 } }
 else = { set_variable = { name = sed_auto_action_status value = 14 } }
}
''')
    return '\n'.join(result).rstrip() + '\n'


def preference_effects():
    result = []
    for name in ACTION_NAMES:
        result.append(f"""sed_ignore_{name} = {{
 if = {{
  limit = {{ owner = {{ is_player = yes has_variable = sed_enabled }} sed_{name}_candidate_eligible = yes }}
  set_variable = {{ name = sed_{name}_ignored value = yes }}
  owner = {{ sed_refresh_diagnostics = yes }}
 }}
}}
""")
    cleanup = '\n'.join('  remove_variable = ' + name for name in IGNORED_VARIABLES)
    result.append('sed_restore_ignored = {\n if = {\n  limit = { is_player = yes has_variable = sed_enabled }\n  every_scope_state = {\n'
                  + cleanup + '\n  }\n  sed_refresh_diagnostics = yes\n }\n}\n')
    return '\n'.join(result)


def sgui(name, method):
    return f"GetScriptedGui('{name}').{method}(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)"


def textbox(key, visibility=None, heading=False, width=500, state=False):
    shown = ''
    if visibility:
        binding = (f"GetScriptedGui('{visibility}').IsShown(GuiScope.SetRoot(State.MakeScope).End)"
                   if state else sgui(visibility, 'IsShown'))
        shown = f' visible = "[{binding}]"\n'
    return f"""textbox = {{
{shown} autoresize = yes multiline = yes align = left|nobaseline
 using = {'fontsize_xxl' if heading else 'fontsize_large'}
 minimumsize = {{ {width} -1 }} maximumsize = {{ {width} -1 }}
 text = "{key}"
}}
"""


def button(key, action, width=500, state=False, native_action=None):
    binding = lambda method: (f"GetScriptedGui('{action}').{method}(GuiScope.SetRoot(State.MakeScope).End)"
                              if state else sgui(action, method))
    execute = native_action or binding('Execute')
    return f"""button = {{
 using = default_button
 using = fontsize_large
 using = tooltip_se
 size = {{ {width} 52 }}
 text = "{key}" tooltip = "{key}_tt"
 visible = "[{binding('IsShown')}]"
 enabled = "[{binding('IsValid')}]"
 onclick = "[{execute}]"
}}
"""


def mode_button(key, action):
    return button(key, action, width=160)


def details(content):
    return ('flowcontainer = { direction = vertical spacing = 10 ignoreinvisible = yes\n'
            + f' visible = "[{sgui("sed_details_visible_sgui", "IsShown")}]"\n'
            + content + '}\n')


def candidate_item(name):
    supply = name not in ('railway', 'construction')
    approve = f'sed_{name}_approve' if supply else f'sed_approve_{name}'
    prefix = 'sed_supply' if supply else f'sed_{name}'
    content = textbox(f'sed_{name}_candidate_title', heading=True, width=468)
    content += textbox(f'sed_{name}_candidate_reason', width=468)
    content += textbox(f'sed_plan_{name}_score', f'sed_plan_{name}_score_visible_sgui', width=468, state=True)
    if name != 'railway':
        content += textbox('sed_candidate_infrastructure', width=468)
        content += textbox('sed_expansion_infrastructure_blocked', f'sed_{name}_infrastructure_blocked_sgui', width=468, state=True)
    content += textbox('sed_approval_ready', f'sed_{name}_ready_sgui', width=468, state=True)
    content += textbox('sed_mode_approval_blocked', f'sed_{name}_switch_assisted_sgui', width=468, state=True)
    content += button('sed_switch_assisted', f'sed_{name}_switch_assisted_sgui', width=468, state=True)
    content += button(approve, f'sed_approve_{name}_sgui', width=468, state=True)
    content += button('sed_ignore_recommendation', f'sed_ignore_{name}_sgui', width=468, state=True)
    for guard in (('queue', 'private', 'default') if name == 'construction' else ('private', 'default')):
        content += textbox(f'{prefix}_blocked_{guard}', f'sed_{name}_blocked_{guard}_sgui', width=468, state=True)
    for kind in ('stale', 'pending', 'finance_caution'):
        content += textbox(f'{prefix}_{kind}', f'sed_{name}_{kind}_sgui', width=468, state=True)
    content += button('sed_refresh_card', f'sed_{name}_refresh_card_sgui', width=468, state=True)
    return f""" type sed_{name}_candidate_item = flowcontainer {{
 datacontext = "[Scope.GetState]"
 direction = vertical spacing = 10 ignoreinvisible = yes
 minimumsize = {{ 500 -1 }} maximumsize = {{ 500 -1 }}
 background = {{ using = dark_area }}
 flowcontainer = {{ direction = vertical spacing = 10 ignoreinvisible = yes
  margin = {{ 16 12 }}
{content} }}
}}
"""


def candidate_list(name, visibility):
    return f"""flowcontainer = {{
 visible = "[{sgui(visibility, 'IsShown')}]"
 direction = vertical spacing = 16 ignoreinvisible = yes
 datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('sed_{name}_candidates')]"
 item = {{ sed_{name}_candidate_item = {{}} }}
}}
"""


def widget():
    body = textbox('sed_title', heading=True)
    body += textbox('sed_mode_title', heading=True)
    body += textbox('sed_coord_intro')
    body += button('sed_coord_enable', 'sed_coord_enable_sgui')
    body += button('sed_coord_release', 'sed_coord_release_sgui')
    for executor in range(13):
        body += textbox(f'sed_coord_executor_{executor}', f'sed_coord_executor_{executor}_visible_sgui')
    body += textbox('sed_coord_supply_policy', 'sed_coord_supply_policy_visible_sgui')
    for policy in (1, 2, 3):
        body += textbox(f'sed_coord_advisor_policy_{policy}', f'sed_coord_advisor_policy_{policy}_visible_sgui')
    body += 'flowcontainer = { direction = horizontal spacing = 10\n'
    for mode in ('manual', 'assisted', 'automatic'):
        body += mode_button(f'sed_mode_{mode}_button', f'sed_set_mode_{mode}_sgui')
    body += '}\n'
    for mode in ('manual', 'assisted', 'automatic'):
        body += textbox(f'sed_mode_{mode}_status', f'sed_mode_{mode}_visible_sgui')
    for state in ('pending', 'idle', 'unrecorded'):
        body += textbox(f'sed_auto_{state}', f'sed_auto_{state}_visible_sgui')
    for blocker in ('default', 'month_limit', 'queue', 'paused', 'competing', 'fiscal', 'budget', 'clear'):
        body += textbox(f'sed_auto_current_{blocker}', f'sed_auto_current_{blocker}_visible_sgui')
    body += textbox('sed_auto_builders_title', 'sed_auto_builders_visible_sgui')
    for name, option, pt, en in COMPETING_BUILDERS:
        body += textbox(f'sed_auto_builder_{name}', f'sed_auto_builder_{name}_visible_sgui')
    body += textbox('sed_auto_builders_help', 'sed_auto_builders_visible_sgui')
    for policy in ('tax', 'wage'):
        body += textbox(f'sed_{policy}_last_command', f'sed_{policy}_last_command_visible_sgui')
    body += textbox('sed_auto_last_review', 'sed_auto_last_review_visible_sgui')
    for status in ('success', 'no_action', 'default', 'queue', 'paused', 'competing', 'safety', 'unconfirmed', 'month_limit', 'fiscal', 'delegated', 'unsupported', 'waiting', 'reserve_queue', 'budget'):
        body += textbox(f'sed_auto_status_{status}', f'sed_auto_status_{status}_visible_sgui')
    body += 'flowcontainer = { direction = horizontal spacing = 12\n'
    body += button('sed_refresh', 'sed_refresh_sgui', width=244)
    body += button('sed_disable', 'sed_disable_sgui', width=244) + '}\n'
    body += button('sed_use_manual', 'sed_manual_updates_sgui')
    body += button('sed_use_monthly', 'sed_monthly_updates_sgui')
    body += textbox('sed_last_refresh')
    body += textbox('sed_dashboard_budget') + textbox('sed_dashboard_queue')
    body += button('sed_open_queue', 'sed_refresh_sgui', native_action="InformationPanelBar.OpenConstructionPanelTab( GetPlayer.Self, 'default' )")
    body += button('sed_show_details', 'sed_show_details_sgui')
    body += button('sed_hide_details', 'sed_hide_details_sgui')
    body += button('sed_restore_ignored', 'sed_restore_ignored_sgui')
    body += textbox('sed_ignored_notice', 'sed_restore_ignored_sgui')
    body += textbox('sed_default_warning', 'sed_default_visible_sgui')
    body += textbox('sed_deficit_warning', 'sed_deficit_visible_sgui')
    body += textbox('sed_plan_title', heading=True)
    body += textbox('sed_plan_date')
    body += textbox('sed_plan_waiting', 'sed_plan_waiting_visible_sgui')
    body += textbox('sed_reserve_budget', 'sed_reserve_budget_visible_sgui')
    body += textbox('sed_build_budget', 'sed_build_budget_visible_sgui')
    body += textbox('sed_build_budget_unknown', 'sed_build_budget_unknown_visible_sgui')
    for status in range(1, 6):
        body += textbox(f'sed_fiscal_{status}', f'sed_fiscal_{status}_visible_sgui')
    for goal in range(10):
        body += textbox(f'sed_goal_{goal}', f'sed_goal_{goal}_visible_sgui')
    body += textbox('sed_military_title', heading=True)
    body += textbox('sed_military_summary')
    for war in (0, 1):
        body += textbox(f'sed_military_war_{war}', f'sed_military_war_{war}_visible_sgui')
    for posture in range(5):
        body += textbox(f'sed_military_posture_{posture}', f'sed_military_posture_{posture}_visible_sgui')
    for good, _, _ in planning.MILITARY_GOODS:
        body += textbox(f'sed_military_short_{good}', f'sed_military_short_{good}_visible_sgui')
    body += textbox('sed_military_scope')
    body += textbox('sed_plan_policy')
    body += textbox('sed_tax_policy', 'sed_tax_policy_visible_sgui')
    body += textbox('sed_wage_policy', 'sed_tax_policy_visible_sgui')
    for item in SUPPLY_TARGETS:
        name = item['good']
        body += textbox(f'sed_meta_{name}', f'sed_meta_{name}_visible_sgui')
    for item in SUPPLY_TARGETS:
        name = item['good']
        body += textbox(f'sed_plan_missing_{name}', f'sed_plan_missing_{name}_visible_sgui')
    for item in SUPPLY_TARGETS:
        name = item['good']
        body += textbox(f'sed_book_{name}', f'sed_book_{name}_visible_sgui')
    for name in ('railway', 'construction'):
        body += textbox(f'sed_book_{name}', f'sed_book_{name}_visible_sgui')
    body += textbox('sed_plan_empty', 'sed_plan_empty_visible_sgui')
    for rank in planning.RANKS:
        body += textbox(f'sed_plan_rank_{rank}', f'sed_plan_rank_{rank}_visible_sgui', heading=True)
        for name in ACTION_NAMES:
            body += f"""flowcontainer = {{
 visible = "[{sgui(f'sed_plan_{rank}_{name}_visible_sgui', 'IsShown')}]"
 direction = vertical spacing = 16 ignoreinvisible = yes
 datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('sed_plan_{rank}_{name}')]"
 item = {{ sed_{name}_candidate_item = {{}} }}
}}
"""
    # Keep detailed per-type candidate lists available under the existing toggle.
    all_candidates = ''
    all_candidates += textbox('sed_recommendations_title', heading=True)
    all_candidates += textbox('sed_recommendations_intro')
    all_candidates += textbox('sed_no_infrastructure_opportunity', 'sed_no_infrastructure_opportunity_visible_sgui')
    all_candidates += textbox('sed_no_railway_candidate', 'sed_no_railway_candidate_visible_sgui')
    all_candidates += details(textbox('sed_railway_breakdown', 'sed_railway_breakdown_visible_sgui'))
    all_candidates += candidate_list('railway', 'sed_recommendations_visible_sgui')
    all_candidates += textbox('sed_railway_action_success', 'sed_action_success_visible_sgui')
    all_candidates += textbox('sed_railway_action_failed', 'sed_action_failed_visible_sgui')
    all_candidates += textbox('sed_construction_title', heading=True) + textbox('sed_construction_intro')
    all_candidates += textbox('sed_no_construction_queue', 'sed_no_construction_queue_visible_sgui')
    all_candidates += textbox('sed_no_construction_candidate', 'sed_no_construction_candidate_visible_sgui')
    all_candidates += details(textbox('sed_construction_breakdown', 'sed_construction_breakdown_visible_sgui'))
    all_candidates += candidate_list('construction', 'sed_construction_recommendations_visible_sgui')
    all_candidates += textbox('sed_construction_action_success', 'sed_construction_action_success_visible_sgui')
    all_candidates += textbox('sed_construction_action_failed', 'sed_construction_action_failed_visible_sgui')
    all_candidates += textbox('sed_supply_title', heading=True) + textbox('sed_supply_intro')
    for item in SUPPLY_TARGETS:
        good = item['good']
        all_candidates += textbox(f'sed_{good}_section_title', f'sed_{good}_section_visible_sgui', heading=True)
        all_candidates += candidate_list(good, f'sed_{good}_recommendations_visible_sgui')
        all_candidates += textbox('sed_supply_no_candidate', f'sed_{good}_no_candidates_visible_sgui')
        all_candidates += details(textbox(f'sed_{good}_rejection_summary', f'sed_{good}_no_candidates_visible_sgui')
                        + textbox(f'sed_{good}_rejection_details', f'sed_{good}_no_candidates_visible_sgui'))
        all_candidates += textbox(f'sed_{good}_action_success', f'sed_{good}_action_success_visible_sgui')
        all_candidates += textbox(f'sed_{good}_action_failed', f'sed_{good}_action_failed_visible_sgui')
    body += details(all_candidates)
    diagnostic = textbox('sed_details_title', heading=True)
    for title, metrics in [('sed_finance_title', ['balance', 'operating_balance', 'fixed_expenses', 'gold', 'debt', 'credit']),
                           ('sed_development_title', ['gdp', 'population', 'sol', 'literacy']),
                           ('sed_production_title', ['construction', 'public_projects', 'private_projects'])]:
        diagnostic += textbox(title, heading=True)
        for metric in metrics:
            diagnostic += textbox('sed_metric_' + metric)
    for key, visibility in [('sed_operating_warning', 'sed_operating_deficit_visible_sgui'),
                            ('sed_nonnegative_note', 'sed_nonnegative_visible_sgui'),
                            ('sed_debt_share_text', 'sed_debt_share_visible_sgui'),
                            ('sed_debt_share_unavailable', 'sed_no_debt_share_visible_sgui'),
                            ('sed_runway_text', 'sed_runway_visible_sgui'),
                            ('sed_runway_unavailable', 'sed_no_runway_visible_sgui'),
                            ('sed_per_capita_text', 'sed_per_capita_visible_sgui'),
                            ('sed_per_capita_unavailable', 'sed_no_per_capita_visible_sgui'),
                            ('sed_growth_text', 'sed_growth_visible_sgui'),
                            ('sed_growth_unavailable', 'sed_no_growth_visible_sgui')]:
        diagnostic += textbox(key, visibility)
    diagnostic += textbox('sed_state_readings') + textbox('sed_employment_readings')
    diagnostic += textbox('sed_limitations_title', heading=True) + textbox('sed_limitations')
    body += details(diagnostic)
    types = ''.join(candidate_item(name) for name in ACTION_NAMES)
    return ('# Generated by tools/build_mod.py.\ntypes sed_diagnostics_types {\n' + types + '}\n'
            + 'flowcontainer = { name = "sed_diagnostics_widget"\n'
            + ' minimumsize = { 500 -1 } maximumsize = { 500 -1 }\n'
            + ' direction = vertical spacing = 12 ignoreinvisible = yes\n' + body + '}\n')


def effects():
    readings = '\n'.join(f' # {m["source"]}\n set_variable = {{ name = sed_{m["id"]} value = {m["expression"]} }}' for m in METRICS)
    script = '''# Generated by tools/build_mod.py. Country scope except state-targeted actions.
# Explicit opt-in on both new campaigns and existing saves. Approved actions only.
sed_enable_country = {
 if = {
  limit = { NOT = { has_variable = sed_schema_version } }
  set_variable = { name = sed_schema_version value = 1 }
 }
 set_variable = { name = sed_enabled value = yes }
 set_variable = { name = sed_monthly_refresh value = yes }
 set_variable = { name = sed_railway_action_status value = 0 }
 set_variable = { name = sed_construction_action_status value = 0 }
 if = {
  limit = { NOT = { OR = { has_variable = sed_mode_manual has_variable = sed_mode_assisted has_variable = sed_mode_automatic } } }
  sed_set_mode_assisted = yes
 }
 sed_refresh_diagnostics = yes
 sed_ensure_journal_entry = yes
}

sed_disable_country = {
 sed_coord_restore = yes
 sed_restore_fiscal_policy = yes
 sed_restore_wage_policy = yes
''' + '\n'.join(' remove_variable = ' + name for name in country_variables()) + '''
 clear_variable_list = sed_railway_candidates
 clear_variable_list = sed_construction_candidates
 every_scope_state = {
  remove_variable = sed_railway_request_pending
  remove_variable = sed_construction_request_pending
  remove_variable = sed_railway_intent_level
  remove_variable = sed_construction_intent_level
__SUPPLY_STATE_CLEANUP__
 }
 # Schema and automatic attempt month persist; disabling cannot reset the monthly cap.
}

sed_ensure_journal_entry = {
 if = {
  limit = {
   has_variable = sed_enabled
   NOT = { has_journal_entry = je_sed_diagnostics }
   NOT = { has_inactive_journal_entry = je_sed_diagnostics }
  }
  add_journal_entry = { type = je_sed_diagnostics }
 }
}

sed_monthly_update = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
  sed_ensure_journal_entry = yes
  if = {
   limit = { has_variable = sed_monthly_refresh }
   sed_refresh_diagnostics = yes
  }
  if = { limit = { has_variable = sed_coord_active } sed_refresh_national_plan = yes sed_coord_sync = yes }
  sed_schedule_auto_event = yes
 }
}

sed_refresh_diagnostics = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
  sed_ensure_mode_default = yes
''' + readings + '''
  set_variable = { name = sed_last_year value = year }
  # The game's month trigger is zero-based (vanilla ip4_custom_loc.txt).
  set_variable = { name = sed_last_month value = { value = month add = 1 } }
  set_variable = { name = sed_month_key value = { value = year multiply = 12 add = month } }
  set_variable = { name = sed_in_default value = 0 }
  if = { limit = { in_default = yes } set_variable = { name = sed_in_default value = 1 } }
  set_variable = { name = sed_gdp_per_capita value = 0 }
  set_variable = { name = sed_per_capita_available value = 0 }
  if = {
   limit = { var:sed_population > 0 }
   set_variable = { name = sed_gdp_per_capita value = { value = var:sed_gdp divide = var:sed_population } }
   set_variable = { name = sed_per_capita_available value = 1 }
  }
  set_variable = { name = sed_debt_share value = 0 }
  set_variable = { name = sed_debt_share_available value = 0 }
  if = {
   limit = { var:sed_credit > 0 }
   set_variable = { name = sed_debt_share value = { value = var:sed_debt divide = var:sed_credit } }
   set_variable = { name = sed_debt_share_available value = 1 }
  }
  set_variable = { name = sed_reserve_weeks value = 0 }
  set_variable = { name = sed_reserve_weeks_available value = 0 }
  if = {
   limit = { var:sed_balance < 0 }
   set_variable = { name = sed_reserve_weeks value = { value = var:sed_gold min = 0 divide = { value = var:sed_balance multiply = -1 } } }
   set_variable = { name = sed_reserve_weeks_available value = 1 }
  }
  set_variable = { name = sed_states value = 0 }
  set_variable = { name = sed_infrastructure_short_states value = 0 }
  set_variable = { name = sed_low_access_states value = 0 }
  set_variable = { name = sed_shortage_buildings value = 0 }
  set_variable = { name = sed_understaffed_buildings value = 0 }
  set_variable = { name = sed_hiring_failure_buildings value = 0 }
  every_scope_state = {
   root = { change_variable = { name = sed_states add = 1 } }
   if = { limit = { infrastructure_delta < 0 } root = { change_variable = { name = sed_infrastructure_short_states add = 1 } } }
   if = { limit = { market_access < 1 } root = { change_variable = { name = sed_low_access_states add = 1 } } }
   every_scope_building = {
    limit = { level > 0 }
    if = { limit = { building_has_goods_shortage = yes } root = { change_variable = { name = sed_shortage_buildings add = 1 } } }
    if = { limit = { occupancy < 1 } root = { change_variable = { name = sed_understaffed_buildings add = 1 } } }
    if = { limit = { has_failed_hires = yes } root = { change_variable = { name = sed_hiring_failure_buildings add = 1 } } }
   }
  }
  sed_update_growth = yes
  sed_refresh_railway_candidates = yes
  sed_refresh_construction_candidates = yes
  sed_refresh_supply_candidates = yes
 }
}

sed_refresh_railway_candidates = {
 clear_variable_list = sed_railway_candidates
 # Counts use one primary reason per state so the breakdown adds up to the
 # deficit total instead of counting the same state under several filters.
 set_variable = { name = sed_railway_ignored_states value = 0 }
 set_variable = { name = sed_railway_deficit_states value = 0 }
 set_variable = { name = sed_railway_no_railway_states value = 0 }
 set_variable = { name = sed_railway_not_ready_states value = 0 }
 set_variable = { name = sed_railway_blocked_states value = 0 }
 every_scope_state = {
  if = {
   limit = {
    has_variable = sed_railway_request_pending
    OR = {
     NOT = { has_building = building_railway }
     b:building_railway = { level_after_queued_constructions <= level }
    }
   }
   if = {
    limit = { has_variable = sed_railway_intent_level
     has_building = building_railway
     b:building_railway.level > var:sed_railway_intent_level
    }
    sed_railway_record_completed = yes
   }
   else_if = {
    limit = { has_variable = sed_railway_intent_level }
    sed_railway_record_abandoned = yes
   }
   remove_variable = sed_railway_request_pending
   remove_variable = sed_railway_intent_level
  }
  if = {
   limit = { infrastructure_delta < 0 }
   root = { change_variable = { name = sed_railway_deficit_states add = 1 } }
   if = {
    limit = { has_variable = sed_railway_ignored }
    root = { change_variable = { name = sed_railway_ignored_states add = 1 } }
   }
   else_if = {
    limit = { NOT = { has_building = building_railway } }
    root = { change_variable = { name = sed_railway_no_railway_states add = 1 } }
   }
   else_if = {
    limit = {
     b:building_railway = {
      OR = {
       level <= 0
       occupancy < 0.8
       has_failed_hires = yes
       building_has_goods_shortage = yes
       level_after_queued_constructions > level
      }
     }
    }
    root = { change_variable = { name = sed_railway_not_ready_states add = 1 } }
   }
   else_if = {
    limit = {
     OR = {
      NOT = { is_incorporated = yes }
      NOT = { can_construct_building = building_railway }
     }
    }
    root = { change_variable = { name = sed_railway_blocked_states add = 1 } }
   }
  }
 }
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
  ordered_scope_state = {
   limit = { sed_railway_candidate_eligible = yes }
   order_by = { value = infrastructure_delta multiply = -1 }
   max = 3
   check_range_bounds = no
   root = {
    add_to_variable_list = { name = sed_railway_candidates target = prev }
   }
  }
 }
}

sed_run_railway_approval = {
 owner = { if = { limit = { is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic } sed_refresh_direct_budget = yes } }
 if = {
  limit = { sed_railway_approval_valid = yes }
  owner = {
   set_variable = { name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }
  }
  owner = { sed_record_auto_attempt = yes }
  set_variable = { name = sed_railway_intent_level value = b:building_railway.level }
  start_building_construction = building_railway
  owner = {
   if = {
    limit = { construction_queue_num_queued_government_levels > var:sed_queue_levels_before }
    set_variable = { name = sed_railway_action_status value = 1 }
    if = { limit = { has_variable = sed_railway_intents }
     change_variable = { name = sed_railway_intents add = 1 }
    }
    else = { set_variable = { name = sed_railway_intents value = 1 } }
    prev = { set_variable = { name = sed_railway_request_pending value = yes } }
   }
   else = {
    set_variable = { name = sed_railway_action_status value = 2 }
    prev = { remove_variable = sed_railway_intent_level }
   }
   remove_variable = sed_queue_levels_before
  }
 }
}

sed_refresh_construction_candidates = {
 clear_variable_list = sed_construction_candidates
 # Same primary-reason cascade as the railway counts. Only states that already
 # have a construction sector enter this denominator.
 set_variable = { name = sed_construction_ignored_states value = 0 }
 set_variable = { name = sed_construction_infrastructure_states value = 0 }
 set_variable = { name = sed_construction_sector_states value = 0 }
 set_variable = { name = sed_construction_not_ready_states value = 0 }
 set_variable = { name = sed_construction_blocked_states value = 0 }
 every_scope_state = {
  if = {
   limit = {
    has_variable = sed_construction_request_pending
    OR = {
     NOT = { has_building = building_construction_sector }
     b:building_construction_sector = { level_after_queued_constructions <= level }
    }
   }
   if = {
    limit = { has_variable = sed_construction_intent_level
     has_building = building_construction_sector
     b:building_construction_sector.level > var:sed_construction_intent_level
    }
    sed_construction_record_completed = yes
   }
   else_if = {
    limit = { has_variable = sed_construction_intent_level }
    sed_construction_record_abandoned = yes
   }
   remove_variable = sed_construction_request_pending
   remove_variable = sed_construction_intent_level
  }
  if = {
   limit = { has_building = building_construction_sector }
   root = { change_variable = { name = sed_construction_sector_states add = 1 } }
   if = {
    limit = { has_variable = sed_construction_ignored }
    root = { change_variable = { name = sed_construction_ignored_states add = 1 } }
   }
   else_if = {
    limit = {
     b:building_construction_sector = {
      OR = {
       level <= 0
       occupancy < 0.9
       has_failed_hires = yes
       building_has_goods_shortage = yes
       level_after_queued_constructions > level
      }
     }
    }
    root = { change_variable = { name = sed_construction_not_ready_states add = 1 } }
   }
   else_if = {
    limit = {
     OR = {
      NOT = { is_incorporated = yes }
      NOT = { can_construct_building = building_construction_sector }
     }
    }
    root = { change_variable = { name = sed_construction_blocked_states add = 1 } }
   }
   else_if = {
    limit = { infrastructure_delta < 0 }
    root = { change_variable = { name = sed_construction_infrastructure_states add = 1 } }
   }
  }
 }
 if = {
  limit = {
   is_player = yes
   has_variable = sed_enabled
   num_queued_government_constructions >= 3
  }
  ordered_scope_state = {
   limit = { sed_construction_candidate_eligible = yes }
   order_by = { value = state_population }
   max = 1
   check_range_bounds = no
   root = {
    add_to_variable_list = { name = sed_construction_candidates target = prev }
   }
  }
 }
}

sed_run_construction_approval = {
 owner = { if = { limit = { is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic } sed_refresh_direct_budget = yes } }
 if = {
  limit = { sed_construction_approval_valid = yes }
  owner = {
   set_variable = { name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }
  }
  owner = { sed_record_auto_attempt = yes }
  set_variable = { name = sed_construction_intent_level value = b:building_construction_sector.level }
  start_building_construction = building_construction_sector
  owner = {
   if = {
    limit = { construction_queue_num_queued_government_levels > var:sed_queue_levels_before }
    set_variable = { name = sed_construction_action_status value = 1 }
    if = { limit = { has_variable = sed_construction_intents }
     change_variable = { name = sed_construction_intents add = 1 }
    }
    else = { set_variable = { name = sed_construction_intents value = 1 } }
    prev = { set_variable = { name = sed_construction_request_pending value = yes } }
   }
   else = {
    set_variable = { name = sed_construction_action_status value = 2 }
    prev = { remove_variable = sed_construction_intent_level }
   }
   remove_variable = sed_queue_levels_before
  }
 }
}

# Country counters; completion is inferred from the queue leaving and level rising.
sed_railway_record_completed = {
 owner = {
  if = { limit = { has_variable = sed_railway_completed }
   change_variable = { name = sed_railway_completed add = 1 }
  }
  else = { set_variable = { name = sed_railway_completed value = 1 } }
  set_variable = { name = sed_railway_result value = 1 }
  set_variable = { name = sed_railway_result_month value = sed_live_month_key }
 }
 remove_variable = sed_railway_intent_level
}

sed_railway_record_abandoned = {
 owner = {
  if = { limit = { has_variable = sed_railway_abandoned }
   change_variable = { name = sed_railway_abandoned add = 1 }
  }
  else = { set_variable = { name = sed_railway_abandoned value = 1 } }
  set_variable = { name = sed_railway_result value = 2 }
  set_variable = { name = sed_railway_result_month value = sed_live_month_key }
 }
 remove_variable = sed_railway_intent_level
}

sed_construction_record_completed = {
 owner = {
  if = { limit = { has_variable = sed_construction_completed }
   change_variable = { name = sed_construction_completed add = 1 }
  }
  else = { set_variable = { name = sed_construction_completed value = 1 } }
  set_variable = { name = sed_construction_result value = 1 }
  set_variable = { name = sed_construction_result_month value = sed_live_month_key }
 }
 remove_variable = sed_construction_intent_level
}

sed_construction_record_abandoned = {
 owner = {
  if = { limit = { has_variable = sed_construction_abandoned }
   change_variable = { name = sed_construction_abandoned add = 1 }
  }
  else = { set_variable = { name = sed_construction_abandoned value = 1 } }
  set_variable = { name = sed_construction_result value = 2 }
  set_variable = { name = sed_construction_result_month value = sed_live_month_key }
 }
 remove_variable = sed_construction_intent_level
}

# Keep the first sample of each recorded month as the anchor. A second click in
# the same month cannot erase the baseline or pretend that a whole month passed.
sed_update_growth = {
 if = {
  limit = { NOT = { has_variable = sed_anchor_month } }
  set_variable = { name = sed_anchor_month value = var:sed_month_key }
  set_variable = { name = sed_anchor_gdp value = var:sed_gdp }
 }
 else_if = {
  limit = { var:sed_month_key > var:sed_anchor_month }
  set_variable = { name = sed_previous_month value = var:sed_anchor_month }
  set_variable = { name = sed_previous_gdp value = var:sed_anchor_gdp }
  set_variable = { name = sed_anchor_month value = var:sed_month_key }
  set_variable = { name = sed_anchor_gdp value = var:sed_gdp }
 }
 set_variable = { name = sed_growth_available value = 0 }
 set_variable = { name = sed_growth value = 0 }
 set_variable = { name = sed_growth_months value = 0 }
 if = {
  limit = { has_variable = sed_previous_gdp var:sed_previous_gdp > 0 }
  set_variable = { name = sed_growth value = { value = var:sed_gdp divide = var:sed_previous_gdp subtract = 1 } }
  set_variable = { name = sed_growth_months value = { value = var:sed_month_key subtract = var:sed_previous_month } }
  set_variable = { name = sed_growth_available value = 1 }
 }
}
'''
    supply_status = '\n'.join(
        f" set_variable = {{ name = sed_{item['good']}_action_status value = 0 }}"
        for item in SUPPLY_TARGETS)
    supply_lists = '\n'.join(
        f" clear_variable_list = sed_{item['good']}_candidates"
        for item in SUPPLY_TARGETS)
    supply_state_cleanup = '\n'.join(
        f"  remove_variable = sed_{item['good']}_{field}"
        for item in SUPPLY_TARGETS
        for field in ('request_pending', 'intent_level', 'intent_variant'))
    script = script.replace(
        ' set_variable = { name = sed_construction_action_status value = 0 }',
        ' set_variable = { name = sed_construction_action_status value = 0 }\n' + supply_status)
    script = script.replace(
        ' clear_variable_list = sed_construction_candidates',
        ' clear_variable_list = sed_construction_candidates\n' + supply_lists)
    # Supply markers belong to their own queued buildings. Clear them all only
    # when disabling, never when a construction-sector request resolves.
    script = script.replace(
        '__SUPPLY_STATE_CLEANUP__',
        supply_state_cleanup + '\n'
        + '\n'.join('  remove_variable = ' + name for name in IGNORED_VARIABLES))
    script = script.replace(
        '    set_variable = { name = sed_railway_action_status value = 1 }',
        '    set_variable = { name = sed_railway_action_status value = 1 }\n'
        '    if = { limit = { has_variable = sed_mode_automatic } set_variable = { name = sed_auto_action_status value = 1 } }')
    for item in SUPPLY_TARGETS:
        good = item['good']
        script = script.replace(
            f'    set_variable = {{ name = sed_{good}_action_status value = 1 }}',
            f'    set_variable = {{ name = sed_{good}_action_status value = 1 }}\n'
            '    if = { limit = { has_variable = sed_mode_automatic } set_variable = { name = sed_auto_action_status value = 1 } }')
    script = script.replace('  sed_refresh_supply_candidates = yes\n }\n}',
                            '  sed_refresh_supply_candidates = yes\n  sed_refresh_national_plan = yes\n  if = { limit = { has_variable = sed_coord_active } sed_coord_sync = yes }\n }\n}', 1)
    cleanup = '\n'.join(' clear_variable_list = ' + name for name in planning.lists(ACTION_NAMES))
    script = script.replace('sed_disable_country = {', 'sed_disable_country = {\n' + cleanup, 1)
    # All state-scoped planner variables are removed on deactivation.
    state_cleanup = '\n'.join('  remove_variable = ' + name for name in planning.state_variables(ACTION_NAMES))
    script = script.replace(' # Schema and automatic attempt month',
                            ' every_scope_state = {\n' + state_cleanup + '\n }\n # Schema and automatic attempt month', 1)
    return script + supply_effects() + preference_effects() + planning.effects(ACTION_NAMES, {item['good']: [variant['building'] for variant in variants(item)] for item in SUPPLY_TARGETS}) + construction_budget.effects() + planning.military_effects() + planning.tax_policy_effects() + planning.wage_policy_effects() + coordination.effects()


def scripted_guis():
    result = ''
    actions = {
        'refresh': ('has_variable = sed_enabled', 'sed_refresh_diagnostics = yes'),
        'show_details': ('has_variable = sed_enabled NOT = { has_variable = sed_details_visible }', 'set_variable = { name = sed_details_visible value = yes }'),
        'hide_details': ('has_variable = sed_enabled has_variable = sed_details_visible', 'remove_variable = sed_details_visible'),
        'coord_enable': ('has_variable = sed_enabled NOT = { has_variable = sed_coord_active } sed_coord_tools_available = yes', 'sed_coord_enable = yes'),
        'coord_release': ('has_variable = sed_enabled has_variable = sed_coord_active', 'sed_coord_restore = yes sed_set_mode_assisted = yes'),
        'disable': ('has_variable = sed_enabled', 'sed_disable_country = yes'),
        'manual_updates': ('has_variable = sed_enabled has_variable = sed_monthly_refresh', 'remove_variable = sed_monthly_refresh'),
        'monthly_updates': ('has_variable = sed_enabled NOT = { has_variable = sed_monthly_refresh }', 'set_variable = { name = sed_monthly_refresh value = yes } sed_refresh_diagnostics = yes'),
    }
    for name, (condition, effect) in actions.items():
        result += f'sed_{name}_sgui = {{\n scope = country\n is_shown = {{ is_player = yes {condition} }}\n is_valid = {{ is_player = yes {condition} }}\n effect = {{ {effect} }}\n}}\n'
    result += '''sed_approve_railway_sgui = {
 scope = state
 is_shown = { owner = { is_player = yes has_variable = sed_enabled } }
 is_valid = { owner = { has_variable = sed_mode_assisted } sed_railway_approval_valid = yes }
 effect = { if = { limit = { owner = { has_variable = sed_mode_assisted } sed_railway_approval_valid = yes } sed_run_railway_approval = yes } }
}
sed_approve_construction_sgui = {
 scope = state
 is_shown = { owner = { is_player = yes has_variable = sed_enabled } }
 is_valid = { owner = { has_variable = sed_mode_assisted } sed_construction_approval_valid = yes }
 effect = { if = { limit = { owner = { has_variable = sed_mode_assisted } sed_construction_approval_valid = yes } sed_run_construction_approval = yes } }
}
'''
    for mode in ('manual', 'assisted', 'automatic'):
        result += f'''sed_set_mode_{mode}_sgui = {{
 scope = country
 is_shown = {{ is_player = yes has_variable = sed_enabled }}
 is_valid = {{ is_player = yes has_variable = sed_enabled }}
 effect = {{ sed_set_mode_{mode} = yes }}
}}
sed_mode_{mode}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_mode_{mode} }} }}
'''
    for item in SUPPLY_TARGETS:
        good = item['good']
        result += f'''sed_approve_{good}_sgui = {{
 scope = state
 is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} }}
 is_valid = {{ owner = {{ has_variable = sed_mode_assisted }} sed_{good}_approval_valid = yes }}
 effect = {{ if = {{ limit = {{ owner = {{ has_variable = sed_mode_assisted }} sed_{good}_approval_valid = yes }} sed_run_{good}_approval = yes }} }}
}}
'''
    infrastructure_types = {'construction': ['building_construction_sector'],
                            **{item['good']: [variant['building'] for variant in variants(item)]
                               for item in SUPPLY_TARGETS}}
    for name, building_list in infrastructure_types.items():
        present = ' '.join(f'has_building = {building}' for building in building_list)
        result += f"""sed_{name}_infrastructure_blocked_sgui = {{
 scope = state
 is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }}
  OR = {{ {present} }} infrastructure_delta < 0
  NOT = {{ has_variable = sed_{name}_request_pending }}
  NOT = {{ has_variable = sed_{name}_ignored }} }}
}}
"""
    for name in ACTION_NAMES:
        owner = 'owner = { is_player = yes has_variable = sed_enabled }'
        switch = (owner + f' sed_{name}_candidate_eligible = yes '
                  'owner = { NOT = { has_variable = sed_mode_assisted } }')
        stale = (owner + f' NOT = {{ sed_{name}_candidate_eligible = yes }} '
                 f'NOT = {{ has_variable = sed_{name}_request_pending }}')
        result += f"""sed_{name}_ready_sgui = {{
 scope = state
 is_shown = {{ {owner} owner = {{ has_variable = sed_mode_assisted }} sed_{name}_approval_valid = yes }}
}}
sed_{name}_switch_assisted_sgui = {{
 scope = state
 is_shown = {{ {switch} }}
 is_valid = {{ {switch} }}
 effect = {{ if = {{ limit = {{ {switch} }} owner = {{ sed_set_mode_assisted = yes }} }} }}
}}
sed_{name}_refresh_card_sgui = {{
 scope = state
 is_shown = {{ {stale} }}
 is_valid = {{ {stale} }}
 effect = {{ if = {{ limit = {{ {stale} }} owner = {{ sed_refresh_diagnostics = yes }} }} }}
}}
"""
    for name in ACTION_NAMES:
        result += f"""sed_ignore_{name}_sgui = {{
 scope = state
 is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} sed_{name}_candidate_eligible = yes }}
 is_valid = {{ owner = {{ is_player = yes has_variable = sed_enabled }} sed_{name}_candidate_eligible = yes }}
 effect = {{ sed_ignore_{name} = yes }}
}}
"""
    ignored_conditions = ' '.join('has_variable = ' + name for name in IGNORED_VARIABLES)
    result += f"""sed_restore_ignored_sgui = {{
 scope = country
 is_shown = {{ is_player = yes has_variable = sed_enabled any_scope_state = {{ OR = {{ {ignored_conditions} }} }} }}
 is_valid = {{ is_player = yes has_variable = sed_enabled any_scope_state = {{ OR = {{ {ignored_conditions} }} }} }}
 effect = {{ sed_restore_ignored = yes }}
}}
"""
    # Hard blockers appear in order. A negative budget is a caution, not a
    # blocker. Pending actions and stale cards each have their own message.
    blocked = {
        'railway': {
            'private': 'owner = { construction_queue_num_queued_private_levels > 0 }',
            'default': 'owner = { construction_queue_num_queued_private_levels = 0 in_default = yes }',
        },
        'construction': {
            'queue': 'owner = { num_queued_government_constructions < 3 }',
            'private': 'owner = { num_queued_government_constructions >= 3 construction_queue_num_queued_private_levels > 0 }',
            'default': 'owner = { num_queued_government_constructions >= 3 construction_queue_num_queued_private_levels = 0 in_default = yes }',
        },
    }
    for action, guards in blocked.items():
        for guard, condition in guards.items():
            result += (f'sed_{action}_blocked_{guard}_sgui = {{\n scope = state\n'
                       f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_assisted }} sed_{action}_candidate_eligible = yes {condition} }}\n}}\n')
    for action in ('railway', 'construction'):
        result += (f'sed_{action}_stale_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} '
                   f'NOT = {{ sed_{action}_candidate_eligible = yes }} '
                   f'NOT = {{ has_variable = sed_{action}_request_pending }} }}\n}}\n')
        result += (f'sed_{action}_pending_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} '
                   f'has_variable = sed_{action}_request_pending }}\n}}\n')
        result += (f'sed_{action}_finance_caution_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled '
                   f'net_total_income < 0 }} }}\n}}\n')
    for item in SUPPLY_TARGETS:
        good = item['good']
        guards = {
            'private': 'owner = { construction_queue_num_queued_private_levels > 0 }',
            'default': 'owner = { construction_queue_num_queued_private_levels = 0 in_default = yes }',
        }
        for guard, condition in guards.items():
            result += (f'sed_{good}_blocked_{guard}_sgui = {{\n scope = state\n'
                       f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled has_variable = sed_mode_assisted }} sed_{good}_candidate_eligible = yes {condition} }}\n}}\n')
        result += (f'sed_{good}_stale_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} '
                   f'NOT = {{ sed_{good}_candidate_eligible = yes }} '
                   f'NOT = {{ has_variable = sed_{good}_request_pending }} }}\n}}\n')
        result += (f'sed_{good}_pending_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} '
                   f'has_variable = sed_{good}_request_pending }}\n}}\n')
        result += (f'sed_{good}_finance_caution_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled '
                   f'net_total_income < 0 }} }}\n}}\n')
    conditions = {
        'monthly': 'has_variable = sed_monthly_refresh',
        'manual': 'NOT = { has_variable = sed_monthly_refresh }',
        'default': 'var:sed_in_default = 1',
        'operating_deficit': 'var:sed_operating_balance < 0',
        'deficit': 'var:sed_balance < 0',
        'nonnegative': 'var:sed_balance >= 0',
        'debt_share': 'var:sed_debt_share_available = 1',
        'no_debt_share': 'var:sed_debt_share_available = 0',
        'runway': 'var:sed_reserve_weeks_available = 1',
        'no_runway': 'var:sed_reserve_weeks_available = 0',
        'per_capita': 'var:sed_per_capita_available = 1',
        'no_per_capita': 'var:sed_per_capita_available = 0',
        'growth': 'var:sed_growth_available = 1',
        'no_growth': 'var:sed_growth_available = 0',
        'recommendations': 'has_variable_list = sed_railway_candidates',
        'no_recommendations': 'NOT = { has_variable_list = sed_railway_candidates }',
        'no_infrastructure_opportunity': 'NOT = { has_variable_list = sed_railway_candidates } var:sed_infrastructure_short_states = 0',
        'no_railway_candidate': 'NOT = { has_variable_list = sed_railway_candidates } var:sed_infrastructure_short_states > 0',
        'railway_breakdown': 'NOT = { has_variable_list = sed_railway_candidates } var:sed_infrastructure_short_states > 0',
        'construction_recommendations': 'has_variable_list = sed_construction_candidates',
        'no_construction_queue': 'NOT = { has_variable_list = sed_construction_candidates } num_queued_government_constructions < 3',
        'no_construction_candidate': 'NOT = { has_variable_list = sed_construction_candidates } num_queued_government_constructions >= 3',
        'construction_breakdown': 'NOT = { has_variable_list = sed_construction_candidates } num_queued_government_constructions >= 3',
        'action_success': 'var:sed_railway_action_status = 1',
        'action_failed': 'var:sed_railway_action_status = 2',
        'construction_action_success': 'var:sed_construction_action_status = 1',
        'construction_action_failed': 'var:sed_construction_action_status = 2',
    }
    for name, condition in conditions.items():
        result += f'sed_{name}_visible_sgui = {{\n scope = country\n is_shown = {{ has_variable = sed_enabled {condition} }}\n}}\n'
    for item in SUPPLY_TARGETS:
        good = item['good']
        result += (f'sed_{good}_recommendations_visible_sgui = {{\n scope = country\n'
                   f' is_shown = {{ has_variable = sed_enabled has_variable_list = sed_{good}_candidates }}\n}}\n')
        result += (f'sed_{good}_section_visible_sgui = {{\n scope = country\n'
                   f' is_shown = {{ has_variable = sed_enabled market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} }}\n}}\n')
        result += (f'sed_{good}_no_candidates_visible_sgui = {{\n scope = country\n'
                   f' is_shown = {{ has_variable = sed_enabled market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} NOT = {{ has_variable_list = sed_{good}_candidates }} }}\n}}\n')
        result += (f'sed_{good}_action_success_visible_sgui = {{\n scope = country\n'
                   f' is_shown = {{ has_variable = sed_enabled var:sed_{good}_action_status = 1 }}\n}}\n')
        result += (f'sed_{good}_action_failed_visible_sgui = {{\n scope = country\n'
                   f' is_shown = {{ has_variable = sed_enabled var:sed_{good}_action_status = 2 }}\n}}\n')
    result += '''sed_auto_status_success_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 1 } }
sed_auto_status_no_action_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 2 } }
sed_auto_status_default_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 10 } }
sed_auto_status_queue_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 11 } }
sed_auto_status_paused_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 12 } }
sed_auto_status_competing_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 13 } }
sed_auto_status_safety_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 14 } }
sed_auto_status_unconfirmed_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 15 } }
sed_auto_status_month_limit_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 16 } }
'''
    base = 'is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic'
    for name, condition in {
        'pending': 'has_variable = sed_auto_event_pending',
        'idle': 'NOT = { has_variable = sed_auto_event_pending }',
        'unrecorded': 'NOT = { has_variable = sed_auto_review_status }',
    }.items():
        result += f'sed_auto_{name}_visible_sgui = {{ scope = country is_shown = {{ {base} {condition} }} }}\n'
    result += 'sed_auto_last_review_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status has_variable = sed_auto_review_year has_variable = sed_auto_review_month } }\n'
    result += f'sed_auto_builders_visible_sgui = {{ scope = country is_shown = {{ {base} sed_competing_builder_configured = yes }} }}\n'
    for name, option, pt, en in COMPETING_BUILDERS:
        result += f'sed_auto_builder_{name}_visible_sgui = {{ scope = country is_shown = {{ {base} has_variable = {option} }} }}\n'
    previous = ''
    for name, condition in [
        ('default', 'in_default = yes'),
        ('month_limit', 'sed_auto_month_limit_reached = yes'),
        ('queue', 'OR = { construction_queue_num_queued_government_levels > 0 construction_queue_num_queued_private_levels > 0 }'),
        ('paused', 'is_construction_paused = yes'),
        ('competing', 'AND = { sed_competing_builder_configured = yes NOT = { has_variable = sed_coord_active } }'),
        ('fiscal', 'OR = { AND = { has_variable = sed_coord_active NOT = { sed_coord_fiscal_safe = yes } } AND = { NOT = { has_variable = sed_coord_active } NOT = { sed_auto_fiscal_safe = yes } } }'),
        ('budget', 'AND = { OR = { NOT = { has_variable = sed_coord_active } var:sed_coord_executor = 11 } NOT = { sed_direct_budget_safe = yes } }'),
    ]:
        result += f'sed_auto_current_{name}_visible_sgui = {{ scope = country is_shown = {{ {base} {previous} {condition} }} }}\n'
        previous += f' NOT = {{ {condition} }}'
    result += f'sed_auto_current_clear_visible_sgui = {{ scope = country is_shown = {{ {base} sed_auto_executor_safe = yes }} }}\n'
    result += 'sed_auto_status_delegated_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 18 } }\n'
    for executor in range(13):
        result += f'sed_coord_executor_{executor}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_coord_active has_variable = sed_coord_executor var:sed_coord_executor = {executor} }} }}\n'
    for policy in (1, 2, 3):
        result += f'sed_coord_advisor_policy_{policy}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_coord_active has_variable = sed_coord_executor var:sed_coord_executor = 1 has_variable = sed_coord_advisor_policy var:sed_coord_advisor_policy = {policy} }} }}\n'
    result += 'sed_auto_status_unsupported_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 19 } }\n'
    result += 'sed_coord_supply_policy_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_coord_active has_variable = sed_coord_supply_policy_saved } }\n'
    for policy in ('tax', 'wage'):
        result += f'sed_{policy}_last_command_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_{policy}_last_from has_variable = sed_{policy}_last_to has_variable = sed_{policy}_last_month has_variable = sed_{policy}_last_year }} }}\n'
    result += 'sed_auto_status_waiting_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 20 } }\n'
    result += 'sed_plan_waiting_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_plan_waiting var:sed_plan_waiting = 1 } }\n'
    for war in (0, 1):
        result += f'sed_military_war_{war}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_military_at_war var:sed_military_at_war = {war} }} }}\n'
    for posture in range(5):
        result += f'sed_military_posture_{posture}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_military_posture var:sed_military_posture = {posture} }} }}\n'
    for good, _, _ in planning.MILITARY_GOODS:
        result += f'sed_military_short_{good}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_military_short_{good} var:sed_military_short_{good} = 1 }} }}\n'
    result += 'sed_auto_status_reserve_queue_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 21 } }\n'
    result += 'sed_reserve_budget_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_plan_year net_total_income < 0 } }\n'
    result += 'sed_auto_status_budget_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 22 } }\n'
    result += 'sed_build_budget_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_build_budget_known var:sed_build_budget_known = 1 } }\n'
    result += 'sed_build_budget_unknown_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_build_budget_known var:sed_build_budget_known = 0 } }\n'
    result += 'sed_auto_status_fiscal_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_auto_review_status var:sed_auto_review_status = 17 } }\n'
    for status in range(1, 6):
        result += f'sed_fiscal_{status}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_fiscal_status var:sed_fiscal_status = {status} }} }}\n'
    for goal in range(10):
        result += f'sed_goal_{goal}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_plan_goal var:sed_plan_goal = {goal} }} }}\n'
    for item in SUPPLY_TARGETS:
        name = item['good']
        result += f'sed_meta_{name}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_{name}_meta_year var:sed_{name}_meta_year = year }} }}\n'
    for item in SUPPLY_TARGETS:
        name = item['good']
        result += f'sed_book_{name}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_{name}_intents var:sed_{name}_intents > 0 }} }}\n'
    for name in ('railway', 'construction'):
        result += f'sed_book_{name}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_{name}_intents var:sed_{name}_intents > 0 }} }}\n'
    for item in SUPPLY_TARGETS:
        name = item['good']
        result += f'sed_plan_missing_{name}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_plan_missing_{name} var:sed_plan_missing_{name} = 1 }} }}\n'
    result += 'sed_plan_empty_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_plan_count var:sed_plan_count = 0 } }\n'
    for rank in planning.RANKS:
        result += f'sed_plan_rank_{rank}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable = sed_plan_count var:sed_plan_count >= {rank} }} }}\n'
    for rank in planning.RANKS:
        for name in ACTION_NAMES:
            result += f'sed_plan_{rank}_{name}_visible_sgui = {{ scope = country is_shown = {{ has_variable = sed_enabled has_variable_list = sed_plan_{rank}_{name} }} }}\n'
    for name in ACTION_NAMES:
        result += f'sed_plan_{name}_score_visible_sgui = {{ scope = state is_shown = {{ owner = {{ has_variable = sed_enabled }} has_variable = sed_plan_{name}_score var:sed_plan_{name}_score > 0 }} }}\n'
    result += 'sed_tax_policy_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_mode_automatic } }\n'
    result += 'sed_details_visible_sgui = { scope = country is_shown = { has_variable = sed_enabled has_variable = sed_details_visible } }\n'
    return '# Generated by tools/build_mod.py.\n' + result


def scripted_triggers():
    return '''# State scope. Candidate is limited to an operating railway with a live infrastructure deficit.
sed_railway_candidate_eligible = {
 is_incorporated = yes
 infrastructure_delta < 0
 NOT = { has_variable = sed_railway_ignored }
 NOT = { has_variable = sed_railway_request_pending }
 has_building = building_railway
 b:building_railway = {
  level > 0
  occupancy >= 0.8
  has_failed_hires = no
  building_has_goods_shortage = no
  level_after_queued_constructions <= level
 }
 can_construct_building = building_railway
}

sed_railway_approval_valid = {
 sed_railway_candidate_eligible = yes
 OR = { owner = { NOT = { has_variable = sed_coord_active } } var:sed_plan_railway_rank = 1 }
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }
}

# State scope. A staffed construction sector in a populous incorporated state.
sed_construction_candidate_eligible = {
 is_incorporated = yes
 infrastructure_delta >= 0
 NOT = { has_variable = sed_construction_ignored }
 NOT = { has_variable = sed_construction_request_pending }
 has_building = building_construction_sector
 b:building_construction_sector = {
  level > 0
  occupancy >= 0.9
  has_failed_hires = no
  building_has_goods_shortage = no
  level_after_queued_constructions <= level
 }
 can_construct_building = building_construction_sector
}

sed_construction_approval_valid = {
 sed_construction_candidate_eligible = yes
 OR = { owner = { NOT = { has_variable = sed_coord_active } } var:sed_plan_construction_rank = 1 }
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  num_queued_government_constructions >= 3
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }
}
''' + supply_triggers()


def supply_triggers():
    result = []
    for item in SUPPLY_TARGETS:
        good = item['good']
        vs = variants(item)
        alternatives = ' '.join(f'sed_{good}_{variant_id(variant)}_eligible = yes' for variant in vs)
        military_gate = ('owner = { military_expenses > 0 market = { mg:' + good + ' ?= { market_goods_buy_orders > 0 } } }'
                         if good in planning.MILITARY_INDUSTRY_GOODS else '')
        result.append(f'''# State scope: expand an operating local producer only while its market good is scarce.
sed_{good}_candidate_eligible = {{
 is_incorporated = yes
 infrastructure_delta >= 0
 NOT = {{ has_variable = sed_{good}_ignored }}
 NOT = {{ has_variable = sed_{good}_request_pending }}
{military_gate}
 owner = {{ market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} }}
 OR = {{ {alternatives} }}
}}
''')
        queued_variants = ' '.join(
            f"AND = {{ has_building = {variant['building']} b:{variant['building']} = {{ "
            f"level_after_queued_constructions > level OR = {{ {variant_methods(variant)} }} }} }}"
            for variant in vs)
        result.append(f'sed_{good}_queued_supply = {{ OR = {{ {queued_variants} }} }}\n')
        for variant in vs:
            building = variant['building']
            methods = variant_methods(variant, '  ')
            result.append(f'''# State scope: one verified producer type for {good}; output checked by active method.
sed_{good}_{variant_id(variant)}_eligible = {{
 has_building = {building}
 b:{building} = {{
  level > 0
  occupancy >= 0.8
  has_failed_hires = no
  building_has_goods_shortage = no
  level_after_queued_constructions <= level
  OR = {{
{methods}
  }}
 }}
 can_construct_building = {building}
}}
''')
        result.append(f'''sed_{good}_approval_valid = {{
 sed_{good}_candidate_eligible = yes
 OR = {{ owner = {{ NOT = {{ has_variable = sed_coord_active }} }} var:sed_plan_{good}_rank = 1 }}
 owner = {{
  is_player = yes
  has_variable = sed_enabled
  NOT = {{ in_default = yes }}
  construction_queue_num_queued_private_levels = 0
  sed_execution_mode_permits_approval = yes
 }}
}}''')
    result.append('''# Country scope: prevent this executor from competing with known construction automations.
# Configuration guard, not a prediction that the other mod will build this tick.
# Supply Chain independent options remain enabled without its chains toggle.
sed_auto_month_limit_reached = {
 has_variable = sed_auto_last_attempt_month
 var:sed_auto_last_attempt_month = sed_live_month_key
}

# Require an explicit execution mode even when the effect is called directly.
# Manual wins if an inconsistent save contains multiple mode markers.
sed_execution_mode_permits_approval = {
 NOT = { has_variable = sed_mode_manual }
 OR = {
  AND = {
   has_variable = sed_mode_assisted
   NOT = { has_variable = sed_mode_automatic }
  }
  sed_auto_executor_safe = yes
 }
}

sed_auto_executor_safe = {
 is_player = yes
 has_variable = sed_enabled
 NOT = { has_variable = sed_mode_manual }
 NOT = { has_variable = sed_mode_assisted }
 OR = {
  NOT = { has_variable = sed_coord_active }
  AND = { has_variable = sed_coord_active var:sed_coord_executor = 11 var:sed_plan_goal = 2 sed_direct_supply_priority_exists = yes }
 }
 has_variable = sed_mode_automatic
 NOT = { sed_auto_month_limit_reached = yes }
 NOT = { in_default = yes }
 construction_queue_num_queued_government_levels = 0
 construction_queue_num_queued_private_levels = 0
 is_construction_paused = no
 NOT = { sed_competing_builder_configured = yes }
 sed_auto_fiscal_safe = yes
 sed_direct_budget_safe = yes
}''')
    priorities = '\n'.join(
        f'  any_scope_state = {{ var:sed_plan_{item["good"]}_rank = 1 sed_{item["good"]}_candidate_eligible = yes }}'
        for item in SUPPLY_TARGETS)
    result.append('sed_direct_supply_priority_exists = {\n OR = {\n' + priorities + '\n }\n}')
    options = '\n'.join(f'  has_variable = {option}' for name, option, pt, en in COMPETING_BUILDERS)
    result.append('sed_competing_builder_configured = {\n OR = {\n' + options + '\n }\n}')
    return '\n'.join(result).rstrip() + '\n' + planning.triggers() + construction_budget.triggers() + coordination.triggers()


def value(name, fmt='1'):
    return f"[JournalEntry.GetCountry.MakeScope.Var('sed_{name}').GetValue|{fmt}]"


def localization(language):
    pt = language == 'braz_por'
    v = value
    pairs = {
        'sed_ignore_recommendation': ('Ignorar esta expansão neste estado', 'Ignore this expansion in this state'),
        'sed_ignore_recommendation_tt': ('Retira esta expansão das recomendações e da automação neste estado até restaurar. Não cancela obras. A escolha vale nos três modos.', 'Removes this expansion from recommendations and automation in this state until restored. Does not cancel construction. Applies in all three modes.'),
        'sed_restore_ignored': ('Restaurar recomendações ignoradas', 'Restore ignored recommendations'),
        'sed_restore_ignored_tt': ('Remove todas as escolhas de ignorar nos estados atuais do país e atualiza a análise. Não enfileira obras.', 'Clears all ignore choices in the country’s current states and refreshes analysis. Does not queue construction.'),
        'sed_ignored_notice': ('Há expansões ignoradas por sua escolha. Elas não serão recomendadas nem executadas automaticamente até restaurar. Desativar o Director limpa essas escolhas.', 'Some expansions are ignored by your choice. They will not be recommended or executed automatically until restored. Disabling the Director clears these choices.'),
        'je_sed_diagnostics': ('Smart Economy Director', 'Smart Economy Director'),
        'je_sed_diagnostics_reason': ('Indicadores econômicos do país, atualizados sob solicitação ou todo mês.', 'National economic indicators, refreshed on request or monthly.'),
        'sed_activation_tt': ('Ative o Director pela decisão Ativar Smart Economy Director.', 'Use the Enable Smart Economy Director decision.'),
        'sed_disabled_desc': ('Diagnóstico desativado.', 'Diagnostics disabled.'),
        'sed_enable': ('Ativar Smart Economy Director', 'Enable Smart Economy Director'),
        'sed_enable_desc': ('Abre um diagnóstico econômico no diário e lê os indicadores atuais. A ativação é opcional, inclusive em saves existentes.', 'Opens an economic diagnosis in the journal and reads current indicators. Enabling is optional, including in existing saves.'),
        'sed_disable_decision': ('Desativar Smart Economy Director', 'Disable Smart Economy Director'),
        'sed_disable_decision_desc': ('Remove o diagnóstico e limpa seus indicadores e histórico. Para voltar, use a decisão de ativação.', 'Removes the diagnosis and clears its readings and history. Use the enable decision to return.'),
        'sed_title': ('Economia nacional — diagnóstico', 'National economy — diagnosis'),
        'sed_scope_note': ('Diagnóstico e recomendações. Assistido permite aprovação por botão; Automático pode enfileirar no máximo um nível por mês.', 'Economic diagnosis and recommendations. Assisted allows button approval; Automatic may queue at most one level per month.'),
        'sed_mode_title': ('Modo de operação', 'Operating mode'),
        'sed_mode_manual_button': ('Manual', 'Manual'),
        'sed_mode_manual_button_tt': ('Somente diagnóstico e recomendações sob solicitação. Nenhuma construção é aprovada ou executada automaticamente.', 'Diagnosis and recommendations on request only. No construction is approved or executed automatically.'),
        'sed_mode_assisted_button': ('Assistido', 'Assisted'),
        'sed_mode_assisted_button_tt': ('Mostra botões visíveis para você aprovar individualmente cada nível recomendado. Nenhuma ação econômica automática.', 'Shows visible buttons so you can approve each recommended level individually. No automatic economic action.'),
        'sed_mode_automatic_button': ('Automático', 'Automatic'),
        'sed_mode_automatic_button_tt': ('Revisa uma vez por mês e pode enfileirar no máximo um nível se houver escassez ou déficit de infraestrutura, a fila pública e privada estiverem vazias, o país não estiver em inadimplência e nenhum dos construtores conhecidos estiver ativo. Você pode voltar a Assistido ou Manual a qualquer momento.', 'Reviews once a month and may queue at most one level if a shortage or infrastructure deficit exists, both queues are empty, the country is not in default, and no known construction automation is active. You can switch back to Assisted or Manual at any time.'),
        'sed_mode_manual_status': ('Modo Manual ativo. O Director só atualiza diagnóstico e recomendações; os botões de ação ficam visíveis, mas desativados.', 'Manual mode is active. The Director only updates diagnosis and recommendations; action buttons remain visible but disabled.'),
        'sed_mode_assisted_status': ('Modo Assistido ativo. Você decide pelo botão visível de cada recomendação; a condição do país e a fila são revalidadas no clique.', 'Assisted mode is active. You decide with the visible button on each recommendation; country conditions and queues are rechecked on click.'),
        'sed_mode_automatic_status': ('Modo Automático ativo. Uma revisão mensal pode enfileirar no máximo um nível. A aprovação individual fica desativada enquanto este modo estiver ativo.', 'Automatic mode is active. A monthly review may queue at most one level. Individual approval is disabled while this mode is active.'),
        'sed_mode_approval_blocked': ('Ação individual disponível no modo Assistido. Os botões continuam visíveis nos outros modos.', 'Individual actions are available in Assisted mode. Buttons remain visible in the other modes.'),
        'sed_auto_status_success': ('A revisão automática adicionou um nível à fila pública. Confira o prédio e o prazo na fila do jogo.', 'The automatic review added one level to the government queue. Review the building and timing in the game queue.'),
        'sed_auto_status_no_action': ('A revisão mensal terminou sem uma ação elegível. Nenhuma construção foi enfileirada.', 'The monthly review found no eligible action. No construction was queued.'),
        'sed_auto_status_default': ('A revisão automática foi suspensa porque o país está em inadimplência.', 'The automatic review was suspended because the country is in default.'),
        'sed_auto_status_queue': ('A revisão automática não enfileirou obra: a fila pública ou privada já está ocupada.', 'The automatic review did not queue construction because the government or private queue is already occupied.'),
        'sed_auto_status_paused': ('A revisão automática não enfileirou obra porque a construção está pausada.', 'The automatic review did not queue construction because construction is paused.'),
        'sed_auto_status_competing': ('A revisão automática foi suspensa porque outra automação de construção conhecida está configurada.', 'The automatic review was suspended because another known construction automation is configured.'),
        'sed_auto_status_safety': ('A revisão automática foi suspensa por uma condição de segurança não classificada. Nenhuma obra foi enfileirada.', 'The automatic review was suspended by an unclassified safety condition. No construction was queued.'),
        'sed_auto_status_unconfirmed': ('A revisão automática selecionou uma expansão, mas não confirmou a inclusão na fila pública. Confira a fila do jogo. Esta revisão não tentou outra expansão.', 'The automatic review selected an expansion but did not confirm its addition to the government queue. Check the game queue. This review did not attempt another expansion.'),
        'sed_refresh': ('Atualizar diagnóstico', 'Refresh diagnosis'),
        'sed_refresh_tt': ('Lê novamente os indicadores. Não executa a revisão automática nem aprova obras.', 'Reads indicators again. Does not execute the automatic review or approve construction.'),
        'sed_disable': ('Desativar', 'Disable'),
        'sed_disable_tt': ('Limpa as leituras e o histórico do Director e encerra o diagnóstico.', 'Clear the Director’s readings and history and close the diagnosis.'),
        'sed_use_manual': ('Atualizar sob solicitação', 'Refresh on request'),
        'sed_use_manual_tt': ('Suspende as leituras mensais. Use Atualizar diagnóstico quando desejar uma nova leitura.', 'Suspend monthly readings. Use Refresh diagnosis whenever you want a new reading.'),
        'sed_use_monthly': ('Atualizar todo mês', 'Refresh every month'),
        'sed_use_monthly_tt': ('Atualiza agora e passa a ler os indicadores no pulso mensal.', 'Refresh now and read indicators on the monthly pulse.'),
        'sed_last_refresh': (f'Última leitura: {v("last_month", "0")}/{v("last_year", "0")}.', f'Last reading: {v("last_month", "0")}/{v("last_year", "0")}.'),
        'sed_schedule_monthly': ('Leitura mensal ativada. Os números representam a última leitura.', 'Monthly readings enabled. Figures represent the last reading.'),
        'sed_schedule_manual': ('Leitura sob solicitação. Os números ficam registrados até você atualizar.', 'Readings on request. Figures stay recorded until you refresh.'),
        'sed_default_warning': ('#N O país estava em inadimplência na última leitura.#!', '#N The country was in default at the last reading.#!'),
        'sed_operating_warning': ('#N O saldo sem itens temporários está negativo: há pressão além dos gastos temporários.#!', '#N The balance without temporary items is negative: pressure extends beyond temporary spending.#!'),
        'sed_deficit_warning': ('#warning O saldo semanal está negativo. Confira os compromissos e o orçamento antes de ampliar gastos.#!', '#warning The weekly balance is negative. Check commitments and the budget before increasing spending.#!'),
        'sed_nonnegative_note': ('O saldo semanal é não negativo. Isso, sozinho, não comprova sustentabilidade ou espaço para investir.', 'The weekly balance is nonnegative. This alone does not establish sustainability or room to invest.'),
        'sed_finance_title': ('Finanças públicas', 'Public finances'),
        'sed_development_title': ('Desenvolvimento e população', 'Development and population'),
        'sed_production_title': ('Construção e condições produtivas', 'Construction and production conditions'),
        'sed_debt_share_text': (f'Dívida / limite de crédito: {v("debt_share", "%1")}', f'Debt / credit limit: {v("debt_share", "%1")}'),
        'sed_debt_share_unavailable': ('Dívida / crédito: indisponível, limite de crédito não positivo.', 'Debt / credit: unavailable, credit limit is not positive.'),
        'sed_runway_text': (f'Reservas / déficit atual: {v("reserve_weeks")} semanas, mantendo o saldo atual e sem usar crédito.', f'Reserves / current deficit: {v("reserve_weeks")} weeks at the current balance, excluding credit.'),
        'sed_runway_unavailable': ('Reservas / déficit: não se aplica com saldo não negativo.', 'Reserves / deficit: not applicable with a nonnegative balance.'),
        'sed_per_capita_text': (f'PIB per capita: @money!{v("gdp_per_capita", "2")}', f'GDP per capita: @money!{v("gdp_per_capita", "2")}'),
        'sed_per_capita_unavailable': ('PIB per capita: indisponível, população não positiva.', 'GDP per capita: unavailable, population is not positive.'),
        'sed_growth_text': (f'Variação do PIB desde a leitura-base anterior: {v("growth", "%1")}. Distância entre os meses registrados: {v("growth_months", "0")}.', f'GDP change since the previous baseline reading: {v("growth", "%1")}. Recorded calendar-month separation: {v("growth_months", "0") }.'),
        'sed_growth_unavailable': ('Variação do PIB: aguarde uma leitura em outro mês com uma base positiva.', 'GDP change: requires a reading in another month with a positive baseline.'),
        'sed_state_readings': (f'Estados analisados: {v("states", "0")} · Infraestrutura negativa: {v("infrastructure_short_states", "0")} · Acesso ao mercado abaixo de 100%: {v("low_access_states", "0")}', f'States examined: {v("states", "0")} · Negative infrastructure: {v("infrastructure_short_states", "0")} · Market access below 100%: {v("low_access_states", "0")}'),
        'sed_employment_readings': (f'Edifícios com insumos em falta: {v("shortage_buildings", "0")} · Contratação incompleta: {v("understaffed_buildings", "0")} · Falhas de contratação: {v("hiring_failure_buildings", "0")}', f'Buildings short of inputs: {v("shortage_buildings", "0")} · Incomplete staffing: {v("understaffed_buildings", "0")} · Failed hires: {v("hiring_failure_buildings", "0")}'),
        'sed_limitations_title': ('Como interpretar', 'How to interpret'),
        'sed_recommendations_title': ('Oportunidades de infraestrutura', 'Infrastructure opportunities'),
        'sed_recommendations_intro': ('Protótipo: até três ferrovias operantes em estados incorporados com infraestrutura negativa. A análise não calcula custo nem retorno; aprove uma ação por vez e confira o orçamento.', 'Prototype: up to three operating railways in incorporated states with negative infrastructure. The analysis does not calculate cost or return; approve one action at a time and review the budget.'),
        'sed_no_infrastructure_opportunity': ('Sem déficit atual de infraestrutura nos estados do país. O Director não recomenda expandir ferrovias agora.', 'No current infrastructure deficit in the country’s states. The Director does not recommend railway expansion now.'),
        'sed_no_railway_candidate': ('Há déficit de infraestrutura, mas nenhuma ferrovia passou pelos filtros de operação, contratação, insumos e fila.', 'Infrastructure deficits exist, but no railway passed the operation, hiring, input, and queue filters.'),
        'sed_railway_breakdown': (f'Estados com déficit de infraestrutura: {v("railway_deficit_states", "0")} · Sem ferrovia: {v("railway_no_railway_states", "0")} · Ferrovia não operante: {v("railway_not_ready_states", "0")} · Bloqueados por incorporação ou permissão: {v("railway_blocked_states", "0")}. Cada estado é contado por um motivo principal.', f'States with an infrastructure deficit: {v("railway_deficit_states", "0")} · No railway: {v("railway_no_railway_states", "0")} · Railway not operating: {v("railway_not_ready_states", "0")} · Blocked by incorporation or permission: {v("railway_blocked_states", "0")}. Each state is counted under one primary reason.'),
        'sed_railway_candidate_title': ('#bold [State.GetName]#! — saldo de infraestrutura: #v [State.GetInfrastructureBalance|0+=]#!', '#bold [State.GetName]#! — infrastructure balance: #v [State.GetInfrastructureBalance|0+=]#!'),
        'sed_railway_candidate_reason': ('A ferrovia está empregada, sem falta de insumos nem expansão já enfileirada. Um nível público pode aliviar o gargalo; o efeito e o custo futuros não são previstos.', 'The railway is staffed, has no input shortage, and has no queued expansion. One government level may relieve the bottleneck; future impact and cost are not forecast.'),
        'sed_approve_railway': ('Aprovar: enfileirar 1 nível público', 'Approve: queue 1 government level'),
        'sed_approve_railway_tt': ('Requer modo Assistido, país fora de inadimplência e fila privada vazia; estado e filas são revalidados no clique. Saldo semanal negativo gera um alerta financeiro, mas não bloqueia. Usa a fila normal do jogo.', 'Requires Assisted mode, no default, and an empty private queue; state and queues are rechecked on click. A negative weekly balance raises a caution but does not block. Uses the normal game queue.'),
        'sed_railway_blocked_private': ('Botão bloqueado: há níveis na fila privada.', 'Button blocked: the private queue has levels.'),
        'sed_railway_blocked_default': ('Botão bloqueado: o país está em inadimplência.', 'Button blocked: the country is in default.'),
        'sed_railway_stale': ('Esta recomendação mudou desde a última leitura. Nenhuma ação foi executada; atualize o diagnóstico para recalcular antes de aprovar.', 'This recommendation changed since the last reading. No action was executed; refresh the diagnosis before approving.'),
        'sed_railway_pending': ('Esta expansão já está na fila. Não aprove novamente; a marca será limpa numa leitura após concluir ou cancelar a obra.', 'This expansion is already queued. Do not approve again; the marker clears on a reading after completion or cancellation.'),
        'sed_railway_finance_caution': ('Alerta: o saldo semanal está negativo. A aprovação continua disponível; confira na fila o custo e o prazo antes de prosseguir.', 'Caution: the weekly balance is negative. Approval remains available; review the queue cost and timing before proceeding.'),
        'sed_railway_action_success': ('Pedido adicionado à fila pública. Confira os custos e o prazo na fila do jogo.', 'Request added to the government queue. Review cost and timing in the game queue.'),
        'sed_railway_action_failed': ('Inclusão não confirmada. Confira a fila antes de aprovar novamente.', 'Queue addition not confirmed. Inspect the queue before approving again.'),
        'sed_construction_title': ('Capacidade de construção', 'Construction capacity'),
        'sed_construction_intro': ('Protótipo: um setor de construção existente e empregado em estado incorporado, quando a fila pública tem pelo menos três projetos. A análise não calcula custo nem retorno; aprove uma ação por vez e confira o orçamento.', 'Prototype: one existing, staffed construction sector in an incorporated state when the government queue has at least three projects. The analysis does not calculate cost or return; approve one action at a time and review the budget.'),
        'sed_no_construction_queue': ('A fila pública tem menos de três projetos. O Director não recomenda ampliar a capacidade de construção agora.', 'The government queue has fewer than three projects. The Director does not recommend expanding construction capacity now.'),
        'sed_no_construction_candidate': ('Há fila pública suficiente, mas nenhum setor de construção passou pelos filtros de operação, contratação, insumos e fila.', 'The government queue is long enough, but no construction sector passed the operation, hiring, input, and queue filters.'),
        'sed_construction_breakdown': (f'Estados com setor de construção: {v("construction_sector_states", "0")} · Setor não operante: {v("construction_not_ready_states", "0")} · Bloqueados por incorporação ou permissão: {v("construction_blocked_states", "0")}. Cada estado é contado por um motivo principal.', f'States with a construction sector: {v("construction_sector_states", "0")} · Sector not operating: {v("construction_not_ready_states", "0")} · Blocked by incorporation or permission: {v("construction_blocked_states", "0")}. Each state is counted under one primary reason.'),
        'sed_construction_candidate_title': ('#bold [State.GetName]#! — setor de construção', '#bold [State.GetName]#! — construction sector'),
        'sed_construction_candidate_reason': ('O setor está empregado, sem falta de insumos nem expansão já enfileirada. Um nível público pode aumentar a capacidade; o efeito, o custo e o prazo futuros não são previstos.', 'The sector is staffed, has no input shortage, and has no queued expansion. One government level may raise capacity; future impact, cost, and timing are not forecast.'),
        'sed_approve_construction': ('Aprovar: enfileirar 1 nível do setor', 'Approve: queue 1 construction sector level'),
        'sed_approve_construction_tt': ('Requer modo Assistido, pelo menos três projetos na fila pública, país fora de inadimplência e fila privada vazia; estado e filas são revalidados no clique. Saldo semanal negativo gera um alerta financeiro, mas não bloqueia. Usa a fila normal do jogo.', 'Requires Assisted mode, at least three government projects queued, no default, and an empty private queue; state and queues are rechecked on click. A negative weekly balance raises a caution but does not block. Uses the normal game queue.'),
        'sed_construction_blocked_queue': ('Botão bloqueado: a fila pública tem menos de três projetos.', 'Button blocked: the government queue has fewer than three projects.'),
        'sed_construction_blocked_private': ('Botão bloqueado: há níveis na fila privada.', 'Button blocked: the private queue has levels.'),
        'sed_construction_blocked_default': ('Botão bloqueado: o país está em inadimplência.', 'Button blocked: the country is in default.'),
        'sed_construction_stale': ('Esta recomendação mudou desde a última leitura. Nenhuma ação foi executada; atualize o diagnóstico para recalcular antes de aprovar.', 'This recommendation changed since the last reading. No action was executed; refresh the diagnosis before approving.'),
        'sed_construction_pending': ('Esta expansão já está na fila. Não aprove novamente; a marca será limpa numa leitura após concluir ou cancelar a obra.', 'This expansion is already queued. Do not approve again; the marker clears on a reading after completion or cancellation.'),
        'sed_construction_finance_caution': ('Alerta: o saldo semanal está negativo. A aprovação continua disponível; confira na fila o custo e o prazo antes de prosseguir.', 'Caution: the weekly balance is negative. Approval remains available; review the queue cost and timing before proceeding.'),
        'sed_construction_action_success': ('Pedido do setor de construção adicionado à fila pública. Confira os custos e o prazo na fila do jogo.', 'Construction sector request added to the government queue. Review cost and timing in the game queue.'),
        'sed_construction_action_failed': ('Inclusão do setor não confirmada. Confira a fila antes de aprovar novamente.', 'Construction sector queue addition not confirmed. Inspect the queue before approving again.'),
        'sed_supply_title': ('Oferta para escassez de mercado', 'Supply for market shortages'),
        'sed_supply_intro': ('Aparece quando o mercado registra escassez e há um produtor local operante. A recomendação não prevê preço, retorno ou custo; o botão apenas enfileira um nível público após sua aprovação.', 'Shown when a market good is scarce and an operating local producer exists. The recommendation does not forecast prices, returns, or cost; the button only queues one government level after your approval.'),
        'sed_supply_no_candidate': ('Há escassez no mercado, mas nenhum produtor local passou pelos filtros de operação, incorporação e fila. O Director não sugere construir um prédio novo nesta versão.', 'The market reports a shortage, but no local producer passed the operation, incorporation, and queue filters. This version does not recommend a new building.'),
        'sed_supply_blocked_private': ('Botão bloqueado: esvazie a fila privada antes de usar a fila pública pelo Director.', 'Button blocked: clear the private queue before using the Director’s government queue.'),
        'sed_supply_blocked_default': ('Botão bloqueado: o país está em inadimplência.', 'Button blocked: the country is in default.'),
        'sed_supply_stale': ('A escassez ou as condições do prédio mudaram. Nenhuma ação foi executada; atualize o diagnóstico.', 'The shortage or building conditions changed. No action was executed; refresh the diagnosis.'),
        'sed_supply_pending': ('Esta expansão já está na fila. Aguarde sua conclusão ou cancelamento antes de aprovar outra.', 'This expansion is already queued. Wait for it to complete or be cancelled before approving another.'),
        'sed_supply_finance_caution': ('Alerta: o saldo semanal está negativo. A aprovação continua disponível; confira custo e prazo na fila do jogo.', 'Caution: the weekly balance is negative. Approval remains available; review cost and timing in the game queue.'),
        'sed_limitations': ('Protótipos limitados a ferrovias operantes com infraestrutura negativa, setores de construção operantes com fila pública de ao menos três projetos e produtores locais para madeira, ferro, carvão, cereais, tecido, ferramentas, mantimentos e roupas quando o mercado mostra escassez. As recomendações de oferta não estimam custo, retorno ou contratação futura. Aprovar apenas adiciona um nível à fila pública; custos e tempo dependem do jogo. Saldo negativo é aviso, não bloqueio; inadimplência e fila privada ocupada bloqueiam a aprovação. Qualificações, salários, desempregados e dependência externa ainda não são medidos diretamente. Variações de PIB podem refletir mudanças de fronteira e mercado.', 'Prototypes are limited to operating railways with negative infrastructure, operating construction sectors when the government queue has at least three projects, and local producers for wood, iron, coal, grain, fabric, tools, groceries, and clothes when the market reports a shortage. Supply recommendations do not estimate cost, returns, or future hiring. Approval only adds one level to the government queue; costs and timing depend on the game. A negative balance is a caution, not a blocker; default and a nonempty private queue block approval. Qualifications, wages, unemployment, and external dependence are not directly measured. GDP changes may reflect border and market changes.'),
    }
    for item in SUPPLY_TARGETS:
        good = item['good']
        label_pt, label_en = item['label_pt'], item['label_en']
        vs = variants(item)
        building_pt = ' / '.join(variant['building_pt'] for variant in vs)
        building_en = ' / '.join(variant['building_en'] for variant in vs)
        plural_pt = 'estados com ' + building_pt
        if len(vs) == 1:
            plural_en = 'states with a ' + vs[0]['building_en']
        elif len(vs) == 2:
            plural_en = 'states with a ' + vs[0]['building_en'] + ' or ' + vs[1]['building_en']
        else:
            plural_en = ('states with a ' + ', '.join(variant['building_en'] for variant in vs[:-1])
                         + ', or ' + vs[-1]['building_en'])
        pairs[f'sed_{good}_rejection_summary'] = (
            f"Última leitura — {plural_pt}: " + v(good + '_producer_states', '0')
            + '. Cada estado rejeitado é contado pelo primeiro motivo aplicável.',
            f"Last reading — {plural_en}: " + v(good + '_producer_states', '0')
            + '. Each rejected state is counted under its first applicable reason.')
        labels = [
            ('ignored_states', 'ignorado por você', 'ignored by you'),
            ('pending_states', 'expansão pendente ou enfileirada', 'pending or queued expansion'),
            ('unincorporated_states', 'estado não incorporado', 'unincorporated state'),
            ('understaffed_states', 'nível zero ou ocupação abaixo de 80%', 'zero level or occupancy below 80%'),
            ('hiring_states', 'falha de contratação', 'failed hires'),
            ('input_states', 'falta de insumos', 'input shortage'),
            ('method_states', 'método ativo sem produção confirmada do bem', 'active method without confirmed output of this good'),
            ('permission_states', 'construção não permitida', 'construction not allowed'),
            ('infrastructure_states', 'déficit de infraestrutura', 'infrastructure deficit'),
        ]
        pairs[f'sed_{good}_rejection_details'] = tuple(
            '; '.join(label[language_index] + ': ' + v(good + '_' + label[0], '0')
                      for label in labels) + '.' for language_index in (1, 2))
        if len(vs) > 1:
            title_pt = f'#bold [State.GetName]#! — produtor de {label_pt}'
            title_en = f'#bold [State.GetName]#! — {label_en} producer'
            approve_pt = f'Aprovar: enfileirar 1 nível do produtor de {label_pt}'
            approve_en = f'Approve: queue 1 {label_en} producer level'
            success_pt = f'Pedido de expansão do produtor de {label_pt} adicionado à fila pública. Confira custo e prazo na fila do jogo.'
            success_en = f'{label_en.title()} producer expansion added to the government queue. Review cost and timing in the game queue.'
        else:
            title_pt = f'#bold [State.GetName]#! — {building_pt} → {label_pt}'
            title_en = f'#bold [State.GetName]#! — {building_en} → {label_en}'
            approve_pt = f'Aprovar: enfileirar 1 nível de {building_pt}'
            approve_en = f'Approve: queue 1 {building_en} level'
            success_pt = f'Pedido de expansão de {building_pt} adicionado à fila pública. Confira custo e prazo na fila do jogo.'
            success_en = f'{building_en.title()} expansion added to the government queue. Review cost and timing in the game queue.'
        pairs[f'sed_{good}_section_title'] = (f'Escassez no mercado: {label_pt}', f'Market shortage: {label_en}')
        pairs[f'sed_{good}_candidate_title'] = (title_pt, title_en)
        pairs[f'sed_{good}_candidate_reason'] = (f'O mercado está em escassez de {label_pt}. Este produtor está operante, sem falta de insumos nem expansão já enfileirada. Um nível pode ampliar a oferta; efeito e custo não são previstos.', f'The market reports a shortage of {label_en}. This producer is operating, has no input shortage, and has no expansion queued. One level may increase supply; impact and cost are not forecast.')
        pairs[f'sed_{good}_approve'] = (approve_pt, approve_en)
        pairs[f'sed_{good}_approve_tt'] = ('Requer modo Assistido, país fora de inadimplência e fila privada vazia. A escassez e o prédio existente são revalidados no clique; entre produtores alternativos, o Director usa o primeiro elegível. Saldo semanal negativo gera alerta, mas não bloqueia. Usa a fila normal do jogo.', 'Requires Assisted mode, no default, and an empty private queue. The shortage and existing building are rechecked on click; among alternative producers, the Director uses the first eligible one. A negative balance raises a caution but does not block. Uses the normal game queue.')
        pairs[f'sed_{good}_action_success'] = (success_pt, success_en)
        pairs[f'sed_{good}_action_failed'] = ('Inclusão não confirmada. Confira a fila antes de aprovar novamente.', 'Queue addition not confirmed. Inspect the queue before approving again.')
    pairs.update({
        'sed_title': ('Economia e construções', 'Economy and construction'),
        'sed_auto_status_month_limit': ('A revisão não tentou outra expansão: já houve uma tentativa automática neste mês.', 'The review did not attempt another expansion: an automatic attempt already occurred this month.'),
        'sed_auto_current_month_limit': ('Agora: limite mensal atingido. Uma nova tentativa automática só pode ocorrer em outro mês; aprovação manual continua no Assistido.', 'Now: the monthly limit is reached. A new automatic attempt requires a different month; manual approval remains available in Assisted.'),
        'sed_auto_pending': ('Revisão programada para 23 dias após o agendamento.', 'Review scheduled for 23 days after scheduling.'),
        'sed_auto_idle': ('Próxima revisão: aguardando o pulso mensal.', 'Next review: waiting for the monthly pulse.'),
        'sed_auto_unrecorded': ('Última revisão: sem registro nesta ativação.', 'Last review: no record in this activation.'),
        'sed_auto_last_review': ('Última revisão automática: ' + v('auto_review_month', '0') + '/' + v('auto_review_year', '0') + '. Resultado:', 'Last automatic review: ' + v('auto_review_month', '0') + '/' + v('auto_review_year', '0') + '. Result:'),
        'sed_auto_current_default': ('Agora: país em inadimplência. A execução automática está bloqueada.', 'Now: the country is in default. Automatic execution is blocked.'),
        'sed_auto_current_queue': ('Agora: filas ocupadas. O Automático aguarda.', 'Now: queues occupied. Automatic mode waits.'),
        'sed_auto_current_paused': ('Agora: a construção está pausada. A execução automática está bloqueada.', 'Now: construction is paused. Automatic execution is blocked.'),
        'sed_auto_current_competing': ('Agora: outro construtor conhecido está configurado. A execução automática está bloqueada.', 'Now: another known builder is configured. Automatic execution is blocked.'),
        'sed_auto_current_clear': ('Agora: sem trava operacional conhecida. Falta avaliar candidatos.', 'Now: no known operational blocker. Candidates still need evaluation.'),
        'sed_candidate_infrastructure': ('Saldo atual de infraestrutura: [State.GetInfrastructureBalance|1+=]', 'Current infrastructure balance: [State.GetInfrastructureBalance|1+=]'),
        'sed_expansion_infrastructure_blocked': ('Infraestrutura em déficit. Resolva o gargalo antes de expandir neste estado.', 'Infrastructure is in deficit. Resolve the bottleneck before expanding in this state.'),
        'sed_approval_ready': ('Aprovação disponível: +1 nível público.', 'Approval available: +1 government level.'),
        'sed_switch_assisted': ('Passar para Assistido', 'Switch to Assisted'),
        'sed_switch_assisted_tt': ('Muda o país para o modo Assistido, sem aprovar obras. A próxima revisão automática não construirá enquanto este modo estiver ativo.', 'Changes the country to Assisted without approving construction. The next automatic review will not build while this mode remains active.'),
        'sed_refresh_card': ('Atualizar recomendações', 'Refresh recommendations'),
        'sed_refresh_card_tt': ('Relê as condições e recalcula os cartões. Não aprova obras; o cartão antigo pode desaparecer se deixou de ser elegível.', 'Reads conditions again and recalculates the cards. Does not approve construction; an old card may disappear if no longer eligible.'),
        'sed_open_queue': ('Abrir fila de construção', 'Open construction queue'),
        'sed_open_queue_tt': ('Abre a fila nativa do jogo para conferir os projetos públicos e privados.', 'Opens the native game queue to inspect government and private projects.'),
        'sed_show_details': ('Mostrar indicadores e detalhes', 'Show indicators and details'),
        'sed_show_details_tt': ('Abre indicadores, motivos detalhados e limites da análise abaixo das recomendações.', 'Shows indicators, detailed rejection reasons and analysis limits below recommendations.'),
        'sed_hide_details': ('Ocultar indicadores e detalhes', 'Hide indicators and details'),
        'sed_hide_details_tt': ('Recolhe os detalhes. As recomendações e os controles continuam disponíveis.', 'Collapses details. Recommendations and controls remain available.'),
        'sed_details_title': ('Indicadores e detalhes', 'Indicators and details'),
        'sed_dashboard_budget': ('Saldo: @money!' + v('balance', 'K') + '  |  Reservas: @money!' + v('gold', 'K'), 'Balance: @money!' + v('balance', 'K') + '  |  Reserves: @money!' + v('gold', 'K')),
        'sed_dashboard_queue': ('Projetos na fila — pública: ' + v('public_projects', '0') + '  |  privada: ' + v('private_projects', '0'), 'Queue projects — government: ' + v('public_projects', '0') + '  |  private: ' + v('private_projects', '0')),
        'sed_mode_manual_status': ('Manual: consulta e recomendações, sem executar obras.', 'Manual: readings and recommendations, without construction.'),
        'sed_mode_assisted_status': ('Assistido: você aprova uma expansão por botão.', 'Assisted: approve one expansion using its button.'),
        'sed_mode_automatic_status': ('Automático: até uma tentativa de expansão por mês.', 'Automatic: at most one expansion attempt per month.'),
        'sed_mode_approval_blocked': ('A aprovação individual requer o modo Assistido.', 'Individual approval requires Assisted mode.'),
        'sed_ignore_recommendation': ('Ignorar neste estado', 'Ignore in this state'),
        'sed_recommendations_intro': ('Expansões de ferrovias existentes quando falta infraestrutura. Aprovar adiciona um nível público.', 'Expand existing railways where infrastructure is insufficient. Approval adds one government level.'),
        'sed_construction_intro': ('Expandir um setor existente quando há pelo menos três projetos públicos.', 'Expand an existing sector when at least three government projects are queued.'),
        'sed_supply_intro': ('Expandir um produtor existente para um bem em escassez. Custos e retorno não são estimados.', 'Expand an existing producer for a scarce good. Costs and returns are not estimated.'),
        'sed_supply_no_candidate': ('Nenhum produtor elegível nesta leitura. Esta versão só expande prédios existentes.', 'No eligible producer in this reading. This version only expands existing buildings.'),
    })
    for name in ACTION_NAMES:
        key = f'sed_{name}_approve' if name not in ('railway', 'construction') else f'sed_approve_{name}'
        pairs[key] = ('Aprovar expansão: +1 nível', 'Approve expansion: +1 level')
    pairs.update({
        'sed_coord_advisor_policy_1': ('Orientação do Advisor aplicada para crescimento, orçamento equilibrado e endividamento desabilitado pela opção dele. O plano interno do Advisor reserva doze semanas de despesas fixas.', 'Advisor guidance applied for growth, balanced budget and borrowing disabled through its setting. The Advisor internal plan reserves twelve weeks of fixed expenses.'),
        'sed_coord_advisor_policy_2': ('Orientação do Advisor aplicada para padrão de vida, com orçamento equilibrado e opção de endividamento desabilitada. Bens essenciais lideram o plano.', 'Advisor guidance applied for standard of living, balanced budget and borrowing disabled. Essential goods lead the plan.'),
        'sed_coord_advisor_policy_3': ('Orientação do Advisor aplicada para retorno ao tesouro e preservação das reservas, com opção de endividamento desabilitada. A dívida atingiu ao menos 50% do crédito.', 'Advisor guidance applied for treasury return and reserve protection, with borrowing disabled. Debt reached at least 50% of credit.'),
    })
    pairs['sed_fiscal_5'] = (
        'Fiscal com construção financiada por reservas. Saldo operacional não negativo, sem dívida e ouro cobrindo doze semanas de despesas fixas mais 26 semanas do déficit observado. O Advisor pode avaliar investimentos com seu próprio orçamento quando a fila pública estiver livre. Os caminhos diretos e do Supply Chain exigem a guarda de saldo não negativo.',
        'Fiscal state with reserve-funded construction. Nonnegative operating balance, no debt and gold covering twelve weeks of fixed expenses plus 26 weeks of the observed deficit. The Advisor can assess investment using its own budget when the government queue is empty. Direct and Supply Chain paths require the nonnegative-balance guard.')
    pairs['sed_mode_automatic_button_tt'] = (
        'Coordena os construtores detectados e aplica a política fiscal. Impostos e salários civis admitem um ajuste por mês de calendário. Sair do Automático restaura as opções e níveis anteriores. O executor próprio admite uma tentativa de obra por mês. As ferramentas externas seguem seus próprios limites.',
        'Coordinates detected builders and applies fiscal policy. Taxes and civilian government wages allow one adjustment per calendar month. Leaving Automatic restores previous options and levels. The direct executor allows one construction attempt per month. External tools follow their own limits.')
    pairs['sed_mode_automatic_status'] = (
        'Automático ativo. As revisões periódicas atualizam plano, executor e política fiscal.',
        'Automatic is active. Periodic reviews update the plan, executor and fiscal policy.')
    pairs.update({
        'sed_coord_intro': ('No Automático, o Director coordena os construtores detectados e aplica a política fiscal. Voltar para Assistido ou Manual restaura suas opções e níveis originais.', 'In Automatic, the Director coordinates detected builders and applies fiscal policy. Returning to Assisted or Manual restores your original options and levels.'),
        'sed_coord_enable': ('Coordenar construtores externos', 'Coordinate external builders'),
        'sed_coord_enable_tt': ('Guarda as opções verificadas de construção, objetivo e orçamento, entra no Automático e configura um executor. Pode suspender rotinas de energia e administração que o plano ainda não cobre. Não inicia obra neste clique. Sair do Automático, desativar ou liberar restaura as opções originais, inclusive valores numéricos. Não controla PMs ou outros construtores.', 'Saves verified construction, objective and budget options, enters Automatic mode and configures one executor. May suspend power and administration routines not yet covered by the plan. Does not start construction on click. Leaving Automatic, disabling or releasing restores original options, including numeric values. Does not control PMs or other builders.'),
        'sed_coord_release': ('Restaurar opções e voltar ao Assistido', 'Restore options and return to Assisted'),
        'sed_coord_release_tt': ('Restaura as opções guardadas ao assumir o controle. Mudanças manuais feitas nessas opções coordenadas durante a coordenação serão substituídas pelas opções originais. Obras já na fila permanecem.', 'Restores options saved when taking control. Manual changes to these coordinated options during coordination will be replaced by the original options. Existing queued projects remain.'),
        'sed_coord_executor_0': ('Coordenação ativa: novas construções externas suspensas por finanças, ausência de prioridade ou executor disponível. Projetos existentes continuam. ARoAI e autoexpansões nativas não são controlados.', 'Coordination active: new external construction suspended for finances, lack of priority or available executor. Existing projects continue. ARoAI and native autoexpansion are not controlled.'),
        'sed_coord_executor_1': ('Executor escolhido pelo Director é o Economy Advisor. O Director aplica o objetivo e a política financeira mostrados abaixo. O Advisor escolhe prédios e estados pelos próprios critérios; o Director transmite orientação geral de investimento.', 'The Director selected Economy Advisor as executor. The Director applies the objective and financial policy shown below. The Advisor selects buildings and states using its own criteria; the Director transmits general investment guidance.'),
        'sed_coord_executor_2': ('Executor escolhido: Supply Chain, somente ferrovias, para aliviar infraestrutura. Aguarda a agenda e os filtros do Supply Chain.', 'Selected executor: Supply Chain, railways only, to relieve infrastructure. Waits for Supply Chain scheduling and filters.'),
        'sed_coord_executor_3': ('Executor escolhido: Supply Chain, cadeias produtivas. Categorias internas preservadas; o Director não força um prédio ou estado.', 'Selected executor: Supply Chain, production chains. Internal categories preserved; the Director does not force a building or state.'),
        'sed_coord_executor_5': ('Coordenação suspensa: construção do ARoAI detectada. Este adaptador controla somente Economy Advisor e Supply Chain; desligue o construtor do ARoAI para delegar com estes controles.', 'Coordination suspended: ARoAI construction detected. This adapter controls only Economy Advisor and Supply Chain; turn off the ARoAI builder to delegate using these controls.'),
        'sed_coord_executor_4': ('Executor escolhido: Supply Chain, setores de construção. A execução depende da agenda e do orçamento do Supply Chain.', 'Selected executor: Supply Chain, construction sectors. Execution depends on Supply Chain scheduling and budget.'),
        'sed_auto_status_delegated': ('Última revisão: orientação externa atualizada. Isto não confirma inclusão de obra; o executor escolhido tem agenda e filtros próprios.', 'Last review: external guidance updated. This does not confirm construction insertion; the selected executor has its own schedule and filters.'),
    })
    pairs.update({
        'sed_plan_title': ('Plano nacional — prioridades atuais', 'National plan — current priorities'),
        'sed_plan_date': ('Plano de ' + v('plan_month', '0') + '/' + v('plan_year', '0') + '.', 'Plan for ' + v('plan_month', '0') + '/' + v('plan_year', '0') + '.'),
        'sed_plan_policy': ('Até três expansões elegíveis, comparadas entre estados e setores. Pontos combinam déficit de infraestrutura, falta relativa de oferta e prioridade a bens essenciais. São uma regra inicial, não retorno previsto. Curto prazo: tratar a primeira prioridade; médio prazo: reavaliar oferta e infraestrutura após a obra; longo prazo: diversificação e desenvolvimento ainda sem modelo validado.', 'Up to three eligible expansions compared across states and sectors. Scores combine infrastructure deficit, relative supply gap and essential goods priority. Initial policy, not predicted returns. Short term: address first priority; medium term: reassess supply and infrastructure after construction; long term: diversification and development still lack a validated model.'),
        'sed_tax_policy': ('Impostos sob o Director: no Automático, uma alteração por revisão mensal. Sobe um nível em cautela, crise ou default; desce um nível com saldo positivo, sem dívida e reservas de doze semanas de despesas fixas. O nível original é restaurado ao sair do Automático ou desativar. Não altera despesas ou alíquotas de consumo.', 'Taxes under the Director: in Automatic, one change per monthly review. One step up under caution, crisis or default; one step down with positive balance, no debt and twelve weeks of fixed expenses in reserves. The original level is restored when leaving Automatic or disabling. Does not change spending or consumption tax rates.'),
        'sed_wage_policy': ('Salários do governo sob o Director: no Automático, caem um nível em crise ou default (mínimo baixo) e sobem um nível com saúde fiscal (máximo médio). O nível original é restaurado ao sair do Automático ou desativar. Salários militares e despesas não são alterados.', 'Government wages under the Director: in Automatic, one step down under crisis or default (floor low) and one step up with fiscal health (ceiling medium). The original level is restored when leaving Automatic or disabling. Military wages and spending are not changed.'),
        'sed_plan_empty': ('Sem expansão elegível no escopo atual. Não construir é um resultado válido; consulte os detalhes para os motivos.', 'No eligible expansion in the current scope. Not building is a valid outcome; see details for rejection reasons.'),
        'sed_fiscal_1': ('Fiscal: condições iniciais para expansão. Saldo e saldo operacional não negativos, reservas de ao menos quatro semanas de despesas fixas e dívida até 75% do crédito. Isso não garante capacidade de pagar a próxima obra.', 'Fiscal: initial expansion conditions. Nonnegative balance and operating balance, reserves covering at least four weeks of fixed expenses and debt up to 75% of credit. This does not guarantee affordability of the next project.'),
        'sed_fiscal_2': ('Fiscal: cautela. A política inicial suspende novas tentativas automáticas; aprovação Assistida continua explícita.', 'Fiscal: caution. Initial policy suspends new automatic attempts; Assisted approval remains explicit.'),
        'sed_fiscal_3': ('Fiscal: crise pela política inicial — déficit com menos de quatro semanas de reservas, dívida acima de 90% do crédito ou dívida sem limite de crédito positivo. Prioridade: estabilizar as finanças.', 'Fiscal: crisis under the initial policy — deficit with less than four weeks of reserves, debt above 90% of credit or debt without a positive credit limit. Priority: stabilize finances.'),
        'sed_fiscal_4': ('Fiscal: emergência por inadimplência. Nenhuma expansão autorizada.', 'Fiscal: default emergency. No expansion authorized.'),
        'sed_goal_0': ('Objetivo atual: observar e preservar recursos; sem expansão elegível.', 'Current objective: observe and preserve resources; no eligible expansion.'),
        'sed_goal_1': ('Objetivo atual: aliviar o gargalo de infraestrutura.', 'Current objective: relieve the infrastructure bottleneck.'),
        'sed_goal_2': ('Objetivo atual: reduzir escassez de bens com produtores viáveis.', 'Current objective: reduce goods shortages using viable producers.'),
        'sed_goal_3': ('Objetivo atual: ampliar capacidade para a demanda da fila pública, com aprovação Assistida.', 'Current objective: expand capacity for government queue demand, with Assisted approval.'),
        'sed_goal_4': ('Objetivo atual: estabilizar as finanças antes de ampliar compromissos.', 'Current objective: stabilize finances before expanding commitments.'),
        'sed_auto_current_fiscal': ('Agora: política fiscal bloqueia novas tentativas automáticas. Requer saldos não negativos, reservas de quatro semanas de despesas fixas e dívida até 75% do crédito. A política de impostos e salários civis continua ativa no Automático.', 'Now: fiscal policy blocks new automatic attempts. Requires nonnegative balances, reserves covering four weeks of fixed expenses and debt up to 75% of credit. Tax and civilian government wage policy remains active in Automatic.'),
        'sed_auto_status_fiscal': ('A última revisão não tentou obra por proteção fiscal.', 'The last review did not attempt construction because of fiscal protection.'),
    })
    pairs.update({
        'sed_goal_6': ('Objetivo atual: recuperar capacidade administrativa; burocracia nacional negativa.', 'Current objective: restore administrative capacity; national bureaucracy is negative.'),
        'sed_goal_7': ('Objetivo atual: recuperar capacidade tributária em estados incorporados. A ação depende da rotina tributária do Supply Chain.', 'Current objective: restore tax capacity in incorporated states. Action depends on the Supply Chain tax routine.'),
        'sed_goal_8': ('Objetivo atual: buscar crescimento e diversificação. Sem gargalo elegível no escopo direto, o executor externo avalia novos investimentos com seus próprios filtros.', 'Current objective: seek growth and diversification. With no eligible bottleneck in direct scope, the external executor evaluates new investment using its own filters.'),
        'sed_goal_9': ('Objetivo atual: investigar energia local cara, com preço ao menos 20% acima da base em algum estado. A ferramenta externa verifica viabilidade.', 'Current objective: investigate costly local power, priced at least 20% above base in a state. The external tool checks feasibility.'),
        'sed_coord_supply_policy': ('Política do Supply Chain sob o Director. Expansões em estados incorporados; administração trata o déficit atual de burocracia. Limites numéricos de construção em um nível por local escolhido, conforme a rotina externa. A soma nacional pode superar um nível. Tributação é avaliada em junho/dezembro e setores em fevereiro/agosto. Opções anteriores são restauradas ao sair do Automático.', 'Supply Chain policy under the Director. Expansion in incorporated states; administration addresses the current bureaucracy deficit. Numeric construction limits are one level per selected location, according to the external routine. The national total may exceed one level. Tax capacity is evaluated in June/December and construction sectors in February/August. Previous settings are restored when leaving Automatic.'),
        'sed_auto_current_budget': ('Agora: orçamento direto aguarda cobertura da referência de materiais, capacidade de construção ou método reconhecido. Confira os valores no plano nacional.', 'Now: direct execution awaits material-reference coverage, construction capacity or a recognized method. Check the national plan values.'),
        'sed_auto_status_budget': ('Última revisão: referência de materiais da próxima obra sem cobertura ou método de construção desconhecido. Nenhuma tentativa consumida. Confira o orçamento direto no plano.', 'Last review: next-project material benchmark is uncovered or construction method is unknown. No attempt consumed. See the direct budget in the plan.'),
        'sed_build_budget_unknown': ('Orçamento direto pendente. Um setor ativo usa método de construção fora dos quatro perfis verificados. O Automático direto aguarda uma leitura reconhecida; aprovação Assistida permanece explícita.', 'Direct budget pending. An active sector uses a construction method outside the four verified profiles. Direct Automatic awaits recognized data; Assisted approval remains explicit.'),
        'sed_build_budget': ('Referência conservadora para materiais da próxima obra direta: @money!' + v('build_budget_weekly', 'K') + '/semana, para até ' + v('build_budget_points', '1') + ' pontos. Teto de materiais pelos níveis e ocupação dos setores: @money!' + v('build_budget_material_capacity', 'K') + '/semana. Ouro exigido se o saldo não cobrir a referência: @money!' + v('build_budget_required_gold', 'K') + ', com ausência de dívida. Usa o maior custo entre métodos ativos, limitado pelos materiais dos setores existentes, com preços-base acrescidos de 75%. Pode superestimar; salários futuros, subsídios, modificadores e duração da obra ainda precisam ser avaliados.', 'Conservative material benchmark for the next direct project: @money!' + v('build_budget_weekly', 'K') + '/week, for up to ' + v('build_budget_points', '1') + ' points. Sector level/occupancy material cap: @money!' + v('build_budget_material_capacity', 'K') + '/week. Gold required if the balance does not cover the benchmark: @money!' + v('build_budget_required_gold', 'K') + ', with no debt. Uses the highest active-method cost, capped by existing sector materials, with base prices plus 75%. May overestimate; future wages, subsidies, modifiers and project duration still require assessment.'),
        'sed_coord_executor_12': ('Ritmo por reservas: aguardando a fila pública existente. Com déficit financiado por ouro, novas autorizações externas ficam suspensas enquanto houver níveis públicos enfileirados. A política fiscal continua ativa e o orçamento é reavaliado nas revisões.', 'Reserve-funded pace: waiting for the existing government queue. While gold funds a deficit, new external authorizations remain suspended while government levels are queued. Fiscal policy remains active and the budget is reassessed on reviews.'),
        'sed_auto_status_reserve_queue': ('Última revisão: preservação de reservas, aguardando obras públicas já enfileiradas antes de autorizar novos investimentos.', 'Last review: preserving reserves, waiting for already queued government projects before authorizing new investment.'),
        'sed_reserve_budget': ('Orçamento por reservas nesta leitura. Piso de doze semanas de despesas fixas: @money!' + v('reserve_floor', 'K') + '. Ouro acima do piso: @money!' + v('reserve_spare', 'K') + '. Cobertura do déficit atual acima do piso: ' + v('reserve_runway', '1') + ' semanas. Ouro exigido pela regra de 26 semanas: @money!' + v('reserve_required', 'K') + '. Estimativa com despesas e déficit atuais; custo de novas obras ainda precisa ser avaliado.', 'Reserve budget in this reading. Twelve-week fixed-expense floor: @money!' + v('reserve_floor', 'K') + '. Gold above the floor: @money!' + v('reserve_spare', 'K') + '. Current deficit coverage above the floor: ' + v('reserve_runway', '1') + ' weeks. Gold required by the 26-week rule: @money!' + v('reserve_required', 'K') + '. Estimate using current expenses and deficit; new construction costs still require assessment.'),
        'sed_coord_executor_11': ('Executor escolhido: Director, expansão da primeira prioridade de oferta. As opções verificadas de construção do Advisor e Supply Chain ficam suspensas. Aguarda orçamento e filas livres; no máximo uma tentativa por mês. O resultado da revisão confirma se houve inclusão.', 'Selected executor: Director, expansion of the first supply priority. Verified Advisor and Supply Chain construction options remain suspended. Waits for budget and empty queues; at most one attempt per month. The review outcome confirms insertion.'),
        'sed_coord_executor_10': ('Coordenação em espera. Há expansão enfileirada de um prédio relacionado ao objetivo atual. Novas opções externas ficam suspensas até reavaliar a fila ou surgir outra prioridade elegível.', 'Coordination waiting. A building related to the current objective has a queued expansion. New external options remain suspended until queue reassessment or another eligible priority appears.'),
        'sed_plan_waiting': ('Plano em acompanhamento de obra relacionada. A fila ainda não comprova resolução do gargalo. A autoria e o efeito futuro do projeto não foram identificados.', 'Plan monitoring related construction. The queue does not yet prove resolution of the bottleneck. Project origin and future impact have not been identified.'),
        'sed_auto_status_waiting': ('Última revisão: aguardando expansão relacionada ao objetivo. Reavalia após mudança da fila; nenhuma nova rotina externa autorizada nesta revisão.', 'Last review: waiting for an expansion related to the objective. Reassesses after queue changes; no new external routine authorized in this review.'),
        'sed_coord_executor_9': ('Objetivo identificado, execução pendente. Administração, capacidade tributária e energia exigem uma rotina específica do Supply Chain e condições fiscais próprias. A rotina necessária está indisponível ou bloqueada nesta leitura. Confira o objetivo no plano nacional.', 'Objective identified, execution pending. Administration, tax capacity and power require a dedicated Supply Chain routine and its fiscal conditions. The required routine is unavailable or blocked in this reading. See the national plan for the objective.'),
        'sed_auto_status_unsupported': ('Última revisão: objetivo identificado sem executor específico autorizado. A coordenação aguarda uma rotina compatível e condições fiscais para essa ação.', 'Last review: objective identified without an authorized dedicated executor. Coordination awaits a compatible routine and fiscal conditions for this action.'),
        'sed_coord_executor_6': ('Executor escolhido: Supply Chain, administração geral. Aguarda a agenda e os filtros de burocracia do Supply Chain.', 'Selected executor: Supply Chain, general administration. Waits for Supply Chain scheduling and bureaucracy filters.'),
        'sed_coord_executor_7': ('Executor escolhido: Supply Chain, administração tributária. Não altera impostos; busca capacidade administrativa conforme os filtros externos.', 'Selected executor: Supply Chain, tax administration. Does not change taxes; seeks administrative capacity using external filters.'),
        'sed_coord_executor_8': ('Executor escolhido: Supply Chain, energia. Preço local alto é sinal de investigação, não garantia de lucro ou falta física de oferta.', 'Selected executor: Supply Chain, power. High local price is a signal to investigate, not a guarantee of profit or physical shortage.'),
    })
    for policy, pt, en in (('tax', 'impostos', 'taxes'), ('wage', 'salários civis', 'civilian wages')):
        command_date = v(f'{policy}_last_month', '0') + '/' + v(f'{policy}_last_year', '0')
        levels = v(f'{policy}_last_from', '0') + ' → ' + v(f'{policy}_last_to', '0')
        pairs[f'sed_{policy}_last_command'] = (
            f'Último comando do Director para {pt}: ' + command_date + ', nível ' + levels + '. Escala de 1 (muito baixo) a 5 (muito alto). Confira o resultado no orçamento.',
            f'Last Director command for {en}: ' + command_date + ', level ' + levels + '. Scale from 1 (very low) to 5 (very high). Check the outcome in the budget.')
    pairs['sed_goal_5'] = ('Objetivo atual: investigar ausência dos produtores atendidos pelo protótipo para bens em escassez. A construção direta do Director ainda exige produtor existente; a ferramenta externa mantém sua própria seleção.', 'Current objective: investigate missing prototype-supported producers for scarce goods. Direct Director construction still requires an existing producer; the external tool keeps its own selection.')
    for item in SUPPLY_TARGETS:
        name = item['good']
        names_pt = [variant['building_pt'] for variant in variants(item)]
        names_en = [variant['building_en'] for variant in variants(item)]
        producers_pt = ', '.join(names_pt[:-1]) + (' ou ' if len(names_pt) > 1 else '') + names_pt[-1]
        producers_en = ', '.join(names_en[:-1]) + (' or ' if len(names_en) > 1 else '') + names_en[-1]
        pairs[f'sed_plan_missing_{name}'] = (f"Setor a investigar: {item['label_pt']} em escassez no mercado, sem produtor verificado ({producers_pt}) nos estados do país. Importação ou outros produtores podem suprir o bem; não é ordem de autossuficiência.", f"Sector to investigate: market shortage of {item['label_en']}, with no verified producer ({producers_en}) in the country's states. Imports or other producers may supply it; this is not a self-sufficiency mandate.")
        pairs[f'sed_book_{name}'] = (f"Histórico de {item['label_pt']}: {v(name + '_intents', '0')} pedidos, {v(name + '_completed', '0')} concluídos, {v(name + '_abandoned', '0')} abandonados. Conclusão inferida quando o nível do produtor sobe ao sair da fila; cancelamento ou obra externa podem distorcer a leitura.", f"{item['label_en'].capitalize()} history: {v(name + '_intents', '0')} requested, {v(name + '_completed', '0')} completed, {v(name + '_abandoned', '0')} abandoned. Completion is inferred when the producer level rises after leaving the queue; cancellation or external work can distort it.")
        pairs[f'sed_meta_{name}'] = (f"Meta industrial anual: ampliar a oferta de {item['label_pt']}. A escassez foi observada em três meses de calendário consecutivos; ele mantém prioridade no plano até o fim do ano. A meta não dispensa os filtros de trabalhadores, insumos, fila, infraestrutura e proteção fiscal.", f"Annual industrial goal: expand the supply of {item['label_en']}. Shortage was observed in three consecutive calendar months; it keeps priority in the plan until the end of the year. The goal does not bypass the worker, input, queue, infrastructure and fiscal guards.")
    pairs['sed_book_railway'] = (f"Histórico de ferrovias: {v('railway_intents', '0')} pedidos, {v('railway_completed', '0')} concluídos, {v('railway_abandoned', '0')} abandonados. Conclusão inferida quando o nível sobe ao sair da fila.", f"Railway history: {v('railway_intents', '0')} requested, {v('railway_completed', '0')} completed, {v('railway_abandoned', '0')} abandoned. Completion is inferred when the level rises after leaving the queue.")
    pairs['sed_book_construction'] = (f"Histórico de setores de construção: {v('construction_intents', '0')} pedidos, {v('construction_completed', '0')} concluídos, {v('construction_abandoned', '0')} abandonados. Conclusão inferida quando o nível sobe ao sair da fila.", f"Construction sector history: {v('construction_intents', '0')} requested, {v('construction_completed', '0')} completed, {v('construction_abandoned', '0')} abandoned. Completion is inferred when the level rises after leaving the queue.")
    for rank in planning.RANKS:
        pairs[f'sed_plan_rank_{rank}'] = (f'Prioridade {rank}', f'Priority {rank}')
    for name in ACTION_NAMES:
        score = f"[State.MakeScope.Var('sed_plan_{name}_score').GetValue|1]"
        pairs[f'sed_plan_{name}_score'] = ('Pontuação da última análise: ' + score + '. Custo incremental não estimado.', 'Last analysis score: ' + score + '. Incremental cost not estimated.')
    pairs['sed_auto_builders_title'] = ('Opções externas detectadas agora:', 'External options detected now:')
    pairs['sed_auto_builders_help'] = (
        'Sem coordenação ativa, opção ligada suspende a construção direta do Director. Na coordenação, esta lista mostra o executor autorizado. Sair do Automático restaura suas opções originais. Esta lista não confirma execução externa.',
        'Without active coordination, an enabled option suspends direct Director construction. During coordination, this list shows the authorized executor. Leaving Automatic restores original options. This list does not confirm external execution.')
    for name, option, pt_label, en_label in COMPETING_BUILDERS:
        pairs[f'sed_auto_builder_{name}'] = (pt_label, en_label)
    pairs['sed_railway_candidate_reason'] = ('Ferrovia operante em estado com déficit de infraestrutura. Custo e retorno não estimados.', 'Operating railway in a state with an infrastructure deficit. Cost and return not estimated.')
    pairs['sed_construction_candidate_reason'] = ('Setor operante e fila pública com demanda. Custo e contratação futura não estimados.', 'Operating sector with demand in the government queue. Cost and future hiring not estimated.')
    for item in SUPPLY_TARGETS:
        pairs[f"sed_{item['good']}_candidate_reason"] = (
            f"Escassez de {item['label_pt']}; produtor operante, sem falta de insumos ou expansão enfileirada.",
            f"Shortage of {item['label_en']}; operating producer, without input shortage or queued expansion.")
    for name in ('railway', 'construction'):
        key = f'sed_{name}_breakdown'
        pairs[key] = (pairs[key][0] + ' Ignorados por você: ' + v(name + '_ignored_states', '0') + '.',
                      pairs[key][1] + ' Ignored by you: ' + v(name + '_ignored_states', '0') + '.')
        if name == 'construction':
            pairs[key] = (pairs[key][0] + ' Déficit de infraestrutura: ' + v('construction_infrastructure_states', '0') + '.',
                          pairs[key][1] + ' Infrastructure deficit: ' + v('construction_infrastructure_states', '0') + '.')
    pairs.update({
        'sed_military_war_0': ('País em paz. Acompanhar o custo permanente das forças.', 'Country at peace. Monitor recurring force costs.'),
        'sed_military_war_1': ('País em guerra. Acompanhar abastecimento e custos de mobilização durante as próximas revisões.', 'Country at war. Monitor supply and mobilization costs in subsequent reviews.'),
        'sed_military_title': ('Economia militar e capacidade de modernização', 'Military economy and modernization capacity'),
        'sed_military_summary': ('Despesas militares semanais: @money!' + v('military_expenses', 'K') + '. Participação indicada pelo jogo: ' + v('military_share', '%1') + '. Bens militares em escassez: ' + v('military_shortage_count', '0') + '.', 'Weekly military expenses: @money!' + v('military_expenses', 'K') + '. Game expense share: ' + v('military_share', '%1') + '. Military goods in shortage: ' + v('military_shortage_count', '0') + '.'),
        'sed_military_posture_0': ('Diretriz militar: observar demanda; sem despesa militar positiva nesta leitura.', 'Military guidance: monitor demand; no positive military spending in this reading.'),
        'sed_military_posture_1': ('Diretriz militar: sustentar a força atual e acompanhar o abastecimento.', 'Military guidance: sustain current forces and monitor supply.'),
        'sed_military_posture_2': ('Diretriz militar: investigar abastecimento antes de ampliar compromissos. Há bens militares com demanda e escassez no mercado.', 'Military guidance: investigate supply before increasing commitments. Military goods have market demand and shortages.'),
        'sed_military_posture_3': ('Diretriz militar: estabilizar o orçamento e preservar o abastecimento da força atual. A avaliação fiscal está em crise ou o saldo operacional é negativo.', 'Military guidance: stabilize the budget and preserve current force supply. Fiscal assessment is in crisis or operating balance is negative.'),
        'sed_military_posture_4': ('Diretriz militar: orçamento permite estudar modernização. Há superávit, ausência de dívida e doze semanas de despesas fixas em reservas. Custo de uma modernização específica ainda precisa ser avaliado.', 'Military guidance: budget permits studying modernization. Positive balance, no debt and twelve weeks of fixed expenses in reserves. A specific modernization cost still requires assessment.'),
        'sed_military_scope': ('Avaliação econômica de apoio. Escassez é do mercado compartilhado; demanda das tropas nacionais ainda requer diagnóstico próprio. Armas, artilharia e munição podem gerar expansão de produtor existente com filtros de operação, insumos e orçamento. O executor externo mantém a própria seleção. Modernização das forças permanece pendente.', 'Supporting economic assessment. Shortages refer to the shared market; national troop demand still requires dedicated diagnosis. Arms, artillery and ammunition can yield existing-producer expansion with operation, input and budget filters. The external executor retains its own selection. Force modernization remains pending.'),
    })
    for good, pt, en in planning.MILITARY_GOODS:
        pairs[f'sed_military_short_{good}'] = (f'Abastecimento militar a investigar: {pt}, com demanda positiva e escassez no mercado.', f'Military supply to investigate: {en}, with positive demand and a market shortage.')
    for metric in METRICS:
        unit = metric['unit']
        fmt = {'money': 'K', 'money_week': 'K', 'count': '0', 'decimal': '1', 'ratio': '%1'}[unit]
        reading = ('@money!' if unit.startswith('money') else '') + v(metric['id'], fmt)
        pairs['sed_metric_' + metric['id']] = (metric['pt'] + ': ' + reading, metric['en'] + ': ' + reading)
    lines = [f'l_{language}:']
    for key, pair in pairs.items():
        text = pair[0 if pt else 1].replace('"', '\\"')
        lines.append(f' {key}:0 "{text}"')
    return '\n'.join(lines) + '\n'


def outputs():
    decisions = '''sed_enable = {
 is_shown = { is_player = yes NOT = { has_variable = sed_enabled } }
 possible = { is_player = yes NOT = { has_variable = sed_enabled } }
 when_taken = { hidden_effect = { sed_enable_country = yes } }
 ai_chance = { value = 0 }
}
sed_disable_decision = {
 is_shown = { is_player = yes has_variable = sed_enabled }
 possible = { is_player = yes has_variable = sed_enabled }
 when_taken = { sed_disable_country = yes }
 ai_chance = { value = 0 }
}
'''
    journal = '''je_sed_diagnostics = {
 icon = "gfx/interface/icons/generic_icons/gdp.dds"
 group = je_group_internal_affairs
 activation_description = { custom_tooltip = sed_activation_tt }
 widget = {
  gui = "gui/journal_entry_widgets/sed_diagnostics.gui"
  name = "sed_diagnostics_widget"
  container = "custom_widget_container_3"
 }
 is_shown_when_inactive = { is_player = yes has_variable = sed_enabled }
 possible = { is_player = yes has_variable = sed_enabled }
 disable_evaluation = { NOT = { has_variable = sed_enabled } }
 can_deactivate = yes
 should_be_pinned_by_default_uninvolved_or_context = yes
 outcome = {
  flags = { hidden invalid_outcome }
  conclusion_desc = "sed_disabled_desc"
  trigger = { NOT = { has_variable = sed_enabled } }
 }
 # Recurring reads belong ONLY to the country dispatcher, never to a second JE pulse.
}
'''
    on_actions = '''# Additive dispatcher; enabling is always an explicit player decision.
on_monthly_pulse_country = { on_actions = { sed_monthly_dispatcher } }
sed_monthly_dispatcher = {
 trigger = { is_player = yes has_variable = sed_enabled }
 effect = { sed_monthly_update = yes }
}
'''
    events = '''namespace = sed_pulse

# Run the Director's optional construction review after the other monthly builders.
sed_pulse.1 = {
 type = country_event
 hidden = yes
 trigger = { is_player = yes has_variable = sed_enabled }
 immediate = {
  remove_variable = sed_auto_event_pending
  if = {
   limit = { has_variable = sed_mode_automatic }
   sed_refresh_railway_candidates = yes
   sed_refresh_supply_candidates = yes
   sed_auto_apply_monthly = yes
  }
 }
}
'''
    result = {
        'common/decisions/sed_decisions.txt': decisions,
        'common/journal_entries/sed_journal_entries.txt': journal,
        'common/on_actions/sed_on_actions.txt': on_actions,
        'events/sed_events.txt': events,
        'common/scripted_effects/sed_effects.txt': effects(),
        'common/scripted_guis/sed_scripted_guis.txt': scripted_guis(),
        'common/scripted_triggers/sed_triggers.txt': scripted_triggers(),
        'common/script_values/sed_values.txt': '# Current calendar, independent of diagnostic refresh.\nsed_live_month_key = { value = year multiply = 12 add = month }\n',
        'gui/journal_entry_widgets/sed_diagnostics.gui': widget(),
        'localization/braz_por/sed_l_braz_por.yml': localization('braz_por'),
        'localization/english/sed_l_english.yml': localization('english'),
    }
    encoded = {path: b'\xef\xbb\xbf' + text.encode() for path, text in result.items()}
    descriptor = f'version="{VERSION}"\nname="Smart Economy Director"\ntags={{ "Economy" "Utilities" "UI" }}\nsupported_version="1.15.*"\n'
    encoded['descriptor.mod'] = descriptor.encode()
    encoded['Smart Economy Director.mod'] = (descriptor + 'path="mod/Smart Economy Director"\n').encode()
    metadata = {'name': 'Smart Economy Director', 'id': 'sed.smart_economy_director',
                'version': VERSION, 'supported_game_version': '1.15.*',
                'short_description': 'Economic recommendations with individually approved construction actions.',
                'tags': ['Economy', 'Utilities', 'UI'], 'relationships': [],
                'game_custom_data': {'multiplayer_synchronized': True}}
    encoded['.metadata/metadata.json'] = (json.dumps(metadata, indent=2) + '\n').encode()
    return encoded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail on stale artifacts without writing')
    args = parser.parse_args()
    stale = []
    for name, data in outputs().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_bytes() != data:
                path.write_bytes(data)
    if stale:
        raise SystemExit('Stale generated artifacts: ' + ', '.join(stale))
    print('Generated artifacts are current.' if args.check else 'Built Smart Economy Director ' + VERSION)


if __name__ == '__main__':
    main()
