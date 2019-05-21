from aiohttp import ClientResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from .GetPendingTradesRequest import TradeType


def trade_cancel(
    session: "Session", trade_id: int, trade_type: TradeType
) -> ClientResponse:
    """
    Cancel a trade request.

    :param trade_id: the ID of the trade being cancelled
    :param trade_type: the type of the trade being cancelled
    """

    params = {
        "whichoffer": trade_id,
        "action": "cancel2" if trade_type == TradeType.OutgoingResponse else "cancel1",
    }
    return session.request("makeoffer.php", pwd=True, params=params)
