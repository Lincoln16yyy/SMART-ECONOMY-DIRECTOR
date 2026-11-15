"""Build the standalone Automatic edition for Cold War Era 0.99."""

import json
from pathlib import Path
import zipfile

try:
    from .pdx_script import child, parse
except ImportError:
    from pdx_script import child, parse


NAME = 'Smart Economy Director - Cold War Era'
BUILDINGS = {
    'rail': ('building_railway', 'infrastructure_delta < 0'),
    'administration': (
        'building_government_administration',
        'infrastructure_delta >= 0 OR = { owner = { bureaucracy < 0 } tax_capacity_usage > tax_capacity }',
    ),
    'electricity': ('building_power_plant', 'infrastructure_delta >= 0 sg:electricity ?= { state_goods_pricier >= 0.2 }'),
}
SECTOR = 'building_construction_sector'


def definitions(root, kind):
    return {entry.key: entry.value
            for path in sorted((root / 'common' / kind).glob('*.txt'))
            for entry in parse(path.read_text(encoding='utf-8-sig'))
            if entry.op == '=' and isinstance(entry.value, list)}


def construction_profiles(root):
    metadata = json.loads((root / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))
    if (metadata['id'], metadata['version'], metadata['supported_game_version']) != ('2988303719', '0.99', '1.15.1'):
        raise ValueError('Expected Cold War Era (1950) 0.99 for Victoria 3 1.15.1.')
    buildings = definitions(root, 'buildings')
    for building, _ in BUILDINGS.values():
        if building not in buildings:
            raise ValueError(f'Cold War Era building missing: {building}')
    goods = definitions(root, 'goods')
    if 'electricity' not in goods:
        raise ValueError('Cold War Era good missing: electricity')
    groups = definitions(root, 'production_method_groups')
    methods = definitions(root, 'production_methods')
    profiles = {}
    for group in child(buildings[SECTOR], 'production_method_groups'):
        costs = {}
        for method in child(groups[group.key], 'production_methods'):
            cost = 0.0
            for entry in methods[method.key]:
                if entry.key != 'building_modifiers':
                    continue
                for scale in entry.value:
                    for modifier in scale.value:
                        if modifier.key.startswith('goods_input_') and modifier.key.endswith('_add'):
                            good = modifier.key.removeprefix('goods_input_').removesuffix('_add')
                            cost += float(child(goods[good], 'cost')) * max(float(modifier.value), 0)
            costs[method.key] = cost
        if not costs:
            raise ValueError(f'Empty construction method group: {group.key}')
        profiles[group.key] = costs
    if not profiles or not any(cost for group in profiles.values() for cost in group.values()):
        raise ValueError('Cold War Era construction profile has no material costs.')
    return profiles


def budget_scripts(profiles):
    known_groups = []
    price_terms = []
    for costs in profiles.values():
        options = ' '.join(f'has_active_production_method = {method}' for method in costs)
        known_groups.append(f'OR = {{ {options} }}')
        for method, cost in costs.items():
            if cost > 0:
                price_terms.append(
                    f'  if = {{ limit = {{ has_active_production_method = {method} }} add = {cost * 1.75:g} }}'
                )
    known = '\n  '.join(known_groups)
    prices = '\n'.join(price_terms)
    return f'''sed_cwe_known_construction_sector = {{
  {known}
}}

sed_cwe_budget_safe = {{
 NOT = {{ in_default = yes }}
 net_fixed_income >= 0
 gold_reserves >= sed_cwe_reserve_floor
 modifier:country_construction_add > 0
 modifier:country_max_weekly_construction_progress_add > 0
 NOT = {{ any_scope_state = {{ has_building = {SECTOR}
  b:{SECTOR} = {{ level > 0 occupancy > 0 NOT = {{ sed_cwe_known_construction_sector = yes }} }}
 }} }}
 net_total_income >= sed_cwe_weekly_material_cost
}}
''', f'''sed_cwe_month = {{ value = year multiply = 12 add = month }}
sed_cwe_reserve_floor = {{ value = fixed_income subtract = net_fixed_income min = 0 multiply = 4 }}

sed_cwe_material_cost_per_level = {{
 value = 0
{prices}
}}

sed_cwe_weekly_material_cost = {{
 value = 0
 every_scope_state = {{
  limit = {{ has_building = {SECTOR} b:{SECTOR} = {{ level > 0 occupancy > 0 }} }}
  b:{SECTOR} = {{
   add = {{ value = sed_cwe_material_cost_per_level multiply = level }}
  }}
 }}
}}
'''


