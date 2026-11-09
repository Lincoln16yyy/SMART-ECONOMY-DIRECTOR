"""Execute this mod's limited arithmetic/control-flow subset with supplied readings.

This harness catches behavioral regressions in the actual generated scripts.
It does not emulate the game, validate primitive names, or test GUI rendering.
"""

from tools.pdx_script import child


class Country:
    def __init__(self, definitions, **readings):
        self.definitions = definitions
        self.readings = dict(net_total_income=100, net_fixed_income=200, fixed_expenses=50,
                             gold_reserves=1000, principal=100, credit=1000, gdp=10000,
                             total_population=1000, average_sol=10, literacy_rate=0.2,
                             **{'modifier:country_construction_add': 10},
                             num_queued_government_constructions=2, num_queued_private_constructions=1,
                             year=1836, month=0, is_player=True, in_default=False)
        self.readings.update(readings)
        self.variables = {}
        self.states = []
        self.journals_added = 0
        self.active_journal = False

    def lookup(self, name, scope):
        if name.startswith('var:'):
            return self.variables[name[4:]]
        if name in ('yes', 'no'):
            return name == 'yes'
        try:
            return float(name)
        except ValueError:
            return scope[name]

    def number(self, value, scope):
        if not isinstance(value, list):
            return self.lookup(value, scope)
        result = 0
        for entry in value:
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

    def condition(self, entries, scope):
        return all(self.single_condition(entry, scope) for entry in entries)

    def single_condition(self, entry, scope):
        key = entry.key
        if key == 'NOT':
            return not self.condition(entry.value, scope)
        if key == 'OR':
            return any(self.single_condition(e, scope) for e in entry.value)
        if key == 'has_variable':
            return entry.value in self.variables
        if key == 'has_journal_entry':
            return self.active_journal
        if key == 'has_inactive_journal_entry':
            return False
        left, right = self.lookup(key, scope), self.number(entry.value, scope)
        return {'=': lambda: left == right, '<': lambda: left < right,
                '>': lambda: left > right, '>=': lambda: left >= right,
                '<=': lambda: left <= right, '!=': lambda: left != right}[entry.op]()

    def run(self, name):
        self.execute(self.definitions[name], self.readings)

    def execute(self, entries, scope):
        chain_matched = None
        for entry in entries:
            key, value = entry.key, entry.value
            if key in ('if', 'else_if', 'else'):
                if key == 'if':
                    chain_matched = False
                if not chain_matched:
                    matches = key == 'else' or self.condition(child(value, 'limit'), scope)
                    if matches:
                        self.execute([e for e in value if e.key != 'limit'], scope)
                        chain_matched = True
                continue
            chain_matched = None
            if key == 'set_variable':
                self.variables[child(value, 'name')] = self.number(child(value, 'value'), scope)
            elif key == 'remove_variable':
                self.variables.pop(value, None)
            elif key == 'change_variable':
                name = child(value, 'name')
                self.variables[name] += self.number(child(value, 'add'), scope)
            elif key == 'root':
                self.execute(value, self.readings)
            elif key in ('every_scope_state', 'every_scope_building'):
                scopes = self.states if key == 'every_scope_state' else scope.get('buildings', [])
                limit = next((e.value for e in value if e.key == 'limit'), [])
                for target in scopes:
                    if self.condition(limit, target):
                        self.execute([e for e in value if e.key != 'limit'], target)
            elif key == 'add_journal_entry':
                self.journals_added += 1
                self.active_journal = True
            elif key in self.definitions:
                self.run(key)
            else:
                raise AssertionError('Unsupported effect in harness: ' + key)
