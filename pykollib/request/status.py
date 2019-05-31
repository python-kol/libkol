from typing import Any, Dict
from .request import Request

import pykollib


class status(Request):
    returns_json = True

    def __init__(self, session: "pykollib.Session") -> None:
        payload = {"for": session.state.get("user_agent", "pykollib"), "what": "status"}
        self.request = session.request("api.php", json=True, data=payload)

    @staticmethod
    def parser(json: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return json
