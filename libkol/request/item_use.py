import libkol

from ..Item import Item
from ..Error import NotEnoughItemsError, WrongKindOfItemError
from .request import Request
from ..util import parsing


class item_use(Request[str]):
    """
    Uses the requested item.
    """

    def __init__(self, session: "libkol.Session", item: Item) -> None:
        super().__init__(session)

        params = {"which": 3, "whichitem": item.id}
        self.request = session.request(
            "inv_use.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> str:
        if "<td>You don't have the item you're trying to use.</td>" in content:
            raise NotEnoughItemsError("You do not have that item")

        if (
            "<blockquote>This item is not implemented yet.  Try again later.</blockquote>"
            in content
        ):
            raise WrongKindOfItemError("This item cannot be used")

        return str(parsing.panel(content))
