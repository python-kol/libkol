from typing import Any, Dict

import libkol

from .request import Request


class status(Request[bool]):
    returns_json = True

    def __init__(self, session: "libkol.Session") -> None:
        """
        Fetch status from KoL API
        """
        super().__init__(session)
        payload = {"for": session.state.get("user_agent", "libkol"), "what": "status"}
        self.request = session.request("api.php", json=True, data=payload)

    @staticmethod
    async def parser(content: Dict[str, Any], **kwargs) -> bool:
        session = kwargs["session"]  # type: "libkol.Session"

        session.state.pwd = content["pwd"]
        session.state.username = content["name"]
        session.state.user_id = int(content["playerid"])
        session.state.rollover = int(content["rollover"])
        session.state.inebriety = int(content["drunk"])
        session.state.fullness = int(content["full"])
        session.state.spleenhit = int(content["spleen"])

        return True
