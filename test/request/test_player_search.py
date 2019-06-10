from libkol.request import player_search

from .test_base import TestCase


class PlayerSearchTestCase(TestCase):
    request = "player_search"

    def test_player_search_basic(self):
        async def run_test(file):
            players = await player_search.parser(file.read())
            self.assertEqual(len(players), 1000)
            self.assertEqual(players[50].clan_id, None)
            self.assertEqual(players[13].clan_name, None)
            self.assertEqual(players[112].fame, None)

        self.run_async("basic", run_test)

    def test_player_search_pvp(self):
        async def run_test(file):
            players = await player_search.parser(file.read())
            self.assertEqual(len(players), 676)
            self.assertEqual(players[50].clan_id, 82072)
            self.assertEqual(players[13].clan_name, "Tainted Meat AIliance")
            self.assertEqual(players[112].fame, 24)

        self.run_async("pvp", run_test)
