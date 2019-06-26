from typing import List

import libkol

from ..util import parsing
from .request import Request


class clan_vip_lookingglass(Request[List["libkol.types.ItemQuantity"]]):
    """
    Uses the Looking Glass in the clan VIP room.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"action": "lookingglass"}
        self.request = session.request("clan_viplounge.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List["libkol.types.ItemQuantity"]:
        return await parsing.item(content)
