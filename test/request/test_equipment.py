from collections import Counter

from .test_base import TestCase
from pykollib.request import equipment
from pykollib.request.equip import Slot


class EquipmentTestCase(TestCase):
    request = "equipment"

    def test_equipment_accessories_merged(self):
        with self.open_test_data("accessories_merged") as file:
            outfit = equipment.parser(file.read())

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

    def test_equipment_accessories_separate(self):
        with self.open_test_data("accessories_separate") as file:
            outfit = equipment.parser(file.read())
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
