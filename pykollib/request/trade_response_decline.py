import pykollib

from ..Error import UnknownError
from .request import Request


class trade_response_decline(Request):
    def __init__(self, session: "pykollib.Session", trade_id: int) -> None:
        super().__init__(session)
        params = {"action": "decline2", "whichoffer": trade_id}
        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        if "Offer cancelled." not in content:
            raise UnknownError("Unknown error declining trade response for trade")

        return True
