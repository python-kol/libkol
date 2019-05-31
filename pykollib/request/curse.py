from typing import Union
from yarl import URL
from .request import Request

import pykollib

from ..Error import (AlreadyCompletedError, InvalidUserError,
                     ItemNotFoundError, UnknownError, UserInHardcoreRoninError,
                     UserNotFoundError, WrongKindOfItemError)
from ..Item import Item


class curse(Request):
    def __init__(self, session: "pykollib.Session", player: Union[str, int], item: Item) -> None:
        params = {"action": "use", "whichitem": item.id, "targetplayer": player}

        self.request = session.request("curse.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, url: URL, **kwargs) -> bool:
        if len(html) < 10:
            raise WrongKindOfItemError("You can't curse with that item.")

        if "<td>You don't have that item.</td>" in html:
            raise ItemNotFoundError("You don't have that item.")

        if "<td>That player could not be found." in html:
            raise UserNotFoundError("That player could not be found.")

        item_id = int(url.query["whichitem"])

        # Time's Arrow
        if item_id == 4939:
            if "<td>You can't fire that at yourself" in html:
                raise InvalidUserError("You can't fire an arrow at yourself")

            if (
                "<td>You can't fire a time's arrow at somebody in Ronin or Hardcore.</td>"
                in html
            ):
                raise UserInHardcoreRoninError(
                    "You can't fire an arrow at a person in hardcore or ronin."
                )

            if (
                "<td>That player has already been hit with a time's arrow today.</td>"
                in html
            ):
                raise AlreadyCompletedError("That person has already been arrowed today.")

            if "It hits with a satisfying <i>thwock</i>" not in html:
                raise UnknownError("Using Time's Arrow failed")

            return True

        # Rubber Spider
        if item_id == 7698:
            if "You decide against scaring yourself with that spider." in html:
                raise InvalidUserError("You can't use a rubber spider on yourself.")

            if "That item cannot be used on a player in Ronin or Hardcore." in html:
                raise UserInHardcoreRoninError(
                    "You can't use a rubber spider on a person in hardcore or ronin."
                )

            if (
                "You run across an already hidden spider when you go to hide this spider, and decide to wait a while."
                in html
            ):
                raise AlreadyCompletedError(
                    "That person already has a rubber spider on them."
                )

            if "You carefully hide the spider where" not in html:
                raise UnknownError("Using rubber spider failed")

            return True

        return True
