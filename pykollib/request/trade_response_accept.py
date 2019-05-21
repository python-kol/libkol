from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session


def parse(html: str, **kwargs) -> bool:
    return "Offer Accepted." in html


def trade_response_accept(session: "Session", trade_id: int) -> ClientResponse:
    params = {"action": "accept", "whichoffer": trade_id}

    return session.request("makeoffer.php", pwd=True, params=params, parse=parse)
