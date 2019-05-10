import re
from aiohttp import ClientResponse

from typing import Dict, Any, TYPE_CHECKING

from .. import Clan

if TYPE_CHECKING:
    from ..Session import Session

username = re.compile(
    r"<td valign=\"?center\"?>(?:<center>)?<b>([^<>]+)<\/b> \(#[0-9]+\)<br>"
)
clan = re.compile(
    r"Clan: <b><a class=nounder href=\"showclan\.php\?whichclan=([0-9]+)\">(.*?)<\/a>"
)
numAscensions = re.compile(r"Ascensions<\/a>:<\/b><\/td><td>([0-9,]+)<\/td>")
numTrophies = re.compile(r"Trophies Collected:<\/b><\/td><td>([0-9,]+)<\/td>")
numTattoos = re.compile(r"Tattoos Collected:<\/b><\/td><td>([0-9,]+)<\/td>")


def parse(html: str, session: "Session", **kwargs) -> Dict[str, Any]:
    usernameMatch = username.search(html)
    ascensionsMatch = numAscensions.search(html)
    trophiesMatch = numTrophies.search(html)
    tattoosMatch = numTattoos.search(html)

    data = {
        "username": usernameMatch.group(1),
        "numAscensions": int(ascensionsMatch.group(1)) if ascensionsMatch else 0,
        "numTrophies": int(trophiesMatch.group(1)) if trophiesMatch else 0,
        "numTattoos": int(tattoosMatch.group(1)) if tattoosMatch else 0,
    }

    clanMatch = clan.search(html)
    if clanMatch:
        data = {
            **data,
            "clanId": int(clanMatch.group(1)),
            "clanName": clanMatch.group(2),
        }
        session.clan = Clan.Clan(session, id=data["clanId"], name=data["clanName"])

    session.preferences.setall(data)

    return data


def userProfileRequest(session: "Session", playerId: str) -> ClientResponse:
    payload = {"who": playerId}
    return session.request("showplayer.php", data=payload, parse=parse)
