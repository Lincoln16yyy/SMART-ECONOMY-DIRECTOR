"""Execute this mod's limited arithmetic/control-flow subset with supplied readings.

This harness catches behavioral regressions in the actual generated scripts.
It does not emulate the game, validate primitive names, or test GUI rendering.
"""

from tools.pdx_script import child


COUNTRY = 'country'
STATE = 'state'
TAX_LEVELS = ('very_low', 'low', 'medium', 'high', 'very_high')
BUILDING = 'building'


def state(infrastructure_delta=0, market_access=1, incorporated=True,
          can_construct=True, buildings=None, population=1000, **readings):
    """Build the reading shape used by state-scoped scripts in this harness."""
    result = dict(infrastructure_delta=infrastructure_delta,
                  market_access=market_access, is_incorporated=incorporated,
                  can_construct_building=can_construct,
                  state_population=population,
                  buildings=buildings or [], variables={})
    result.update(readings)
    result['__scope__'] = STATE
    return result


def railway(level=1, occupancy=1, failed_hires=False, shortage=False,
            queued_levels=0):
    """A railway building reading; queued_levels raises the post-queue level."""
    return building('building_railway', level, occupancy, failed_hires,
                    shortage, queued_levels)


def construction_sector(level=1, occupancy=1, failed_hires=False,
                        shortage=False, queued_levels=0):
    """A construction sector reading; queued_levels raises the post-queue level."""
    return building('building_construction_sector', level, occupancy,
                    failed_hires, shortage, queued_levels)


def building(kind, level=1, occupancy=1, failed_hires=False, shortage=False,
             queued_levels=0):
    return dict(building=kind, level=level,
                level_after_queued_constructions=level + queued_levels,
                occupancy=occupancy, has_failed_hires=failed_hires,
                building_has_goods_shortage=shortage,
                __scope__=BUILDING)


