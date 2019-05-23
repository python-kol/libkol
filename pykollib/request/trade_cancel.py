from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from .trade_pending import Status


def trade_cancel(session: "Session", id: int, status: Status) -> ClientResponse:
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
