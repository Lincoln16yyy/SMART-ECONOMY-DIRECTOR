"""Validate generated files, references and the approved-action boundary."""

import argparse
import json
import os
from pathlib import Path
import re

try:
    from .build_mod import PERSISTENT_VARIABLES, ROOT, outputs, runtime_variables
    from .pdx_script import parse, walk, child
except ImportError:
    from build_mod import PERSISTENT_VARIABLES, ROOT, outputs, runtime_variables
    from pdx_script import parse, walk, child


def validate(root=ROOT, game=None):
    errors = []
    trees = {}
    expected = outputs()
    for name, data in expected.items():
        path = root / name
        if not path.is_file():
            errors.append('Missing file: ' + name)
        elif path.read_bytes() != data:
            errors.append('Generated file differs: ' + name)
    for folder, pattern in [('common', '*.txt'), ('events', '*.txt'), ('gui', '*.gui')]:
        for path in (root / folder).rglob(pattern):
            relative = path.relative_to(root).as_posix()
            if relative not in expected:
                errors.append('Unexpected game file: ' + relative)
            if not path.read_bytes().startswith(b'\xef\xbb\xbf'):
                errors.append('Missing UTF-8 BOM: ' + relative)
            try:
                trees[relative] = parse(path.read_text(encoding='utf-8-sig'))
            except ValueError as error:
                errors.append(relative + ': ' + str(error))
    custom = {}
    for name, tree in trees.items():
        if not name.startswith('common/'):
            continue
        for entry in tree:
            if entry.key == 'on_monthly_pulse_country' and '/on_actions/' in name:
                continue
            if not entry.key.startswith(('sed_', 'je_sed_')):
                errors.append('Foreign top-level ID: ' + entry.key)
            if entry.key in custom:
                errors.append('Duplicate custom definition: ' + entry.key)
            custom[entry.key] = entry.value
    allowed_effects = {'if', 'else_if', 'else', 'limit', 'set_variable', 'remove_variable',
                       'change_variable', 'root', 'prev', 'owner', 'every_scope_state',
                       'every_scope_building', 'ordered_scope_state', 'clear_variable_list',
                       'add_to_variable_list', 'add_journal_entry', 'start_building_construction',
                       'trigger_event', 'order_by', 'max', 'check_range_bounds',
                       'set_tax_level', 'set_government_wage_level'}
    tax_effects = {'sed_apply_fiscal_policy', 'sed_restore_fiscal_policy'}
    wage_effects = {'sed_apply_wage_policy', 'sed_restore_wage_policy'}
    tax_levels = {'very_low', 'low', 'medium', 'high', 'very_high'}

    # Narrow, reviewed exception: only two guarded adapter effects may change
    # these reviewed country options. All other foreign mutations stay rejected.
    coordinated_options = {
        'advisor_auto_construction_enabled', 'zw_var_expand_building',
        'zw_var_more_construction_sectors', 'zw_var_scsab_construct_railway',
        'zw_var_scsab_construct_power_plant', 'zw_var_scsab_gov_admin',
        'zw_var_scsab_gov_admin_for_tax',
        'advisor_setting_sc_goal_sol', 'advisor_setting_sc_goal_treasury',
        'advisor_setting_treasury_off', 'advisor_setting_borrow',
    }
    for effect_name in ('sed_coord_sync', 'sed_coord_restore'):
        top = custom.get(effect_name, [])
        outer = top[0] if len(top) == 1 else None
        guard = child(outer.value, 'limit') if outer and outer.key == 'if' else []
        required = {'is_player': 'yes', 'has_variable': 'sed_coord_active'}
        if not all(any(e.key == key and e.value == value for e in guard)
                   for key, value in required.items()):
            errors.append('External adapter lacks explicit player/coordination guard: ' + effect_name)
    def check_effects(entries, effect_name=None):
        for entry in entries:
            if entry.key.startswith('sed_'):
                if entry.key not in custom:
                    errors.append('Undefined effect: ' + entry.key)
            elif entry.key not in allowed_effects:
                errors.append('Unexpected effect in diagnostics: ' + entry.key)
            if entry.key == 'set_tax_level':
                if effect_name not in tax_effects or entry.value not in tax_levels:
                    errors.append('Tax level change outside the reviewed fiscal policy: ' + str(entry.value))
            if entry.key == 'set_government_wage_level':
                if effect_name not in wage_effects or entry.value not in tax_levels:
                    errors.append('Wage level change outside the reviewed wage policy: ' + str(entry.value))
            if entry.key == 'remove_variable':
                if not str(entry.value).startswith('sed_'):
                    if effect_name not in ('sed_coord_sync', 'sed_coord_restore') or entry.value not in coordinated_options:
                        errors.append('Foreign variable removed: ' + str(entry.value))
            elif entry.key in ('set_variable', 'change_variable'):
                target_name = child(entry.value, 'name')
                if not target_name.startswith('sed_'):
                    if effect_name not in ('sed_coord_sync', 'sed_coord_restore') or target_name not in coordinated_options:
                        errors.append('Foreign variable written')
            elif entry.key in ('if', 'else_if', 'else', 'root', 'prev', 'owner',
                               'every_scope_state', 'every_scope_building', 'ordered_scope_state'):
                check_effects([e for e in entry.value if e.key != 'limit'], effect_name)
    for name, tree in trees.items():
        if '/scripted_effects/' in name:
            for entry in tree:
                check_effects(entry.value, entry.key)
        for entry in walk(tree):
            if entry.key == 'effect' and isinstance(entry.value, list):
                check_effects(entry.value)
            if '/events/' in name and entry.key == 'immediate' and isinstance(entry.value, list):
                check_effects(entry.value)
            if entry.key.startswith('var:') and entry.op == '=' and isinstance(entry.value, list):
                numeric_ops = {'value', 'add', 'subtract', 'multiply', 'divide'}
                if any(item.key in numeric_ops for item in entry.value):
                    errors.append('Inline arithmetic in variable equality requires a named script value: ' + entry.key)
            if entry.key.startswith('sed_') and entry.value == 'yes' and entry.key not in custom:
                errors.append('Undefined scripted call: ' + entry.key)
    all_text = '\n'.join(p.read_text(encoding='utf-8-sig') for p in (root / 'common').rglob('*.txt'))
    for name, monthly_guard in (
        ('sed_apply_fiscal_policy', 'sed_tax_month_limit_reached'),
        ('sed_apply_wage_policy', 'sed_wage_month_limit_reached'),
    ):
        body = custom.get(name, [])
        outer = body[0] if len(body) == 1 else None
        limit = child(outer.value, 'limit') if outer and outer.key == 'if' else []
        for key, value in [('is_player', 'yes'), ('has_variable', 'sed_enabled'),
                           ('has_variable', 'sed_mode_automatic')]:
            if not any(entry.key == key and entry.value == value for entry in limit):
                errors.append('Fiscal/wage policy lacks required execution guard: ' + name + ' ' + value)
        for key, value in [(monthly_guard, 'yes'), ('has_variable', 'sed_mode_manual'),
                           ('has_variable', 'sed_mode_assisted')]:
            if not any(entry.key == 'NOT' and isinstance(entry.value, list)
                       and any(item.key == key and item.value == value for item in entry.value)
                       for entry in limit):
                errors.append('Fiscal/wage policy lacks monthly or mode exclusion: ' + name + ' ' + value)
    for mutation in ('activate_production_method', 'start_enactment', 'add_treasury',
                     'declare_war', 'add_modifier'):
        if re.search(r'\b' + mutation + r'\s*=', all_text):
            errors.append('Unexpected economic/political mutation: ' + mutation)
    construction_calls = [(name, entry) for name, tree in trees.items() for entry in walk(tree)
                          if entry.key == 'start_building_construction']
    approved_actions = {'sed_run_railway_approval': {'building_railway'},
                        'sed_run_construction_approval': {'building_construction_sector'}}
    try:
        from .build_mod import SUPPLY_TARGETS, variants
    except ImportError:
        from build_mod import SUPPLY_TARGETS, variants
    approved_actions.update({f"sed_run_{item['good']}_approval":
                             {variant['building'] for variant in variants(item)}
                             for item in SUPPLY_TARGETS})
    construction_error = False
    covered = 0
    for effect, allowed in approved_actions.items():
        approved_construction = [entry for entry in walk(custom.get(effect, []))
                                 if entry.key == 'start_building_construction']
        covered += len(approved_construction)
        if not approved_construction or any(entry.value not in allowed
                                            for entry in approved_construction):
            construction_error = True
    if (covered != len(construction_calls) or construction_error
            or any(name != 'common/scripted_effects/sed_effects.txt' for name, _ in construction_calls)):
        errors.append('Each approved action may queue only its declared building levels')
    cleaned = {entry.value for entry in walk(custom.get('sed_disable_country', []))
               if entry.key == 'remove_variable'}
    assigned = {child(entry.value, 'name') for tree in trees.values() for entry in walk(tree)
                if entry.key == 'set_variable' and str(child(entry.value, 'name')).startswith('sed_')}
    if assigned - cleaned != set(PERSISTENT_VARIABLES):
        errors.append('Cleanup must retain only declared persistent safety state: ' + str(sorted(assigned - cleaned)))
    if cleaned & set(PERSISTENT_VARIABLES):
        errors.append('Cleanup must preserve the schema and monthly safety markers')
    if set(runtime_variables()) != cleaned:
        errors.append('Runtime variable registry differs from cleanup')
    keys = {}
    for language in ('braz_por', 'english'):
        path = root / f'localization/{language}/sed_l_{language}.yml'
        if not path.exists():
            continue
        if not path.read_bytes().startswith(b'\xef\xbb\xbf'):
            errors.append('Missing localization BOM: ' + language)
        text = path.read_text(encoding='utf-8-sig')
        if not text.startswith('l_' + language + ':'):
            errors.append('Wrong localization header: ' + language)
        found = re.findall(r'^ (\w+):0 "', text, re.M)
        if len(found) != len(set(found)):
            errors.append('Duplicate localization key: ' + language)
        keys[language] = set(found)
        for variable in re.findall(r"Var\('(sed_\w+)'\)", text):
            if variable not in assigned:
                errors.append('Uninitialized displayed variable: ' + variable)
    if keys.get('braz_por') != keys.get('english'):
        errors.append('Localization key sets differ')
    gui = root / 'gui/journal_entry_widgets/sed_diagnostics.gui'
    if gui.exists():
        text = gui.read_text(encoding='utf-8-sig')
        for key in re.findall(r'(?:text|tooltip)\s*=\s*"(sed_\w+)"', text):
            if key not in keys.get('english', set()):
                errors.append('Missing GUI localization: ' + key)
        for name in re.findall(r"GetScriptedGui\('([^']+)'\)", text):
            if name not in custom:
                errors.append('Missing SGUI: ' + name)
        if 'HasVariable(' in text:
            errors.append('HasVariable is not a valid GUI data function')
        for entry in walk(trees.get('gui/journal_entry_widgets/sed_diagnostics.gui', [])):
            if entry.key == 'widget' and any(e.key == 'autoresize' for e in entry.value):
                errors.append('autoresize is only allowed on textboxes')
    journal = custom.get('je_sed_diagnostics', [])
    if any(e.key == 'on_monthly_pulse' for e in journal):
        errors.append('Duplicate update owner: Journal Entry must not refresh monthly')
    for key in ('je_sed_diagnostics', 'je_sed_diagnostics_reason', 'sed_enable', 'sed_enable_desc',
                'sed_disable_decision', 'sed_disable_decision_desc', 'sed_activation_tt', 'sed_disabled_desc'):
        if key not in keys.get('english', set()):
            errors.append('Missing game localization: ' + key)
    if game:
        game = Path(game)
        if not (game / 'common').is_dir():
            errors.append('Invalid game directory: ' + str(game))
        if not (game / 'gfx/interface/icons/generic_icons/gdp.dds').is_file():
            errors.append('Missing GDP icon in game installation')
        for path in (root / 'common').rglob('*.txt'):
            if (game / path.relative_to(root)).exists():
                errors.append('Overrides vanilla file: ' + str(path.relative_to(root)))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, default=os.environ.get('VICTORIA3_GAME'))
    args = parser.parse_args()
    errors = validate(game=args.game)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Static validation passed. Engine loading and in-game actions still require runtime tests.')
    if not args.game:
        print('Game asset checks skipped: pass --game or VICTORIA3_GAME.')


if __name__ == '__main__':
    main()
