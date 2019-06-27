from typing import Optional
from yarl import URL

import libkol

from ..Error import ItemNotFoundError, UserIsDrunkError, WrongKindOfItemError
from ..util import parsing
from .request import Request


class eat(Request[parsing.ResourceGain]):
    """
    This request is for eating food from the inventory.

    :param session: Active session
    :param item: Consumable to eat
    """

    def __init__(
        self,
        session: "libkol.Session",
        item: "libkol.Item",
        utensil: Optional["libkol.Item"] = None,
    ) -> None:
        super().__init__(session)

        params = {"which": 1, "whichitem": item.id}

        if utensil:
            params["which"] = 99
            params["utensil"] = utensil.id

        self.request = session.request(
            "inv_eat.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        if "You're way too drunk already." in content:
            raise UserIsDrunkError("You're too full to eat that.")

        if "That's not booze." in content:
            raise WrongKindOfItemError("That's not something you can eat.")

        if ">You don't have the item you're trying to use.<" in content:
            raise ItemNotFoundError("Item not in inventory.")

        from libkol import Item

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        eaten = await Item[int(url.query["whichitem"])]
        session.state.inventory[eaten] -= 1

        if url.query.get("utensil"):
            utensil = await Item[int(url.query["utensil"])]
            session.state.inventory[utensil] -= 1

        # Check the results
        return await parsing.resource_gain(content, session=session)
