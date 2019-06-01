import pykollib

from .request import Request


class logout(Request):
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)
        self.request = session.request("logout.php")

    @staticmethod
    def parser(html: str, url, session: "pykollib.Session", **kwargs) -> None:
        session.is_connected = False
