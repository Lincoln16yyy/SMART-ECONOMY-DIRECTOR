"""Build an isolated, opt-in queue diagnostic mod; never install or enqueue.

The probe is a measurement aid for the pending engine tests, not evidence that
project identity or coverage has been verified. It is not part of outputs()
or the release package of the Director.
"""

import argparse
import json
from pathlib import Path
import re
import zipfile

try:
    from .build_mod import ROOT, SUPPLY_TARGETS
    from .pdx_script import parse, walk
except ImportError:
    from build_mod import ROOT, SUPPLY_TARGETS
    from pdx_script import parse, walk

VERSION = '0.1.0'
NAME = 'Smart Economy Queue Probe'
BUILDINGS = ['building_railway', 'building_construction_sector'] + [
    item['building'] for item in SUPPLY_TARGETS]
READINGS = {
    'public_projects': 'num_queued_government_constructions',
    'private_projects': 'num_queued_private_constructions',
    'public_levels': 'construction_queue_num_queued_government_levels',
    'private_levels': 'construction_queue_num_queued_private_levels',
    'year': 'year', 'month': 'month',
}
COUNTRY_VARIABLES = ['sedqp_enabled'] + ['sedqp_' + name for name in READINGS]
BUILDING_VARIABLES = ['sedqp_current', 'sedqp_after', 'sedqp_delta']


def effects():
    readings = '\n'.join(
        f'  set_variable = {{ name = sedqp_{name} value = {expression} }}'
        for name, expression in READINGS.items())
    filters = ' '.join('is_building_type = ' + building for building in BUILDINGS)
    clean_country = '\n'.join(' remove_variable = ' + name for name in COUNTRY_VARIABLES)
    clean_building = '\n'.join('   remove_variable = ' + name for name in BUILDING_VARIABLES)
    return f'''sedqp_enable = {{
 if = {{
  limit = {{ is_player = yes }}
  set_variable = {{ name = sedqp_enabled value = yes }}
  sedqp_refresh = yes
  if = {{
   limit = {{ NOT = {{ has_journal_entry = je_sedqp_queue }} NOT = {{ has_inactive_journal_entry = je_sedqp_queue }} }}
   add_journal_entry = {{ type = je_sedqp_queue }}
  }}
 }}
}}
sedqp_refresh = {{
 if = {{
  limit = {{ is_player = yes has_variable = sedqp_enabled }}
{readings}
  change_variable = {{ name = sedqp_month add = 1 }}
  clear_variable_list = sedqp_buildings
  every_scope_state = {{
   every_scope_building = {{
    limit = {{ OR = {{ {filters} }} }}
    set_variable = {{ name = sedqp_current value = level }}
    set_variable = {{ name = sedqp_after value = level_after_queued_constructions }}
    set_variable = {{ name = sedqp_delta value = {{ value = level_after_queued_constructions subtract = level }} }}
    root = {{ add_to_variable_list = {{ name = sedqp_buildings target = prev }} }}
   }}
  }}
 }}
}}
sedqp_disable = {{
 if = {{
  limit = {{ is_player = yes }}
{clean_country}
 clear_variable_list = sedqp_buildings
 every_scope_state = {{ every_scope_building = {{
{clean_building}
 }} }}
 }}
}}
'''


def gui_text(key):
    return f'''textbox = {{ autoresize = yes multiline = yes align = left|nobaseline
 using = fontsize_small minimumsize = {{ 480 -1 }} maximumsize = {{ 480 -1 }} text = "{key}" }}\n'''


def widget():
    row = gui_text('sedqp_row_title') + gui_text('sedqp_row_levels')
    body = ''.join(gui_text(key) for key in ('sedqp_notice', 'sedqp_date', 'sedqp_country_projects',
                                            'sedqp_country_levels', 'sedqp_coverage'))
    for action in ('refresh', 'disable'):
        body += f'''button = {{ size = {{ 360 32 }} using = select_button_sound using = tooltip_se
 text = "sedqp_{action}_button" tooltip = "sedqp_{action}_tt"
 visible = "[GetScriptedGui('sedqp_{action}_sgui').IsShown(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)]"
 enabled = "[GetScriptedGui('sedqp_{action}_sgui').IsValid(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)]"
 onclick = "[GetScriptedGui('sedqp_{action}_sgui').Execute(GuiScope.SetRoot(JournalEntry.GetCountry.MakeScope).End)]" }}\n'''
    body += '''fixedgridbox = {
 datamodel = "[JournalEntry.GetCountry.MakeScope.GetList('sedqp_buildings')]"
 addcolumn = 500 addrow = 112 item = { sedqp_building_item = {} }
}
'''
    return f'''types sedqp_types {{
 type sedqp_building_item = flowcontainer {{
  direction = vertical spacing = 4
  widget = {{ datacontext = "[Scope.GetBuilding]" size = {{ 500 106 }}
   background = {{ using = dark_area }}
   flowcontainer = {{ position = {{ 8 4 }} direction = vertical spacing = 4
{row}   }}
  }}
 }}
}}
flowcontainer = {{ name = "sedqp_queue_widget" direction = vertical spacing = 6
{body}}}
'''


