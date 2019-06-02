from typing import List

import pykollib

from ..types import ItemQuantity
from ..util import parsing
from .request import Request


class clan_vip_klaw(Request):
    """
    Uses the Deluxe Mr. Klaw in the clan VIP room.
    """
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)

        params = {"action": "klaw"}
        self.request = session.request("clan_viplounge.php", params=params)

    @staticmethod
    async def parser(html: str, **kwargs) -> List[ItemQuantity]:
        return await parsing.item(html)
