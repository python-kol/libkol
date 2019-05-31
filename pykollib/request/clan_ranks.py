from typing import Any, Dict, List

from .request import Request
from bs4 import BeautifulSoup, Tag

import pykollib

class clan_ranks(Request):
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)
        self.request = session.request("clan_editranks.php")


    @staticmethod
    def parse_privileges(container: Tag) -> Dict[str, Any]:
        checkboxes = {
            c.next_sibling.strip(): c["value"]
            for c in container.find_all("input", type="checkbox")
        }

        inputs = {
            str(c["name"]): int(c["value"]) for c in container.find_all("input", type="text")
        }

        return {
            **checkboxes,
            **inputs,
            "forum": int(
                container.find_all("input", type="radio", checked="")[-1]["value"]
            ),
        }

    @classmethod
    def parser(cls, html: str, **kwargs) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")

        ranks = [
            {
                "id": int(form.find("input", attrs={"name": "whichlevel"})["value"]),
                "name": form.find("input", attrs={"name": "levelname"})["value"],
                "degree": int(form.find("input", attrs={"name": "degree"})["value"]),
                "privileges": cls.parse_privileges(
                    form.find("span", id=lambda i: i.startswith("expanded"))
                ),
            }
            for form in soup.find_all(
                "form", attrs={"name": None}, action="clan_editranks.php"
            )
        ]
        return ranks
