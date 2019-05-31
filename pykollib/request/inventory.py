from typing import Any, Dict, List

from .request import Request

import pykollib

from ..Item import Item, ItemQuantity


class inventory(Request):
    returns_json = True

    def __init__(self, session: "pykollib.Session") -> None:
        """
        Get a list of items in the user's inventory.
        """
        super().__init__(session)
        data = {"for": session.state.get("user_agent", "pykollib"), "what": "inventory"}

        self.request = session.request("api.php", json=True, data=data)

    @staticmethod
    def parser(json: Dict[str, Any], **kwargs) -> List[ItemQuantity]:
        return [ItemQuantity(Item[id], quantity) for id, quantity in json.items()]
