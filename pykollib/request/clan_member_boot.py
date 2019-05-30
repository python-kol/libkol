from typing import Any, Coroutine, List, Union

from aiohttp import ClientResponse

import pykollib


def clan_member_boot(
    session: "pykollib.Session", user_id: Union[int, List[int]]
) -> Coroutine[Any, Any, ClientResponse]:
    """
    Boot member from clan (also removes their whitelist)
    """
    params = {"action": "modify", "begin": 1}

    # Wrap user_id in array if a single was supplied
    user_ids = [user_id] if isinstance(user_id, int) else user_id

    # Move to a list of tuples so we can have duplicate keys, then build the request
    params = params.items()
    for user_id in user_ids:
        params += [("pids[]", user_id), ("boot{}".format(user_id), "on")]

    return session.request("clan_members.php", pwd=True, params=params)
