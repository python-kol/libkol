import pykollib
from pykollib.pattern import PatternManager

from ..Error import UnknownError
from .request import Request

success_pattern = PatternManager.getOrCompilePattern("tradeCancelledSuccessfully")


class trade_response_decline(Request):
    def __init__(self, session: "pykollib.Session", trade_id: int) -> None:
        super().__init__(session)
        params = {"action": "decline2", "whichoffer": trade_id}
        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, **kwargs) -> bool:
        if success_pattern.search(html) is False:
            raise UnknownError("Unknown error declining trade response for trade")

        return True
