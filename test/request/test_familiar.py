from libkol.request import familiar

from .test_base import TestCase


class MiningTestCase(TestCase):
    request = "familiar"

    def test_familiar_basic(self):
        async def run_test(file):
            result = await familiar.parser(file.read(), session=self.session)
            self.assertEqual(len(result), 6)
            self.assertEqual(result[0].familiar.id, 1)
            self.assertEqual(result[0].weight, 4)
            self.assertEqual(result[0].nickname, "Ass")
            self.assertEqual(result[0].experience, 21)
            self.assertEqual(result[0].kills, 1176)

            self.assertEqual(result[1].familiar.id, 142)
            self.assertEqual(result[1].weight, 1)
            self.assertEqual(result[1].nickname, "Titties")
            self.assertEqual(result[1].experience, 0)
            self.assertEqual(result[1].kills, 732)

            self.assertEqual(result[2].familiar.id, 16)
            self.assertEqual(result[2].weight, 1)
            self.assertEqual(result[2].nickname, "Ass & Titties")
            self.assertEqual(result[2].experience, 0)
            self.assertEqual(result[2].kills, 0)

            self.assertEqual(result[3].familiar.id, 59)
            self.assertEqual(result[3].weight, 1)
            self.assertEqual(result[3].nickname, "Stonklin")
            self.assertEqual(result[3].experience, 0)
            self.assertEqual(result[3].kills, 0)

            self.assertEqual(result[4].familiar.id, 168)
            self.assertEqual(result[4].weight, 1)
            self.assertEqual(result[4].nickname, "Botchell")
            self.assertEqual(result[4].experience, 0)
            self.assertEqual(result[4].kills, 0)

            self.assertEqual(result[5].familiar.id, 261)
            self.assertEqual(result[5].weight, 1)
            self.assertEqual(result[5].nickname, "Basevelt")
            self.assertEqual(result[5].experience, 0)
            self.assertEqual(result[5].kills, 0)

        self.run_async("basic", run_test)
