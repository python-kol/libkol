from typing import List

import libkol

from .request import Request


class kmail_delete(Request):
    def __init__(
        self, session: "libkol.Session", message_ids: List[int], box: str = "Inbox"
    ) -> None:
        super().__init__(session)
        payload = {"the_action": "delete", "box": box}

        for message_id in message_ids:
            payload["sel{}".format(message_id)] = "on"

        self.request = session.request("messages.php", pwd=True, data=payload)
