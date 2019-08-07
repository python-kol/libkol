from typing import Tuple, Union
from yarl import URL

import libkol

from .choice import choice, Choice
from ..Error import NotEnoughItemsError, WrongKindOfItemError
from .request import Request
from ..util import parsing


class item_use(Request[Union[Choice, Tuple[str, parsing.ResourceGain]]]):
    """
    Uses the requested item.
    """

    def __init__(self, session: "libkol.Session", item: "libkol.Item") -> None:
        super().__init__(session)

        params = {"which": 3, "whichitem": item.id}
        self.request = session.request(
            "inv_use.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> Union[Choice, Tuple[str, parsing.ResourceGain]]:
        if "<td>You don't have the item you're trying to use.</td>" in content:
            raise NotEnoughItemsError("You do not have that item")

        if (
            "<blockquote>This item is not implemented yet.  Try again later.</blockquote>"
            in content
        ):
            raise WrongKindOfItemError("This item cannot be used")

        from libkol import Item

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        if url.path == "/choice.php":
            return await choice.parser(content, **kwargs)

        used = await Item[int(url.query["whichitem"])]
        session.state.inventory[used] -= 1

        result = str(parsing.panel(content))

        return result, await parsing.resource_gain(result)
