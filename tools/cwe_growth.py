"""Generate the opt-in growth preset for the local OGAS for CWE installation."""

import argparse
from pathlib import Path


MANAGERS = (
    ('je_cnm_construct_manager', 'cnm_default_construct_manager'),
    ('je_OGAS_building_weight_manager', 'cnm_default_building_manager'),
    ('je_cnm_pm_manager', 'cnm_default_pm_manager'),
)
SWITCHES = (
    'cnm_auto_construct_manager',
    'cnm_auto_railway_manager',
    'cnm_auto_construction_sector_manager',
    'cnm_upgrade_pm_manager',
    'cnm_balance_pm_manager',
    'cnm_workforce_employment_pm_manager',
)
JOURNAL_PATH = 'common/journal_entries/cnm_construct_manager.txt'


def preset_scripts():
    managers = '\n'.join(f''' if = {{
  limit = {{ NOT = {{ has_journal_entry = {journal} }} NOT = {{ has_inactive_journal_entry = {journal} }} }}
  add_journal_entry = {{ type = {journal} }}
  {initialize} = yes
 }}''' for journal, initialize in MANAGERS)
    switches_on = '\n'.join(f' set_variable = {{ name = {key} value = 1 }}' for key in SWITCHES)
    switches_off = '\n'.join(f' set_variable = {{ name = {key} value = 0 }}' for key in SWITCHES)
    return {
        'common/decisions/sed_cwe_growth_decisions.txt': '''sed_cwe_start_growth = {
 is_shown = { is_player = yes NOT = { has_variable = sed_cwe_growth_enabled } }
 possible = { is_player = yes }
 when_taken = { sed_cwe_start_growth_effect = yes }
 ai_chance = { value = 0 }
}

sed_cwe_stop_growth = {
 is_shown = { is_player = yes has_variable = sed_cwe_growth_enabled }
 possible = { is_player = yes }
 when_taken = { sed_cwe_stop_growth_effect = yes }
 ai_chance = { value = 0 }
}
''',
        'common/scripted_effects/sed_cwe_growth_effects.txt': f'''sed_cwe_start_growth_effect = {{
{managers}
{switches_on}
 set_variable = {{ name = OGAS_building_unit_config value = 1 }}
 set_variable = {{ name = OGAS_building_queue_config value = 12 }}
 set_variable = {{ name = cnm_pm_manage_amount value = 1 }}
 set_variable = {{ name = cnm_pm_manage_frequency value = 2 }}
 set_variable = {{ name = sed_cwe_enabled value = yes }}
 set_variable = {{ name = sed_cwe_growth_enabled value = yes }}
 sed_cwe_ensure_journal = yes
}}

sed_cwe_stop_growth_effect = {{
{switches_off}
 remove_variable = sed_cwe_growth_enabled
 remove_variable = sed_cwe_enabled
}}
''',
        'common/scripted_triggers/sed_cwe_growth_triggers.txt': '''sed_cwe_growth_allows_queue = {
 OR = {
  NOT = { has_variable = sed_cwe_growth_enabled }
  AND = {
   is_player = yes
   NOT = { in_default = yes }
   is_construction_paused = no
   net_fixed_income >= 0
   net_total_income >= 0
   gold_reserves >= sed_cwe_reserve_floor
   modifier:country_construction_add > 0
   has_variable = OGAS_building_queue_config
   construction_queue_government_duration < var:OGAS_building_queue_config
  }
 }
}
''',
    }


def guarded_journal(text):
    if 'sed_cwe_growth_allows_queue' in text:
        raise ValueError('Use the OGAS copy from before the growth preset.')
    guards = [f'root.var:{key} = 1' for key in SWITCHES[:3]]
    guards.append('construction_queue_government_duration < root.var:OGAS_building_queue_config')
    for needle in guards:
        if text.count(needle) != 1:
            raise ValueError(f'Unexpected OGAS construction journal: {needle}')
        text = text.replace(needle, needle + '\n\t\t\t\t\troot = { sed_cwe_growth_allows_queue = yes }')
    needle = '\t\t\t\t\t\tOGAS_find_best_profit_building = yes'
    if text.count(needle) != 1:
        raise ValueError('Unexpected OGAS project selection.')
    return text.replace(needle, '''						if = {
							limit = { root = { sed_cwe_growth_allows_queue = yes } }
							OGAS_find_best_profit_building = yes
						}''')


def outputs(ogas):
    scripts = preset_scripts()
    scripts[JOURNAL_PATH] = guarded_journal((ogas / JOURNAL_PATH).read_text(encoding='utf-8-sig'))
    names = {
        'braz_por': ('Ativar crescimento automático', 'Delega a construção pública e os métodos de produção ao OGAS e ativa o Director.', 'Pausar crescimento automático', 'Desliga as rotinas automáticas do perfil de crescimento.'),
        'english': ('Enable automatic growth', 'Delegates government construction and production methods to OGAS and enables the Director.', 'Pause automatic growth', 'Turns off the growth preset automation.'),
    }
    keys = ('sed_cwe_start_growth', 'sed_cwe_start_growth_desc', 'sed_cwe_stop_growth', 'sed_cwe_stop_growth_desc')
    for language, texts in names.items():
        scripts[f'localization/{language}/sed_cwe_growth_l_{language}.yml'] = (
            f'l_{language}:\n' + ''.join(f' {key}:0 "{text}"\n' for key, text in zip(keys, texts))
        )
    return {filename: text.encode('utf-8-sig') for filename, text in scripts.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ogas', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    for filename, data in outputs(args.ogas).items():
        path = args.output / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


if __name__ == '__main__':
    main()
