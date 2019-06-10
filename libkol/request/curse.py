from typing import Union

from yarl import URL

import libkol

from ..Error import (
    AlreadyCompletedError,
    InvalidUserError,
    ItemNotFoundError,
    UnknownError,
    UserInHardcoreRoninError,
    UserNotFoundError,
    WrongKindOfItemError,
)
from ..Item import Item
from .request import Request


class curse(Request[bool]):
    def __init__(
        self, session: "libkol.Session", player: Union[str, int], item: Item
    ) -> None:
        params = {"action": "use", "whichitem": item.id, "targetplayer": player}

        self.request = session.request("curse.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        url = kwargs["url"]  # type: URL

        if len(content) < 10:
            raise WrongKindOfItemError("You can't curse with that item.")

        if "<td>You don't have that item.</td>" in content:
            raise ItemNotFoundError("You don't have that item.")

        if "<td>That player could not be found." in content:
            raise UserNotFoundError("That player could not be found.")

        item_id = int(url.query["whichitem"])

        # Time's Arrow
        if item_id == 4939:
            if "<td>You can't fire that at yourself" in content:
                raise InvalidUserError("You can't fire an arrow at yourself")

            if (
                "<td>You can't fire a time's arrow at somebody in Ronin or Hardcore.</td>"
                in content
            ):
                raise UserInHardcoreRoninError(
                    "You can't fire an arrow at a person in hardcore or ronin."
                )

            if (
                "<td>That player has already been hit with a time's arrow today.</td>"
                in content
            ):
                raise AlreadyCompletedError(
                    "That person has already been arrowed today."
                )

            if "It hits with a satisfying <i>thwock</i>" not in content:
                raise UnknownError("Using Time's Arrow failed")

            return True

        # Rubber Spider
        if item_id == 7698:
            if "You decide against scaring yourself with that spider." in content:
                raise InvalidUserError("You can't use a rubber spider on yourself.")

            if "That item cannot be used on a player in Ronin or Hardcore." in content:
                raise UserInHardcoreRoninError(
                    "You can't use a rubber spider on a person in hardcore or ronin."
                )

            if (
                "You run across an already hidden spider when you go to hide this spider, and decide to wait a while."
                in content
            ):
                raise AlreadyCompletedError(
                    "That person already has a rubber spider on them."
                )

            if "You carefully hide the spider where" not in content:
                raise UnknownError("Using rubber spider failed")

            return True

        return True
