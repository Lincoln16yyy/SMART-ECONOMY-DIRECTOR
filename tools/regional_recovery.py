"""Recupera setores por local, sem usar uma falha como veto nacional."""
try:
    from . import investment_outcomes, labor, planning
except ImportError:
    import investment_outcomes, labor, planning


def triggers(items, variants):
    parts = []
    for item in items:
        good = item['good']
        if good in planning.MILITARY_INDUSTRY_GOODS:
            continue
        vs = variants(item)
        present = ' '.join('has_building = '+v['building'] for v in vs)
        pending = ' '.join(f"AND = {{ has_building = {v['building']} b:{v['building']} = {{ level_after_queued_constructions > level }} }}" for v in vs)
        bad, healthy = [], []
        for v in vs:
            b = v['building']; key = investment_outcomes.LEGACY_KEYS.get(b, b.removeprefix('building_'))
            bad.append(f'''AND = {{ has_building = {b} has_variable = sed_outcome_{key}_pending
 has_variable = sed_outcome_{key}_since
 owner.var:sed_calendar_month_key >= {{ value = var:sed_outcome_{key}_since add = 3 }}
 b:{b} = {{ level > 0 OR = {{ occupancy < 0.8 has_failed_hires = yes building_has_goods_shortage = yes }} }} }}''')
            healthy.append(f'''AND = {{ has_building = {b} b:{b} = {{ level > 0 occupancy >= 0.8
 has_failed_hires = no building_has_goods_shortage = no }} }}''')
        # Two full levels of labor provide extra room for relocating a failed base.
        workers = min(labor.REQUIREMENTS[v['building']] for v in vs)*2
        parts.append(f'''sed_regional_{good}_site = {{
 is_incorporated = yes infrastructure_delta >= 0
 NOT = {{ OR = {{ {present} }} }}
 sed_state_labor_available >= {workers:g}
 owner = {{
  is_player = yes has_variable = sed_enabled has_variable = sed_mode_automatic
  NOT = {{ has_variable = sed_mode_manual }} NOT = {{ has_variable = sed_mode_assisted }}
  sed_direct_fiscal_safe = yes
  any_scope_state = {{ OR = {{ {' '.join(bad)} }} }}
  NOT = {{ any_scope_state = {{ OR = {{ {' '.join(healthy)} }} }} }}
  NOT = {{ any_scope_state = {{ OR = {{ has_variable = sed_{good}_request_pending {pending} }} }} }}
 }}
}}
''')
    return ''.join(parts)
