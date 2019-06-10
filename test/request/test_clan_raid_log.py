from libkol.request import clan_raid_log

from .test_base import TestCase


class ClanRaidLogTestCase(TestCase):
    request = "clan_raid_log"

    def test_clan_raid_log_events(self):
        """
        This is a file containing a singular and plural example of every supported clan raid log
        """
        async def run_test(file):
            parsed = [clan_raid_log.parse_raid_log(line.strip()) for line in file]
            # Check that we filter out the annoying x <turns> thing
            self.assertEqual(parsed[12].data["monster"], "giant zombie goldfish")
            self.assertEqual(parsed[101].data["monster"], "stench vampire")
            self.assertEqual(parsed[154].data["monster"], "the Zombie Homeowners' Association")
            self.assertEqual(parsed[155].data["monster"], "The Great Wolf of the Air")
            self.assertEqual(parsed[156].data["monster"], "giant zombie goldfish")

        self.run_async("events", run_test, ext="txt")
