import unittest
from script_harness import Country, building, state
from test_diagnostics import script_definitions


class OperatingCostTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), principal=0, gold_reserves=100000)
        self.c.run('sed_enable_country')

    def test_public_reference_needs_recurring_surplus(self):
        c = self.c
        from tools.public_upkeep import PROFILES
        c.readings['technologies'] = list({t for data in PROFILES.values() for group in data['groups']
                                           for spec in group.values() for t in spec['technologies']})
        c.variables.update(sed_investment_wage_known=1, sed_investment_wage_unit=0.1)
        c.run('sed_refresh_public_upkeep')
        cost = c.variables['sed_upkeep_university_cost']
        self.assertEqual(cost, 1150)
        c.readings['net_total_income'] = cost - 1
        gate = c.definitions['sed_upkeep_university_safe']
        self.assertFalse(c.condition(gate, c.country_scope()))
        c.readings['net_total_income'] = cost
        self.assertTrue(c.condition(gate, c.country_scope()))

    def test_staffing_grace_and_named_input(self):
        c = self.c
        mill = building('building_paper_mill', level=2, occupancy=0.2, shortage=True)
        mill['production_methods'] = ['pm_pulp_pressing']
        location = state(buildings=[mill])
        location['variables'].update(sed_outcome_paper_level=1)
        c.states = [location]
        c.market_goods['wood']['market_goods_has_goods_shortage'] = True
        c.readings['month'] = 1
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_staff'], 0)
        self.assertEqual(c.variables['sed_outcome_hiring'], 1)
        self.assertIs(c.variables['sed_problem_state'], location)
        from tools.investment_outcomes import INPUT_GOODS
        self.assertEqual(c.variables['sed_problem_good'], INPUT_GOODS.index('wood') + 1)
        c.readings['month'] = 3
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_staff'], 0)
        c.readings['month'] = 4
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_staff'], 1)

    def test_legacy_pending_gets_grace_on_first_new_review(self):
        c = self.c
        location = state(buildings=[building('building_paper_mill', occupancy=0.2)])
        location['variables']['sed_outcome_paper_pending'] = True
        c.states = [location]
        c.readings['month'] = 1
        c.run('sed_outcome_review')
        self.assertEqual(c.variables['sed_outcome_staff'], 0)
        self.assertIn('sed_outcome_paper_since', location['variables'])
