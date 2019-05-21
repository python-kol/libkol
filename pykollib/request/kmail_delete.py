from aiohttp import ClientResponse
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..Session import Session


def kmail_delete(
    session: "Session", message_ids: List[int], box: str = "Inbox"
) -> ClientResponse:
    params = {"the_action": "delete", "box": box}

    for message_id in message_ids:
        params["sel{}".format(message_id)] = "1"

    return session.request("messages.php", pwd=True, params=params)
