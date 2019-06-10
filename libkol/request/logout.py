import libkol

from .request import Request


class logout(Request):
    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)
        self.request = session.request("logout.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> None:
        session = kwargs["session"]  # type: "libkol.Session"

        session.is_connected = False
