from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib


def parse(html: str, **kwargs) -> bool:
    return "Offer Accepted." in html


def trade_response_accept(session: "pykollib.Session", trade_id: int) -> Coroutine[Any, Any, ClientResponse]:
    params = {"action": "accept", "whichoffer": trade_id}

    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
