"""Build the diagnostics and approved-action prototype. Game files use UTF-8 BOM."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = json.loads((ROOT / 'data/metrics.json').read_text())
VERSION = '0.5.3'
SUPPLY_TARGETS = [
    {'good': 'wood', 'building': 'building_logging_camp', 'methods': ['pm_electric_saw_mills', 'pm_saw_mills', 'pm_simple_forestry'], 'label_pt': 'madeira', 'label_en': 'wood', 'building_pt': 'acampamento madeireiro', 'building_en': 'logging camp'},
    {'good': 'iron', 'building': 'building_iron_mine', 'methods': ['pm_atmospheric_engine_pump_building_iron_mine', 'pm_condensing_engine_pump_building_iron_mine', 'pm_diesel_pump_building_iron_mine', 'pm_dynamite_building_iron_mine', 'pm_nitroglycerin_building_iron_mine', 'pm_picks_and_shovels_building_iron_mine'], 'label_pt': 'ferro', 'label_en': 'iron', 'building_pt': 'mina de ferro', 'building_en': 'iron mine'},
    {'good': 'coal', 'building': 'building_coal_mine', 'methods': ['pm_atmospheric_engine_pump_building_coal_mine', 'pm_condensing_engine_pump_building_coal_mine', 'pm_diesel_pump_building_coal_mine', 'pm_dynamite_building_coal_mine', 'pm_nitroglycerin_building_coal_mine', 'pm_picks_and_shovels_building_coal_mine'], 'label_pt': 'carvão', 'label_en': 'coal', 'building_pt': 'mina de carvão', 'building_en': 'coal mine'},
    {'good': 'grain', 'building': 'building_wheat_farm', 'methods': ['pm_chemical_fertilizer', 'pm_simple_farming', 'pm_soil_enriching_farming'], 'label_pt': 'cereais', 'label_en': 'grain', 'building_pt': 'fazenda de trigo', 'building_en': 'wheat farm'},
    {'good': 'fabric', 'building': 'building_cotton_plantation', 'methods': ['automatic_irrigation_building_cotton_plantation', 'default_building_cotton_plantation', 'slave_exploitation_cotton', 'worker_exploitation_cotton'], 'label_pt': 'tecido', 'label_en': 'fabric', 'building_pt': 'plantação de algodão', 'building_en': 'cotton plantation'},
    {'good': 'tools', 'building': 'building_tooling_workshop', 'methods': ['pm_crude_tools', 'pm_pig_iron', 'pm_rubber_grips', 'pm_steel'], 'label_pt': 'ferramentas', 'label_en': 'tools', 'building_pt': 'oficina de ferramentas', 'building_en': 'tooling workshop'},
    {'good': 'groceries', 'building': 'building_food_industry', 'methods': ['pm_bakery', 'pm_baking_powder', 'pm_cannery', 'pm_cannery_fish', 'pm_sweeteners', 'pm_vacuum_canning', 'pm_vacuum_canning_principle_3'], 'label_pt': 'mantimentos', 'label_en': 'groceries', 'building_pt': 'indústria alimentícia', 'building_en': 'food industry'},
    {'good': 'clothes', 'building': 'building_textile_mill', 'methods': ['pm_dye_workshops', 'pm_electric_sewing_machines', 'pm_handsewn_clothes', 'pm_sewing_machines'], 'label_pt': 'roupas', 'label_en': 'clothes', 'building_pt': 'fábrica têxtil', 'building_en': 'textile mill'},
]
PERSISTENT_VARIABLES = ['sed_schema_version', 'sed_auto_last_attempt_month']
ACTION_NAMES = ('railway', 'construction') + tuple(item['good'] for item in SUPPLY_TARGETS)
IGNORED_VARIABLES = [f'sed_{name}_ignored' for name in ACTION_NAMES]
SUPPLY_DIAGNOSTICS = ('producer_states', 'ignored_states', 'pending_states', 'unincorporated_states',
                      'understaffed_states', 'hiring_states', 'input_states',
                      'method_states', 'permission_states')
STATE_VARIABLES = ['sed_railway_request_pending', 'sed_construction_request_pending'] + [
    f"sed_{item['good']}_request_pending" for item in SUPPLY_TARGETS] + IGNORED_VARIABLES
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
sed_construction_blocked_states
sed_queue_levels_before'''.split() + [
    'sed_supply_action_status',
    'sed_mode_manual', 'sed_mode_assisted', 'sed_mode_automatic',
    'sed_auto_action_status', 'sed_auto_event_pending', 'sed_details_visible',
    'sed_auto_review_status', 'sed_auto_review_year', 'sed_auto_review_month',
    *[f"sed_{item['good']}_action_status" for item in SUPPLY_TARGETS],
    *[f"sed_{item['good']}_{reason}" for item in SUPPLY_TARGETS
      for reason in SUPPLY_DIAGNOSTICS],
]


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
        building = item['building']
        methods = ' '.join(f'has_active_production_method = {method}' for method in item['methods'])
        reasons = [
            ('ignored_states', f'has_variable = sed_{good}_ignored'),
            ('pending_states', f'OR = {{ has_variable = sed_{good}_request_pending b:{building} = {{ level_after_queued_constructions > level }} }}'),
            ('unincorporated_states', 'NOT = { is_incorporated = yes }'),
            ('understaffed_states', f'b:{building} = {{ OR = {{ level <= 0 occupancy < 0.8 }} }}'),
            ('hiring_states', f'b:{building} = {{ has_failed_hires = yes }}'),
            ('input_states', f'b:{building} = {{ building_has_goods_shortage = yes }}'),
            ('method_states', f'b:{building} = {{ NOT = {{ OR = {{ {methods} }} }} }}'),
            ('permission_states', f'NOT = {{ can_construct_building = {building} }}'),
        ]
        reset = '\n'.join(f' set_variable = {{ name = sed_{good}_{reason} value = 0 }}'
                          for reason in SUPPLY_DIAGNOSTICS)
        breakdown = f'''  if = {{
   limit = {{ has_building = {building} }}
   root = {{ change_variable = {{ name = sed_{good}_producer_states add = 1 }} }}
'''
        for index, (reason, condition) in enumerate(reasons):
            branch = 'if' if index == 0 else 'else_if'
            breakdown += f'''   {branch} = {{
    limit = {{ {condition} }}
    root = {{ change_variable = {{ name = sed_{good}_{reason} add = 1 }} }}
   }}
'''
        breakdown += '  }'
        result.extend([
            reset,
            f' clear_variable_list = sed_{good}_candidates',
            f''' every_scope_state = {{
  if = {{
   limit = {{ has_variable = sed_{good}_request_pending
    OR = {{ NOT = {{ has_building = {building} }} b:{building} = {{ level_after_queued_constructions <= level }} }}
   }}
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
        good, building = item['good'], item['building']
        result.append(f'''sed_run_{good}_approval = {{
 if = {{
  limit = {{ sed_{good}_approval_valid = yes }}
  owner = {{ set_variable = {{ name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }} }}
  owner = {{ sed_record_auto_attempt = yes }}
  start_building_construction = {building}
  owner = {{
   if = {{
    limit = {{ construction_queue_num_queued_government_levels > var:sed_queue_levels_before }}
    set_variable = {{ name = sed_{good}_action_status value = 1 }}
    if = {{ limit = {{ has_variable = sed_mode_automatic }} set_variable = {{ name = sed_auto_action_status value = 1 }} }}
    prev = {{ set_variable = {{ name = sed_{good}_request_pending value = yes }} }}
   }}
   else = {{ set_variable = {{ name = sed_{good}_action_status value = 2 }} }}
   remove_variable = sed_queue_levels_before
  }}
 }}
}}''')
    mode_actions = []
    for mode in ('manual', 'assisted', 'automatic'):
        other_modes = [value for value in ('manual', 'assisted', 'automatic') if value != mode]
        cleanup = '\n'.join(f' remove_variable = sed_mode_{value}' for value in other_modes)
        mode_actions.append(f'''sed_set_mode_{mode} = {{
 remove_variable = sed_mode_{mode}{cleanup}
 set_variable = {{ name = sed_mode_{mode} value = yes }}
 set_variable = {{ name = sed_auto_action_status value = 0 }}
 if = {{ limit = {{ has_variable = sed_mode_automatic }} sed_schedule_auto_event = yes }}
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
 set_variable = { name = sed_auto_action_status value = 2 }
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
   limit = {{ any_scope_state = {{ {eligibility} = yes }} }}
   ordered_scope_state = {{
    limit = {{ {eligibility} = yes }}
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
 else_if = { limit = { OR = { has_variable = advisor_auto_construction_enabled has_variable = zw_var_expand_building has_variable = aroai_autobuild } } set_variable = { name = sed_auto_action_status value = 13 } }
 else = { set_variable = { name = sed_auto_action_status value = 14 } }
 # Preserve the result independently from mode controls and diagnostic refreshes.
 set_variable = { name = sed_auto_review_status value = var:sed_auto_action_status }
 set_variable = { name = sed_auto_review_year value = year }
 set_variable = { name = sed_auto_review_month value = { value = month add = 1 } }
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
    body += 'flowcontainer = { direction = horizontal spacing = 10\n'
    for mode in ('manual', 'assisted', 'automatic'):
        body += mode_button(f'sed_mode_{mode}_button', f'sed_set_mode_{mode}_sgui')
    body += '}\n'
    for mode in ('manual', 'assisted', 'automatic'):
        body += textbox(f'sed_mode_{mode}_status', f'sed_mode_{mode}_visible_sgui')
    for state in ('pending', 'idle', 'unrecorded'):
        body += textbox(f'sed_auto_{state}', f'sed_auto_{state}_visible_sgui')
    for blocker in ('default', 'month_limit', 'queue', 'paused', 'competing', 'clear'):
        body += textbox(f'sed_auto_current_{blocker}', f'sed_auto_current_{blocker}_visible_sgui')
    body += textbox('sed_auto_last_review', 'sed_auto_last_review_visible_sgui')
    for status in ('success', 'no_action', 'default', 'queue', 'paused', 'competing', 'safety', 'unconfirmed', 'month_limit'):
        body += textbox(f'sed_auto_status_{status}', f'sed_auto_status_{status}_visible_sgui')
    body += 'flowcontainer = { direction = horizontal spacing = 12\n'
    body += button('sed_refresh', 'sed_refresh_sgui', width=244)
    body += button('sed_disable', 'sed_disable_sgui', width=244) + '}\n'
    body += button('sed_use_manual', 'sed_manual_updates_sgui')
    body += button('sed_use_monthly', 'sed_monthly_updates_sgui')
    body += textbox('sed_last_refresh')
    body += textbox('sed_dashboard_budget') + textbox('sed_dashboard_queue')
    body += button('sed_open_queue', 'sed_refresh_sgui', native_action="InformationPanelBar.OpenPanelTab('production_methods', 'construction_queues')")
    body += button('sed_show_details', 'sed_show_details_sgui')
    body += button('sed_hide_details', 'sed_hide_details_sgui')
    body += button('sed_restore_ignored', 'sed_restore_ignored_sgui')
    body += textbox('sed_ignored_notice', 'sed_restore_ignored_sgui')
    body += textbox('sed_default_warning', 'sed_default_visible_sgui')
    body += textbox('sed_deficit_warning', 'sed_deficit_visible_sgui')
    body += textbox('sed_recommendations_title', heading=True)
    body += textbox('sed_recommendations_intro')
    body += textbox('sed_no_infrastructure_opportunity', 'sed_no_infrastructure_opportunity_visible_sgui')
    body += textbox('sed_no_railway_candidate', 'sed_no_railway_candidate_visible_sgui')
    body += details(textbox('sed_railway_breakdown', 'sed_railway_breakdown_visible_sgui'))
    body += candidate_list('railway', 'sed_recommendations_visible_sgui')
    body += textbox('sed_railway_action_success', 'sed_action_success_visible_sgui')
    body += textbox('sed_railway_action_failed', 'sed_action_failed_visible_sgui')
    body += textbox('sed_construction_title', heading=True) + textbox('sed_construction_intro')
    body += textbox('sed_no_construction_queue', 'sed_no_construction_queue_visible_sgui')
    body += textbox('sed_no_construction_candidate', 'sed_no_construction_candidate_visible_sgui')
    body += details(textbox('sed_construction_breakdown', 'sed_construction_breakdown_visible_sgui'))
    body += candidate_list('construction', 'sed_construction_recommendations_visible_sgui')
    body += textbox('sed_construction_action_success', 'sed_construction_action_success_visible_sgui')
    body += textbox('sed_construction_action_failed', 'sed_construction_action_failed_visible_sgui')
    body += textbox('sed_supply_title', heading=True) + textbox('sed_supply_intro')
    for item in SUPPLY_TARGETS:
        good = item['good']
        body += textbox(f'sed_{good}_section_title', f'sed_{good}_section_visible_sgui', heading=True)
        body += candidate_list(good, f'sed_{good}_recommendations_visible_sgui')
        body += textbox('sed_supply_no_candidate', f'sed_{good}_no_candidates_visible_sgui')
        body += details(textbox(f'sed_{good}_rejection_summary', f'sed_{good}_no_candidates_visible_sgui')
                        + textbox(f'sed_{good}_rejection_details', f'sed_{good}_no_candidates_visible_sgui'))
        body += textbox(f'sed_{good}_action_success', f'sed_{good}_action_success_visible_sgui')
        body += textbox(f'sed_{good}_action_failed', f'sed_{good}_action_failed_visible_sgui')
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
''' + '\n'.join(' remove_variable = ' + name for name in country_variables()) + '''
 clear_variable_list = sed_railway_candidates
 clear_variable_list = sed_construction_candidates
 every_scope_state = {
  remove_variable = sed_railway_request_pending
  remove_variable = sed_construction_request_pending
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
   remove_variable = sed_railway_request_pending
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
 if = {
  limit = { sed_railway_approval_valid = yes }
  owner = {
   set_variable = { name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }
  }
  owner = { sed_record_auto_attempt = yes }
  start_building_construction = building_railway
  owner = {
   if = {
    limit = { construction_queue_num_queued_government_levels > var:sed_queue_levels_before }
    set_variable = { name = sed_railway_action_status value = 1 }
    prev = { set_variable = { name = sed_railway_request_pending value = yes } }
   }
   else = { set_variable = { name = sed_railway_action_status value = 2 } }
   remove_variable = sed_queue_levels_before
  }
 }
}

sed_refresh_construction_candidates = {
 clear_variable_list = sed_construction_candidates
 # Same primary-reason cascade as the railway counts. Only states that already
 # have a construction sector enter this denominator.
 set_variable = { name = sed_construction_ignored_states value = 0 }
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
   remove_variable = sed_construction_request_pending
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
 if = {
  limit = { sed_construction_approval_valid = yes }
  owner = {
   set_variable = { name = sed_queue_levels_before value = construction_queue_num_queued_government_levels }
  }
  owner = { sed_record_auto_attempt = yes }
  start_building_construction = building_construction_sector
  owner = {
   if = {
    limit = { construction_queue_num_queued_government_levels > var:sed_queue_levels_before }
    set_variable = { name = sed_construction_action_status value = 1 }
    prev = { set_variable = { name = sed_construction_request_pending value = yes } }
   }
   else = { set_variable = { name = sed_construction_action_status value = 2 } }
   remove_variable = sed_queue_levels_before
  }
 }
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
        f"  remove_variable = sed_{item['good']}_request_pending"
        for item in SUPPLY_TARGETS)
    script = script.replace(
        ' set_variable = { name = sed_construction_action_status value = 0 }',
        ' set_variable = { name = sed_construction_action_status value = 0 }\n' + supply_status)
    script = script.replace(
        ' clear_variable_list = sed_construction_candidates',
        ' clear_variable_list = sed_construction_candidates\n' + supply_lists)
    # Supply markers belong to their own queued buildings. Clear them all only
    # when disabling, never when a construction-sector request resolves.
    script = script.replace(
        '  remove_variable = sed_construction_request_pending\n }\n # Schema and automatic attempt month',
        '  remove_variable = sed_construction_request_pending\n' + supply_state_cleanup
        + '\n' + '\n'.join('  remove_variable = ' + name for name in IGNORED_VARIABLES)
        + '\n }\n # Schema and automatic attempt month', 1)
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
    return script + supply_effects() + preference_effects()


def scripted_guis():
    result = ''
    actions = {
        'refresh': ('has_variable = sed_enabled', 'sed_refresh_diagnostics = yes'),
        'show_details': ('has_variable = sed_enabled NOT = { has_variable = sed_details_visible }', 'set_variable = { name = sed_details_visible value = yes }'),
        'hide_details': ('has_variable = sed_enabled has_variable = sed_details_visible', 'remove_variable = sed_details_visible'),
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
    previous = ''
    for name, condition in [
        ('default', 'in_default = yes'),
        ('month_limit', 'sed_auto_month_limit_reached = yes'),
        ('queue', 'OR = { construction_queue_num_queued_government_levels > 0 construction_queue_num_queued_private_levels > 0 }'),
        ('paused', 'is_construction_paused = yes'),
        ('competing', 'OR = { has_variable = advisor_auto_construction_enabled has_variable = zw_var_expand_building has_variable = aroai_autobuild }'),
    ]:
        result += f'sed_auto_current_{name}_visible_sgui = {{ scope = country is_shown = {{ {base} {previous} {condition} }} }}\n'
        previous += f' NOT = {{ {condition} }}'
    result += f'sed_auto_current_clear_visible_sgui = {{ scope = country is_shown = {{ {base} sed_auto_executor_safe = yes }} }}\n'
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
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  construction_queue_num_queued_private_levels = 0
  OR = { NOT = { has_variable = sed_mode_automatic } NOT = { sed_auto_month_limit_reached = yes } }
 }
}

# State scope. A staffed construction sector in a populous incorporated state.
sed_construction_candidate_eligible = {
 is_incorporated = yes
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
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  num_queued_government_constructions >= 3
  construction_queue_num_queued_private_levels = 0
  OR = { NOT = { has_variable = sed_mode_automatic } NOT = { sed_auto_month_limit_reached = yes } }
 }
}
''' + supply_triggers()


def supply_triggers():
    result = []
    for item in SUPPLY_TARGETS:
        good, building = item['good'], item['building']
        methods = '\n'.join(f'    has_active_production_method = {method}' for method in item['methods'])
        result.append(f'''# State scope: expand an operating local producer only while its market good is scarce.
sed_{good}_candidate_eligible = {{
 is_incorporated = yes
 NOT = {{ has_variable = sed_{good}_ignored }}
 NOT = {{ has_variable = sed_{good}_request_pending }}
 owner = {{ market = {{ mg:{good} ?= {{ market_goods_has_goods_shortage = yes }} }} }}
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

sed_{good}_approval_valid = {{
 sed_{good}_candidate_eligible = yes
 owner = {{
  is_player = yes
  has_variable = sed_enabled
  NOT = {{ in_default = yes }}
  construction_queue_num_queued_private_levels = 0
  OR = {{ NOT = {{ has_variable = sed_mode_automatic }} NOT = {{ sed_auto_month_limit_reached = yes }} }}
 }}
}}''')
    result.append('''# Country scope: prevent this executor from competing with known construction automations.
sed_auto_month_limit_reached = {
 has_variable = sed_auto_last_attempt_month
 var:sed_auto_last_attempt_month = { value = year multiply = 12 add = month }
}

sed_auto_executor_safe = {
 has_variable = sed_mode_automatic
 NOT = { sed_auto_month_limit_reached = yes }
 NOT = { in_default = yes }
 construction_queue_num_queued_government_levels = 0
 construction_queue_num_queued_private_levels = 0
 is_construction_paused = no
 NOT = { has_variable = advisor_auto_construction_enabled }
 NOT = { has_variable = zw_var_expand_building }
 NOT = { has_variable = aroai_autobuild }
}''')
    return '\n'.join(result).rstrip() + '\n'


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
        'sed_auto_status_competing': ('A revisão automática foi suspensa porque outra automação de construção conhecida está ativa.', 'The automatic review was suspended because another known construction automation is active.'),
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
        building_pt, building_en = item['building_pt'], item['building_en']
        pairs[f'sed_{good}_rejection_summary'] = (
            f"Última leitura — estados com {building_pt}: " + v(good + '_producer_states', '0')
            + '. Cada estado rejeitado é contado pelo primeiro motivo aplicável.',
            f"Last reading — states with a {building_en}: " + v(good + '_producer_states', '0')
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
        ]
        pairs[f'sed_{good}_rejection_details'] = tuple(
            '; '.join(label[language_index] + ': ' + v(good + '_' + label[0], '0')
                      for label in labels) + '.' for language_index in (1, 2))
        pairs[f'sed_{good}_section_title'] = (f'Escassez no mercado: {label_pt}', f'Market shortage: {label_en}')
        pairs[f'sed_{good}_candidate_title'] = (f'#bold [State.GetName]#! — {building_pt} → {label_pt}', f'#bold [State.GetName]#! — {building_en} → {label_en}')
        pairs[f'sed_{good}_candidate_reason'] = (f'O mercado está em escassez de {label_pt}. Este produtor está operante, sem falta de insumos nem expansão já enfileirada. Um nível pode ampliar a oferta; efeito e custo não são previstos.', f'The market reports a shortage of {label_en}. This producer is operating, has no input shortage, and has no expansion queued. One level may increase supply; impact and cost are not forecast.')
        pairs[f'sed_{good}_approve'] = (f'Aprovar: enfileirar 1 nível de {building_pt}', f'Approve: queue 1 {building_en} level')
        pairs[f'sed_{good}_approve_tt'] = ('Requer modo Assistido, país fora de inadimplência e fila privada vazia. A escassez e o prédio são revalidados no clique. Saldo semanal negativo gera alerta, mas não bloqueia. Usa a fila normal do jogo.', 'Requires Assisted mode, no default, and an empty private queue. The shortage and building are rechecked on click. A negative balance raises a caution but does not block. Uses the normal game queue.')
        pairs[f'sed_{good}_action_success'] = (f'Pedido de expansão de {building_pt} adicionado à fila pública. Confira custo e prazo na fila do jogo.', f'{building_en.title()} expansion added to the government queue. Review cost and timing in the game queue.')
        pairs[f'sed_{good}_action_failed'] = ('Inclusão não confirmada. Confira a fila antes de aprovar novamente.', 'Queue addition not confirmed. Inspect the queue before approving again.')
    pairs.update({
        'sed_title': ('Economia e construções', 'Economy and construction'),
        'sed_auto_status_month_limit': ('A revisão não tentou outra expansão: já houve uma tentativa automática neste mês.', 'The review did not attempt another expansion: an automatic attempt already occurred this month.'),
        'sed_auto_current_month_limit': ('Agora: limite mensal atingido. Uma nova tentativa automática só pode ocorrer em outro mês; aprovação manual continua no Assistido.', 'Now: the monthly limit is reached. A new automatic attempt requires a different month; manual approval remains available in Assisted.'),
        'sed_auto_pending': ('Revisão agendada: atraso de 23 dias a partir do agendamento.', 'Review scheduled: a 23-day delay from scheduling.'),
        'sed_auto_idle': ('Próxima revisão: aguardando o pulso mensal.', 'Next review: waiting for the monthly pulse.'),
        'sed_auto_unrecorded': ('Última revisão: sem registro nesta ativação.', 'Last review: no record in this activation.'),
        'sed_auto_last_review': ('Última revisão automática: ' + v('auto_review_month', '0') + '/' + v('auto_review_year', '0') + '. Resultado:', 'Last automatic review: ' + v('auto_review_month', '0') + '/' + v('auto_review_year', '0') + '. Result:'),
        'sed_auto_current_default': ('Agora: país em inadimplência. A execução automática está bloqueada.', 'Now: the country is in default. Automatic execution is blocked.'),
        'sed_auto_current_queue': ('Agora: filas ocupadas. O Automático aguarda.', 'Now: queues occupied. Automatic mode waits.'),
        'sed_auto_current_paused': ('Agora: a construção está pausada. A execução automática está bloqueada.', 'Now: construction is paused. Automatic execution is blocked.'),
        'sed_auto_current_competing': ('Agora: outro construtor conhecido foi detectado. A execução automática está bloqueada.', 'Now: another known builder was detected. Automatic execution is blocked.'),
        'sed_auto_current_clear': ('Agora: sem trava operacional conhecida. Falta avaliar candidatos.', 'Now: no known operational blocker. Candidates still need evaluation.'),
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
