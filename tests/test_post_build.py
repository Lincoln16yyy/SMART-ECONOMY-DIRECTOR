import unittest
from script_harness import Country, building, state
from test_diagnostics import script_definitions


class PostBuildTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), principal=0)
        self.c.run('sed_enable_country')

    def test_completed_project_waits_for_staff_and_inputs(self):
        c = self.c
        camp = building('building_logging_camp', level=2, occupancy=0.5, shortage=True)
        location = state(buildings=[camp])
        location['variables']['sed_wood_intent_level'] = 1
        c.states = [location]
        c.run('sed_follow_projects')
        self.assertEqual(c.variables['sed_follow_staff'], 1)
        self.assertEqual(c.variables['sed_follow_inputs'], 1)
        self.assertIn('sed_follow_wood', location['variables'])
        location['variables'].pop('sed_wood_intent_level')
        c.run('sed_follow_projects')
        self.assertIn('sed_follow_wood', location['variables'])
        camp.update(occupancy=1, building_has_goods_shortage=False)
        c.run('sed_follow_projects')
        self.assertNotIn('sed_follow_wood', location['variables'])

    def test_cash_covered_project_uses_two_week_floor(self):
        c = self.c
        c.variables.update(sed_build_budget_known=1, sed_build_budget_weekly=100)
        c.readings.update(net_total_income=100, net_fixed_income=200, gold_reserves=100)
        gate = c.definitions['sed_direct_fiscal_safe']
        self.assertTrue(c.condition(gate, c.country_scope()))
        c.readings['gold_reserves'] = 99
        self.assertFalse(c.condition(gate, c.country_scope()))
        c.readings.update(gold_reserves=100, principal=1)
        self.assertFalse(c.condition(gate, c.country_scope()))

    def test_stagnation_changes_advisor_objective(self):
        c = self.c
        c.variables.update(advisor_enabled=True, sed_asc_rank_delta=0, sed_asc_sol_delta=0)
        c.run('sed_set_mode_automatic')
        self.assertEqual(c.variables['sed_coord_advisor_policy'], 2)
        self.assertIn('advisor_setting_sc_goal_sol', c.variables)
        c.run('sed_set_mode_assisted')
        self.assertNotIn('advisor_setting_sc_goal_sol', c.variables)
