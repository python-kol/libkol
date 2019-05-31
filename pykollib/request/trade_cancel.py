

from .request import Request

import pykollib

from .trade_pending import Status


class trade_cancel(Request):
    def __init__(self, session: "pykollib.Session", id: int, status: Status) -> None:
        """
        Cancel a trade request.

        :param id: Identifier of the trade to be cancelled
        :param status: Status of the trade to be cancelled
        """
        super().__init__(session)

        params = {
            "whichoffer": id,
            "action": "cancel2" if status == Status.OutgoingResponse else "cancel1",
        }
        self.request = session.request("makeoffer.php", pwd=True, params=params)
