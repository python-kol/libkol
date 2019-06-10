import libkol

from .request import Request
from .trade_pending import Status


class trade_cancel(Request):
    """
    Cancel a trade request.

    :param id: Identifier of the trade to be cancelled
    :param status: Status of the trade to be cancelled
    """

    def __init__(self, session: "libkol.Session", id: int, status: Status) -> None:
        super().__init__(session)

        params = {
            "whichoffer": id,
            "action": "cancel2" if status == Status.OutgoingResponse else "cancel1",
        }
        self.request = session.request("makeoffer.php", pwd=True, params=params)
