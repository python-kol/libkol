from enum import Enum
from typing import List, NamedTuple, Tuple

from yarl import URL

import libkol

from ..Error import (
    ItemNotFoundError,
    NotEnoughAdventuresError,
    RecipeNotFoundError,
    SkillNotFoundError,
)
from ..types import ItemQuantity
from ..Item import Item
from ..util import parsing
from .request import Request


class Mode(Enum):
    Cocktail = "cocktail"
    Cook = "cook"
    Combine = "combine"


class Response(NamedTuple):
    created: List[ItemQuantity]
    explosion: bool


class craft(Request[Response]):
    def __init__(
        self,
        session: "libkol.Session",
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
    async def parser(content: str, **kwargs) -> Response:
        url = kwargs["url"]  # type: URL
        mode = Mode(url.query["mode"])

        if "<td>Those two items don't combine to make" in content:
            raise RecipeNotFoundError("Unable to craft. Does not match any recipe.")

        if (
            mode in [Mode.Cocktail, Mode.Cook]
            and "<td>You don't have the skill necessary to " in content
        ):
            raise SkillNotFoundError("Unable to craft. We are not skilled enough.")

        if "<td>You don't have enough of one the " in content:
            raise ItemNotFoundError("Unable to craft. You don't have all of the items.")

        if "<td>You don't have that many adventures left." in content:
            raise NotEnoughAdventuresError("Unable to craft. Not enough adventures.")

        if (
            mode is Mode.Combine
            and '<div style="text-align:left">You don\'t have any meat paste.'
            in content
        ):
            raise ItemNotFoundError("Unable to craft. You need sufficient meatpaste")

        explosion = "Smoke begins to pour from the head of your" in content

        return Response(await parsing.item(content), explosion)
