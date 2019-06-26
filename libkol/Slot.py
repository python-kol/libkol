from enum import Enum
from typing import Optional


class Slot(Enum):
    Hat = "hat"
    Back = "back"
    Weapon = "weapon"
    Offhand = "offhand"
    Shirt = "shirt"
    Pants = "pants"
    Acc1 = "acc1"
    Acc2 = "acc2"
    Acc3 = "acc3"
    FamiliarEquipment = "familiarequip"

    @classmethod
    def from_acc_number(cls, num: int) -> "Slot":
        return Slot.Acc1 if num == 1 else Slot.Acc2 if num == 2 else Slot.Acc3

    def to_acc_number(self):
        return int(self.value[-1])

    def is_accessory(self):
        return self in [Slot.Acc1, Slot.Acc2, Slot.Acc3]

    @classmethod
    def from_db(cls, key: str) -> Optional["Slot"]:
        return (
            Slot.Hat
            if key == "hat"
            else Slot.Shirt
            if key == "shirt"
            else Slot.Weapon
            if key == "weapon"
            else Slot.Offhand
            if key == "offhand"
            else Slot.Pants
            if key == "pants"
            else Slot.FamiliarEquipment
            if key == "familiar_equipment"
            else Slot.Acc1
            if key == "accessory"
            else None
        )
