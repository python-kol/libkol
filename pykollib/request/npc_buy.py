from enum import Enum
from typing import List, NamedTuple

from .request import Request

import pykollib

from ..Error import (InvalidLocationError, NotEnoughMeatError, UnknownError,
                     WrongKindOfItemError)
from ..Item import Item, ItemQuantity
from ..util import parsing


class Store(Enum):
    Smacketeria = "3"
    GoudasGrimoireAndGrocery = "2"
    ShadowyStore = "1"
    Laboratory = "g"
    BlackMarket = "l"
    WhiteCitadel = "w"
    Bakery = "4"
    GeneralStore = "5"
    LittleCanadiaJewelers = "j"
    GnoMart = "n"
    Nervewreckers = "y"
    ArmoryAndLeggery = "z"
    BugbearBakery = "b"
    Market = "m"
    Meatsmith = "s"
    BartelbysBargainBookstore = "r"
    HippyProduceStand = "h"
    UnclePsAntiques = "p"


class Response(NamedTuple):
    items: List[ItemQuantity]
    meat_gained: int

class npc_buy(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        store: Store,
        item: Item,
        quantity: int = 1,
    ) -> None:
        """
        Purchases items from an NPC store.

        :param session: Active session
        :param store: NPC store to buy from
        :param item: Item to buy
        :param quantity: Quantity of said item to buy
        """
        data = {
            "phash": session.pwd,
            "whichstore": store.value,
            "buying": "Yep.",
            "howmany": quantity,
            "whichitem": item,
        }
        self.request = session.request("store.php", data=data)

    @staticmethod
    def parser(html: str, **kwargs) -> Response:
        if len(html) == 0:
            raise InvalidLocationError("You cannot visit that store yet.")

        if "You've been sent back here by some kind of bug" in html:
            raise InvalidLocationError("The store you tried to visit doesn't exist.")

        if "This store doesn't sell that item" in html or "Invalid item selected" in html:
            raise WrongKindOfItemError("This store doesn't carry that item.")

        if "You can't afford " in html:
            raise NotEnoughMeatError("You do not have enough meat to purchase the item(s).")

        items = parsing.item(html)

        if len(items) == 0:
            raise UnknownError("Unknown error. No items received.")

        meat = parsing.meat(html)

        return Response(items, meat)
