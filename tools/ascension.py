"""Country-scope prestige, diplomatic screening and twelve-month accounting."""

METRICS = {
    'rank': ('posição estimada', 'estimated position', '0', 'var:sed_asc_rank'),
    'prestige': ('prestígio', 'prestige', '1', 'prestige'),
    'balance': ('saldo semanal', 'weekly balance', 'K', 'net_total_income'),
    'sol': ('padrão de vida', 'standard of living', '1', 'average_sol'),
    'army': ('projeção terrestre', 'army projection', '1', 'army_power_projection'),
    'navy': ('tamanho naval', 'naval size', '0', 'navy_size'),
}
COUNTERS = {
    'construction': ('obras do Director', 'Director projects'),
    'tax': ('impostos', 'tax changes'),
    'wage': ('salários civis', 'government wage changes'),
    'military_wage': ('salários militares', 'military wage changes'),
}
VARIABLES = [
    'sed_asc_rank', 'sed_asc_gap', 'sed_asc_next', 'sed_asc_partner',
    'sed_asc_overlord', 'sed_asc_liberty', 'sed_asc_protection', 'sed_asc_priority',
    'sed_asc_window_start', 'sed_asc_queue_before', 'sed_asc_policy_month',
    *(f'sed_asc_{key}_{field}' for key in METRICS for field in ('base', 'now', 'delta')),
    *(f'sed_asc_{key}_{field}' for key in COUNTERS for field in ('count', 'annual')),
]
PRIORITIES = (
    ('in_default = yes', 'Estabilizar o orçamento', 'Stabilize the budget'),
    ('OR = { is_at_war = yes is_diplomatic_play_committed_participant = yes is_diplomatic_play_initiator = yes is_diplomatic_play_target = yes }', 'Preservar prontidão. Consulte o painel militar antes de expandir.', 'Preserve readiness. Review the military panel before expanding.'),
    ('OR = { net_total_income < 0 NOT = { sed_auto_fiscal_safe = yes } }',
     'Dar folga ao caixa antes de ampliar despesas permanentes.', 'Rebuild fiscal headroom before increasing permanent expenses.'),
    ('has_variable = sed_plan_goal OR = { var:sed_plan_goal = 2 var:sed_plan_goal = 5 var:sed_plan_goal = 6 var:sed_plan_goal = 7 var:sed_plan_goal = 9 }',
     'Resolver o gargalo de economia indicado no plano nacional.', 'Resolve the economic bottleneck in the national plan.'),
    ('NOT = { has_technology_researched = railways } any_scope_state = { is_incorporated = yes infrastructure_delta < 0 }',
     'Pesquisar a rota para Ferrovias. Veja os pré-requisitos no Conselheiro Tecnológico.', 'Research the path to Railways. Check prerequisites in the Technology Advisor.'),
    ('var:sed_asc_protection = 2 has_variable = sed_asc_partner',
     'Buscar proteção antes de assumir novos compromissos.', 'Seek protection before taking on new commitments.'),
    ('has_variable = sed_asc_rank_delta var:sed_asc_rank_delta >= 0 var:sed_asc_army_delta <= 0',
     'O ranking não avançou no último período e a projeção terrestre não aumentou. Confira no Conselheiro Militar se há um reforço sustentável.', 'Rank and army projection did not improve in the last period. Check the Military Advisor for a sustainable reinforcement.'),
    ('has_variable = sed_plan_goal var:sed_plan_goal = 1',
     'Recuperar a infraestrutura para sustentar a produção.', 'Recover infrastructure to sustain production.'),
    (None,
     'Investir na produção e usar o Conselheiro de Governo para escolher reformas elegíveis.', 'Invest in production and use the Government Advisor to select eligible reforms.'),
)


def track_actions():
    record = []
    for kind in ('tax', 'wage', 'military_wage'):
        marker = f'sed_{kind}_last_change_month'
        record.append(f'''  if = {{ limit = {{ has_variable = {marker} var:{marker} = var:sed_calendar_month_key }}
   change_variable = {{ name = sed_asc_{kind}_count add = 1 }}
  }}''')
    return '''sed_asc_record_actions = {
 if = { limit = { has_variable = sed_asc_queue_before
  construction_queue_num_queued_government_levels > var:sed_asc_queue_before }
  change_variable = { name = sed_asc_construction_count add = {
   value = construction_queue_num_queued_government_levels subtract = var:sed_asc_queue_before
  } }
 }
 remove_variable = sed_asc_queue_before
 if = { limit = { NOT = { has_variable = sed_asc_policy_month var:sed_asc_policy_month = var:sed_calendar_month_key } }
  set_variable = { name = sed_asc_policy_month value = var:sed_calendar_month_key }
''' + '\n'.join(record) + '''
 }
}
'''


