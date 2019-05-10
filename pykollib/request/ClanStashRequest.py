from typing import List, Dict, Any, TYPE_CHECKING
import re

if TYPE_CHECKING:
    from ..Session import Session

stashItemsPattern = re.compile(
    r"<option value=(?P<id>\d*) descid=\d*>(?P<name>.*?)(?: \((?P<quantity>\d*)\))?(?: \(-(?P<cost>\d*)\))?</option>"
)


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    return [
        {
            "id": int(i["id"]),
            "name": i["name"],
            "quantity": int(i["quantity"] or 1),
            "cost": int(i["cost"] or 0),
        }
        for i in (m.groupdict() for m in stashItemsPattern.finditer(html))
    ]


def clanStashRequest(session: "Session"):
    "This class is used to get a list of items in the user's clan stash."
    return session.request("clan_stash.php", parse=parse, pwd=True)
