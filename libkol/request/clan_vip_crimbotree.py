from typing import List

import libkol

from ..types import ItemQuantity
from ..util import parsing
from .request import Request


class clan_vip_crimbotree(Request[List[ItemQuantity]]):
    """
    Uses the Crimbo Tree in the clan VIP room.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"action": "crimbotree"}
        self.request = session.request("clan_viplounge.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        return await parsing.item(content)
