"""Verificações sintéticas de recuperação regional, fila compartilhada e estratégia."""
import copy
from pathlib import Path
import tempfile
import unittest
from script_harness import Country, building, state, construction_sector
from test_diagnostics import script_definitions
from tools.production_methods import PROFILES
from tools.build_mod import outputs
from tools.validate import validate
from tools.pdx_script import parse, child


def plant(kind, queued=0, **kw):
    b = building(kind, queued_levels=queued, **kw)
    b['production_methods'] = [g['method'] for g in PROFILES[kind]]
    return b


def country(sites, **readings):
    defaults = dict(principal=0, credit=1000000, gold_reserves=100000,
                    net_total_income=100000, net_fixed_income=100000,
                    total_population=sum(s['state_population'] for s in sites),
                    construction_queue_num_queued_government_levels=0)
    defaults.update(readings)
    c=Country(script_definitions(), **defaults);c.states=sites
    for good in ('paper','groceries','clothes','steel','glass','engines','fertilizer','sulfur','lead'):
        c.market_goods.setdefault(good,dict(market_goods_buy_orders=1000, market_goods_sell_orders=1000,
                                           market_goods_has_goods_shortage=False))
    c.run('sed_enable_country');return c


class RegionalRecoveryTests(unittest.TestCase):
    def fixture(self, destination='building_tooling_workshop', age=4):
        failed=state(population=100000,buildings=[plant('building_paper_mill',occupancy=.2,failed_hires=True)],can_construct=['building_paper_mill'])
        target=state(population=300000,can_construct=[destination])
        c=country([failed,target]);c.variables['advisor_enabled']=True
        c.run('sed_set_mode_automatic')
        failed['variables'].update(sed_outcome_paper_pending=True,sed_outcome_paper_since=1836*12)
        c.readings['month']=age
        return c,failed,target

    def test_failed_paper_does_not_stop_healthy_tools_elsewhere(self):
        c,failed,target=self.fixture();c.run('sed_auto_apply_monthly')
        self.assertGreater(c.variables['sed_outcome_staff'],0)
        self.assertEqual([x['building'] for x in c.constructions],['building_tooling_workshop'])
        self.assertIs(c.constructions[0]['state'],target)
        self.assertEqual(c.variables['sed_coord_executor'],11)

    def test_mature_failure_can_relocate_the_same_sector(self):
        c,failed,target=self.fixture('building_paper_mill');c.run('sed_auto_apply_monthly')
        self.assertEqual([x['building'] for x in c.constructions],['building_paper_mill'])
        self.assertIs(c.constructions[0]['state'],target)
        self.assertEqual(target['variables']['sed_paper_intent_level'],0)
        c.run('sed_auto_apply_monthly');self.assertEqual(len(c.constructions),1)

    def test_temporary_hiring_delay_does_not_duplicate_a_base(self):
        c,_,_=self.fixture('building_paper_mill',age=1);c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions,[])

    def test_a_healthy_producer_prevents_unnecessary_relocation(self):
        c,_,target=self.fixture('building_paper_mill')
        c.states.append(state(buildings=[plant('building_paper_mill')],can_construct=False))
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])

    def test_destination_needs_extra_labor_and_inputs(self):
        c,_,target=self.fixture('building_paper_mill');target['state_population']=10000
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])
        c,_,_=self.fixture('building_paper_mill')
        c.market_goods['wood'].update(market_goods_sell_orders=0)
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])


    def test_regional_variant_reserves_its_own_two_levels_of_labor(self):
        failed=state(population=100000,buildings=[plant('building_wheat_farm',occupancy=.2,failed_hires=True)],can_construct=['building_wheat_farm'])
        destination=state(population=170000,can_construct=['building_rice_farm'])
        c=country([failed,destination]);c.run('sed_set_mode_automatic')
        failed['variables'].update(sed_outcome_wheat_farm_pending=True,sed_outcome_wheat_farm_since=1836*12)
        c.readings['month']=4;c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions,[])


