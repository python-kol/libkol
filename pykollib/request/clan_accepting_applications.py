import pykollib

from ..Error import UnknownError
from ..util import parsing
from .request import Request


class clan_accepting_applications(Request):
    """
    Toggle whether or not the clan accepts new applications.
    """
    def __init__(self, session: "pykollib.Session") -> None:
        super().__init__(session)

        params = {"action": "noapp"}
        self.request = session.request("clan_admin.php", params=params)

    @staticmethod
    async def parser(html: str, **kwargs) -> bool:
        results = parsing.panel(html)

        if results.string == "Applications turned on.":
            return True

        if results.string == "Applications turned off.":
            return False

        raise UnknownError("Unknown response")
