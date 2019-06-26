from libkol.request import mining
from libkol.request.mining import MiningSpotType

from .test_base import TestCase


class MiningTestCase(TestCase):
    request = "mining"

    def test_mining_mid_mine(self):
        async def run_test(file):
            result = await mining.parser(file.read(), session=self.session)
            self.assertEqual(result.resource_gain.hp, 0)
            self.assertEqual(result.resource_gain.mp, 0)
            self.assertEqual(result.resource_gain.adventures, 0)
            self.assertEqual(result.resource_gain.inebriety, 0)

            self.assertEqual(result.mine[0][0], MiningSpotType.Open)
            self.assertEqual(result.mine[1][0], MiningSpotType.Open)
            self.assertEqual(result.mine[2][0], MiningSpotType.Promising)
            self.assertEqual(result.mine[3][0], MiningSpotType.Promising)
            self.assertEqual(result.mine[4][0], MiningSpotType.Rocky)
            self.assertEqual(result.mine[5][0], MiningSpotType.Promising)

        self.run_async("mid_mine", run_test)
