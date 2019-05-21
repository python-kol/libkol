from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def choice(session: "Session", choice: int, option: int) -> ClientResponse:
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param choice: The id of the choice
    :param option: The number option to submit
    """
    params = {"whichchoce": choice, "option": option}
    return session.request("choice.php", params=params, pwd=True)
