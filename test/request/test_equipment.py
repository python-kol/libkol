from collections import Counter

from libkol import Slot
from libkol.request import equipment

from .test_base import TestCase


class EquipmentTestCase(TestCase):
    request = "equipment"

    def test_equipment_accessories_merged(self):
        async def run_test(file):
            outfit = await equipment.parser(file.read(), session=self.session)

            self.assertEqual(outfit[Slot.Hat].id, 2078)
            self.assertEqual(outfit[Slot.Back].id, 5738)
            self.assertEqual(outfit[Slot.Shirt].id, 3837)
            self.assertEqual(outfit[Slot.Weapon].id, 9893)
            self.assertEqual(outfit[Slot.Offhand], None)
            self.assertEqual(outfit[Slot.Pants].id, 9406)
            self.assertEqual(
                Counter(
                    [outfit[Slot.Acc1].id, outfit[Slot.Acc2].id, outfit[Slot.Acc3].id]
                ),
                Counter([6955, 3322, 6956]),
            )
            self.assertEqual(outfit[Slot.FamiliarEquipment].id, 4135)

        self.run_async("accessories_merged", run_test)

    def test_equipment_accessories_separate(self):
        async def run_test(file):
            outfit = await equipment.parser(file.read(), session=self.session)
            self.assertEqual(outfit[Slot.Hat].id, 2078)
            self.assertEqual(outfit[Slot.Back].id, 5738)
            self.assertEqual(outfit[Slot.Shirt].id, 3837)
            self.assertEqual(outfit[Slot.Weapon].id, 9893)
            self.assertEqual(outfit[Slot.Offhand], None)
            self.assertEqual(outfit[Slot.Pants].id, 9406)
            self.assertEqual(outfit[Slot.Acc1].id, 6955)
            self.assertEqual(outfit[Slot.Acc2].id, 3322)
            self.assertEqual(outfit[Slot.Acc3].id, 6956)
            self.assertEqual(outfit[Slot.FamiliarEquipment].id, 4135)

        self.run_async("accessories_separate", run_test)
