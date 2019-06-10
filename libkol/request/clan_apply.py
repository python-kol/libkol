from typing import NamedTuple

import libkol

from ..Error import CannotChangeClanError
from .request import Request


class Response(NamedTuple):
    success: bool
    already_member: bool


class clan_apply(Request[Response]):
    """
    Apply to a clan

    :param clan_id: id of clan
    """

    def __init__(self, session: "libkol.Session", clan_id: int) -> None:
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
    async def parser(content: str, **kwargs) -> Response:
        """
        Formats the clan application response
        """

        if (
            "You can't apply to a new clan when you're the leader of an existing clan."
            in content
        ):
            raise CannotChangeClanError(
                "Cannot apply to another clan because you are the leader of another clan"
            )

        accepted = "clanhalltop.gif" in content
        already_member = "You can't apply to a clan you're already in." in content

        return Response(accepted or already_member, already_member)
