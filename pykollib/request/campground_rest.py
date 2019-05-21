from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def campgroud_rest(session: "Session") -> ClientResponse:
    """
    Rests at the user's campground.
    """

    params = {"action": "rest"}
    return session.request("campground.php", params=params)
