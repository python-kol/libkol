from yarl import URL

import libkol

from ..Error import UnknownError
from .request import Request


class trade_offer_decline(Request[bool]):
    def __init__(self, session: "libkol.Session", trade_id: int) -> None:
        params = {"action": "decline", "whichoffer": trade_id}
        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        url = kwargs["url"]  # type: URL

        if "Offer cancelled." not in content:
            raise UnknownError(
                "Unknown error declining trade offer for trade {}".format(
                    url.query["whichoffer"]
                )
            )

        return True
