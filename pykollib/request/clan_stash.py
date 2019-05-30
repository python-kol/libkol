import re
from typing import Any, Coroutine, Dict, List

import pykollib

from ..Item import Item

stashItemsPattern = re.compile(
    r"<option value=(?P<id>\d*) descid=\d*>(?P<name>.*?)(?: \((?P<quantity>\d*)\))?(?: \(-(?P<cost>\d*)\))?</option>"
)


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    return [
        {
            "item": Item[int(i["id"])],
            "quantity": int(i["quantity"] or 1),
            "cost": int(i["cost"] or 0),
        }
        for i in (m.groupdict() for m in stashItemsPattern.finditer(html))
    ]


def clan_stash(session: "pykollib.Session"):
    "This class is used to get a list of items in the user's clan stash."
    return session.request("clan_stash.php", parse=parse, pwd=True)
