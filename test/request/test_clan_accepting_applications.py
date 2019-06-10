from libkol.request import clan_accepting_applications

from .test_base import TestCase


class ClanAcceptingApplicationsTestCase(TestCase):
    request = "clan_accepting_applications"

    def test_clan_accepting_applications_on(self):
        async def run_test(file):
            parsed = await clan_accepting_applications.parser(file.read())
            assert parsed is True

        self.run_async("on", run_test)

    def test_clan_accepting_applications_off(self):
        async def run_test(file):
            parsed = await clan_accepting_applications.parser(file.read())
            assert parsed is False

        self.run_async("off", run_test)