def effects():
    live = '\n'.join(f' set_variable = {{ name = sed_asc_{key}_now value = {spec[3]} }}'
                     for key, spec in METRICS.items())
    snapshots = '\n'.join(f'  set_variable = {{ name = sed_asc_{key}_base value = var:sed_asc_{key}_now }}'
                          for key in METRICS)
    deltas = '\n'.join(f'''  set_variable = {{ name = sed_asc_{key}_delta value = {{
   value = var:sed_asc_{key}_now subtract = var:sed_asc_{key}_base
  }} }}''' for key in METRICS)
    annual_counts = '\n'.join(f'''  set_variable = {{ name = sed_asc_{key}_annual value = var:sed_asc_{key}_count }}
  set_variable = {{ name = sed_asc_{key}_count value = 0 }}''' for key in COUNTERS)
    init_counts = '\n'.join(f'  set_variable = {{ name = sed_asc_{key}_count value = 0 }}'
                           for key in COUNTERS)
    choices = []
    for i, (criteria, _, _) in enumerate(PRIORITIES, 1):
        branch = 'if' if i == 1 else 'else_if'
        guard = f' limit = {{ {criteria} }}' if criteria else ''
        choices.append(f""" {branch if criteria else 'else'} = {{{guard}
  set_variable = {{ name = sed_asc_priority value = {i} }}
 }}""")
    return '''# All entry points use the player country as root.
sed_asc_refresh = {
 sed_refresh_calendar = yes
 set_variable = { name = sed_asc_rank value = 1 }
 remove_variable = sed_asc_next
 remove_variable = sed_asc_gap
 every_country = {
  limit = { sed_asc_ahead = yes }
  root = { change_variable = { name = sed_asc_rank add = 1 } }
 }
 ordered_country = {
  limit = { sed_asc_ahead = yes }
  order_by = { value = prestige multiply = -1 }
  max = 1
  check_range_bounds = no
  root = {
   set_variable = { name = sed_asc_next value = prev }
   set_variable = { name = sed_asc_gap value = { value = prev.prestige subtract = prestige } }
  }
 }
 sed_asc_diplomacy = yes
''' + live + '''
 if = { limit = { NOT = { has_variable = sed_asc_window_start } }
  set_variable = { name = sed_asc_window_start value = var:sed_calendar_month_key }
''' + snapshots + '\n' + init_counts + '''
 }
 else_if = { limit = {
  var:sed_calendar_month_key >= { value = var:sed_asc_window_start add = 12 }
 }
''' + deltas + '\n' + snapshots + '\n' + annual_counts + '''
  set_variable = { name = sed_asc_window_start value = var:sed_calendar_month_key }
 }
''' + '\n'.join(choices) + '''
}

sed_asc_diplomacy = {
 remove_variable = sed_asc_overlord
 remove_variable = sed_asc_liberty
 remove_variable = sed_asc_partner
 set_variable = { name = sed_asc_protection value = 2 }
 if = { limit = { is_subject = yes exists = overlord }
  set_variable = { name = sed_asc_protection value = 1 }
  set_variable = { name = sed_asc_overlord value = overlord }
  set_variable = { name = sed_asc_liberty value = liberty_desire }
 }
 else_if = { limit = { any_scope_treaty = { any_scope_article = {
  OR = { has_type = alliance has_type = defensive_pact }
 } } }
  set_variable = { name = sed_asc_protection value = 3 }
 }
 else = {
  ordered_country = {
   limit = { sed_asc_partner_candidate = yes }
   order_by = { value = relations:root add = { value = army_power_projection divide = 100 } }
   max = 1
   check_range_bounds = no
   root = { set_variable = { name = sed_asc_partner value = prev } }
  }
 }
}
''' + track_actions()


def triggers():
    return '''sed_asc_ahead = {
 NOT = { is_country_type = decentralized }
 prestige > root.prestige
}
sed_asc_partner_candidate = {
 NOT = { this = root }
 NOT = { is_country_type = decentralized }
 is_subject = no
 is_at_war = no
 army_power_projection > root.army_power_projection
 has_overlapping_interests = root
 relations:root >= relations_threshold:cordial
 NOT = { has_diplomatic_pact = { who = root type = rivalry } }
}
'''


def rows():
    return ('summary', 'gap', 'first_year', 'annual', 'actions', 'advisor', 'subject',
            'partner', 'protected', 'no_partner', *(f'priority_{i}' for i in range(1, len(PRIORITIES) + 1)))


