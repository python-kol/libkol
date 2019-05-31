import re
from enum import Enum
from typing import List, NamedTuple

import pykollib

from ..Item import Item, ItemQuantity
from .request import Request

response_pattern = re.compile(r"You sell your (.*?) to (?:.*?) for ([0-9,]+) Meat.")


class Response(NamedTuple):
    items: List[ItemQuantity]
    meat_gained: int


class AutosellMode(Enum):
    All = 1
    AllButOne = 2
    Quantity = 3


class autosell_items(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        items: List[Item],
        quantity: int = 1,
        all: bool = False,
        keep_one: bool = False,
    ):
        """
        Sells items via the autosell system
        """

        params = {"action": "sell"}

        if keep_one:
            params["mode"] = AutosellMode.AllButOne.value
        elif all:
            params["mode"] = AutosellMode.All.value
        else:
            params["mode"] = AutosellMode.Quantity.value
            params["quantity"] = str(quantity)

        for item in items:
            params["item{}".format(item.id)] = str(item.id)

        self.request = session.request("sellstuff_ugly.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, items: List[Item] = [], **kwargs) -> Response:
        response_match = response_pattern.search(html)

        if response_match is None:
            return Response([], 0)

        item_quantities = []  # type: List[ItemQuantity]

        for item in items:
            pattern = re.compile(
                r"(?:(?:([0-9,]+) {})|{})(?:,|$)".format(
                    re.escape(item.pluralize()), re.escape(item.name)
                )
            )
            match = pattern.search(response_match.group(1))
            quantity = (
                0
                if match is None
                else 1
                if match.group(1) is None
                else int(match.group(1).replace(",", ""))
            )
            item_quantities += [ItemQuantity(item, quantity)]

        return Response(
            items=item_quantities,
            meat_gained=int(response_match.group(2).replace(",", "")),
        )
