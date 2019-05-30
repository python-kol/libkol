from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def choice(session: "pykollib.Session", choice: int, option: int) -> Coroutine[Any, Any, ClientResponse]:
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param choice: The id of the choice
    :param option: The number option to submit
    """
    params = {"whichchoce": choice, "option": option}
    return session.request("choice.php", params=params, pwd=True)
