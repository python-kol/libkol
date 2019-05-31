import re
from typing import Any, Dict

from bs4 import BeautifulSoup, Tag
from yarl import URL

import pykollib

from ..Error import UnknownError
from ..util import parsing
from .request import Request

previous_run_pattern = re.compile(r"^(.+?) run, ([A-Za-z]+) ([0-9]{2}), ([0-9]{4})$")


class clan_raid_log(Request):
    def __init__(self, session: "pykollib.Session", raid_id: int) -> None:
        """
        Retrieves on a previous raid.
        """
        super().__init__(session)

        params = {"viewlog": raid_id}

        self.request = session.request("clan_viewraidlog.php", params=params)

    @staticmethod
    def center_with_no_link(tag):
        return tag.name == "center" and tag.a is None

    @staticmethod
    def parse_raid_log(name: str, id: int, raid: Tag) -> Dict[str, Any]:
        """
        Parse a single raid's HTML tree
        """
        # They throw random <p>s everywhere, so get rid of them
        for p in raid.find_all("p", recursive=True):
            p.unwrap()

        summary = raid.find_all(clan_raid_log.center_with_no_link)

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
                for g in parsing.split_by_br(section)
            ]

            events.append((title, logs))

            section = section.find_next_sibling("b")

        return {
            "id": id,
            "name": name.lower(),
            "summary": [s.text for s in summary],
            "events": events,
        }

    @classmethod
    def parser(cls, html: str, url: URL, **kwargs) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("b", text=previous_run_pattern)

        m = previous_run_pattern.match(title.text)

        if m is None:
            raise UnknownError("Cannot parse previous run")

        name = m.group(1)
        id = int(url.query["viewlog"])
        first = title.parent
        raid = first.parent
        first.decompose()
        return cls.parse_raid_log(name, id, raid)
