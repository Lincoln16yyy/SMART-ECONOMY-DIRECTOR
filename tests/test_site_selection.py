import unittest
from script_harness import Country, building, state
from test_diagnostics import script_definitions


class SiteSelectionTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), principal=0, gold_reserves=100000,
                         net_total_income=1000, construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def camp(self):
        item = building('building_logging_camp')
        item['production_methods'] = ['pm_simple_forestry']
        return item

    def test_growth_prefers_ready_site_and_records_confirmed_project(self):
        c = self.c
        cramped = state(population=60000, infrastructure_delta=0, buildings=[self.camp()])
        ready = state(population=100000, infrastructure_delta=20, buildings=[self.camp()])
        c.states = [cramped, ready]
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions[0]['building'], 'building_logging_camp')
        self.assertIs(c.constructions[0]['state'], ready)
        self.assertIs(c.variables['sed_last_build_state'], ready)

    def test_existing_factory_shortage_prioritizes_its_input(self):
        c = self.c
        mill = building('building_paper_mill', shortage=True)
        mill['production_methods'] = ['pm_pulp_pressing']
        c.states = [state(buildings=[mill])]
        c.market_goods['wood'].update(market_goods_has_goods_shortage=True)
        c.variables['sed_mode_automatic'] = True
        c.run('sed_refresh_input_priorities')
        self.assertIn('sed_input_priority_wood', c.variables)

    def test_rejected_construction_does_not_create_success_record(self):
        c = self.c
        c.states = [state(population=100000, buildings=[self.camp()])]
        c.construction_accepted = False
        c.run('sed_set_mode_automatic')
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('sed_last_build_state', c.variables)
