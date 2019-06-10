import re
from datetime import datetime
from typing import List, NamedTuple

from bs4 import BeautifulSoup
from yarl import URL

import libkol

from ..Error import UnknownError
from ..Item import Item
from ..util import parsing
from .request import Request

details_pattern = re.compile(r"^ bought ([0-9]+) \((.*)\) for ([0-9]+) Meat.$")


class Transaction(NamedTuple):
    date: datetime
    username: str
    user_id: int
    quantity: int
    item: Item
    meat: int


class mall_transactions(Request):
    """
	Get the last 2 weeks of transactions from your store.

    :param session: Active session
	"""

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"which": 3}
        self.request = session.request("backoffice.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Transaction]:
        soup = BeautifulSoup(content, "html.parser")

        container = soup.find("span", class_="small")

        lines = parsing.split_by_br(container)[:-1]

        transactions = []  # type: List[Transaction]

        for l in lines:
            match = details_pattern.match(l[2])

            if match is None:
                raise UnknownError("Parsing transaction failed")

            item = await Item.get_or_discover(name=match.group(2))

            if item is None:
                print("Item not recognised: {}".format(match.group(2)))
                continue

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
