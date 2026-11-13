"""Supply investment choice keeps the national objective and compares material references."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state


class InvestmentTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')

    def producer(self, kind, methods, population=200000):
        producer = building(kind)
        producer['production_methods'] = methods
        target = state(buildings=[producer], population=population)
        self.c.states.append(target)
        return target

    def shortage(self, good):
        self.c.market_goods[good] = dict(market_goods_has_goods_shortage=True,
                                        market_goods_buy_orders=100, market_goods_sell_orders=40)

    def test_automatic_invests_in_expensive_civilian_goods_without_shortage(self):
        target = self.producer('building_logging_camp', ['pm_simple_forestry'])
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=False,
                                         market_goods_buy_orders=100, market_goods_sell_orders=80,
                                         market_goods_pricier=0.25)
        self.c.variables['advisor_enabled'] = True
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions, [dict(building='building_logging_camp', state=target)])
        self.assertEqual(self.c.variables['sed_plan_goal'], 2)

    def test_assisted_does_not_expand_demand_to_expensive_goods(self):
        self.producer('building_logging_camp', ['pm_simple_forestry'])
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=False,
                                         market_goods_buy_orders=100, market_goods_sell_orders=80,
                                         market_goods_pricier=0.25)
        self.c.run('sed_refresh_diagnostics')
        self.assertNotIn('sed_wood_candidates', self.c.variable_lists)

    def test_automatic_waits_when_price_pressure_is_below_threshold(self):
        # A non-core good: the core inputs have their own growth lane since
        # 0.7.33 and would build even below the 20% threshold.
        self.producer('building_food_industry', ['pm_bakery'])
        self.c.market_goods['groceries'] = dict(market_goods_has_goods_shortage=False,
                                               market_goods_buy_orders=100, market_goods_sell_orders=95,
                                               market_goods_pricier=0.1)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions, [])

    def test_core_growth_does_not_wait_for_a_positive_material_reference(self):
        # Deliberate rule change in 0.7.33: the stressed reference (75% revenue,
        # 125% inputs) is negative for most industries at base prices, so waiting
        # for it kept a healthy country idle. Wood, iron and tools grow under the
        # fiscal guard instead; every other good still needs the reference.
        self.producer('building_tooling_workshop',
                      ['pm_crude_tools', 'pm_rotary_valve_engine_building_tooling_workshop'])
        self.c.market_goods['tools'] = dict(market_goods_has_goods_shortage=False,
                                          market_goods_buy_orders=100, market_goods_sell_orders=80,
                                          market_goods_pricier=0.25)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual([item.get('building') for item in self.c.constructions],
                         ['building_tooling_workshop'])

    def test_expensive_growth_keeps_labor_guard(self):
        self.producer('building_logging_camp', ['pm_simple_forestry'], population=1)
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=False,
                                         market_goods_buy_orders=100, market_goods_sell_orders=80,
                                         market_goods_pricier=0.25)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions, [])

    def test_expensive_military_goods_keep_shortage_requirement(self):
        self.producer('building_arms_industry', ['pm_muskets'])
        self.c.market_goods['small_arms'] = dict(market_goods_has_goods_shortage=False,
                                               market_goods_buy_orders=100, market_goods_sell_orders=80,
                                               market_goods_pricier=0.25)
        self.c.run('sed_set_mode_automatic')
        self.assertFalse(self.c.condition(self.c.definitions['sed_small_arms_supply_demand'], self.c.country_scope()))

    def test_equal_output_prefers_the_stronger_material_margin(self):
        costly = self.producer('building_logging_camp', ['pm_simple_forestry', 'pm_steam_donkey_building_logging_camp'], 100000)
        cheaper = self.producer('building_logging_camp', ['pm_simple_forestry'])
        self.shortage('wood')
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.variable_lists['sed_plan_1_wood'], [cheaper])
        self.assertEqual(self.c.constructions, [dict(building='building_logging_camp', state=cheaper)])
        self.assertLess(costly['variables']['sed_plan_wood_margin'], cheaper['variables']['sed_plan_wood_margin'])

    def test_nonnegative_material_reference_precedes_a_negative_supplier(self):
        self.producer('building_tooling_workshop', ['pm_pig_iron', 'pm_watertube_boiler_building_tooling_workshop'], 100000)
        basic = self.producer('building_tooling_workshop', ['pm_crude_tools'])
        self.shortage('tools')
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.variable_lists['sed_plan_1_tools'], [basic])
        self.assertEqual(self.c.constructions, [dict(building='building_tooling_workshop', state=basic)])

    def test_all_negative_references_keep_a_strategic_supply_choice(self):
        self.producer('building_tooling_workshop', ['pm_crude_tools', 'pm_rotary_valve_engine_building_tooling_workshop'])
        higher = self.producer('building_tooling_workshop', ['pm_pig_iron', 'pm_watertube_boiler_building_tooling_workshop'])
        self.shortage('tools')
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.variable_lists['sed_plan_1_tools'], [higher])
        self.assertLess(higher['variables']['sed_plan_tools_margin'], 0)
        self.assertEqual(len(self.c.constructions), 1)

    def test_regular_shortage_selects_the_preferred_variant_inside_the_state(self):
        wheat = building('building_wheat_farm')
        wheat['production_methods'] = ['pm_simple_farming']
        rice = building('building_rice_farm')
        rice['production_methods'] = ['pm_simple_farming_building_rice_farm']
        target = state(buildings=[wheat, rice])
        self.c.states = [target]
        self.shortage('grain')
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions, [dict(building='building_rice_farm', state=target)])

    def test_reference_values_include_byproducts_and_all_active_inputs(self):
        target = self.producer('building_food_industry', ['pm_bakery', 'pm_pot_stills'])
        self.assertEqual(self.c.number('sed_investment_food_industry_output', target), 20)
        self.assertEqual(self.c.number('sed_investment_food_industry_margin', target), -387.5)

    def test_zero_target_output_is_excluded_even_with_valuable_byproducts(self):
        target = self.producer('building_logging_camp', ['pm_simple_forestry', 'pm_increased_hardwood'])
        self.shortage('wood')
        self.c.run('sed_refresh_diagnostics')
        self.assertEqual(self.c.number('sed_investment_logging_camp_output', target), 0)
        self.assertNotIn('sed_wood_candidates', self.c.variable_lists)
        self.assertEqual(self.c.variables['sed_wood_method_states'], 1)

    def test_assisted_approval_preserves_the_first_eligible_variant(self):
        wheat = building('building_wheat_farm')
        wheat['production_methods'] = ['pm_simple_farming']
        rice = building('building_rice_farm')
        rice['production_methods'] = ['pm_simple_farming_building_rice_farm']
        target = state(buildings=[wheat, rice])
        self.c.states = [target]
        self.shortage('grain')
        self.c.run('sed_refresh_diagnostics')
        self.c.run('sed_run_grain_approval', target)
        self.assertEqual(self.c.constructions, [dict(building='building_wheat_farm', state=target)])

    def test_missing_industry_has_a_basic_per_level_reference(self):
        target = state()
        self.c.states = [target]
        self.assertEqual(self.c.number('sed_investment_tooling_workshop_output', target), 30)
        self.assertEqual(self.c.number('sed_investment_tooling_workshop_margin', target), 150)


if __name__ == '__main__':
    unittest.main()
