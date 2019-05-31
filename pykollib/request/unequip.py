import pykollib

from .equip import Slot
from .request import Request


class unequip(Request):
    def __init__(self, session: "pykollib.Session", slot: "Slot" = None) -> None:
        """
        Unequips the equipment in the designated slot.

        :param slot: Will unequip item from the specified Slot, or completely undress if `slot` is None
        """
        super().__init__(session)

        params = {}

        if slot is None:
            params["action"] = "unequipall"
        else:
            params["action"] = "unequip"
            params["type"] = slot.value

        self.request = session.request("inv_equip.php", params=params)