def localization(language):
    country = lambda name: f"[JournalEntry.GetCountry.MakeScope.Var('sedqp_{name}').GetValue|0]"
    building = lambda name: f"[Building.MakeScope.Var('sedqp_{name}').GetValue|0]"
    pairs = {
        'je_sedqp_queue': ('Inspeção de filas — teste', 'Queue inspection — test'),
        'je_sedqp_queue_reason': ('Leituras manuais para conferir a cobertura das filas.', 'Manual readings to check queue coverage.'),
        'sedqp_enable_decision': ('Ativar inspeção de filas (teste)', 'Enable queue inspection (test)'),
        'sedqp_enable_decision_desc': ('Abre um diário auxiliar, sem construir ou alterar as filas.', 'Opens a helper journal without building or changing queues.'),
        'sedqp_disable_decision': ('Desativar inspeção de filas (teste)', 'Disable queue inspection (test)'),
        'sedqp_disable_decision_desc': ('Limpa apenas as leituras do auxiliar; preserva obras e o Director.', 'Clears helper readings only; preserves construction and the Director.'),
        'sedqp_activation': ('Ative pela decisão de inspeção de filas.', 'Enable through the queue inspection decision.'),
        'sedqp_disabled': ('Inspeção de filas desativada.', 'Queue inspection disabled.'),
        'sedqp_notice': ('Ferramenta de teste: não constrói, não cancela e não reordena. Todos os valores são da última leitura; não identificam projetos nem seu investidor.', 'Test tool: does not build, cancel or reorder. All values are from the last reading; they do not identify projects or their investor.'),
        'sedqp_date': ('Última leitura: ' + country('month') + '/' + country('year') + '.', 'Last reading: ' + country('month') + '/' + country('year') + '.'),
        'sedqp_country_projects': ('Projetos — pública: ' + country('public_projects') + '; privada: ' + country('private_projects') + '.', 'Projects — government: ' + country('public_projects') + '; private: ' + country('private_projects') + '.'),
        'sedqp_country_levels': ('Níveis — pública: ' + country('public_levels') + '; privada: ' + country('private_levels') + '.', 'Levels — government: ' + country('public_levels') + '; private: ' + country('private_levels') + '.'),
        'sedqp_coverage': ('Lista somente os dez tipos de prédio do Director encontrados nos estados atuais do país. Prédio ausente da lista não significa fila vazia. A diferença por prédio não separa público/privado; confira o projeto na fila nativa.', 'Lists only the ten Director building types found in the country’s current states. Absence from the list does not mean an empty queue. The per-building difference does not separate public/private; check the project in the native queue.'),
        'sedqp_row_title': ('[Building.GetState.GetName] — [Building.GetName]', '[Building.GetState.GetName] — [Building.GetName]'),
        'sedqp_row_levels': ('Nível atual: ' + building('current') + '; após fila: ' + building('after') + '; diferença: ' + building('delta') + '.', 'Current level: ' + building('current') + '; after queue: ' + building('after') + '; difference: ' + building('delta') + '.'),
        'sedqp_refresh_button': ('Ler filas agora', 'Read queues now'),
        'sedqp_refresh_tt': ('Recolhe uma nova amostra manual, sem executar obras.', 'Collects a new manual sample without executing construction.'),
        'sedqp_disable_button': ('Desativar inspeção', 'Disable inspection'),
        'sedqp_disable_tt': ('Remove as variáveis e a lista do auxiliar. Não cancela obras.', 'Removes helper variables and list. Does not cancel construction.'),
    }
    index = 0 if language == 'braz_por' else 1
    return 'l_' + language + ':\n' + '\n'.join(
        f' {key}:0 "{pair[index]}"' for key, pair in pairs.items()) + '\n'


