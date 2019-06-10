from typing import Any, Dict

import libkol

from ..Item import Item
from .request import Request


class inventory(Request[Dict[Item, int]]):
    returns_json = True

    """
    Get a list of items in the user's inventory.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)
        data = {"for": session.state.get("user_agent", "libkol"), "what": "inventory"}

        self.request = session.request("api.php", json=True, data=data)

    @staticmethod
    async def parser(content: Dict[str, Any], **kwargs) -> Dict[Item, int]:
        return {await Item[int(id)]: int(quantity) for id, quantity in content.items()}
