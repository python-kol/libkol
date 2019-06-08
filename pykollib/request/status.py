from typing import Any, Dict

import pykollib

from .request import Request


class status(Request[Dict[str, Any]]):
    returns_json = True

    def __init__(self, session: "pykollib.Session") -> None:
        """
        Fetch status from KoL API
        """
        super().__init__(session)
        payload = {"for": session.state.get("user_agent", "pykollib"), "what": "status"}
        self.request = session.request("api.php", json=True, data=payload)
