"""Native price-band signals used by the investment reference."""
import unittest

from test_diagnostics import script_definitions
from script_harness import Country, building, state


class InvestmentPriceTests(unittest.TestCase):
    def setUp(self):
        self.c = Country(script_definitions(), construction_queue_num_queued_government_levels=0)
        self.c.run('sed_enable_country')
        self.target = state()
        self.c.states = [self.target]

    def local_price(self, target, good, pricier=0, cheaper=0):
        target['state_goods'][good] = dict(state_goods_production=10, state_goods_consumption=10,
                                           state_goods_pricier=pricier, state_goods_cheaper=cheaper)

    def reference(self, good, bound, target=None):
        return self.c.number(f'sed_investment_price_{good}_{bound}', target or self.target)

    def test_market_price_read_adjusts_both_reference_bounds(self):
        c = self.c
        c.market_goods['wood']['market_goods_pricier'] = 0.5
        c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 25)
        self.assertEqual(self.reference('wood', 'upper'), 35)
        c.market_goods['wood'].update(market_goods_pricier=0, market_goods_cheaper=0.5)
        c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 5)
        self.assertEqual(self.reference('wood', 'upper'), 15)

    def test_local_signals_override_the_market_fallback(self):
        self.c.market_goods['wood']['market_goods_pricier'] = 0.5
        self.local_price(self.target, 'wood', cheaper=0.5)
        other = state()
        self.c.states.append(other)
        self.c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 3)
        self.assertEqual(self.reference('wood', 'lower', other), 25)

    def test_diagnostic_refresh_replaces_old_cached_prices_without_actions(self):
        self.local_price(self.target, 'wood', cheaper=0.5)
        self.c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 3)
        self.local_price(self.target, 'wood', pricier=0.5)
        self.c.run('sed_refresh_diagnostics')
        self.assertEqual(self.reference('wood', 'lower'), 25)
        self.assertEqual(self.c.constructions, [])
        self.assertEqual(self.c.production_method_changes, [])

    def test_direct_market_read_and_local_band_cover_a_fractional_change(self):
        self.c.market_goods['wood']['market_goods_pricier'] = 0.15
        self.c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 18)
        self.assertEqual(self.reference('wood', 'upper'), 28)
        self.local_price(self.target, 'wood', pricier=0.15)
        self.c.run('sed_refresh_investment_prices')
        self.assertLessEqual(self.reference('wood', 'lower'), 18)
        self.assertGreaterEqual(self.reference('wood', 'upper'), 28)

    def test_local_output_prices_can_change_the_automatic_destination(self):
        self.c.states = []
        for cheaper, pricier in [(0.5, 0), (0, 0.5)]:
            producer = building('building_logging_camp')
            producer['production_methods'] = ['pm_simple_forestry']
            target = state(buildings=[producer])
            self.local_price(target, 'wood', pricier=pricier, cheaper=cheaper)
            self.c.states.append(target)
        self.c.market_goods['wood'] = dict(market_goods_has_goods_shortage=True,
                                           market_goods_buy_orders=100, market_goods_sell_orders=40)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions,
                         [dict(building='building_logging_camp', state=self.c.states[1])])

    def test_local_input_prices_can_change_the_automatic_destination(self):
        self.c.states = []
        for pricier, cheaper in [(0.5, 0), (0, 0.5)]:
            producer = building('building_tooling_workshop')
            producer['production_methods'] = ['pm_crude_tools']
            target = state(buildings=[producer])
            self.local_price(target, 'wood', pricier=pricier, cheaper=cheaper)
            self.c.states.append(target)
        self.c.market_goods['tools'] = dict(market_goods_has_goods_shortage=True,
                                            market_goods_buy_orders=100, market_goods_sell_orders=40)
        self.c.run('sed_set_mode_automatic')
        self.c.run('sed_auto_apply_monthly')
        self.assertEqual(self.c.constructions,
                         [dict(building='building_tooling_workshop', state=self.c.states[1])])

    def test_founding_reference_uses_observed_local_bands(self):
        self.local_price(self.target, 'wood', cheaper=0.5)
        self.local_price(self.target, 'tools', pricier=0.5)
        self.c.run('sed_refresh_investment_prices')
        self.assertEqual(self.c.number('sed_investment_tooling_workshop_margin', self.target), 1050)

    def test_approval_refreshes_prices_before_selecting_the_variant(self):
        wheat = building('building_wheat_farm')
        wheat['production_methods'] = ['pm_chemical_fertilizer', 'pm_tools']
        rice = building('building_rice_farm')
        rice['production_methods'] = ['pm_simple_farming_building_rice_farm']
        self.target['buildings'] = [wheat, rice]
        self.c.market_goods['grain'] = dict(market_goods_has_goods_shortage=True,
                                            market_goods_buy_orders=100, market_goods_sell_orders=40)
        self.c.run('sed_set_mode_automatic')
        self.assertTrue(self.c.condition(self.c.definitions['sed_grain_wheat_farm_preferred_supplier'], self.target))
        self.c.market_goods['fertilizer']['market_goods_pricier'] = 0.75
        self.c.run('sed_run_grain_approval', self.target)
        self.assertEqual(self.c.constructions, [dict(building='building_rice_farm', state=self.target)])

    def test_extreme_bands_remain_nonnegative_and_disable_clears_caches(self):
        self.local_price(self.target, 'wood', cheaper=0.75)
        self.c.run('sed_refresh_investment_prices')
        self.assertEqual(self.reference('wood', 'lower'), 0)
        self.assertEqual(self.reference('wood', 'upper'), 10)
        self.c.run('sed_disable_country')
        self.assertFalse(any(name.startswith('sed_investment_market_') for name in self.c.variables))
        self.assertFalse(any(name.startswith('sed_investment_local_') for name in self.target['variables']))


if __name__ == '__main__':
    unittest.main()
