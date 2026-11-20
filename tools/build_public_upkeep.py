"""Extract upper material/employment references for public-building methods."""
import argparse
import json
from pathlib import Path
try:
    from .pdx_script import parse, walk
except ImportError:
    from pdx_script import parse, walk


def build(game):
    def definitions(folder):
        return {e.key: e.value for p in sorted((game / 'common' / folder).glob('*.txt'))
                for e in parse(p.read_text(encoding='utf-8-sig')) if isinstance(e.value, list)}
    buildings = definitions('buildings')
    groups = definitions('production_method_groups')
    methods = definitions('production_methods')
    prices = {name: float(next(e.value for e in body if e.key == 'cost'))
              for name, body in definitions('goods').items()}
    root = Path(__file__).resolve().parents[1]
    weights = json.loads((root / 'data/employment_profiles.json').read_text())['wage_weights']
    result = {}
    for name, key in [('university', 'building_university'), ('admin', 'building_government_administration')]:
        material = jobs = 0
        profiles = []
        for group in next(e.value for e in buildings[key] if e.key == 'production_method_groups'):
            costs, employment = [], []
            profile = {}
            for method in next((e.value for e in groups.get(group.key, []) if e.key == 'production_methods'), []):
                cost = job = 0
                for entry in walk(methods.get(method.key, [])):
                    try:
                        amount = float(entry.value)
                    except (ValueError, TypeError):
                        continue
                    if amount <= 0:
                        continue
                    if entry.key.startswith('goods_input_') and entry.key.endswith('_add'):
                        cost += amount * prices[entry.key[len('goods_input_'):-4]] * 1.75
                    if entry.key.startswith('building_employment_') and entry.key.endswith('_add'):
                        job += amount * weights[entry.key[len('building_employment_'):-4]]
                technologies = next((e.value for e in methods.get(method.key, []) if e.key == 'unlocking_technologies'), [])
                profile[method.key] = dict(materials=cost, weighted_jobs=job, technologies=[e.key for e in technologies])
                costs.append(cost)
                employment.append(job)
            profiles.append(profile)
            material += max(costs, default=0)
            jobs += max(employment, default=0)
        result[name] = dict(building=key, materials=material, weighted_jobs=jobs, groups=profiles)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / 'data/public_upkeep.json'
    output.write_text(json.dumps(build(args.game), indent=2) + '\n')
    print(output)
