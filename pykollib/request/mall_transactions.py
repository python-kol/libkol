from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from datetime import datetime
from typing import TYPE_CHECKING, Coroutine, Any, NamedTuple, List
from yarl import URL
import re

if TYPE_CHECKING:
    from ..Session import Session

from ..Error import UnknownError
from ..Item import Item
from ..util import parsing

details_pattern = re.compile(r"^ bought ([0-9]+) \((.*)\) for ([0-9]+) Meat.$")


class Transaction(NamedTuple):
    date: datetime
    username: str
    user_id: int
    quantity: int
    item: Item
    meat: int


def parse(html: str, **kwargs) -> List[Transaction]:
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("span", class_="small")

    lines = parsing.split_by_br(container)[:-1]

    transactions = []  # type: List[Transaction]

    for l in lines:
        match = details_pattern.match(l[2])

        if match is None:
            raise UnknownError("Parsing transaction failed")

        item = Item.get_or_none(name=match.group(2))

        if item is None:
            print("Item not recognised: {}".format(match.group(2)))

        transactions += [
            Transaction(
                datetime.strptime(l[0], "%m/%d/%y %H:%M:%S "),
                l[1].string,
                int(URL(l[1]["href"]).query["who"]),
                int(match.group(1)),
                item,
                int(match.group(3)),
            )
        ]

    return transactions


def mall_transactions(session: "Session") -> Coroutine[Any, Any, ClientResponse]:
    """
	Get the last 2 weeks of transactions from your store.
	"""
    params = {"which": 3}
    return session.request("backoffice.php", pwd=True, params=params, parse=parse)