def automation_scripts():
    candidates = []
    branches = []
    for project_id, (name, (building, need)) in enumerate(BUILDINGS.items(), 1):
        if name == 'rail':
            need += ' owner = { NOT = { has_variable = cnm_auto_railway_manager var:cnm_auto_railway_manager = 1 } }'
        candidate = f'sed_cwe_{name}_candidate'
        candidates.append(f'''{candidate} = {{
 is_incorporated = yes
 {need}
 can_construct_building = {building}
 OR = {{
  NOT = {{ has_building = {building} }}
  b:{building} = {{ level_after_queued_constructions <= level occupancy >= 0.5 has_failed_hires = no }}
 }}
}}
''')
        branch = 'if' if not branches else 'else_if'
        branches.append(f'''  {branch} = {{
   limit = {{ any_scope_state = {{ {candidate} = yes }} }}
   ordered_scope_state = {{
    limit = {{ {candidate} = yes }}
    order_by = state_population
    max = 1
    check_range_bounds = no
    owner = {{
     set_variable = {{ name = sed_cwe_last_attempt value = sed_cwe_month }}
     set_variable = {{ name = sed_cwe_queue_before value = construction_queue_num_queued_government_levels }}
     set_variable = {{ name = sed_cwe_result value = 4 }}
    }}
    start_building_construction = {building}
    owner = {{
     if = {{
      limit = {{ construction_queue_num_queued_government_levels > var:sed_cwe_queue_before }}
      set_variable = {{ name = sed_cwe_result value = {project_id} }}
     }}
     remove_variable = sed_cwe_queue_before
    }}
   }}
  }}''')
    return '\n'.join(candidates), '''sed_cwe_ensure_journal = {
 if = {
  limit = { NOT = { has_journal_entry = je_sed_cwe_automatic } NOT = { has_inactive_journal_entry = je_sed_cwe_automatic } }
  add_journal_entry = { type = je_sed_cwe_automatic }
 }
}

sed_cwe_automatic_review = {
 if = {
  limit = {
   is_player = yes
   has_variable = sed_cwe_enabled
   NOT = { has_variable = sed_enabled }
   NOT = { has_variable = cnm_auto_construct_manager var:cnm_auto_construct_manager = 1 }
   NOT = { AND = { has_variable = sed_cwe_last_attempt var:sed_cwe_last_attempt = sed_cwe_month } }
   is_construction_paused = no
   construction_queue_num_queued_private_levels = 0
   sed_cwe_budget_safe = yes
  }
''' + '\n'.join(branches) + '''
 }
}
'''


def journal():
    statuses = (
        ('disabled', 'NOT = { has_variable = sed_cwe_enabled }'),
        ('rail', 'has_variable = sed_cwe_result var:sed_cwe_result = 1 var:sed_cwe_last_attempt = sed_cwe_month'),
        ('administration', 'has_variable = sed_cwe_result var:sed_cwe_result = 2 var:sed_cwe_last_attempt = sed_cwe_month'),
        ('electricity', 'has_variable = sed_cwe_result var:sed_cwe_result = 3 var:sed_cwe_last_attempt = sed_cwe_month'),
        ('unconfirmed', 'has_variable = sed_cwe_result var:sed_cwe_result = 4 var:sed_cwe_last_attempt = sed_cwe_month'),
        ('ogas', 'has_variable = cnm_auto_construct_manager var:cnm_auto_construct_manager = 1'),
        ('paused', 'is_construction_paused = yes'),
        ('private_queue', 'construction_queue_num_queued_private_levels > 0'),
        ('budget', 'NOT = { sed_cwe_budget_safe = yes }'),
        ('ready', 'always = yes'),
    )
    descriptions = '\n'.join(
        f'   triggered_desc = {{ desc = sed_cwe_{key} trigger = {{ {condition} }} }}'
        for key, condition in statuses)
    return f'''je_sed_cwe_automatic = {{
 icon = "gfx/interface/icons/generic_icons/gdp.dds"
 group = je_group_internal_affairs
 is_shown_when_inactive = {{ is_player = yes has_variable = sed_cwe_enabled }}
 possible = {{ is_player = yes has_variable = sed_cwe_enabled }}
 should_be_pinned_by_default_uninvolved_or_context = yes
 status_desc = {{
  first_valid = {{
{descriptions}
  }}
 }}
}}
'''


