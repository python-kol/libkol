from enum import Enum
from typing import List, NamedTuple, Tuple

from yarl import URL

import pykollib

from ..Error import (
    ItemNotFoundError,
    NotEnoughAdventuresError,
    RecipeNotFoundError,
    SkillNotFoundError,
)
from ..Item import Item, ItemQuantity
from ..util import parsing
from .request import Request


class Mode(Enum):
    Cocktail = "cocktail"
    Cook = "cook"
    Combine = "combine"


class Response(NamedTuple):
    created: List[ItemQuantity]
    explosion: bool


class craft(Request):
    def __init__(
        self,
        session: "pykollib.Session",
        mode: Mode,
        ingredients: Tuple[Item, Item],
        quantity: int = 1,
        max: bool = False,
    ) -> None:
        params = {
            "action": "craft",
            "mode": mode,
            "qty": quantity,
            "a": ingredients[0].id,
            "b": ingredients[1].id,
            "max": "on" if max else "off",
        }

        self.request = session.request("craft.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, url: URL, **kwargs) -> Response:
        mode = Mode(url.query["mode"])

        if "<td>Those two items don't combine to make" in html:
            raise RecipeNotFoundError("Unable to craft. Does not match any recipe.")

        if (
            mode in [Mode.Cocktail, Mode.Cook]
            and "<td>You don't have the skill necessary to " in html
        ):
            raise SkillNotFoundError("Unable to craft. We are not skilled enough.")

        if "<td>You don't have enough of one the " in html:
            raise ItemNotFoundError("Unable to craft. You don't have all of the items.")

        if "<td>You don't have that many adventures left." in html:
            raise NotEnoughAdventuresError("Unable to craft. Not enough adventures.")

        if (
            mode is Mode.Combine
            and '<div style="text-align:left">You don\'t have any meat paste.' in html
        ):
            raise ItemNotFoundError("Unable to craft. You need sufficient meatpaste")

        explosion = "Smoke begins to pour from the head of your" in html

        return Response(parsing.item(html), explosion)
