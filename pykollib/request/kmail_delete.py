from typing import Any, Coroutine, List

from aiohttp import ClientResponse

import pykollib


def kmail_delete(
    session: "pykollib.Session", message_ids: List[int], box: str = "Inbox"
) -> Coroutine[Any, Any, ClientResponse]:
    params = {"the_action": "delete", "box": box}

    for message_id in message_ids:
        params["sel{}".format(message_id)] = "1"

    return session.request("messages.php", pwd=True, params=params)
