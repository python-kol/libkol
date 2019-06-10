from typing import List, Union

from multidict import MultiDict

import libkol

from .request import Request


class clan_member_boot(Request):
    """
    Boot member from clan (also removes their whitelist)
    """

    def __init__(
        self, session: "libkol.Session", user_id: Union[int, List[int]]
    ) -> None:
        super().__init__(session)

        params = {"action": "modify", "begin": 1}

        # Wrap user_id in array if a single was supplied
        user_ids = [user_id] if isinstance(user_id, int) else user_id

        # Move to a list of tuples so we can have duplicate keys, then build the request
        multidict = MultiDict(params.items())
        for user_id in user_ids:
            multidict.add("pids[]", user_id)
            multidict.add("boot{}".format(user_id), "on")

        self.request = session.request("clan_members.php", pwd=True, params=multidict)
