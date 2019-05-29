from .test_base import TestCase
from ...request.player_search import parse


class MallTransactionsTestCase(TestCase):
    request = "player_search"

    def test_player_search_basic(self):
        with self.open_test_data("basic") as file:
            players = parse(file.read())
            self.assertEqual(len(players), 1000)
            self.assertEqual(players[50].clan_id, None)
            self.assertEqual(players[13].clan_name, None)
            self.assertEqual(players[112].fame, None)

    def test_player_search_pvp(self):
        with self.open_test_data("pvp") as file:
            players = parse(file.read())
            self.assertEqual(len(players), 676)
            self.assertEqual(players[50].clan_id, 82072)
            self.assertEqual(players[13].clan_name, "Tainted Meat AIliance")
            self.assertEqual(players[112].fame, 24)
