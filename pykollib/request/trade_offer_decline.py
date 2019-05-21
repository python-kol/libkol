from aiohttp import ClientResponse
from typing import TYPE_CHECKING
from yarl import URL

if TYPE_CHECKING:
    from ..Session import Session

from ..pattern import PatternManager
from ..Error import RequestGenericError

success_pattern = PatternManager.getOrCompilePattern("tradeCancelledSuccessfully")


def parse(html: str, url: URL, **kwargs) -> bool:
    if success_pattern.search(html) is None:
        raise RequestGenericError(
            "Unknown error declining trade offer for trade {}".format(
                url.query["whichoffer"]
            )
        )

    return True


def trade_offer_decline(session: "Session", trade_id: int) -> ClientResponse:
    params = {"action": "decline", "whichoffer": trade_id}
    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
