from aiohttp import ClientResponse
from typing import Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def clan_member_boot(
    session: "Session", user_id: Union[int, List[int]]
) -> ClientResponse:
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
