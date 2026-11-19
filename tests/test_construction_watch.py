import unittest

from script_harness import Country, building, state
from test_diagnostics import script_definitions


class ConstructionWatchTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.c.variables.update(sed_mode_automatic=True, sed_coord_active=True,
                                sed_coord_executor=1, sed_coord_advisor_known=True)
        self.c.variables.pop('sed_mode_assisted', None)

    def test_waits_for_two_distinct_delegated_months(self):
        c = self.c
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 0)
        c.readings['month'] = 1
        c.run('sed_watch_review')
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 1)
        c.readings['month'] = 2
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 2)
        self.assertEqual(c.variables['sed_watch_status'], 1)
        c.readings.update(month=3, construction_queue_num_queued_government_levels=1)
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 0)

    def test_paused_and_private_work_do_not_add_idle_months(self):
        c = self.c
        c.variables.update(sed_watch_delegated=True, sed_watch_idle=1)
        c.readings['is_construction_paused'] = True
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 0)
        c.readings.update(month=1, is_construction_paused=False,
                          construction_queue_num_queued_private_levels=1)
        c.run('sed_watch_review')
        self.assertEqual(c.variables['sed_watch_idle'], 0)

    def test_assisted_mode_does_not_take_control(self):
        c = self.c
        c.variables['sed_mode_assisted'] = True
        c.run('sed_watch_review')
        self.assertNotIn('sed_watch_month', c.variables)
        self.assertEqual(c.variables['sed_watch_status'], 0)


    def test_recovery_takes_one_direct_project_then_releases_advisor(self):
        c = self.c
        c.readings.update(principal=0, net_total_income=1000, gold_reserves=1000000)
        camp = building('building_logging_camp')
        camp['production_methods'] = ['pm_simple_forestry']
        c.states = [state(population=60000, buildings=[camp])]
        c.variables.update(advisor_enabled=True, sed_watch_idle=2, sed_watch_delegated=True)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_coord_executor'], 11)
        self.assertEqual([item['building'] for item in c.constructions], ['building_logging_camp'])
        self.assertNotIn('advisor_auto_construction_enabled', c.variables)
        c.run('sed_auto_apply_monthly')
        self.assertEqual(len(c.constructions), 1)
        c.readings['month'] = 1
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.variables['sed_watch_idle'], 0)
        self.assertEqual(c.variables['sed_coord_executor'], 1)
        self.assertIn('advisor_auto_construction_enabled', c.variables)
