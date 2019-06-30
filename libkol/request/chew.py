from yarl import URL

import libkol

from ..Error import ItemNotFoundError, UserIsSpleenedError
from ..util import parsing
from .request import Request


class chew(Request[parsing.ResourceGain]):
    """
    This request is for chewing spleenables from the inventory.

    :param session: Active session
    :param item: Consumable to chew
    """

    def __init__(self, session: "libkol.Session", item: "libkol.Item") -> None:
        super().__init__(session)

        params = {"which": 1, "whichitem": item.id}
        self.request = session.request(
            "inv_spleen.php", ajax=True, pwd=True, params=params
        )

    @staticmethod
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        if (
            "Your spleen can't handle any more toxins today. You don't want it to rupture, do you?"
            in content
        ):
            raise UserIsSpleenedError("Your spleen is too full to chew that.")

        if ">You don't have the item you're trying to use.<" in content:
            raise ItemNotFoundError("Item not in inventory.")

        from libkol import Item

        session = kwargs["session"]  # type: libkol.Session
        url = kwargs["url"]  # type: URL

        chewed = await Item[int(url.query["whichitem"])]
        session.state.inventory[chewed] -= 1

        # Check the results
        return await parsing.resource_gain(content, session=session)