class ParallelConstructionTests(unittest.TestCase):
    def fixture(self):
        private=state(population=300000,buildings=[plant('building_logging_camp',queued=1)],can_construct=['building_logging_camp'])
        target=state(population=300000,can_construct=['building_tooling_workshop'])
        sector=construction_sector();sector['production_methods']=['pm_wooden_buildings']
        private['buildings'].append(sector)
        c=country([private,target],construction_queue_num_queued_private_levels=1,
                  **{'modifier:country_construction_add':100,'modifier:country_private_construction_allocation_mult':.5})
        c.variables['advisor_enabled']=True;c.run('sed_set_mode_automatic')
        return c,private,target

    def test_uses_spare_public_capacity_without_changing_private_queue(self):
        c,_,target=self.fixture();c.run('sed_auto_apply_monthly')
        self.assertEqual(c.readings['construction_queue_num_queued_private_levels'],1)
        self.assertEqual([x['building'] for x in c.constructions],['building_tooling_workshop'])
        self.assertIs(c.constructions[0]['state'],target)
        self.assertNotIn('advisor_auto_construction_enabled',c.variables)
        c.run('sed_auto_apply_monthly');self.assertEqual(len(c.constructions),1)

    def test_insufficient_points_allocation_or_cash_keeps_the_block(self):
        for readings in ({'modifier:country_construction_add':49},
                         {'modifier:country_private_construction_allocation_mult':.9},
                         {'modifier:country_private_construction_allocation_mult':1},
                         {'net_total_income':1}, {'is_construction_paused':True}):
            with self.subTest(readings=readings):
                c,_,_=self.fixture();c.readings.update(readings);c.run('sed_auto_apply_monthly')
                self.assertEqual(c.constructions,[])

    def test_unknown_private_types_or_initial_methods_are_rejected(self):
        c,private,_=self.fixture()
        private['buildings'][0]['production_methods']=[]
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])
        c,_,_=self.fixture();c.readings['construction_queue_num_queued_private_levels']=2
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])

    def test_unknown_visible_project_cannot_be_masked_by_a_known_project(self):
        c,private,_=self.fixture()
        private['buildings'].append(building('building_furniture_manufactory',queued_levels=1))
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])

    def test_duplicate_good_in_another_state_is_not_expanded(self):
        c,_,target=self.fixture()
        target['buildings']=[plant('building_logging_camp')]
        target['can_construct_building']=['building_logging_camp']
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])

    def test_pending_private_workers_and_inputs_are_reserved(self):
        c,private,target=self.fixture()
        private['buildings'][0]=plant('building_paper_mill',queued=1)
        target['can_construct_building']=['building_tooling_workshop']
        c.market_goods['wood'].update(market_goods_buy_orders=100,market_goods_sell_orders=75)
        c.run('sed_auto_apply_monthly')
        self.assertNotIn('building_tooling_workshop',[p['building'] for p in c.constructions])
        self.assertGreaterEqual(c.lookup('sed_input_pending_wood',private),37.5)

    def test_private_jobs_are_not_reused_for_public_hiring(self):
        c,private,_=self.fixture()
        private['buildings'][0]=plant('building_paper_mill',queued=1)
        private['state_population']=80000;private['can_construct_building']=['building_tooling_workshop']
        c.states=[private]
        c.run('sed_auto_apply_monthly');self.assertEqual(c.constructions,[])
        self.assertEqual(c.lookup('sed_state_labor_committed',private),5000)

    def test_completed_public_attempt_does_not_enable_an_unchecked_advisor(self):
        c,_,_=self.fixture();c.run('sed_auto_apply_monthly');c.run('sed_coord_sync')
        self.assertEqual(c.variables['sed_coord_executor'],0)
        self.assertNotIn('advisor_auto_construction_enabled',c.variables)

    def test_parallel_ownership_survives_reload_and_clears_when_queue_ends(self):
        c,_,_=self.fixture();c.run('sed_auto_apply_monthly')
        self.assertIn('sed_parallel_direct_pending',c.variables)
        loaded=copy.deepcopy(c);loaded.run('sed_coord_sync')
        self.assertNotIn('advisor_auto_construction_enabled',loaded.variables)
        loaded.readings['construction_queue_num_queued_government_levels']=0
        loaded.run('sed_refresh_parallel_ownership')
        self.assertNotIn('sed_parallel_direct_pending',loaded.variables)
        loaded.run('sed_set_mode_manual')
        self.assertNotIn('advisor_auto_construction_enabled',loaded.variables)

    def test_validator_rejects_private_permission_without_its_capacity_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name,data in outputs().items():
                target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            path=root/'common/scripted_triggers/sed_triggers.txt'
            before='AND = { sed_growth_wood_candidate = yes owner = { sed_private_parallel_capacity_safe = yes } }'
            data=path.read_text(encoding='utf-8-sig');self.assertIn(before,data)
            path.write_text(data.replace(before,'AND = { sed_growth_wood_candidate = yes }',1),encoding='utf-8-sig')
            self.assertTrue(any('private queue safety guard' in e for e in validate(root)))

    def test_weekly_retry_reconsiders_new_capacity_with_private_queue_still_active(self):
        c,_,_=self.fixture()
        # Exercita o executor direto sem a delegação externa ao Advisor.
        c.run('sed_set_mode_manual');c.variables.pop('advisor_enabled',None)
        c.readings['modifier:country_construction_add']=49
        c.run('sed_set_mode_automatic')
        event=next(e for e in parse(outputs()['events/sed_events.txt'].decode('utf-8-sig')) if e.key=='sed_pulse.1')
        # A entrada real consome o evento pendente antes de agendar a revisão semanal.
        c.execute(child(event.value,'immediate'),c.country_scope())
        self.assertEqual(c.variables['sed_auto_review_status'],11)
        self.assertIn('sed_auto_retry_month',c.variables)
        c.readings['modifier:country_construction_add']=100
        c.execute(child(event.value,'immediate'),c.country_scope())
        self.assertEqual([x['building'] for x in c.constructions],['building_tooling_workshop'])
        self.assertEqual(c.readings['construction_queue_num_queued_private_levels'],1)

    def test_ready_parallel_project_does_not_show_a_false_queue_block(self):
        c,_,_=self.fixture()
        gui=c.definitions['sed_auto_current_queue_visible_sgui']
        self.assertFalse(c.condition(child(gui,'is_shown'),c.country_scope()))

    def test_assisted_approval_and_late_queue_changes_keep_the_guard(self):
        c,_,target=self.fixture();c.run('sed_set_mode_assisted')
        c.run('sed_run_tools_approval',target);self.assertEqual(c.constructions,[])
        c,_,target=self.fixture();c.readings['construction_queue_num_queued_private_levels']=2
        c.run('sed_run_tools_approval',target);self.assertEqual(c.constructions,[])


