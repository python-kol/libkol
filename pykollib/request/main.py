import pykollib

from .request import Request


class main(Request):
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)
        self.request = session.request("main.php")
