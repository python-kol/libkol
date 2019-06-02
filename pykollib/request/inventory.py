from typing import Any, Dict, List

import pykollib

from ..types import ItemQuantity
from ..Item import Item
from .request import Request


class inventory(Request):
    returns_json = True

    """
    Get a list of items in the user's inventory.
    """
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)
        data = {"for": session.state.get("user_agent", "pykollib"), "what": "inventory"}

        self.request = session.request("api.php", json=True, data=data)

    @staticmethod
    async def parser(json: Dict[str, Any], **kwargs) -> List[ItemQuantity]:
        return [
            ItemQuantity(await Item.get_or_discover(id=id), quantity)
            for id, quantity in json.items()
        ]
