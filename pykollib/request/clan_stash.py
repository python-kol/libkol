import re
from typing import Any, Dict, List

import pykollib

from ..Item import Item
from .request import Request

stashItemsPattern = re.compile(
    r"<option value=(?P<id>\d*) descid=\d*>(?P<name>.*?)(?: \((?P<quantity>\d*)\))?(?: \(-(?P<cost>\d*)\))?</option>"
)


class clan_stash(Request):
    def __init__(self, session: "pykollib.Session"):
        """
        This class is used to get a list of items in the user's clan stash.
        """
        super().__init__(session)

        self.request = session.request("clan_stash.php", pwd=True)

    @staticmethod
    def parser(html: str, **kwargs) -> List[Dict[str, Any]]:
        return [
            {
                "item": Item[int(i["id"])],
                "quantity": int(i["quantity"] or 1),
                "cost": int(i["cost"] or 0),
            }
            for i in (m.groupdict() for m in stashItemsPattern.finditer(html))
        ]
