from collections import Counter

from .test_base import TestCase
from ...request.equipment import parse
from ...request.equip import Slot


class EquipmentTestCase(TestCase):
    request = "equipment"

    def test_equipment_accessories_merged(self):
        with self.open_test_data("accessories_merged") as file:
            equipment = parse(file.read())

            self.assertEqual(equipment[Slot.Hat].id, 2078)
            self.assertEqual(equipment[Slot.Back].id, 5738)
            self.assertEqual(equipment[Slot.Shirt].id, 3837)
            self.assertEqual(equipment[Slot.Weapon].id, 9893)
            self.assertEqual(equipment[Slot.Offhand], None)
            self.assertEqual(equipment[Slot.Pants].id, 9406)
            self.assertEqual(
                Counter(
                    [
                        i.id
                        for k, i in equipment.items()
                        if k in [Slot.Acc1, Slot.Acc2, Slot.Acc3]
                    ]
                ),
                Counter([6955, 3322, 6956]),
            )
            self.assertEqual(equipment[Slot.Familiar].id, 4135)

    def test_equipment_accessories_separate(self):
        with self.open_test_data("accessories_separate") as file:
            equipment = parse(file.read())
            self.assertEqual(equipment[Slot.Hat].id, 2078)
            self.assertEqual(equipment[Slot.Back].id, 5738)
            self.assertEqual(equipment[Slot.Shirt].id, 3837)
            self.assertEqual(equipment[Slot.Weapon].id, 9893)
            self.assertEqual(equipment[Slot.Offhand], None)
            self.assertEqual(equipment[Slot.Pants].id, 9406)
            self.assertEqual(equipment[Slot.Acc1].id, 6955)
            self.assertEqual(equipment[Slot.Acc2].id, 3322)
            self.assertEqual(equipment[Slot.Acc3].id, 6956)
            self.assertEqual(equipment[Slot.Familiar].id, 4135)
