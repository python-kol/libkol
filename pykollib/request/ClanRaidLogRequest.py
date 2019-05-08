from aiohttp import ClientResponse
from yarl import URL
from bs4 import BeautifulSoup
from typing import Dict, Any, TYPE_CHECKING
import re
import itertools

if TYPE_CHECKING:
    from ..Session import Session

previousRunPattern = re.compile(r"^(.+?) run, ([A-Za-z]+) ([0-9]{2}), ([0-9]{4})$")


def center_with_no_link(tag):
    return tag.name == "center" and tag.a is None


def parse_raid_log(name: str, id: int, raid: "BeautifulSoup") -> Dict[str, Any]:
    """
    Parse a single raid's HTML tree
    """
    # They throw random <p>s everywhere, so get rid of them
    for p in raid.find_all("p", recursive=True):
        p.unwrap()

    summary = raid.find_all(center_with_no_link)

    events = []

    # In the old days there were no summaries
    if len(summary) == 0:
        section = raid.find("b")
    else:
        section = summary[-1].find_next_sibling("b")

    # We now look for subsection titles, these are zones or
    # sections like "Loot Distribution"
    while section is not None:
        title = section.text
        section = section.find_next_sibling("blockquote")

        # This just traverses the list of HTML elements,
        # breaking it up by <br /> tag
        logs = [
            "".join([e.text if e.name else e for e in g])
            for k, g in itertools.groupby(
                section.children, key=lambda e: e.name != "br"
            )
            if k
        ]

        events.append((title, logs))

        section = section.find_next_sibling("b")

    return {
        "id": id,
        "name": name.lower(),
        "summary": [s.text for s in summary],
        "events": events,
    }


def parse(html: str, url: "URL", **kwargs) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("b", text=previousRunPattern)
    name = previousRunPattern.match(title.text).group(1)
    id = int(url.query["viewlog"])
    first = title.parent
    raid = first.parent
    first.decompose()
    return parse_raid_log(name, id, raid)


async def clanRaidLogRequest(session: "Session", raid_id: int) -> ClientResponse:
    """
    Retrieves on a previous raid.
    """
    params = {"viewlog": raid_id}

    return await session.post("clan_viewraidlog.php", params=params, parse=parse)