def outputs(cwe, version):
    budget, values = budget_scripts(construction_profiles(cwe))
    candidates, effects = automation_scripts()
    scripts = {
        'common/scripted_triggers/sed_cwe_triggers.txt': budget + candidates,
        'common/script_values/sed_cwe_values.txt': values,
        'common/journal_entries/sed_cwe_journal.txt': journal(),
        'common/scripted_effects/sed_cwe_effects.txt': effects,
        'common/on_actions/sed_cwe_on_actions.txt': '''on_monthly_pulse_country = { on_actions = { sed_cwe_dispatch } }
sed_cwe_dispatch = {
 trigger = { is_player = yes has_variable = sed_cwe_enabled }
 effect = { sed_cwe_ensure_journal = yes sed_cwe_automatic_review = yes }
}
''',
        'common/decisions/sed_cwe_decisions.txt': '''sed_cwe_enable = {
 is_shown = { is_player = yes NOT = { has_variable = sed_cwe_enabled } NOT = { has_variable = sed_enabled } }
 possible = { always = yes }
 when_taken = { set_variable = { name = sed_cwe_enabled value = yes } sed_cwe_ensure_journal = yes }
 ai_chance = { value = 0 }
}
sed_cwe_disable = {
 is_shown = { is_player = yes has_variable = sed_cwe_enabled }
 possible = { always = yes }
 when_taken = { remove_variable = sed_cwe_enabled }
 ai_chance = { value = 0 }
}
''',
    }
    journal_text = {
        'je_sed_cwe_automatic': ('Director — Cold War Era', 'Director — Cold War Era'),
        'je_sed_cwe_automatic_reason': ('Construção pública automática. Uma tentativa por mês.', 'Automatic government construction. One attempt per month.'),
        'sed_cwe_disabled': ('Automático desligado.', 'Automatic construction is off.'),
        'sed_cwe_rail': ('Neste mês: ferrovia incluída na fila pública.', 'This month: railway added to the government queue.'),
        'sed_cwe_administration': ('Neste mês: administração incluída na fila pública.', 'This month: administration added to the government queue.'),
        'sed_cwe_electricity': ('Neste mês: usina incluída na fila pública.', 'This month: power plant added to the government queue.'),
        'sed_cwe_unconfirmed': ('Neste mês: o jogo não confirmou a inclusão da obra.', 'This month: the game did not confirm queue insertion.'),
        'sed_cwe_ogas': ('OGAS está gerenciando a fila pública.', 'OGAS is managing the government queue.'),
        'sed_cwe_paused': ('Construção pausada.', 'Construction is paused.'),
        'sed_cwe_private_queue': ('Aguardando a fila privada esvaziar.', 'Waiting for the private queue to clear.'),
        'sed_cwe_budget': ('Aguardando capacidade e cobertura do orçamento.', 'Waiting for capacity and budget coverage.'),
        'sed_cwe_ready': ('Na próxima revisão, o Director procura uma obra elegível.', 'At the next review, the Director looks for an eligible project.'),
    }
    for language, terms in {
        'braz_por': ('Ativar Director para Cold War Era', 'Autoriza construção pública automática mensal.', 'Desativar Director para Cold War Era', 'Encerra novas tentativas automáticas.'),
        'english': ('Enable Director for Cold War Era', 'Authorize automatic monthly government construction.', 'Disable Director for Cold War Era', 'Stop new automatic construction attempts.'),
    }.items():
        keys = ('sed_cwe_enable', 'sed_cwe_enable_desc', 'sed_cwe_disable', 'sed_cwe_disable_desc')
        lines = [f' {key}:0 "{term}"' for key, term in zip(keys, terms)]
        column = 0 if language == 'braz_por' else 1
        lines.extend(f' {key}:0 "{terms[column]}"' for key, terms in journal_text.items())
        scripts[f'localization/{language}/sed_cwe_l_{language}.yml'] = f'l_{language}:\n' + '\n'.join(lines) + '\n'
    generated = {path: text.encode('utf-8-sig') for path, text in scripts.items()}
    descriptor = f'version="{version}"\nname="{NAME}"\nsupported_version="1.15.1"\n'
    generated['descriptor.mod'] = descriptor.encode()
    generated['.metadata/metadata.json'] = (json.dumps({
        'name': NAME, 'id': 'sed.smart_economy_director_cwe',
        'version': version, 'supported_game_version': '1.15.1',
        'relationships': [{'rel_type': 'dependency', 'id': '2988303719',
                           'display_name': 'Cold War Era (1950)', 'resource_type': 'mod', 'version': '0.99'}],
        'game_custom_data': {'multiplayer_synchronized': True},
    }, indent=2) + '\n').encode()
    return generated


def package(cwe, output, version):
    generated = outputs(cwe, version)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f'{NAME}.mod', generated['descriptor.mod'] + f'path="mod/{NAME}"\n'.encode())
        for name, data in generated.items():
            archive.writestr(f'{NAME}/{name}', data)
    return output
