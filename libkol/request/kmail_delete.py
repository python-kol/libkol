from typing import List

import libkol

from .request import Request


class kmail_delete(Request):
    def __init__(
        self, session: "libkol.Session", message_ids: List[int], box: str = "Inbox"
    ) -> None:
        params = {"the_action": "delete", "box": box}

        for message_id in message_ids:
            params["sel{}".format(message_id)] = "1"

        self.request = session.request("messages.php", pwd=True, params=params)
