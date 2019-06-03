import pykollib
from typing import Any, Dict, List
from dataclasses import dataclass
from unicodedata import normalize

from .request import Request
from ..Error import UnknownError

@dataclass
class Response:
    output: str
    msgs: List[str]

class chat_send(Request):
    returns_json = True

    def __init__(self, session: "pykollib.Session", text: str = ""):
        super().__init__(session)

        params = {
            "playerid": session.get_user_id(),
            "graf": normalize("NFKD", text),
            "j": 1
        }

        self.request = session.request("submitnewchat.php", pwd=True, params=params)

    @staticmethod
    async def parser(json: Dict[str, Any], **kwargs) -> Response:
        try:
            return Response(**json)
        except TypeError as e:
            raise UnknownError("Unusual response from sending chat message {}".format(e))
