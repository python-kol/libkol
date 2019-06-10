from libkol.request import clan_log

from .test_base import TestCase


class ClanLogTestCase(TestCase):
    request = "clan_log"

    def test_clan_log_basic(self):
        async def run_test(file):
            parsed = await clan_log.parser(file.read())
            self.assertEqual(len(parsed), 1294)

        self.run_async("basic", run_test)

    def test_clan_log_busy(self):
        async def run_test(file):
            parsed = await clan_log.parser(file.read())
            self.assertEqual(len(parsed), 2927)

        self.run_async("reddit_united", run_test)
