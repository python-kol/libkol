import re
from aiohttp import ClientResponse

from typing import List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

clan_search_result_pattern = re.compile(
    r"<b><a href=\"showclan\.php\?recruiter=1&whichclan=([0-9]+)\">([^<>]*)</a></b>"
)


def parse(html: str) -> List[Dict[str, Any]]:
    return [
        {"id": int(m.group(1)), "name": m.group(2)}
        for m in clan_search_result_pattern.finditer(html)
    ]


def clan_search(
    session: "Session", query: str, nameonly: bool = True
) -> ClientResponse:
    data = {
        "action": "search",
        "searchstring": query,
        "whichfield": 1 if nameonly else 0,
        "countoper": 0,
        "countqty": 0,
        "furn1": 0,
        "furn2": 0,
        "furn3": 0,
        "furn4": 0,
        "furn5": 0,
        "furn9": 0,
    }

    return session.request("clan_signup.php", data=data)