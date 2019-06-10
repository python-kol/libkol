from libkol.request import trophy

from .test_base import TestCase


class TrophyTestCase(TestCase):
    request = "trophy"

    def test_trophy_none(self):
        async def run_test(file):
            trophies = await trophy.parser(file.read())
            self.assertEqual(len(trophies), 0)

        self.run_async("none", run_test)

    def test_trophy_one(self):
        async def run_test(file):
            trophies = await trophy.parser(file.read())
            self.assertEqual(len(trophies), 1)
            self.assertEqual(trophies[0].id, 111)

        self.run_async("one", run_test)
