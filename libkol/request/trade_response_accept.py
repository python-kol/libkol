import libkol

from .request import Request


class trade_response_accept(Request[bool]):
    def __init__(self, session: "libkol.Session", trade_id: int) -> None:
        super().__init__(session)
        params = {"action": "accept", "whichoffer": trade_id}
        self.request = session.request("makeoffer.php", pwd=True, params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        return "Offer Accepted." in content
