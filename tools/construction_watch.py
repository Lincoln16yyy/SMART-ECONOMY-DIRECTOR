"""Monthly empty-queue observation and bounded recovery of delegated building."""

VARIABLES = ['sed_watch_month', 'sed_watch_idle', 'sed_watch_status', 'sed_watch_delegated']

def effects():
    return '''sed_watch_review = {
 if = { limit = {
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  NOT = { has_variable = sed_mode_assisted }
  NOT = { has_variable = sed_mode_manual }
  NOT = { has_variable = sed_watch_month var:sed_watch_month = sed_live_month_key }
 }
  set_variable = { name = sed_watch_month value = sed_live_month_key }
  if = { limit = { NOT = { has_variable = sed_watch_idle } }
   set_variable = { name = sed_watch_idle value = 0 }
  }
  if = { limit = { construction_queue_num_queued_government_levels > 0 }
   set_variable = { name = sed_watch_idle value = 0 }
  }
  else_if = { limit = { has_variable = sed_watch_delegated
   has_variable = sed_coord_executor var:sed_coord_executor = 1
   construction_queue_num_queued_private_levels = 0 is_construction_paused = no
  }
   change_variable = { name = sed_watch_idle add = 1 }
  }
  else = { set_variable = { name = sed_watch_idle value = 0 } }
  remove_variable = sed_watch_delegated
  if = { limit = { has_variable = sed_coord_active has_variable = sed_coord_executor
   var:sed_coord_executor = 1 }
   set_variable = { name = sed_watch_delegated value = yes }
  }
 }
 sed_watch_diagnose = yes
}
sed_watch_diagnose = {
 set_variable = { name = sed_watch_status value = 0 }
 if = { limit = { has_variable = sed_watch_idle var:sed_watch_idle >= 2
  has_variable = sed_mode_automatic NOT = { has_variable = sed_mode_assisted }
 }
  set_variable = { name = sed_watch_status value = 1 }
  if = { limit = { NOT = { sed_direct_fiscal_safe = yes } }
   set_variable = { name = sed_watch_status value = 2 }
  }
  else_if = { limit = { construction_queue_num_queued_private_levels > 0 is_construction_paused = no }
   set_variable = { name = sed_watch_status value = 3 }
  }
  else_if = { limit = { is_construction_paused = yes }
   set_variable = { name = sed_watch_status value = 4 }
  }
  else_if = { limit = { sed_watch_recovery_candidate = yes }
   set_variable = { name = sed_watch_status value = 5 }
  }
 }
}
'''

def triggers():
    return '''sed_watch_recovery_candidate = {
 has_variable = sed_watch_idle var:sed_watch_idle >= 2
 has_variable = sed_coord_active has_variable = sed_coord_advisor_known
 construction_queue_num_queued_government_levels = 0
 construction_queue_num_queued_private_levels = 0
 OR = {
  any_scope_state = { sed_admin_candidate_eligible = yes }
  any_scope_state = { sed_power_candidate_eligible = yes }
  any_scope_state = { sed_trade_center_candidate_eligible = yes }
  any_scope_state = { sed_core_wood_eligible = yes }
  any_scope_state = { sed_core_iron_eligible = yes }
  any_scope_state = { sed_core_tools_eligible = yes }
 }
}
'''

def localization():
    return {
        'sed_watch_1': ('A fila ficou vazia após pelo menos duas delegações mensais. Nenhuma alternativa direta passou nos filtros atuais de prédio, trabalhadores e insumos.', 'The queue was empty after at least two monthly delegations. No direct alternative passed current building, labor and input filters.'),
        'sed_watch_2': ('Fila vazia recorrente. A guarda fiscal bloqueia novas despesas. Confira saldo operacional, dívida e reservas no orçamento.', 'Recurring empty queue. The fiscal guard blocks new spending. Check operating balance, debt and reserves.'),
        'sed_watch_3': ('Fila vazia recorrente. A fila privada ocupada impede a recuperação direta.', 'Recurring empty queue. Private construction blocks direct recovery.'),
        'sed_watch_4': ('Fila vazia recorrente. A construção está pausada.', 'Recurring empty queue. Construction is paused.'),
        'sed_watch_5': ('Fila vazia recorrente. O Director reservou uma tentativa direta de recuperação, sujeita ao orçamento de materiais e ao limite mensal. Confira o resultado da revisão.', 'Recurring empty queue. The Director reserved a direct recovery attempt under material-budget and monthly limits. Check the review outcome.'),
    }
