"""Build the diagnostics and approved-action prototype. Game files use UTF-8 BOM."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS = json.loads((ROOT / 'data/metrics.json').read_text())
VERSION = '0.3.3'
STATE_VARIABLES = ['sed_railway_request_pending', 'sed_construction_request_pending']
EXTRA_VARIABLES = '''sed_last_year sed_last_month sed_month_key sed_in_default
sed_gdp_per_capita sed_per_capita_available sed_debt_share sed_debt_share_available
sed_reserve_weeks sed_reserve_weeks_available sed_states sed_infrastructure_short_states
sed_low_access_states sed_shortage_buildings sed_understaffed_buildings
sed_hiring_failure_buildings sed_anchor_month sed_anchor_gdp sed_previous_month
sed_previous_gdp sed_growth sed_growth_months sed_growth_available
sed_railway_action_status sed_construction_action_status
sed_railway_deficit_states sed_railway_no_railway_states
sed_railway_not_ready_states sed_railway_blocked_states
sed_construction_sector_states sed_construction_not_ready_states
sed_construction_blocked_states
sed_queue_levels_before'''.split()


def runtime_variables():
    return ['sed_enabled', 'sed_monthly_refresh'] + [
        'sed_' + metric['id'] for metric in METRICS] + EXTRA_VARIABLES + STATE_VARIABLES


def country_variables():
    return ['sed_enabled', 'sed_monthly_refresh'] + [
        'sed_' + metric['id'] for metric in METRICS] + EXTRA_VARIABLES


def textbox(key, visibility=None, heading=False):
    shown = f'\n visible = "[{sgui(visibility, "IsShown")}]"' if visibility else ''
    return f'''textbox = {{{shown}
 autoresize = yes
 multiline = yes
 align = left|nobaseline
 using = {'fontsize_medium' if heading else 'fontsize_small'}
 minimumsize = {{ 500 -1 }}
 maximumsize = {{ 500 -1 }}
 text = "{key}"
}}
'''


def sgui(name, method):
    return f"GetScriptedGui('{name}').{method}(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)"


def button(key, action):
    return f'''button = {{
 size = {{ 244 32 }}
 using = select_button_sound
 using = tooltip_se
 text = "{key}"
 tooltip = "{key}_tt"
 visible = "[{sgui(action, 'IsShown')}]"
 enabled = "[{sgui(action, 'IsValid')}]"
 onclick = "[{sgui(action, 'Execute')}]"
}}
'''


def widget():
    body = textbox('sed_title', heading=True) + textbox('sed_scope_note')
    body += 'flowcontainer = { direction = horizontal spacing = 8\n'
    body += button('sed_refresh', 'sed_refresh_sgui') + button('sed_disable', 'sed_disable_sgui') + '}\n'
    body += button('sed_use_manual', 'sed_manual_updates_sgui')
    body += button('sed_use_monthly', 'sed_monthly_updates_sgui')
    body += textbox('sed_last_refresh')
    body += textbox('sed_schedule_monthly', 'sed_monthly_visible_sgui')
    body += textbox('sed_schedule_manual', 'sed_manual_visible_sgui')
    body += textbox('sed_default_warning', 'sed_default_visible_sgui')
    body += textbox('sed_operating_warning', 'sed_operating_deficit_visible_sgui')
    body += textbox('sed_deficit_warning', 'sed_deficit_visible_sgui')
    body += textbox('sed_nonnegative_note', 'sed_nonnegative_visible_sgui')
    sections = [('sed_finance_title', ['balance', 'operating_balance', 'fixed_expenses', 'gold', 'debt', 'credit']),
                ('sed_development_title', ['gdp', 'population', 'sol', 'literacy']),
                ('sed_production_title', ['construction', 'public_projects', 'private_projects'])]
    for title, metrics in sections:
        body += textbox(title, heading=True)
        for name in metrics:
            body += textbox('sed_metric_' + name)
        if title == 'sed_finance_title':
            for key, condition in [('sed_debt_share_text', 'sed_debt_share_visible_sgui'),
                                   ('sed_debt_share_unavailable', 'sed_no_debt_share_visible_sgui'),
                                   ('sed_runway_text', 'sed_runway_visible_sgui'),
                                   ('sed_runway_unavailable', 'sed_no_runway_visible_sgui')]:
                body += textbox(key, condition)
        if title == 'sed_development_title':
            for key, condition in [('sed_per_capita_text', 'sed_per_capita_visible_sgui'),
                                   ('sed_per_capita_unavailable', 'sed_no_per_capita_visible_sgui'),
                                   ('sed_growth_text', 'sed_growth_visible_sgui'),
                                   ('sed_growth_unavailable', 'sed_no_growth_visible_sgui')]:
                body += textbox(key, condition)
    body += textbox('sed_state_readings') + textbox('sed_employment_readings')
    body += textbox('sed_recommendations_title', heading=True)
    body += textbox('sed_recommendations_intro')
    body += textbox('sed_no_infrastructure_opportunity', 'sed_no_infrastructure_opportunity_visible_sgui')
    body += textbox('sed_no_railway_candidate', 'sed_no_railway_candidate_visible_sgui')
    body += textbox('sed_railway_breakdown', 'sed_railway_breakdown_visible_sgui')
    body += '''fixedgridbox = {
 visible = "[GetScriptedGui('sed_recommendations_visible_sgui').IsShown(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)]"
 datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('sed_railway_candidates')]"
 addcolumn = 500
 addrow = 166
 item = { sed_railway_candidate_item = {} }
}
'''
    body += textbox('sed_railway_action_success', 'sed_action_success_visible_sgui')
    body += textbox('sed_railway_action_failed', 'sed_action_failed_visible_sgui')
    body += textbox('sed_construction_title', heading=True)
    body += textbox('sed_construction_intro')
    body += textbox('sed_no_construction_queue', 'sed_no_construction_queue_visible_sgui')
    body += textbox('sed_no_construction_candidate', 'sed_no_construction_candidate_visible_sgui')
    body += textbox('sed_construction_breakdown', 'sed_construction_breakdown_visible_sgui')
    body += '''fixedgridbox = {
 visible = "[GetScriptedGui('sed_construction_recommendations_visible_sgui').IsShown(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)]"
 datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('sed_construction_candidates')]"
 addcolumn = 500
 addrow = 166
 item = { sed_construction_candidate_item = {} }
}
'''
    body += textbox('sed_construction_action_success', 'sed_construction_action_success_visible_sgui')
    body += textbox('sed_construction_action_failed', 'sed_construction_action_failed_visible_sgui')
    body += textbox('sed_limitations_title', heading=True) + textbox('sed_limitations')
    item_type = '''types sed_diagnostics_types {
 type sed_railway_candidate_item = flowcontainer {
  direction = vertical
  spacing = 4
  widget = {
   datacontext = "[Scope.GetState]"
   size = { 500 160 }
   background = { using = dark_area }
   flowcontainer = {
    position = { 8 4 }
    direction = vertical
    spacing = 4
    textbox = {
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_candidate_title"
    }
    textbox = {
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_candidate_reason"
    }
    button = {
     size = { 300 30 }
     using = select_button_sound
     using = tooltip_se
     text = "sed_approve_railway"
     tooltip = "sed_approve_railway_tt"
     visible = "[GetScriptedGui('sed_approve_railway_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     enabled = "[GetScriptedGui('sed_approve_railway_sgui').IsValid(GuiScope.SetRoot(State.MakeScope).End)]"
     onclick = "[GetScriptedGui('sed_approve_railway_sgui').Execute(GuiScope.SetRoot(State.MakeScope).End)]"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_railway_blocked_paused_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_blocked_paused"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_railway_blocked_private_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_blocked_private"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_railway_blocked_default_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_blocked_default"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_railway_blocked_balance_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_blocked_balance"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_railway_stale_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_railway_stale"
    }
   }
  }
 }
 type sed_construction_candidate_item = flowcontainer {
  direction = vertical
  spacing = 4
  widget = {
   datacontext = "[Scope.GetState]"
   size = { 500 160 }
   background = { using = dark_area }
   flowcontainer = {
    position = { 8 4 }
    direction = vertical
    spacing = 4
    textbox = {
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_candidate_title"
    }
    textbox = {
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_candidate_reason"
    }
    button = {
     size = { 300 30 }
     using = select_button_sound
     using = tooltip_se
     text = "sed_approve_construction"
     tooltip = "sed_approve_construction_tt"
     visible = "[GetScriptedGui('sed_approve_construction_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     enabled = "[GetScriptedGui('sed_approve_construction_sgui').IsValid(GuiScope.SetRoot(State.MakeScope).End)]"
     onclick = "[GetScriptedGui('sed_approve_construction_sgui').Execute(GuiScope.SetRoot(State.MakeScope).End)]"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_blocked_paused_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_blocked_paused"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_blocked_queue_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_blocked_queue"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_blocked_private_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_blocked_private"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_blocked_default_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_blocked_default"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_blocked_balance_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_blocked_balance"
    }
    textbox = {
     visible = "[GetScriptedGui('sed_construction_stale_sgui').IsShown(GuiScope.SetRoot(State.MakeScope).End)]"
     autoresize = yes
     multiline = yes
     align = left|nobaseline
     using = fontsize_small
     minimumsize = { 480 -1 }
     text = "sed_construction_stale"
    }
   }
  }
 }
}
'''
    return '# Generated by tools/build_mod.py.\n' + item_type + '\nflowcontainer = {\n name = "sed_diagnostics_widget"\n minimumsize = { 500 -1 }\n maximumsize = { 500 -1 }\n direction = vertical\n spacing = 6\n ignoreinvisible = yes\n' + body + '}\n'


def effects():
    readings = '\n'.join(f' # {m["source"]}\n set_variable = {{ name = sed_{m["id"]} value = {m["expression"]} }}' for m in METRICS)
    return '''# Generated by tools/build_mod.py. Country scope except state-targeted actions.
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
 # The schema marker is the only retained variable. Re-enable uses a decision.
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
 }
}

sed_refresh_diagnostics = {
 if = {
  limit = { is_player = yes has_variable = sed_enabled }
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
 }
}

sed_refresh_railway_candidates = {
 clear_variable_list = sed_railway_candidates
 # Counts use one primary reason per state so the breakdown adds up to the
 # deficit total instead of counting the same state under several filters.
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


def scripted_guis():
    result = ''
    actions = {
        'refresh': ('has_variable = sed_enabled', 'sed_refresh_diagnostics = yes'),
        'disable': ('has_variable = sed_enabled', 'sed_disable_country = yes'),
        'manual_updates': ('has_variable = sed_enabled has_variable = sed_monthly_refresh', 'remove_variable = sed_monthly_refresh'),
        'monthly_updates': ('has_variable = sed_enabled NOT = { has_variable = sed_monthly_refresh }', 'set_variable = { name = sed_monthly_refresh value = yes } sed_refresh_diagnostics = yes'),
    }
    for name, (condition, effect) in actions.items():
        result += f'sed_{name}_sgui = {{\n scope = country\n is_shown = {{ is_player = yes {condition} }}\n is_valid = {{ is_player = yes {condition} }}\n effect = {{ {effect} }}\n}}\n'
    result += '''sed_approve_railway_sgui = {
 scope = state
 is_shown = { owner = { is_player = yes has_variable = sed_enabled } }
 is_valid = { sed_railway_approval_valid = yes }
 effect = { if = { limit = { sed_railway_approval_valid = yes } sed_run_railway_approval = yes } }
}
sed_approve_construction_sgui = {
 scope = state
 is_shown = { owner = { is_player = yes has_variable = sed_enabled } }
 is_valid = { sed_construction_approval_valid = yes }
 effect = { if = { limit = { sed_construction_approval_valid = yes } sed_run_construction_approval = yes } }
}
'''
    # Blocked-reason lines, cascading so exactly one guard is named. Guard
    # order: paused, queue (construction only), private queue, default, balance.
    blocked = {
        'railway': {
            'paused': 'NOT = { is_game_paused = yes }',
            'private': 'is_game_paused = yes owner = { construction_queue_num_queued_private_levels > 0 }',
            'default': 'is_game_paused = yes owner = { construction_queue_num_queued_private_levels = 0 in_default = yes }',
            'balance': 'is_game_paused = yes owner = { construction_queue_num_queued_private_levels = 0 NOT = { in_default = yes } net_total_income < 0 }',
        },
        'construction': {
            'paused': 'NOT = { is_game_paused = yes }',
            'queue': 'is_game_paused = yes owner = { num_queued_government_constructions < 3 }',
            'private': 'is_game_paused = yes owner = { num_queued_government_constructions >= 3 construction_queue_num_queued_private_levels > 0 }',
            'default': 'is_game_paused = yes owner = { num_queued_government_constructions >= 3 construction_queue_num_queued_private_levels = 0 in_default = yes }',
            'balance': 'is_game_paused = yes owner = { num_queued_government_constructions >= 3 construction_queue_num_queued_private_levels = 0 NOT = { in_default = yes } net_total_income < 0 }',
        },
    }
    for action, guards in blocked.items():
        for guard, condition in guards.items():
            result += (f'sed_{action}_blocked_{guard}_sgui = {{\n scope = state\n'
                       f' is_shown = {{ sed_{action}_candidate_eligible = yes {condition} }}\n}}\n')
    for action in ('railway', 'construction'):
        result += (f'sed_{action}_stale_sgui = {{\n scope = state\n'
                   f' is_shown = {{ owner = {{ is_player = yes has_variable = sed_enabled }} '
                   f'NOT = {{ sed_{action}_candidate_eligible = yes }} }}\n}}\n')
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
    return '# Generated by tools/build_mod.py.\n' + result


def scripted_triggers():
    return '''# State scope. Candidate is limited to an operating railway with a live infrastructure deficit.
sed_railway_candidate_eligible = {
 is_incorporated = yes
 infrastructure_delta < 0
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
 is_game_paused = yes
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  net_total_income >= 0
  construction_queue_num_queued_private_levels = 0
 }
}

# State scope. A staffed construction sector in a populous incorporated state.
sed_construction_candidate_eligible = {
 is_incorporated = yes
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
 is_game_paused = yes
 owner = {
  is_player = yes
  has_variable = sed_enabled
  NOT = { in_default = yes }
  net_total_income >= 0
  num_queued_government_constructions >= 3
  construction_queue_num_queued_private_levels = 0
 }
}
'''


def value(name, fmt='1'):
    return f"[JournalEntry.GetCountry.MakeScope.Var('sed_{name}').GetValue|{fmt}]"


def localization(language):
    pt = language == 'braz_por'
    v = value
    pairs = {
        'je_sed_diagnostics': ('Smart Economy Director', 'Smart Economy Director'),
        'je_sed_diagnostics_reason': ('Indicadores econômicos do país, atualizados sob solicitação ou todo mês.', 'National economic indicators, refreshed on request or monthly.'),
        'sed_activation_tt': ('Ative o Director pela decisão Ativar Smart Economy Director.', 'Use the Enable Smart Economy Director decision.'),
        'sed_disabled_desc': ('Diagnóstico desativado.', 'Diagnostics disabled.'),
        'sed_enable': ('Ativar Smart Economy Director', 'Enable Smart Economy Director'),
        'sed_enable_desc': ('Abre um diagnóstico econômico no diário e lê os indicadores atuais. A ativação é opcional, inclusive em saves existentes.', 'Opens an economic diagnosis in the journal and reads current indicators. Enabling is optional, including in existing saves.'),
        'sed_disable_decision': ('Desativar Smart Economy Director', 'Disable Smart Economy Director'),
        'sed_disable_decision_desc': ('Remove o diagnóstico e limpa seus indicadores e histórico. Para voltar, use a decisão de ativação.', 'Removes the diagnosis and clears its readings and history. Use the enable decision to return.'),
        'sed_title': ('Economia nacional — diagnóstico', 'National economy — diagnosis'),
        'sed_scope_note': ('Diagnóstico e recomendações econômicas com aprovação individual. Nenhuma ação é executada automaticamente.', 'Economic diagnosis and recommendations with individual approval. No action runs automatically.'),
        'sed_refresh': ('Atualizar diagnóstico', 'Refresh diagnosis'),
        'sed_refresh_tt': ('Lê novamente os indicadores deste país.', 'Read this country’s indicators again.'),
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
        'sed_approve_railway_tt': ('Só funciona com o jogo pausado, saldo semanal não negativo, sem inadimplência e sem níveis na fila privada. Também revalida o estado e as filas no clique. Usa a fila normal do jogo.', 'Requires the game paused, nonnegative weekly balance, no default, and no private queued levels. Rechecks the state and queues on click. Uses the game’s normal construction queue.'),
        'sed_railway_blocked_paused': ('Botão bloqueado: o jogo precisa estar pausado.', 'Button blocked: the game must be paused.'),
        'sed_railway_blocked_private': ('Botão bloqueado: há níveis na fila privada.', 'Button blocked: the private queue has levels.'),
        'sed_railway_blocked_default': ('Botão bloqueado: o país está em inadimplência.', 'Button blocked: the country is in default.'),
        'sed_railway_blocked_balance': ('Botão bloqueado: saldo semanal negativo.', 'Button blocked: negative weekly balance.'),
        'sed_railway_stale': ('Recomendação desatualizada ou já enfileirada. Atualize o diagnóstico para recalcular; nenhuma ação será executada enquanto os filtros não forem atendidos.', 'This recommendation is stale or already queued. Refresh the diagnosis to recalculate; no action runs unless the filters pass.'),
        'sed_railway_action_success': ('Pedido adicionado à fila pública. Confira os custos e o prazo na fila do jogo.', 'Request added to the government queue. Review cost and timing in the game queue.'),
        'sed_railway_action_failed': ('A engine não confirmou a inclusão na fila. Nenhuma nova tentativa será automática.', 'The engine did not confirm the queue addition. No automatic retry will occur.'),
        'sed_construction_title': ('Capacidade de construção', 'Construction capacity'),
        'sed_construction_intro': ('Protótipo: um setor de construção existente e empregado em estado incorporado, quando a fila pública tem pelo menos três projetos. A análise não calcula custo nem retorno; aprove uma ação por vez e confira o orçamento.', 'Prototype: one existing, staffed construction sector in an incorporated state when the government queue has at least three projects. The analysis does not calculate cost or return; approve one action at a time and review the budget.'),
        'sed_no_construction_queue': ('A fila pública tem menos de três projetos. O Director não recomenda ampliar a capacidade de construção agora.', 'The government queue has fewer than three projects. The Director does not recommend expanding construction capacity now.'),
        'sed_no_construction_candidate': ('Há fila pública suficiente, mas nenhum setor de construção passou pelos filtros de operação, contratação, insumos e fila.', 'The government queue is long enough, but no construction sector passed the operation, hiring, input, and queue filters.'),
        'sed_construction_breakdown': (f'Estados com setor de construção: {v("construction_sector_states", "0")} · Setor não operante: {v("construction_not_ready_states", "0")} · Bloqueados por incorporação ou permissão: {v("construction_blocked_states", "0")}. Cada estado é contado por um motivo principal.', f'States with a construction sector: {v("construction_sector_states", "0")} · Sector not operating: {v("construction_not_ready_states", "0")} · Blocked by incorporation or permission: {v("construction_blocked_states", "0")}. Each state is counted under one primary reason.'),
        'sed_construction_candidate_title': ('#bold [State.GetName]#! — setor de construção', '#bold [State.GetName]#! — construction sector'),
        'sed_construction_candidate_reason': ('O setor está empregado, sem falta de insumos nem expansão já enfileirada. Um nível público pode aumentar a capacidade; o efeito, o custo e o prazo futuros não são previstos.', 'The sector is staffed, has no input shortage, and has no queued expansion. One government level may raise capacity; future impact, cost, and timing are not forecast.'),
        'sed_approve_construction': ('Aprovar: enfileirar 1 nível do setor', 'Approve: queue 1 construction sector level'),
        'sed_approve_construction_tt': ('Só funciona com o jogo pausado, fila pública de ao menos três projetos, saldo semanal não negativo, sem inadimplência e sem níveis na fila privada. Também revalida o estado e as filas no clique. Usa a fila normal do jogo.', 'Requires the game paused, at least three government projects queued, nonnegative weekly balance, no default, and no private queued levels. Rechecks the state and queues on click. Uses the game’s normal construction queue.'),
        'sed_construction_blocked_paused': ('Botão bloqueado: o jogo precisa estar pausado.', 'Button blocked: the game must be paused.'),
        'sed_construction_blocked_queue': ('Botão bloqueado: a fila pública tem menos de três projetos.', 'Button blocked: the government queue has fewer than three projects.'),
        'sed_construction_blocked_private': ('Botão bloqueado: há níveis na fila privada.', 'Button blocked: the private queue has levels.'),
        'sed_construction_blocked_default': ('Botão bloqueado: o país está em inadimplência.', 'Button blocked: the country is in default.'),
        'sed_construction_blocked_balance': ('Botão bloqueado: saldo semanal negativo.', 'Button blocked: negative weekly balance.'),
        'sed_construction_stale': ('Recomendação desatualizada ou já enfileirada. Atualize o diagnóstico para recalcular; nenhuma ação será executada enquanto os filtros não forem atendidos.', 'This recommendation is stale or already queued. Refresh the diagnosis to recalculate; no action runs unless the filters pass.'),
        'sed_construction_action_success': ('Pedido do setor de construção adicionado à fila pública. Confira os custos e o prazo na fila do jogo.', 'Construction sector request added to the government queue. Review cost and timing in the game queue.'),
        'sed_construction_action_failed': ('A engine não confirmou a inclusão do setor de construção na fila. Nenhuma nova tentativa será automática.', 'The engine did not confirm the construction sector queue addition. No automatic retry will occur.'),
        'sed_limitations': ('Protótipos limitados a ferrovias operantes com infraestrutura negativa e a setores de construção operantes com fila pública de ao menos três projetos. Não estima custo, contratação futura ou retorno. A aprovação apenas adiciona um nível à fila pública; os custos e o tempo dependem do jogo. Qualificações, salários, desempregados e dependência externa ainda não são medidos diretamente. Edifícios com contratação incompleta não equivalem a desempregados. As filas mostram projetos, não níveis nem custos futuros. A alfabetização segue a abrangência do indicador do jogo. Variações de PIB podem refletir mudanças de fronteira e mercado. O setor de construção depende de trabalhadores e insumos disponíveis; a recomendação não garante que o novo nível será contratado.', 'Prototypes limited to operating railways in states with negative infrastructure and operating construction sectors when the government queue has at least three projects. They do not estimate cost, future hiring, or returns. Approval only adds one level to the government queue; costs and timing depend on the game. Qualifications, wages, unemployed workers and external dependence are not directly measured. Incompletely staffed buildings are not a count of unemployed workers. Queues show projects, not levels or future costs. Literacy follows the game indicator’s coverage. GDP changes may reflect borders and markets. Construction sectors depend on available workers and inputs; the recommendation does not guarantee that the new level will be staffed.'),
    }
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
    result = {
        'common/decisions/sed_decisions.txt': decisions,
        'common/journal_entries/sed_journal_entries.txt': journal,
        'common/on_actions/sed_on_actions.txt': on_actions,
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
