from typing import Any, Dict

import libkol

from .request import Request


class status(Request[Dict[str, Any]]):
    returns_json = True

    def __init__(self, session: "libkol.Session") -> None:
        """
        Fetch status from KoL API
        """
        super().__init__(session)
        payload = {"for": session.state.get("user_agent", "libkol"), "what": "status"}
        self.request = session.request("api.php", json=True, data=payload)
