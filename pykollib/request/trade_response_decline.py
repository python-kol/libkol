from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib
from pykollib.pattern import PatternManager

from ..Error import RequestGenericError

success_pattern = PatternManager.getOrCompilePattern("tradeCancelledSuccessfully")


def parse(html: str, **kwargs) -> bool:
    if success_pattern.search(html) is False:
        raise RequestGenericError("Unknown error declining trade response for trade")

    return True


def trade_response_decline(session: "pykollib.Session", trade_id: int) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "decline2", "whichoffer": trade_id}
    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
