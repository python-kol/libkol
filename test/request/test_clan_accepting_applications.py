from pykollib.request import clan_accepting_applications

from .test_base import TestCase


class ClanAcceptingApplicationsTestCase(TestCase):
    request = "clan_accepting_applications"

    def test_clan_accepting_applications_on(self):
        with self.open_test_data("on") as file:
            parsed = clan_accepting_applications.parser(file.read())

            assert parsed is True

    def test_clan_accepting_applications_off(self):
        with self.open_test_data("off") as file:
            parsed = clan_accepting_applications.parser(file.read())

            assert parsed is False
