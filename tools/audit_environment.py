"""Read-only source audit. This is research tooling, not a game-script validator."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import zipfile


TOKEN = re.compile(r'#[^\n]*|"(?:\\.|[^"\\])*"|\s+|[{}=]|[^\s{}=#"]+')
OPERATIONS = {"INJECT", "INJECT_OR_CREATE", "REPLACE", "TRY_INJECT"}
SAVE_MARKERS = (
    "advisor_enabled", "advisor_auto_construction_enabled",
    "advisor_labor_auto_enabled", "advisor_pm_balance_enabled",
)


def field_fingerprints(tokens):
    """Hash token sequences of immediate fields; no numerical/engine equivalence."""
    fields = defaultdict(list)
    i = 0
    while i + 2 < len(tokens):
        if tokens[i + 1] != '=':
            i += 1
            continue
        start = i + 2
        end = start + 1
        if tokens[start] == '{':
            depth = 1
            while depth and end < len(tokens):
                depth += (tokens[end] == '{') - (tokens[end] == '}')
                end += 1
        fields[tokens[i]].append(digest(' '.join(tokens[start:end]).encode()))
        i = end
    return dict(fields)


def definitions(text, include_fields=False):
    """Return top-level block names, operations and lines, without interpreting them."""
    tokens = [m for m in TOKEN.finditer(text.lstrip('\ufeff'))
              if not m.group().isspace() and not m.group().startswith('#')]
    text = text.lstrip('\ufeff')
    depth = 0
    result = []
    start = None
    for i, match in enumerate(tokens):
        token = match.group()
        if depth == 0 and i + 2 < len(tokens):
            if tokens[i + 1].group() == '=' and tokens[i + 2].group() == '{':
                name = token.strip('"')
                operation = 'definition'
                prefix, separator, rest = name.partition(':')
                if separator and prefix in OPERATIONS:
                    operation, name = prefix, rest
                result.append({'id': name, 'operation': operation,
                               'line': text.count('\n', 0, match.start()) + 1})
                start = i + 3
        if token == '{':
            depth += 1
        elif token == '}':
            depth -= 1
            if depth < 0:
                raise ValueError('Unbalanced closing brace')
            if depth == 0 and include_fields and start is not None:
                result[-1]['fields'] = field_fingerprints(
                    [m.group() for m in tokens[start:i]])
                start = None
    if depth:
        raise ValueError('Unbalanced opening brace')
    return result


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_summary(path):
    """Never infer active country variables from strings inside binary saves."""
    with zipfile.ZipFile(path) as archive:
        data = archive.read('gamestate')
    binary = b'\x00' in data[:4096]
    return {
        'file': path.name,
        'gamestate_sha256': digest(data),
        'encoding': 'binary' if binary else 'text_candidate',
        'automation_state': 'unverified_requires_country_scoped_decode',
        'marker_occurrences_not_active_flags': {
            marker: data.count(marker.encode()) for marker in SAVE_MARKERS
        },
        'kuromi_name_present_not_proof_of_current_load_order': b"Kuromi's AI" in data,
    }


def installed_mod_name(raw_path):
    # Handles both Wine paths and native Linux launcher paths, without expanding them.
    return PureWindowsPath(raw_path.replace('/', '\\')).name


def source_files(root):
    for folder, pattern in [('common', '*.txt'), ('gui', '*.gui')]:
        for path in sorted((root / folder).rglob(pattern)):
            yield path.relative_to(root).as_posix(), path.read_bytes()


def audit(game, user_dir, kuromi_zip=None, saves=()):
    load_order = json.loads((user_dir / 'content_load.json').read_text())
    enabled = [installed_mod_name(entry['path']) for entry in load_order['enabledMods']]
    vanilla_files = dict(source_files(game))
    vanilla_ids = set()
    vanilla_pm_fields = {}
    issues = []
    for path, data in vanilla_files.items():
        if path.startswith('common/'):
            try:
                is_pm = path.startswith('common/production_methods/')
                for entry in definitions(data.decode('utf-8-sig'), include_fields=is_pm):
                    vanilla_ids.add((path.split('/')[1], entry['id']))
                    if is_pm:
                        vanilla_pm_fields[entry['id']] = entry.get('fields', {})
            except (ValueError, UnicodeError) as error:
                issues.append({'source': 'vanilla', 'path': path, 'error': str(error)})
    providers = defaultdict(list)
    mods = []
    for name in enabled:
        root = user_dir / 'mod' / name
        record = {'folder': name, 'found': root.is_dir(), 'same_path_as_vanilla': [],
                  'entries_also_in_vanilla': [], 'file_count': 0}
        metadata_path = root / '.metadata/metadata.json'
        if metadata_path.is_file():
            metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
            record['declared_metadata'] = {key: metadata[key] for key in
                ['name', 'version', 'supported_game_version'] if key in metadata}
        for path, data in source_files(root):
            record['file_count'] += 1
            if path in vanilla_files:
                record['same_path_as_vanilla'].append(path)
            if not path.startswith('common/'):
                continue
            category = path.split('/')[1]
            try:
                entries = definitions(data.decode('utf-8-sig'),
                                      include_fields=category == 'production_methods')
            except (ValueError, UnicodeError) as error:
                issues.append({'source': name, 'path': path, 'error': str(error)})
                continue
            for entry in entries:
                fields = entry.pop('fields', {})
                if category == 'production_methods' and entry['id'] in vanilla_pm_fields:
                    original = vanilla_pm_fields[entry['id']]
                    entry['different_token_fields_from_vanilla'] = [
                        field for field in sorted(set(original) | set(fields))
                        if original.get(field) != fields.get(field)]
                reference = {'mod': name, 'path': path, **entry}
                providers[(category, entry['id'])].append(reference)
                if (category, entry['id']) in vanilla_ids:
                    record['entries_also_in_vanilla'].append({
                        'path': path, **entry, 'sha256': digest(data)})
        mods.append(record)
    shared = [
        {'category': category, 'id': name, 'providers': refs}
        for (category, name), refs in sorted(providers.items())
        if len({ref['mod'] for ref in refs}) > 1
    ]
    kuromi = None
    if kuromi_zip:
        with zipfile.ZipFile(kuromi_zip) as archive:
            names = archive.namelist()
            metadata = next(n for n in names if n.endswith('/.metadata/metadata.json'))
            kuromi = {'archive': kuromi_zip.name,
                      'metadata': json.loads(archive.read(metadata).decode('utf-8-sig')),
                      'inspected_as_archive_only': True,
                      'entries_also_in_enabled_mods': []}
            for name in sorted(names):
                relative = name.split('/', 1)[-1]
                if not relative.startswith('common/') or not relative.endswith('.txt'):
                    continue
                category = relative.split('/')[1]
                try:
                    entries = definitions(archive.read(name).decode('utf-8-sig'))
                except (ValueError, UnicodeError) as error:
                    issues.append({'source': 'kuromi_archive', 'path': relative,
                                   'error': str(error)})
                    continue
                for entry in entries:
                    refs = providers.get((category, entry['id']))
                    if refs:
                        kuromi['entries_also_in_enabled_mods'].append({
                            'category': category, 'path': relative, **entry,
                            'enabled_providers': sorted({r['mod'] for r in refs})})
    return {
        'schema': 1, 'game_version': json.loads(
            (game.parent / 'launcher/launcher-settings.json').read_text())['rawVersion'],
        'load_order_sha256': digest((user_dir / 'content_load.json').read_bytes()),
        'limitations': [
            'Static top-level block audit; no engine merge or load-order resolution.',
            'Shared namespaces and INJECT entries are candidates for review, not proven conflicts.',
            'Binary save marker occurrences do not establish value, ownership or activation.',
            'No original source code or save contents included in this report.',
        ],
        'enabled_folders_in_launcher_order': enabled, 'mods': mods,
        'shared_top_level_entries': shared, 'kuromi_archive': kuromi,
        'saves': [save_summary(path) for path in saves], 'parse_issues': issues,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True, help='Victoria 3/game')
    parser.add_argument('--user-dir', type=Path, required=True)
    parser.add_argument('--kuromi-zip', type=Path)
    parser.add_argument('--save', type=Path, action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.game, args.user_dir, args.kuromi_zip, args.save)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"Audited {len(report['mods'])} enabled mods; "
          f"{len(report['shared_top_level_entries'])} shared entries; "
          f"{len(report['parse_issues'])} parse issues. Report: {args.output}")


if __name__ == '__main__':
    main()
