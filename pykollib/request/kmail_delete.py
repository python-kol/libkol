from typing import List

from .request import Request

import pykollib


class kmail_delete(Request):
    def __init__(self, session: "pykollib.Session", message_ids: List[int], box: str = "Inbox") -> None:
        params = {"the_action": "delete", "box": box}

        for message_id in message_ids:
            params["sel{}".format(message_id)] = "1"

        self.request = session.request("messages.php", pwd=True, params=params)
