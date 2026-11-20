"""Fases mensais de dívida; a amortização vem do superávit retido."""
VARIABLES = ['sed_debt_stage', 'sed_debt_sample_month', 'sed_debt_previous_principal', 'sed_debt_rising_months']


def effects():
    return '''sed_refresh_debt_strategy = {
 if = { limit = { is_player = yes has_variable = sed_enabled }
  sed_refresh_calendar = yes
  if = { limit = { NOT = { has_variable = sed_debt_sample_month var:sed_debt_sample_month = var:sed_calendar_month_key } }
   if = { limit = { NOT = { has_variable = sed_debt_rising_months } }
    set_variable = { name = sed_debt_rising_months value = 0 }
   }
   if = { limit = { has_variable = sed_debt_sample_month has_variable = sed_debt_previous_principal
    var:sed_calendar_month_key = sed_debt_next_sample_month
    var:sed_debt_previous_principal > 0
    principal > { value = var:sed_debt_previous_principal multiply = 1.01 }
   } change_variable = { name = sed_debt_rising_months add = 1 } }
   else = { set_variable = { name = sed_debt_rising_months value = 0 } }
   set_variable = { name = sed_debt_sample_month value = var:sed_calendar_month_key }
   set_variable = { name = sed_debt_previous_principal value = principal }
  }
  set_variable = { name = sed_debt_stage value = 0 }
  if = { limit = { principal > 0 }
   set_variable = { name = sed_debt_stage value = 1 }
   if = { limit = { net_total_income > 0 net_fixed_income >= 0 credit > 0 }
    set_variable = { name = sed_debt_stage value = 2 }
    if = { limit = { OR = {
     principal > { value = credit multiply = 0.8 }
     var:sed_debt_rising_months >= 2
    } } set_variable = { name = sed_debt_stage value = 3 } }
   }
  }
  if = { limit = { in_default = yes } set_variable = { name = sed_debt_stage value = 4 } }
 }
}
'''


def triggers():
    return '''sed_debt_discretionary_blocked = {
 has_variable = sed_debt_stage
 OR = { var:sed_debt_stage = 1 var:sed_debt_stage = 3 var:sed_debt_stage = 4 }
}
'''


def values():
    return 'sed_debt_next_sample_month = { value = var:sed_debt_sample_month add = 1 }\n'
