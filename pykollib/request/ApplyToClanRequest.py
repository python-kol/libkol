import re
from aiohttp import ClientResponse

from ..Error import CannotChangeClanError

from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

accepted = re.compile(r"clanhalltop.gif")
alreadyMember = re.compile(r"You can't apply to a clan you're already in\.")
leaderOfExisting = re.compile(
    r"You can't apply to a new clan when you're the leader of an existing clan\."
)


def parse(html: str, session: "Session", **kwargs) -> Dict[str, Any]:
    """
    Returns a dict with the following possible elements:
        success: boolean
        alreadyMember: boolean
    """

    if leaderOfExisting.match(html):
        raise CannotChangeClanError(
            "Cannot apply to another clan because you are the leader of {}".format(
                session.preferences["clanName"]
            )
        )

    acceptedMatch = accepted.match(html)
    alreadyMemberMatch = alreadyMember.match(html)

    return {
        "success": acceptedMatch or alreadyMemberMatch,
        "alreadyMember": alreadyMemberMatch,
    }


async def applyToClanRequest(session: "Session", target_id: int) -> ClientResponse:
    payload = {
        "recruiter": 1,
        "pwd": session.pwd,
        "whichclan": target_id,
        "action": "joinclan",
        "apply": "Apply+to+this+Clan",
        "confirm": "on",
    }

    return session.post("showclan.php", data=payload, parse=parse)