class Country:
    def __init__(self, definitions, **readings):
        self.definitions = definitions
        self.readings = dict(net_total_income=100, net_fixed_income=200, fixed_expenses=50,
                             gold_reserves=1000, principal=100, credit=1000, gdp=10000,
                             total_population=1000, average_sol=10, literacy_rate=0.2,
                             **{'modifier:country_construction_add': 10},
                             num_queued_government_constructions=2, num_queued_private_constructions=1,
                             construction_queue_num_queued_government_levels=2,
                             construction_queue_num_queued_private_levels=0,
                             bureaucracy=0, year=1836, month=0, is_player=True, in_default=False,
                             tax_level='medium', government_wage_level='medium',
                             is_game_paused=True, is_construction_paused=False)
        self.readings.update(readings)
        self.variables = {}
        self.variable_lists = {}
        self.states = []
        self.journals_added = 0
        self.active_journal = False
        self.constructions = []
        self.tax_changes = []
        self.wage_changes = []
        self.construction_accepted = True
        self.market_goods = {}
        self.scheduled_events = []

    def country_scope(self):
        scope = dict(self.readings)
        scope['__scope__'] = COUNTRY
        scope['__country__'] = self
        scope['__variables__'] = self.variables
        return scope

    def variables_for(self, scope):
        if scope is self.readings or scope.get('__scope__') == COUNTRY:
            return self.variables
        return scope.setdefault('variables', {})

    def lookup(self, name, scope):
        if name in ('tax_level', 'government_wage_level'):
            return self.tax_level_rank(scope.get(name, self.readings[name]))
        if name.startswith('b:') and '.' in name:
            building_name, attribute = name[2:].split('.', 1)
            target = self.building(scope, building_name)
            return target.get(attribute, 0) if target else 0
        if name in TAX_LEVELS:
            return TAX_LEVELS.index(name) + 1
        if name.startswith('owner.var:'):
            return self.variables[name[len('owner.var:'):]]
        if name.startswith('var:'):
            return self.variables_for(scope)[name[4:]]
        if name in ('yes', 'no'):
            return name == 'yes'
        try:
            return float(name)
        except ValueError:
            pass
        if name in ('market_goods_buy_orders', 'market_goods_sell_orders'):
            return scope.get(name, 0)  # Explicit synthetic zero-orders default; never engine evidence.
        if name in scope:
            return scope[name]
        if name in self.definitions:
            return self.number(self.definitions[name], scope)
        # Global triggers such as is_game_paused remain readable from any scope.
        if name in self.readings:
            return self.readings[name]
        if scope.get('__scope__') == STATE or 'buildings' in scope:
            # State triggers omitted by a fixture use the engine's neutral value.
            return {'is_incorporated': True, 'can_construct_building': True,
                    'infrastructure_delta': 0, 'market_access': 1,
                    'state_population': 0, 'tax_capacity_usage': 0, 'tax_capacity': 0}[name]
        raise AssertionError('Unsupported reading in harness: ' + name)

    @staticmethod
    def tax_level_rank(level):
        return TAX_LEVELS.index(level) + 1

    def number(self, value, scope):
        if not isinstance(value, list):
            return self.lookup(value, scope)
        result = 0
        for entry in value:
            if entry.key == 'market':
                result += self.number(entry.value, {'goods': self.market_goods})
                continue
            if entry.key.startswith('mg:'):
                good = scope['goods'].get(entry.key[3:])
                if good is not None:
                    result += self.number(entry.value, good)
                continue
            if entry.key == 'if':
                if self.condition(child(entry.value, 'limit'), scope):
                    result += self.number([e for e in entry.value if e.key != 'limit'], scope)
                continue
            n = self.number(entry.value, scope)
            if entry.key == 'value':
                result = n
            elif entry.key == 'add':
                result += n
            elif entry.key == 'subtract':
                result -= n
            elif entry.key == 'multiply':
                result *= n
            elif entry.key == 'divide':
                result /= n
            elif entry.key == 'min':
                result = max(result, n)  # Clausewitz min is a lower bound.
            elif entry.key == 'max':
                result = min(result, n)
            else:
                raise AssertionError('Unsupported numeric operation: ' + entry.key)
        return result

    def building(self, scope, name):
        for entry in scope.get('buildings', []):
            if entry.get('building') == name:
                return entry
        return None

    def condition(self, entries, scope):
        return all(self.single_condition(entry, scope) for entry in entries)

    def single_condition(self, entry, scope):
        key = entry.key
        if key == 'NOT':
            return not self.condition(entry.value, scope)
        if key == 'AND':
            return self.condition(entry.value, scope)
        if key == 'OR':
            return any(self.single_condition(e, scope) for e in entry.value)
        if key == 'market':
            return self.condition(entry.value, {'goods': self.market_goods})
        if key.startswith('sg:'):
            good = scope.get('state_goods', {}).get(key[3:])
            return good is not None and self.condition(entry.value, good)
        if key.startswith('mg:'):
            good = scope['goods'].get(key[3:])
            return good is not None and self.condition(entry.value, good)
        if key == 'any_scope_state':
            return any(self.condition(entry.value, target) for target in self.states)
        if key == 'has_active_production_method':
            return entry.value in scope.get('production_methods', [])
        if key == 'has_variable':
            return entry.value in self.variables_for(scope)
        if key == 'has_journal_entry':
            return self.active_journal
        if key == 'has_inactive_journal_entry':
            return False
        if key == 'has_variable_list':
            return bool(self.variable_lists.get(entry.value))
        if key == 'has_building':
            return self.building(scope, entry.value) is not None
        if key == 'is_building_type':
            return scope.get('building') == entry.value
        if key == 'can_construct_building':
            return bool(scope.get('can_construct_building'))
        if key.startswith('b:') and '.' not in key:
            building = self.building(scope, key[2:])
            return building is not None and self.condition(entry.value, building)
        if key == 'owner':
            return self.condition(entry.value, self.country_scope())
        if key in self.definitions:
            return self.condition(self.definitions[key], scope)
        left, right = self.lookup(key, scope), self.number(entry.value, scope)
        return {'=': lambda: left == right, '<': lambda: left < right,
                '>': lambda: left > right, '>=': lambda: left >= right,
                '<=': lambda: left <= right, '!=': lambda: left != right}[entry.op]()

    def run(self, name, scope=None):
        scope = scope or self.country_scope()
        self.execute(self.definitions[name], scope)

    def execute(self, entries, scope, previous=None):
        chain_matched = None
        for entry in entries:
            key, value = entry.key, entry.value
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    chain_matched = False
                if not chain_matched:
                    matches = key == 'else' or self.condition(child(value, 'limit'), scope)
                    if matches:
                        self.execute([e for e in value if e.key != 'limit'], scope, previous)
                        chain_matched = True
                continue
            chain_matched = None
            if key == 'set_variable':
                self.variables_for(scope)[child(value, 'name')] = self.number(child(value, 'value'), scope)
            elif key == 'remove_variable':
                self.variables_for(scope).pop(value, None)
            elif key == 'change_variable':
                variables = self.variables_for(scope)
                name = child(value, 'name')
                variables[name] = variables.get(name, 0) + self.number(child(value, 'add'), scope)
            elif key == 'clear_variable_list':
                self.variable_lists.pop(value, None)
            elif key == 'add_to_variable_list':
                name = child(value, 'name')
                target = child(value, 'target')
                if target == 'prev':
                    target = previous
                elif target.startswith('var:'):
                    target = self.variables_for(scope)[target[4:]]
                self.variable_lists.setdefault(name, []).append(target)
            elif key == 'root':
                self.execute(value, self.country_scope(), previous=scope)
            elif key == 'prev':
                if previous is None:
                    raise AssertionError('prev used without a previous scope')
                self.execute(value, previous, previous=scope)
            elif key == 'owner':
                self.execute(value, self.country_scope(), previous=scope)
            elif key == 'every_scope_state':
                limit = next((e.value for e in value if e.key == 'limit'), [])
                rest = [e for e in value if e.key != 'limit']
                for target in self.states:
                    if self.condition(limit, target):
                        self.execute(rest, target, previous=scope)
            elif key == 'every_scope_building':
                limit = next((e.value for e in value if e.key == 'limit'), [])
                rest = [e for e in value if e.key != 'limit']
                for target in scope.get('buildings', []):
                    if self.condition(limit, target):
                        self.execute(rest, target, previous=scope)
            elif key == 'ordered_scope_state':
                limit = next((e.value for e in value if e.key == 'limit'), [])
                order = next((e.value for e in value if e.key == 'order_by'), [])
                maximum = int(self.number(next((e.value for e in value if e.key == 'max'), '0'), scope))
                rest = [e for e in value if e.key not in ('limit', 'order_by', 'max', 'check_range_bounds')]
                candidates = [target for target in self.states if self.condition(limit, target)]
                candidates.sort(key=lambda target: self.number(order, target), reverse=True)
                if maximum:
                    candidates = candidates[:maximum]
                for target in candidates:
                    self.execute(rest, target, previous=scope)
            elif key == 'set_tax_level':
                self.readings['tax_level'] = value
                self.tax_changes.append(value)
            elif key == 'set_government_wage_level':
                self.readings['government_wage_level'] = value
                self.wage_changes.append(value)
            elif key == 'start_building_construction':
                target = scope if scope.get('__scope__') == STATE else None
                self.constructions.append(dict(building=value, state=target))
                if self.construction_accepted:
                    name = 'construction_queue_num_queued_government_levels'
                    self.readings[name] = self.readings.get(name, 0) + 1
            elif key == 'add_journal_entry':
                self.journals_added += 1
                self.active_journal = True
            elif key == 'trigger_event':
                self.scheduled_events.append((child(value, 'id'), self.number(child(value, 'days'), scope)))
            elif key in self.definitions:
                self.run(key, scope)
            else:
                raise AssertionError('Unsupported effect in harness: ' + key)
