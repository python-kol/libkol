from .test_base import TestCase
from ...request.clan_accepting_applications import parse


class ClanAcceptingApplicationsTestCase(TestCase):
    request = "clan_accepting_applications"

    def test_clan_accepting_applications_on(self):
        with self.open_test_data("on") as file:
            parsed = parse(file.read())

            assert parsed is True

    def test_clan_accepting_applications_off(self):
        with self.open_test_data("off") as file:
            parsed = parse(file.read())

            assert parsed is False
