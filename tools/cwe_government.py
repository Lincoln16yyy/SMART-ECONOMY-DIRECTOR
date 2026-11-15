"""Rebuild Smart Government Advisor against the Cold War Era law database."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

NAME = 'Smart Government Advisor - Cold War Era'
RUNTIME = ('common', 'gui', 'localization')
LAW_INPUTS = ('laws', 'law_groups', 'technology', 'static_modifiers')
COLLIDING_KEY = 'sg_law_name_191'


def copy_law_inputs(game, cwe, destination):
    metadata = json.loads((cwe / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))
    if (metadata['id'], metadata['version'], metadata['supported_game_version']) != ('2988303719', '0.99', '1.15.1'):
        raise ValueError('Use Cold War Era 0.99 for Victoria 3 1.15.1.')
    replaced = {Path(path) for path in metadata['game_custom_data']['replace_paths']}
    for category in LAW_INPUTS:
        folder = Path('common') / category
        for source in (game, cwe):
            for path in sorted((source / folder).rglob('*.txt')):
                relative = path.relative_to(source)
                if source == game and any(directory in relative.parents for directory in replaced):
                    continue
                target = destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'Unexpected Smart Government generator near {old!r}.')
    return text.replace(old, new, 1)


def adapt_generator(stage):
    path = stage / 'tools/build_law_data.py'
    text = path.read_text(encoding='utf-8-sig')
    needle = '        lines.append("\\tNOT = { enacting_any_law = yes }")'
    text = replace_once(text, needle, needle + '''
        # Keep these laws in group merit comparisons, but do not recommend
        # a change when a prerequisite is absent from the conversion.
        if law["group"] == "lawgroup_army_model" or any(
            tech in {"tech_greeness_2", "tech_greeness_5", "tech_greeness_8"}
            for tech in law["unlocking_technologies"]
        ):
            out += [lines[0], "\\talways = no", "}", ""]
            continue
'''.rstrip())
    # Read deficit and reserves directly. This is a coverage proxy, not a date
    # for bankruptcy, and applies only to this generated edition.
    text, count = re.subn(
        r'weeks_until_bankruptcy < (26|52)',
        lambda match: ('net_total_income < 0 gold_reserves < '
                       f'{{ value = net_total_income multiply = -{match[1]} }}'),
        text,
    )
    if count != 2:
        raise ValueError('Unexpected Smart Government fiscal scoring.')
    path.write_text(text, encoding='utf-8')


def build(source, game, cwe, stage):
    for folder in (*RUNTIME, 'tools', 'data'):
        shutil.copytree(source / folder, stage / folder, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copyfile(source / 'Smart Government Advisor.mod', stage / 'Smart Government Advisor.mod')
    adapt_generator(stage)
    with TemporaryDirectory(prefix='sg-cwe-laws-') as temporary:
        inputs = Path(temporary)
        copy_law_inputs(game, cwe, inputs)
        subprocess.run([sys.executable, str(stage / 'tools/build_law_data.py'),
                        '--game', str(inputs), '--out', str(stage)], check=True)
        subprocess.run([sys.executable, str(stage / 'tools/build_gui.py')], check=True)
        subprocess.run([sys.executable, str(stage / 'tools/validate.py'),
                        '--game', str(inputs)], check=True)
    # This key collides with a character name in the 1.15 game localization.
    paths = [stage / 'gui/journal_entry_widgets/sg_law_advisor.gui',
             *stage.glob('localization/*/sg_generated_l_*.yml')]
    for path in paths:
        text = path.read_text(encoding='utf-8-sig')
        path.write_text(re.sub(rf'\b{COLLIDING_KEY}\b', 'sg_cwe_law_name_191', text), encoding='utf-8-sig')


def package(source, game, cwe, output):
    with TemporaryDirectory(prefix='sg-cwe-build-') as temporary:
        stage = Path(temporary)
        build(source, game, cwe, stage)
        meta = json.loads((source / '.metadata/metadata.json').read_text(encoding='utf-8-sig'))
        meta.update(name=NAME, id='sg.smart_government_advisor_cwe', supported_game_version='1.15.1',
                    relationships=[{'rel_type': 'dependency', 'id': '2988303719',
                                    'display_name': 'Cold War Era (1950)', 'resource_type': 'mod',
                                    'version': '0.99'}])
        descriptor = f'name="{NAME}"\nversion="{meta["version"]}"\nsupported_version="1.15.1"\n'
        files = {
            f'{NAME}.mod': (descriptor + f'path="mod/{NAME}"\n').encode(),
            f'{NAME}/descriptor.mod': descriptor.encode(),
            f'{NAME}/.metadata/metadata.json': (json.dumps(meta, indent=2) + '\n').encode(),
        }
        for folder in RUNTIME:
            for path in (stage / folder).rglob('*'):
                if path.is_file():
                    files[f'{NAME}/{path.relative_to(stage).as_posix()}'] = path.read_bytes()
        output.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                info = ZipInfo(name, date_time=(2026, 11, 15, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, data)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--government', required=True, type=Path)
    parser.add_argument('--game', required=True, type=Path)
    parser.add_argument('--cwe', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path('dist/smart-government-advisor-cwe.zip'))
    args = parser.parse_args()
    print(package(args.government, args.game, args.cwe, args.output))


if __name__ == '__main__':
    main()
