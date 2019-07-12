from libkol.request import player_profile

from .test_base import TestCase


class PlayerSearchTestCase(TestCase):
    request = "player_profile"

    def test_player_profile_public(self):
        async def run_test(file):
            profile = await player_profile.parser(file.read())
            self.assertEqual(profile.username, "Gausie")
            self.assertEqual(profile.ascensions, 216)
            self.assertEqual(len(profile.trophies), 71)
            self.assertEqual(profile.tattoo, "kgbtat")
            self.assertEqual(profile.tattoos, 165)
            self.assertGreaterEqual(profile.clan, "The Piglets of Fate")

        self.run_async("public", run_test)

    def test_player_profile_private(self):
        async def run_test(file):
            profile = await player_profile.parser(file.read())
            self.assertEqual(profile.username, "Lyft")
            self.assertEqual(profile.ascensions, 326)
            self.assertEqual(len(profile.trophies), 0)
            self.assertEqual(profile.tattoo, "gtat")
            self.assertEqual(profile.tattoos, None)
            self.assertGreaterEqual(profile.clan, "Reddit United")

        self.run_async("private", run_test)
