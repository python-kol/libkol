from yarl import URL
from typing import Optional

import libkol

from ..Error import ItemNotFoundError, UserIsDrunkError, WrongKindOfItemError
from ..util import parsing
from .request import Request


class drink(Request[parsing.ResourceGain]):
    """
    This request is for drinking booze from the inventory.
    It accepts the current session and the ID number of the booze to be drank.
    It returns the results, including and stat gain, adventure gain,
    effect gain, or drunkenness gain.
    """

    def __init__(
        self,
        session: "libkol.Session",
        item: "libkol.Item",
        utensil: Optional["libkol.Item"],
    ) -> None:
        super().__init__(session)

        params = {"which": 1, "whichitem": item.id}

        if utensil:
            params["which"] = 99
            params["utensil"] = utensil.id

        self.request = session.request(
            "inv_booze.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        if "You're way too drunk already." in content:
            raise UserIsDrunkError("You are too drunk to drink more booze.")

        if "That's not booze." in content:
            raise WrongKindOfItemError("That item is not booze.")

        if ">You don't have the item you're trying to use.<" in content:
            raise ItemNotFoundError("Item not in inventory.")

        from libkol import Item

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        drunk = await Item[int(url.query["whichitem"])]
        session.state.inventory[drunk] -= 1

        if url.query.get("utensil"):
            utensil = await Item[int(url.query["utensil"])]
            session.state.inventory[utensil] -= 1

        # Check the results
        return await parsing.resource_gain(content, session=session)
