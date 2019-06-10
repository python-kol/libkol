import libkol

from ..Error import UnknownError
from ..util import parsing
from .request import Request


class clan_accepting_applications(Request[bool]):
    """
    Toggle whether or not the clan accepts new applications.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        params = {"action": "noapp"}
        self.request = session.request("clan_admin.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> bool:
        results = parsing.panel(content)

        if results.string == "Applications turned on.":
            return True

        if results.string == "Applications turned off.":
            return False

        raise UnknownError("Unknown response")
