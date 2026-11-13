"""Power plant executor for goal 9; script simulation only."""
import unittest

from tools.build_mod import outputs
from test_diagnostics import script_definitions
from script_harness import Country, building, state


class PowerCapacityTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.c.states = [state()]
        self.c.variables['sed_build_budget_known'] = 1
        self.c.variables['sed_build_budget_weekly'] = 50
        self.c.variables['sed_build_budget_required_gold'] = 100

    def dear_electricity(self, price=0.3):
        self.c.states[0]['state_goods']['electricity'] = {'state_goods_pricier': price}

    def test_dear_electricity_queues_a_power_plant_without_supply_chain(self):
        c = self.c
        self.dear_electricity()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 9)
        self.assertNotIn('sed_coord_active', c.variables)
        self.assertEqual([item.get('building') for item in c.constructions],
                         ['building_power_plant'])
        self.assertEqual(c.variables['sed_power_action_status'], 1)
        self.assertEqual(c.states[0]['variables'].get('sed_power_intent_level'), 0)
        self.assertIn('sed_power_request_pending', c.states[0]['variables'])

    def test_cheap_electricity_does_not_build(self):
        c = self.c
        self.dear_electricity(0.19)
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 8)
        self.assertEqual(c.constructions, [])

    def test_electricity_must_be_dear_in_the_state_that_hosts_the_plant(self):
        c = self.c
        c.states = [state(population=100000),
                    state(population=50000)]
        c.states[1]['state_goods']['electricity'] = {'state_goods_pricier': 0.3}
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_plan_goal'], 9)
        self.assertIn('sed_power_request_pending', c.states[1]['variables'])
        self.assertNotIn('sed_power_request_pending', c.states[0]['variables'])

    def test_a_plant_already_waiting_in_the_queue_is_not_duplicated(self):
        c = self.c
        c.states[0]['buildings'].append(building('building_power_plant', level=1, queued_levels=1))
        self.dear_electricity()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])

    def test_private_queue_blocks_the_power_request(self):
        c = self.c
        self.dear_electricity()
        c.readings['construction_queue_num_queued_private_levels'] = 1
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions, [])
        self.assertEqual(c.variables['sed_auto_action_status'], 11)

    def test_monthly_review_infers_completion_from_the_level(self):
        c = self.c
        c.states[0]['buildings'].append(building('building_power_plant', level=1))
        self.dear_electricity()
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.states[0]['variables'].get('sed_power_intent_level'), 1)
        # The queued level keeps the request pending until the queue leaves it.
        c.states[0]['buildings'][0]['level_after_queued_constructions'] = 2
        c.run('sed_refresh_power')
        self.assertIn('sed_power_request_pending', c.states[0]['variables'])
        c.states[0]['buildings'][0].update(level=2, level_after_queued_constructions=2)
        c.run('sed_refresh_power')
        self.assertNotIn('sed_power_request_pending', c.states[0]['variables'])
        self.assertEqual(c.variables.get('sed_power_completed'), 1)
        self.assertEqual(c.variables.get('sed_power_result'), 1)

    def test_budget_reserves_the_power_plant_points(self):
        c = self.c
        self.dear_electricity()
        c.run('sed_set_mode_automatic')
        c.run('sed_refresh_national_plan')
        c.run('sed_refresh_direct_budget')
        self.assertEqual(c.variables['sed_build_budget_project_points'], 400)

    def test_panel_text_states_the_direct_scope(self):
        outputs_map = outputs()
        pt = outputs_map['localization/braz_por/sed_l_braz_por.yml'].decode('utf-8-sig')
        en = outputs_map['localization/english/sed_l_english.yml'].decode('utf-8-sig')
        self.assertIn('Usina elétrica', pt)
        self.assertIn('Power plant', en)
        self.assertIn('400', pt)


if __name__ == '__main__':
    unittest.main()
