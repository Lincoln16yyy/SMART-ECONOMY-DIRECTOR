"""Prepare the author's OGAS repository for the vanilla Director profile."""

import argparse
from pathlib import Path
import re
import shutil

try:
    from . import cwe_growth
    from .cwe_compat import shortage_supply_methods, shortage_trigger
except ImportError:
    import cwe_growth
    from cwe_compat import shortage_supply_methods, shortage_trigger


def patch_original(root):
    values = root / 'common/script_values/AUTO_database_pm_goods.txt'
    seen = {}
    lines = []
    for line in values.read_text(encoding='utf-8-sig').splitlines(keepends=True):
        entry = re.fullmatch(r'([a-zA-Z0-9_]+)\s*=\s*(-?[\d.]+)\s*', line)
        if entry:
            key, value = entry.groups()
            if key in seen:
                if seen[key] != value:
                    raise ValueError(f'Conflicting OGAS coefficients for {key}.')
                continue
            seen[key] = value
        lines.append(line)
    values.write_text(''.join(lines), encoding='utf-8-sig')
    # Preserve the last (MANUAL) definition and the rest of the AUTO file.
    removals = {
        'common/scripted_effects/AUTO_building_weight_manager.txt': 'OGAS_default_building_weight_manager',
        'common/scripted_triggers/cnm_OGAS_scripted_triggers.txt': 'cnm_state_building_construction_sector_unit_profit_predict',
    }
    for filename, key in removals.items():
        path = root / filename
        text = path.read_text(encoding='utf-8-sig')
        changed, count = re.subn(rf'(?ms)^{key}\s*=\s*\{{\n.*?^\}}\n', '', text)
        if count != 1:
            raise ValueError(f'Unexpected definition of {key}.')
        path.write_text(changed, encoding='utf-8-sig')


def prepare(source, game, output):
    shutil.copytree(source / 'common', output / 'common')
    shutil.copytree(source / 'localization', output / 'localization')
    shutil.copytree(source / '.metadata', output / '.metadata')
    patch_original(output)
    scripts = cwe_growth.outputs(output)
    scripts['common/scripted_triggers/sed_ogas_shortage.txt'] = shortage_trigger(
        shortage_supply_methods(game)).encode('utf-8-sig')
    for filename, raw in scripts.items():
        text = raw.decode('utf-8-sig')
        text = text.replace(
            ' set_variable = { name = sed_cwe_enabled value = yes }\n'
            ' set_variable = { name = sed_cwe_growth_enabled value = yes }\n'
            ' sed_cwe_ensure_journal = yes',
            ' if = { limit = { NOT = { has_variable = sed_enabled } } sed_enable_country = yes }\n'
            ' set_variable = { name = sed_cwe_growth_enabled value = yes }\n'
            ' sed_set_mode_automatic = yes',
        ).replace(' sed_cwe_disable_country = yes', ' sed_set_mode_assisted = yes')
        text = text.replace('sed_cwe_reserve_floor', '{ value = sed_fixed_expenses_value multiply = 4 }')
        if filename == cwe_growth.JOURNAL_PATH:
            # The public repo precedes the loop bound in the CWE fork.
            text = text.replace('while = {\n', 'while = {\n\t\t\t\t\tcount = 1000\n', 1)
        path = output / filename.replace('sed_cwe_', 'sed_ogas_')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.replace('sed_cwe_', 'sed_ogas_'), encoding='utf-8-sig')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('game', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    prepare(args.source, args.game, args.output)
