"""Extrai seis cadeias avançadas das definições do jogo base instalado."""
import argparse
import hashlib
import json
from pathlib import Path
try:
    from .pdx_script import parse, walk
except ImportError:
    from pdx_script import parse, walk

# IDs verified in game/common/buildings and outcome_goods.json, not guessed.
TARGETS = (
    ('steel', 'building_steel_mill', 'aço', 'siderúrgica', 'steel mill'),
    ('glass', 'building_glassworks', 'vidro', 'vidraria', 'glassworks'),
    ('engines', 'building_motor_industry', 'motores', 'indústria de motores', 'motor industry'),
    ('fertilizer', 'building_chemical_plant', 'fertilizante', 'indústria química', 'chemical plant'),
    ('sulfur', 'building_sulfur_mine', 'enxofre', 'mina de enxofre', 'sulfur mine'),
    ('lead', 'building_lead_mine', 'chumbo', 'mina de chumbo', 'lead mine'),
)


def field(body, key, default=None):
    return next((e.value for e in body if e.key == key), default)


def extend(game, data):
    sources = {}
    def definitions(category):
        result = {}
        for path in sorted((game / 'common' / category).glob('*.txt')):
            raw = path.read_bytes()
            for entry in parse(raw.decode('utf-8-sig')):
                if isinstance(entry.value, list):
                    result[entry.key] = entry.value
                    sources[entry.key] = dict(path=str(path.relative_to(game)), sha256=hashlib.sha256(raw).hexdigest())
        return result
    buildings, groups, methods, goods = [definitions(c) for c in ('buildings', 'production_method_groups', 'production_methods', 'goods')]
    names = ['input_profiles', 'founding_method_groups', 'founding_production_methods',
             'founding_method_economics', 'employment_profiles', 'labor_requirements', 'supplier_output_profiles']
    docs = {n: json.loads((data / (n+'.json')).read_text()) for n in names}
    prices = {good: float(field(body, 'cost')) for good, body in goods.items()}
    records, used = [], set()
    for good, building, pt, bpt, ben in TARGETS:
        assert building in buildings
        profiles, startup, inputs, employment, economics, all_outputs = [], [], {}, {}, {}, {}
        workers = 0
        used.add(building)
        for group in field(buildings[building], 'production_method_groups', []):
            used.add(group.key)
            alternatives = [e.key for e in field(groups[group.key], 'production_methods', [])]
            assert alternatives
            profile, jobs = {}, []
            startup.append(dict(group=group.key, method=alternatives[0], alternatives=alternatives))
            for method in alternatives:
                used.add(method)
                body = methods[method]
                tech = [e.key for e in field(body, 'unlocking_technologies', [])]
                inc, out, emp = {}, {}, {}
                for e in walk(body):
                    if not isinstance(e.value, str): continue
                    try: amount = float(e.value)
                    except ValueError: continue
                    for prefix, target in [('goods_input_',inc), ('goods_output_',out), ('building_employment_',emp)]:
                        if e.key.startswith(prefix) and e.key.endswith('_add'):
                            key = e.key[len(prefix):-4]
                            target[key] = target.get(key, 0) + amount
                inputs[method] = inc
                if out: all_outputs[method] = out
                job = sum(emp.values()); jobs.append(job)
                employment[method] = dict(employment=emp, jobs=job,
                    weighted_jobs=sum(v*docs['employment_profiles']['wage_weights'][k] for k,v in emp.items()))
                profile[method] = tech
                if good in out and group == field(buildings[building], 'production_method_groups')[0]:
                    economics[method] = dict(inputs=inc, outputs=out, workers=job, technologies=tech)
            profiles.append(profile)
            workers += max(0, max(jobs, default=0))
        assert economics, (good, building)
        docs['input_profiles'][building] = inputs
        docs['founding_method_groups'][building] = profiles
        docs['founding_production_methods'][building] = startup
        docs['founding_method_economics']['buildings'][building] = economics
        docs['founding_method_economics']['all_outputs'][building] = all_outputs
        for product in ({k for d in inputs.values() for k in d} | {k for d in all_outputs.values() for k in d}):
            docs['founding_method_economics']['prices'][product] = prices[product]
        docs['employment_profiles']['buildings'][building] = employment
        assert workers.is_integer(), (building, workers)
        docs['labor_requirements'][building] = int(workers)
        docs['supplier_output_profiles'][building] = {m:spec['outputs'][good] for m,spec in economics.items()}
        records.append(dict(good=good, building=building, methods=list(economics), label_pt=pt,
                            label_en=good, building_pt=bpt, building_en=ben))
    for name, doc in docs.items():
        (data / (name+'.json')).write_text(json.dumps(doc, ensure_ascii=False, indent=2)+'\n')
    (data/'advanced_targets.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    (data/'advanced_sources.json').write_text(json.dumps({k:sources[k] for k in sorted(used)}, indent=2)+'\n')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--game', type=Path, required=True)
    a=p.parse_args();extend(a.game, Path(__file__).resolve().parents[1]/'data')
