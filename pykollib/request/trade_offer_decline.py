from yarl import URL

import pykollib

from ..Error import UnknownError
from ..pattern import PatternManager
from .request import Request

success_pattern = PatternManager.getOrCompilePattern("tradeCancelledSuccessfully")


class trade_offer_decline(Request):
    def __init__(self, session: "pykollib.Session", trade_id: int) -> None:
        params = {"action": "decline", "whichoffer": trade_id}
        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    def parser(html: str, url: URL, **kwargs) -> bool:
        if success_pattern.search(html) is None:
            raise UnknownError(
                "Unknown error declining trade offer for trade {}".format(
                    url.query["whichoffer"]
                )
            )

        return True
