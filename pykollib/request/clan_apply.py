from typing import NamedTuple

import pykollib

from ..Error import CannotChangeClanError
from .request import Request


class Response(NamedTuple):
    success: bool
    already_member: bool


class clan_apply(Request):
    def __init__(self, session: "pykollib.Session", clan_id: int) -> None:
        """
        Apply to a clan

        :param clan_id: id of clan
        """
        super().__init__(session)

        payload = {
            "recruiter": 1,
            "pwd": session.pwd,
            "whichclan": clan_id,
            "action": "joinclan",
            "apply": "Apply+to+this+Clan",
            "confirm": "on",
        }

        self.request = session.request("showclan.php", data=payload)

    @staticmethod
    def parser(html: str, **kwargs) -> Response:
        """
        Formats the clan application response
        """

        if (
            "You can't apply to a new clan when you're the leader of an existing clan."
            in html
        ):
            raise CannotChangeClanError(
                "Cannot apply to another clan because you are the leader of another clan"
            )

        accepted = "clanhalltop.gif" in html
        already_member = "You can't apply to a clan you're already in." in html

        return Response(accepted or already_member, already_member)
