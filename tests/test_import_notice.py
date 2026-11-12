import unittest

from tools.build_mod import SUPPLY_TARGETS, outputs
from tools.pdx_script import child, parse
from script_harness import Country, state

MONTH_KEY = 1836 * 12


def script_definitions():
    result = {}
    for name, data in outputs().items():
        if name.startswith(('common/', 'events/')):
            result.update((entry.key, entry.value) for entry in parse(data.decode('utf-8-sig')))
    return result


def notices(country):
    return [event for event in country.scheduled_events
            if event[0].startswith('sed_pulse.') and event[0] != 'sed_pulse.1']


def metadata(entries):
    return [entry for entry in entries if entry.key not in
            ('name', 'custom_tooltip', 'ai_chance', 'default_option', 'trigger')]


class ImportNoticeTests(unittest.TestCase):
    def setUp(self):
        self.definitions = script_definitions()

    def country(self, shortage='wood'):
        c = Country(self.definitions)
        if shortage:
            c.market_goods[shortage]['market_goods_has_goods_shortage'] = True
        c.run('sed_enable_country')
        return c

    def test_notice_fires_when_no_local_expansion_is_eligible(self):
        c = self.country()
        c.run('sed_check_import_notices')
        self.assertIn(('sed_pulse.2', 0), c.scheduled_events)

    def test_notice_waits_for_a_shortage(self):
        c = self.country(shortage=None)
        c.run('sed_check_import_notices')
        self.assertEqual(notices(c), [])

    def test_pending_local_expansion_suppresses_the_notice(self):
        c = self.country()
        blocked = state()
        blocked['variables'] = {'sed_wood_request_pending': True}
        c.states.append(blocked)
        c.run('sed_check_import_notices')
        self.assertEqual(notices(c), [])

    def test_cooldown_suppresses_repeat_until_it_expires(self):
        c = self.country()
        c.variables['sed_import_notice_wood_month'] = MONTH_KEY + 5
        c.run('sed_check_import_notices')
        self.assertEqual(notices(c), [])
        c.variables['sed_import_notice_wood_month'] = MONTH_KEY
        c.run('sed_check_import_notices')
        self.assertIn(('sed_pulse.2', 0), notices(c))

    def options(self, good):
        event = self.definitions['sed_pulse.' + str(
            [item['good'] for item in SUPPLY_TARGETS].index(good) + 2)]
        return [entry.value for entry in event if entry.key == 'option']

    def test_event_immediate_and_options_set_the_cooldowns(self):
        c = self.country()
        event = self.definitions['sed_pulse.2']
        c.execute(child(event, 'immediate'), c.country_scope())
        self.assertEqual(c.variables['sed_import_notice_wood_month'], MONTH_KEY + 6)
        trade, plan, mute = self.options('wood')
        c.execute(metadata(trade), c.country_scope())
        self.assertEqual(c.variables['sed_import_notice_wood_month'], MONTH_KEY + 12)
        c.execute(metadata(plan), c.country_scope())
        self.assertEqual(c.variables['sed_last_year'], 1836)
        self.assertEqual(c.variables['sed_import_notice_wood_month'], MONTH_KEY + 12)
        c.execute(metadata(mute), c.country_scope())
        self.assertEqual(c.variables['sed_import_notice_wood_month'], MONTH_KEY + 24)

    def test_event_structure_and_localization_for_every_good(self):
        english = outputs()['localization/english/sed_l_english.yml'].decode('utf-8-sig')
        portuguese = outputs()['localization/braz_por/sed_l_braz_por.yml'].decode('utf-8-sig')
        for index, item in enumerate(SUPPLY_TARGETS, start=2):
            good = item['good']
            event = self.definitions[f'sed_pulse.{index}']
            self.assertIsNotNone(child(event, 'title'))
            self.assertIsNotNone(child(event, 'desc'))
            self.assertIsNotNone(child(event, 'duration'))
            self.assertIsNotNone(child(event, 'immediate'))
            self.assertIsNotNone(child(event, 'trigger'))
            options = self.options(good)
            self.assertEqual(len(options), 3)
            self.assertTrue(any(entry.key == 'default_option'
                                for option in options for entry in option))
            for option in options:
                self.assertTrue(any(entry.key == 'custom_tooltip' for entry in option))
            for suffix in ('title', 'desc', 'option_trade', 'option_trade_tt',
                           'option_plan', 'option_plan_tt', 'option_mute', 'option_mute_tt'):
                key = f'sed_import_notice_{good}_{suffix}'
                self.assertIn(key + ':', english)
                self.assertIn(key + ':', portuguese)

    def test_notice_records_market_orders_for_the_description(self):
        c = self.country()
        c.market_goods['wood']['market_goods_buy_orders'] = 1250
        c.market_goods['wood']['market_goods_sell_orders'] = 900
        c.run('sed_check_import_notices')
        self.assertEqual(c.variables['sed_import_notice_wood_buy'], 1250)
        self.assertEqual(c.variables['sed_import_notice_wood_sell'], 900)

    def test_description_shows_the_recorded_orders(self):
        portuguese = outputs()['localization/braz_por/sed_l_braz_por.yml'].decode('utf-8-sig')
        for item in SUPPLY_TARGETS:
            good = item['good']
            self.assertIn(
                f".Var('sed_import_notice_{good}_buy').GetValue|D", portuguese)
            self.assertIn(
                f".Var('sed_import_notice_{good}_sell').GetValue|D", portuguese)

    def test_description_teaches_the_post_1_9_import_path(self):
        # Terms verified in the installed game 1.15 (concepts, diplomacy and law
        # localization): Trade Center, Trade Capacity, Subventions, Goods
        # Transfer and law_isolationism's country_disallow_trade_bool.
        english = outputs()['localization/english/sed_l_english.yml'].decode('utf-8-sig')
        portuguese = outputs()['localization/braz_por/sed_l_braz_por.yml'].decode('utf-8-sig')
        for text, terms in ((portuguese, ('Centro de Comércio', 'capacidade de comércio',
                                          'subvenção', 'Transferência de Bens', 'Isolacionismo')),
                            (english, ('Trade Center', 'Trade Capacity',
                                       'subvention', 'Goods Transfer', 'Isolationism'))):
            for term in terms:
                with self.subTest(term=term):
                    self.assertIn(term, text)

    def test_notice_is_advisory_and_never_opens_a_trade_route(self):
        events = outputs()['events/sed_events.txt'].decode('utf-8-sig')
        self.assertNotIn('create_trade_route', events)
        self.assertNotIn('add_trade_route_level', events)


if __name__ == '__main__':
    unittest.main()
