from aiohttp import ClientResponse
from typing import Dict, Any, TYPE_CHECKING
import re

from ..Error import CannotChangeClanError

if TYPE_CHECKING:
    from ..Session import Session

acceptedPattern = re.compile(r"clanhalltop.gif")
alreadyMemberPattern = re.compile(r"You can't apply to a clan you're already in\.")
leaderOfExistingPattern = re.compile(
    r"You can't apply to a new clan when you're the leader of an existing clan\."
)


def parse(html: str, session: "Session", **kwargs) -> Dict[str, Any]:
    """
    Returns a dict with the following possible elements:
        success: boolean
        alreadyMember: boolean
    """

    if leaderOfExistingPattern.search(html):
        raise CannotChangeClanError(
            "Cannot apply to another clan because you are the leader of {}".format(
                session.preferences["clanName"]
            )
        )

    accepted = acceptedPattern.search(html) is not None
    alreadyMember = alreadyMemberPattern.search(html) is not None

    return {"success": accepted or alreadyMember, "alreadyMember": alreadyMember}


def applyToClanRequest(session: "Session", target_id: int) -> ClientResponse:
    payload = {
        "recruiter": 1,
        "pwd": session.pwd,
        "whichclan": target_id,
        "action": "joinclan",
        "apply": "Apply+to+this+Clan",
        "confirm": "on",
    }

    return session.request("showclan.php", data=payload, parse=parse)