def guis():
    conditions = {
        'summary': 'has_variable = sed_asc_rank_now',
        'gap': 'has_variable = sed_asc_next has_variable = sed_asc_gap',
        'first_year': 'has_variable = sed_asc_rank_now NOT = { has_variable = sed_asc_rank_delta }',
        'annual': 'has_variable = sed_asc_rank_delta',
        'actions': 'has_variable = sed_asc_construction_count',
        'advisor': 'has_variable = advisor_auto_construction_enabled has_variable = advisor_auto_construction_added_this_month',
        'subject': 'has_variable = sed_asc_overlord has_variable = sed_asc_liberty',
        'partner': 'has_variable = sed_asc_partner',
        'protected': 'has_variable = sed_asc_protection var:sed_asc_protection = 3',
        'no_partner': 'has_variable = sed_asc_protection var:sed_asc_protection = 2 NOT = { has_variable = sed_asc_partner }',
    }
    conditions.update({f'priority_{i}': f'has_variable = sed_asc_priority var:sed_asc_priority = {i}'
                       for i in range(1, len(PRIORITIES) + 1)})
    return '\n'.join(f'sed_asc_{key}_visible_sgui = {{ scope = country is_shown = {{ {condition} }} }}'
                     for key, condition in conditions.items()) + '\n'


def localization(value):
    def country(key):
        return f"[JournalEntry.GetCountry.MakeScope.Var('sed_asc_{key}').GetCountry.GetName]"

    def report(field):
        return tuple(' · '.join(f'{spec[col]} {value(f"asc_{key}_{field}", spec[2])}'
                                for key, spec in METRICS.items()) for col in (0, 1))

    actions = tuple(' · '.join(f'{labels[col]} {value(f"asc_{key}_count", "0")}'
                               for key, labels in COUNTERS.items()) for col in (0, 1))
    completed = tuple(' · '.join(f'{labels[col]} {value(f"asc_{key}_annual", "0")}'
                                  for key, labels in COUNTERS.items()) for col in (0, 1))
    advisor = "[JournalEntry.GetCountry.MakeScope.Var('advisor_auto_construction_added_this_month').GetValue|0]"
    pairs = {
        'title': ('Plano de ascensão', 'Rise to power'),
        'summary': report('now'),
        'gap': (f"Próximo por prestígio: {country('next')} · diferença de {value('asc_gap')} pontos.",
                f"Next by prestige: {country('next')} · gap of {value('asc_gap')} points."),
        'first_year': ('Comparação anual após 12 meses de acompanhamento.', 'The annual comparison appears after 12 months of tracking.'),
        'annual': (f'Variação em 12 meses (posição menor é melhor)\n{report("delta")[0]}\nAções confirmadas no período: {completed[0]}',
                   f'12-month change (lower rank is better)\n{report("delta")[1]}\nConfirmed actions in the period: {completed[1]}'),
        'actions': (f'Verificadas no período atual: {actions[0]}', f'Confirmed in the current period: {actions[1]}'),
        'advisor': (f'Economy Advisor · níveis enfileirados na última leitura dele: {advisor}.',
                    f'Economy Advisor · levels queued in its last reported reading: {advisor}.'),
        'subject': (f'Suserano: {country("overlord")} · desejo de liberdade {value("asc_liberty")}. Compare a proteção e o acesso ao mercado atuais com o custo de operar sozinho. Prepare caixa, insumos e apoio externo antes de buscar independência.',
                    f'Overlord: {country("overlord")} · liberty desire {value("asc_liberty")}. Compare current protection and market access with the cost of standing alone. Prepare reserves, supplies and foreign support before seeking independence.'),
        'partner': (f'Possível parceiro: {country("partner")}. Tem interesses regionais em comum, relações cordiais e mais projeção terrestre. Confira no painel diplomático se aceita um pacto defensivo.',
                    f'Potential partner: {country("partner")}. It shares regional interests, has cordial relations and higher army projection. Check defensive pact acceptance in Diplomacy.'),
        'protected': ('Há um tratado com cláusula de aliança ou defesa. Confira quem pode se comprometer antes de abrir uma jogada.', 'There is a treaty with an alliance or defense clause. Check who can commit before starting a play.'),
        'no_partner': ('Sem candidato cordial e militarmente mais forte nesta leitura. Use o Auto-Diplomacy para ampliar contatos.', 'No cordial and militarily stronger candidate in this reading. Use Auto-Diplomacy to broaden contacts.'),
    }
    pairs.update({f'priority_{i}': (f'Prioridade: {pt}', f'Priority: {en}')
                  for i, (_, pt, en) in enumerate(PRIORITIES, 1)})
    return {f'sed_asc_{key}': text for key, text in pairs.items()}