def outputs():
    decisions = ''
    for action in ('enable', 'disable'):
        condition = 'NOT = { has_variable = sedqp_enabled }' if action == 'enable' else 'has_variable = sedqp_enabled'
        decisions += f'''sedqp_{action}_decision = {{
 is_shown = {{ is_player = yes {condition} }}
 possible = {{ is_player = yes {condition} }}
 when_taken = {{ sedqp_{action} = yes }}
 ai_chance = {{ value = 0 }}
}}
'''
    guis = '\n'.join(f'''sedqp_{action}_sgui = {{
 scope = country
 is_shown = {{ is_player = yes has_variable = sedqp_enabled }}
 is_valid = {{ is_player = yes has_variable = sedqp_enabled }}
 effect = {{ sedqp_{action} = yes }}
}}''' for action in ('refresh', 'disable'))
    journal = '''je_sedqp_queue = {
 icon = "gfx/interface/icons/generic_icons/gdp.dds"
 group = je_group_internal_affairs
 activation_description = { custom_tooltip = sedqp_activation }
 widget = { gui = "gui/journal_entry_widgets/sedqp_queue.gui" name = "sedqp_queue_widget" container = "custom_widget_container_3" }
 is_shown_when_inactive = { is_player = yes has_variable = sedqp_enabled }
 possible = { is_player = yes has_variable = sedqp_enabled }
 disable_evaluation = { NOT = { has_variable = sedqp_enabled } }
 can_deactivate = yes
 outcome = { flags = { hidden invalid_outcome } conclusion_desc = "sedqp_disabled" trigger = { NOT = { has_variable = sedqp_enabled } } }
}
'''
    text = {
        'common/decisions/sedqp_decisions.txt': decisions,
        'common/scripted_effects/sedqp_effects.txt': effects(),
        'common/scripted_guis/sedqp_guis.txt': guis,
        'common/journal_entries/sedqp_journal.txt': journal,
        'gui/journal_entry_widgets/sedqp_queue.gui': widget(),
        **{f'localization/{lang}/sedqp_l_{lang}.yml': localization(lang) for lang in ('braz_por', 'english')},
    }
    result = {name: b'\xef\xbb\xbf' + value.encode() for name, value in text.items()}
    descriptor = f'version="{VERSION}"\nname="{NAME} (test)"\nsupported_version="1.15.*"\n'
    result['descriptor.mod'] = descriptor.encode()
    result[NAME + '.mod'] = (descriptor + f'path="mod/{NAME}"\n').encode()
    result['.metadata/metadata.json'] = (json.dumps({
        'name': NAME + ' (test)', 'id': 'sed.queue_probe', 'version': VERSION,
        'supported_game_version': '1.15.*', 'tags': [], 'relationships': []
    }, indent=2) + '\n').encode()
    validate(result)
    return result


def validate(artifacts):
    """Reject mutation or foreign state in the diagnostic's executable effects."""
    allowed = {'if', 'limit', 'NOT', 'OR', 'is_player', 'has_variable',
               'has_journal_entry', 'has_inactive_journal_entry', 'set_variable',
               'change_variable', 'remove_variable', 'clear_variable_list',
               'every_scope_state', 'every_scope_building', 'is_building_type',
               'root', 'add_to_variable_list', 'add_journal_entry',
               'name', 'value', 'subtract', 'add', 'target', 'type'}
    definitions = {'sedqp_enable', 'sedqp_refresh', 'sedqp_disable'}
    entries = parse(artifacts['common/scripted_effects/sedqp_effects.txt'].decode('utf-8-sig'))
    for entry in walk(entries):
        if entry.key not in allowed | definitions:
            raise ValueError('Unapproved probe effect: ' + entry.key)
        if entry.key in ('name', 'remove_variable', 'clear_variable_list') and not str(entry.value).startswith('sedqp_'):
            raise ValueError('Foreign probe state: ' + str(entry.value))
    for name, data in artifacts.items():
        if name.endswith(('.txt', '.gui')):
            tree = parse(data.decode('utf-8-sig'))
            forbidden = {'start_building_construction', 'activate_production_method',
                         'set_tax_level', 'add_treasury', 'declare_war',
                         'trigger_event', 'cancel_construction', 'start_enactment'}
            if any(entry.key in forbidden for entry in walk(tree)):
                raise ValueError('Economic mutation or scheduling in diagnostic: ' + name)
    keys = [set(re.findall(r'^ (sedqp_\w+|je_sedqp_\w+):', artifacts[f'localization/{lang}/sedqp_l_{lang}.yml'].decode('utf-8-sig'), re.M)) for lang in ('braz_por', 'english')]
    if keys[0] != keys[1]:
        raise ValueError('Probe localization mismatch')


def package(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(outputs().items()):
            target = name if name == NAME + '.mod' else NAME + '/' + name
            info = zipfile.ZipInfo(target, date_time=(2026, 11, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / f'dist/smart-economy-queue-probe-{VERSION}.zip')
    print(package(parser.parse_args().output))
