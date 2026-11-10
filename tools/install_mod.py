"""Update an existing local installation with backup and byte verification.

Requires a closed game and an explicit user-data path. Never edits load order
or saves and does not launch the game. Use --dry-run for read-only preflight.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import shutil
import subprocess

try:
    from .build_mod import VERSION, outputs
    from .validate import validate
except ImportError:
    from build_mod import VERSION, outputs
    from validate import validate


def install(user_data, dry_run=False):
    errors = validate()
    if errors:
        raise ValueError('\n'.join(errors))
    check = subprocess.run(['pgrep', '-ix', 'victoria3.exe'], capture_output=True)
    if check.returncode != 1:
        raise RuntimeError('Close Victoria 3 before installation; process check did not confirm it is closed.')
    base = Path(user_data).expanduser().resolve()
    mod = base / 'mod' / 'Smart Economy Director'
    descriptor = base / 'mod' / 'Smart Economy Director.mod'
    load = base / 'content_load.json'
    if not mod.is_dir() or not descriptor.is_file() or not load.is_file():
        raise ValueError('Expected an existing Director installation and content_load.json: ' + str(base))
    if mod.is_symlink() or descriptor.is_symlink():
        raise ValueError('Refusing to replace a symlink installation.')
    original_load = load.read_bytes()
    expected = outputs()
    result = {'version': VERSION, 'files': len(expected), 'dry_run': dry_run}
    if dry_run:
        return result
    backup = base / 'sed_backups' / ('mod_before_' + VERSION + '_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    backup.mkdir(parents=True)
    staged = backup / 'new_installation'
    retired = backup / 'Smart Economy Director'
    shutil.copy2(descriptor, backup / descriptor.name)
    shutil.copy2(load, backup / load.name)
    for name, data in expected.items():
        if name == descriptor.name:
            continue
        target = staged / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    mod.rename(retired)
    try:
        staged.rename(mod)
        descriptor.write_bytes(expected[descriptor.name])
        for name, data in expected.items():
            target = descriptor if name == descriptor.name else mod / name
            if target.read_bytes() != data:
                raise ValueError('Installation differs: ' + name)
        if load.read_bytes() != original_load:
            raise ValueError('Load order changed during installation; investigate external writer.')
    except BaseException:
        if mod.exists():
            mod.rename(backup / 'failed_installation')
        retired.rename(mod)
        shutil.copy2(backup / descriptor.name, descriptor)
        raise
    result.update(backup=str(backup), load_order_unchanged=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user-data', required=True, type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(args.user_data, args.dry_run), ensure_ascii=False))


if __name__ == '__main__':
    main()
