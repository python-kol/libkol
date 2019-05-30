from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def campground_rest(session: "pykollib.Session") -> Coroutine[Any, Any, ClientResponse]:
    """
    Rests at the user's campground.
    """

    params = {"action": "rest"}
    return session.request("campground.php", params=params)
