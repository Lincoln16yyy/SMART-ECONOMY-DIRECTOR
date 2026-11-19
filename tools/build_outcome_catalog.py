"""Extract buildable vanilla sectors and positive output goods for observation."""
import argparse
import json
from pathlib import Path

try:
    from .pdx_script import parse, walk
except ImportError:
    from pdx_script import parse, walk


def build(game):
    def definitions(category):
        return {entry.key: entry.value for path in sorted((game / 'common' / category).glob('*.txt'))
                for entry in parse(path.read_text(encoding='utf-8-sig'))
                if isinstance(entry.value, list)}
    buildings = definitions('buildings')
    groups = definitions('production_method_groups')
    methods = definitions('production_methods')
    costs = json.loads((Path(__file__).resolve().parents[1] / 'data/queued_building_costs.json').read_text())
    result = {}
    for building in sorted(costs):
        body = buildings.get(building, [])
        group_list = next((e.value for e in body if e.key == 'production_method_groups'), [])
        goods = {}
        for group in group_list:
            method_list = next((e.value for e in groups.get(group.key, []) if e.key == 'production_methods'), [])
            for method in method_list:
                for entry in walk(methods.get(method.key, [])):
                    if entry.key.startswith('goods_output_') and entry.key.endswith('_add'):
                        try:
                            positive = float(entry.value) > 0
                        except (ValueError, TypeError):
                            continue
                        if positive:
                            goods.setdefault(entry.key[len('goods_output_'):-len('_add')], set()).add(method.key)
        result[building] = {good: sorted(methods) for good, methods in sorted(goods.items())}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / 'data/outcome_goods.json'
    output.write_text(json.dumps(build(args.game), indent=2) + '\n')
    print(output)
