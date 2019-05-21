from typing import List, Dict, Any, TYPE_CHECKING
import re

from ..Item import Item

if TYPE_CHECKING:
    from ..Session import Session

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


def clan_stash(session: "Session"):
    "This class is used to get a list of items in the user's clan stash."
    return session.request("clan_stash.php", parse=parse, pwd=True)
