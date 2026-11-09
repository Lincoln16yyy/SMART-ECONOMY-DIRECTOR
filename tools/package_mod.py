"""Package only loadable mod files and an external launcher descriptor."""

import argparse
from pathlib import Path
import zipfile

try:
    from .build_mod import ROOT, VERSION, outputs
    from .validate import validate
except ImportError:
    from build_mod import ROOT, VERSION, outputs
    from validate import validate


def package(output):
    errors = validate()
    if errors:
        raise ValueError('\n'.join(errors))
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(outputs()):
            target = name if name == 'Smart Economy Director.mod' else 'Smart Economy Director/' + name
            info = zipfile.ZipInfo(target, date_time=(2026, 11, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / name).read_bytes())
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / f'dist/smart-economy-director-{VERSION}.zip')
    args = parser.parse_args()
    print(package(args.output))


if __name__ == '__main__':
    main()
