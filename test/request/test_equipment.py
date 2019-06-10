from collections import Counter

from libkol.request import equipment

from .test_base import TestCase


class EquipmentTestCase(TestCase):
    request = "equipment"

    def test_equipment_accessories_merged(self):
        async def run_test(file):
            outfit = await equipment.parser(file.read())

            self.assertEqual(outfit.hat.id, 2078)
            self.assertEqual(outfit.back.id, 5738)
            self.assertEqual(outfit.shirt.id, 3837)
            self.assertEqual(outfit.weapon.id, 9893)
            self.assertEqual(outfit.offhand, None)
            self.assertEqual(outfit.pants.id, 9406)
            self.assertEqual(
                Counter([outfit.acc1.id, outfit.acc2.id, outfit.acc3.id]),
                Counter([6955, 3322, 6956]),
            )
            self.assertEqual(outfit.familiar.id, 4135)

        self.run_async("accessories_merged", run_test)

    def test_equipment_accessories_separate(self):
        async def run_test(file):
            outfit = await equipment.parser(file.read())
            self.assertEqual(outfit.hat.id, 2078)
            self.assertEqual(outfit.back.id, 5738)
            self.assertEqual(outfit.shirt.id, 3837)
            self.assertEqual(outfit.weapon.id, 9893)
            self.assertEqual(outfit.offhand, None)
            self.assertEqual(outfit.pants.id, 9406)
            self.assertEqual(outfit.acc1.id, 6955)
            self.assertEqual(outfit.acc2.id, 3322)
            self.assertEqual(outfit.acc3.id, 6956)
            self.assertEqual(outfit.familiar.id, 4135)

        self.run_async("accessories_separate", run_test)
