from typing import Any, Coroutine

from aiohttp import ClientResponse
from yarl import URL

import pykollib

from ..Error import RequestGenericError
from ..pattern import PatternManager

success_pattern = PatternManager.getOrCompilePattern("tradeCancelledSuccessfully")


def parse(html: str, url: URL, **kwargs) -> bool:
    if success_pattern.search(html) is None:
        raise RequestGenericError(
            "Unknown error declining trade offer for trade {}".format(
                url.query["whichoffer"]
            )
        )

    return True


def trade_offer_decline(session: "pykollib.Session", trade_id: int) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "decline", "whichoffer": trade_id}
    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
