from typing import Any, Coroutine, Dict, List

from aiohttp import ClientResponse
from bs4 import BeautifulSoup

import pykollib


def parse_privileges(container: BeautifulSoup) -> Dict[str, Any]:
    checkboxes = {
        c.next_sibling.strip(): c["value"]
        for c in container.find_all("input", type="checkbox")
    }

    inputs = {
        c["name"]: int(c["value"]) for c in container.find_all("input", type="text")
    }

    return {
        **checkboxes,
        **inputs,
        "forum": int(
            container.find_all("input", type="radio", checked="")[-1]["value"]
        ),
    }


def parse(html: str, **kwargs) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")

    ranks = [
        {
            "id": int(form.find("input", attrs={"name": "whichlevel"})["value"]),
            "name": form.find("input", attrs={"name": "levelname"})["value"],
            "degree": int(form.find("input", attrs={"name": "degree"})["value"]),
            "privileges": parse_privileges(
                form.find("span", id=lambda i: i.startswith("expanded"))
            ),
        }
        for form in soup.find_all(
            "form", attrs={"name": None}, action="clan_editranks.php"
        )
    ]
    return ranks


def clan_ranks(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    return session.request("clan_editranks.php", parse=parse)
