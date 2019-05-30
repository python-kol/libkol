from typing import Any, Coroutine

from aiohttp import ClientResponse

import pykollib

from .trade_pending import Status


def trade_cancel(session: "pykollib.Session", id: int, status: Status) -> Coroutine[Any, Any, ClientResponse]:
    """
    Cancel a trade request.

    :param trade_id: the ID of the trade being cancelled
    :param trade_type: the type of the trade being cancelled
    """

    params = {
        "whichoffer": id,
        "action": "cancel2" if status == Status.OutgoingResponse else "cancel1",
    }
    return session.request("makeoffer.php", pwd=True, params=params)