class CountryStrategyTests(unittest.TestCase):
    def test_small_country_favors_low_capital_choices(self):
        c=country([state(population=200000)])
        c.run('sed_set_mode_automatic');site=c.states[0]
        small=c.lookup('sed_strategy_wood_factor',site)
        c.readings['total_population']=10000000
        self.assertGreater(small,c.lookup('sed_strategy_wood_factor',site))

    def test_large_local_labor_pool_favors_manufacturing(self):
        c=country([state(population=300000)])
        c.run('sed_set_mode_automatic');site=c.states[0]
        abundant=c.lookup('sed_strategy_tools_factor',site)
        site['state_population']=30000
        self.assertGreater(abundant,c.lookup('sed_strategy_tools_factor',site))

    def test_existing_domestic_inputs_improve_a_chain_score(self):
        c=country([state(population=300000,can_construct=['building_tooling_workshop'])]);c.run('sed_set_mode_automatic')
        site=c.states[0];before=c.lookup('sed_strategy_tools_factor',site)
        c.states.append(state(buildings=[plant('building_logging_camp')]))
        self.assertGreater(c.lookup('sed_strategy_tools_factor',site),before)

    def test_low_living_standard_favors_essential_goods(self):
        c=country([state(population=300000)],average_sol=15);c.run('sed_set_mode_automatic')
        site=c.states[0];before=c.lookup('sed_strategy_grain_factor',site)
        c.readings['average_sol']=7
        self.assertGreater(c.lookup('sed_strategy_grain_factor',site),before)

    def test_country_preferences_cannot_make_a_loss_eligible(self):
        c=country([state(can_construct=['building_motor_industry'])],average_sol=7)
        c.run('sed_set_mode_automatic');c.run('sed_auto_apply_monthly')
        self.assertEqual(c.constructions,[])
