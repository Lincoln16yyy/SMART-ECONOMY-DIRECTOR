"""Build a local, provenance-aware index of buildings and production methods.

The report is an audit aid, not the game's resolved definition database. It
keeps every vanilla and enabled-mod layer instead of guessing how the engine
merges definitions and injections.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PureWindowsPath

from pdx_script import parse


CATEGORIES = {
    'buildings': 'buildings',
    'production_methods': 'production_methods',
    'production_method_groups': 'production_method_groups',
}


def walk(entries, key):
    return [entry for entry in entries if entry.key == key]


def one(entries, key):
    values = walk(entries, key)
    return values[0].value if values else None


def strings(value):
    if isinstance(value, list):
        return [entry.key for entry in value if entry.op is None]
    if isinstance(value, str):
        return [value]
    return []


def scalar(value):
    return value if isinstance(value, str) else None


def decode_definition_key(key):
    if ':' not in key:
        return 'definition', key
    operation, identifier = key.split(':', 1)
    if operation in {'INJECT', 'INJECT_OR_CREATE', 'TRY_INJECT', 'REPLACE'}:
        return operation, identifier
    return 'definition', key


def extract(category, entry):
    fields = entry.value if isinstance(entry.value, list) else []
    if category == 'buildings':
        return {
            'building_group': scalar(one(fields, 'building_group')),
            'production_method_groups': strings(one(fields, 'production_method_groups')),
            'unlocking_technologies': strings(one(fields, 'unlocking_technologies')),
            'required_construction': scalar(one(fields, 'required_construction')),
            'ownership_type': scalar(one(fields, 'ownership_type')),
            'city_type': scalar(one(fields, 'city_type')),
        }
    if category == 'production_method_groups':
        return {'production_methods': strings(one(fields, 'production_methods'))}

    modifiers = one(fields, 'building_modifiers')
    modifier_sets = {}
    if isinstance(modifiers, list):
        for scale in ('workforce_scaled', 'level_scaled'):
            values = one(modifiers, scale)
            if isinstance(values, list):
                modifier_sets[scale] = {
                    item.key: item.value for item in values
                    if item.op == '=' and isinstance(item.value, str)
                    and item.key.startswith(('goods_input_', 'goods_output_', 'building_employment_'))
                }
    return {
        'unlocking_technologies': strings(one(fields, 'unlocking_technologies')),
        'replacement_if_valid': scalar(one(fields, 'replacement_if_valid')),
        'building_modifiers': modifier_sets,
    }


def files_in(root):
    for category, folder in CATEGORIES.items():
        base = root / 'common' / folder
        if base.is_dir():
            for path in sorted(base.rglob('*.txt')):
                yield category, path


def read_layer(root, label, load_order, definitions, issues):
    if not root.is_dir():
        issues.append({'source': label, 'issue': 'source directory not found'})
        return
    for category, path in files_in(root):
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        try:
            entries = parse(raw.decode('utf-8-sig'))
        except (UnicodeError, ValueError) as error:
            issues.append({'source': label, 'path': relative, 'issue': str(error)})
            continue
        for entry in entries:
            if entry.op != '=' or not isinstance(entry.value, list):
                continue
            operation, identifier = decode_definition_key(entry.key)
            fields = extract(category, entry)
            fingerprint = hashlib.sha256(
                json.dumps(fields, sort_keys=True, separators=(',', ':')).encode()
            ).hexdigest()
            definitions[category][identifier].append({
                'source': label,
                'load_order': load_order,
                'path': relative,
                'source_sha256': hashlib.sha256(raw).hexdigest(),
                'operation': operation,
                'fields': fields,
                'fingerprint': fingerprint,
            })


def build(game, user_dir):
    load_file = user_dir / 'content_load.json'
    load = json.loads(load_file.read_text(encoding='utf-8-sig'))
    enabled = load.get('enabledMods', [])
    definitions = {category: defaultdict(list) for category in CATEGORIES}
    issues = []
    read_layer(game, 'vanilla', 0, definitions, issues)

    mod_root = user_dir / 'mod'
    enabled_mods = []
    for index, item in enumerate(enabled, start=1):
        raw_path = item.get('path', '')
        folder = PureWindowsPath(raw_path.replace('/', '\\')).name
        if not folder:
            issues.append({'source': 'launcher', 'issue': 'enabled mod has no path'})
            continue
        root = mod_root / folder
        enabled_mods.append({'load_order': index, 'folder': folder, 'found': root.is_dir()})
        read_layer(root, folder, index, definitions, issues)

    catalog = {}
    collisions = []
    for category, entries in definitions.items():
        catalog[category] = dict(sorted(entries.items()))
        for identifier, layers in sorted(entries.items()):
            fingerprints = {layer['fingerprint'] for layer in layers}
            if len(layers) > 1:
                collisions.append({
                    'category': category,
                    'id': identifier,
                    'layers': [{'source': layer['source'], 'path': layer['path'],
                                'operation': layer['operation'],
                                'fingerprint': layer['fingerprint']} for layer in layers],
                    'different_extracted_fields': len(fingerprints) > 1,
                })

    return {
        'schema': 1,
        'game_version': json.loads(
            (game.parent / 'launcher/launcher-settings.json').read_text(encoding='utf-8-sig')
        ).get('rawVersion'),
        'load_order_sha256': hashlib.sha256(load_file.read_bytes()).hexdigest(),
        'limitations': [
            'Keeps source layers; does not reproduce the engine merge or final load order semantics.',
            'INJECT and REPLACE are reported as operations, not applied to definitions.',
            'Extracted fields are a planning aid; they do not prove building eligibility, costs, or profitability.',
            'possible_producers_by_good joins definition layers to show possibilities; it does not resolve active PMs or engine merge semantics.',
            'Local report may contain third-party mod data; do not publish it without reviewing its license.',
        ],
        'enabled_mods': enabled_mods,
        'definitions': catalog,
        'possible_producers_by_good': possible_output_index(definitions),
        'collisions': collisions,
        'parse_issues': issues,
    }


def possible_output_index(definitions):
    """Index definition-layer producer possibilities without resolving merges."""
    producers = defaultdict(list)
    buildings = definitions['buildings']
    groups = definitions['production_method_groups']
    methods = definitions['production_methods']
    for building_id, building_layers in sorted(buildings.items()):
        for building_layer in building_layers:
            for group_id in building_layer['fields'].get('production_method_groups', []):
                for group_layer in groups.get(group_id, []):
                    for method_id in group_layer['fields'].get('production_methods', []):
                        for method_layer in methods.get(method_id, []):
                            goods = set()
                            for modifiers in method_layer['fields'].get('building_modifiers', {}).values():
                                for key in modifiers:
                                    if key.startswith('goods_output_') and key.endswith('_add'):
                                        goods.add(key[len('goods_output_'):-len('_add')])
                            for good in sorted(goods):
                                producers[good].append({
                                    'building_id': building_id,
                                    'building_source': building_layer['source'],
                                    'building_operation': building_layer['operation'],
                                    'pmg_id': group_id,
                                    'pmg_source': group_layer['source'],
                                    'pmg_operation': group_layer['operation'],
                                    'production_method_id': method_id,
                                    'production_method_source': method_layer['source'],
                                    'production_method_operation': method_layer['operation'],
                                })
    return dict(sorted(producers.items()))



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True, help='Victoria 3/game directory')
    parser.add_argument('--user-dir', type=Path, required=True,
                        help='Victoria 3 user data directory containing content_load.json and mod/')
    parser.add_argument('--output', type=Path, required=True,
                        help='Local output JSON path (review before sharing)')
    args = parser.parse_args()
    report = build(args.game, args.user_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts = {category: len(values) for category, values in report['definitions'].items()}
    print('Indexed ' + ', '.join(f'{key}={value}' for key, value in counts.items()))
    print(f"Found {len(report['collisions'])} layered IDs and {len(report['parse_issues'])} parse issues.")
    print(f"Local report: {args.output}")


if __name__ == '__main__':
    main()
