import re
from typing import Any, Dict, List

import libkol

from ..Item import Item
from .request import Request

stashItemsPattern = re.compile(
    r"<option value=(?P<id>\d*) descid=\d*>(?P<name>.*?)(?: \((?P<quantity>\d*)\))?(?: \(-(?P<cost>\d*)\))?</option>"
)


class clan_stash(Request[List[Dict[str, Any]]]):
    """
    This class is used to get a list of items in the user's clan stash.
    """

    def __init__(self, session: "libkol.Session"):
        super().__init__(session)

        self.request = session.request("clan_stash.php", pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Dict[str, Any]]:
        return [
            {
                "item": await Item.get_or_discover(id=int(i["id"])),
                "quantity": int(i["quantity"] or 1),
                "cost": int(i["cost"] or 0),
            }
            for i in (m.groupdict() for m in stashItemsPattern.finditer(content))
        ]
