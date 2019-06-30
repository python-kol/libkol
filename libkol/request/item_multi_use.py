from typing import Tuple
from yarl import URL
import libkol

from ..Error import NotEnoughItemsError, WrongKindOfItemError
from ..util import parsing
from .request import Request


class item_multi_use(Request[Tuple[str, parsing.ResourceGain]]):
    """
    Uses multiple items at once
    """

    def __init__(
        self, session: "libkol.Session", item: "libkol.Item", quantity: int
    ) -> None:
        super().__init__(session)

        params = {"action": "useitem", "whichitem": item.id, "quantity": quantity}
        self.request = session.request("multiuse.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Tuple[str, parsing.ResourceGain]:
        if (
            "<table><tr><td>You don't have that many of that item.</td></tr></table>"
            in content
        ):
            raise NotEnoughItemsError("You don't have that many of that item.")

        if (
            "<table><tr><td>That item isn't usable in quantity.</td></tr></table>"
            in content
        ):
            raise WrongKindOfItemError("You cannot multi-use that item.")

        from libkol import Item

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        used = await Item[int(url.query["whichitem"])]
        session.state["inventory"][used] -= int(url.query["quantity"])

        result = str(parsing.panel(content))

        # Find out what happened
        return result, await parsing.resource_gain(result)
