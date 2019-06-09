import pykollib

from .request import Request


class logout(Request):
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)
        self.request = session.request("logout.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> None:
        session = kwargs["session"]  # type: "pykollib.Session"

        session.is_connected = False
