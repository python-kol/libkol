from typing import List

import libkol

from ..util import parsing
from .request import Request


class clan_vip_klaw(Request[List["libkol.types.ItemQuantity"]]):
    """
    Uses the Deluxe Mr. Klaw in the clan VIP room.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"action": "klaw"}
        self.request = session.request("clan_viplounge.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List["libkol.types.ItemQuantity"]:
        return await parsing.item(content)
