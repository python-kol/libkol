import re
from aiohttp import ClientResponse

from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

from .. import Clan

username = re.compile(
    r"<td valign=\"?center\"?>(?:<center>)?(?:<span [^>]+>)?<b>([^<>]+)<\/b> \(#[0-9]+\)<br>"
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
        "num_ascensions": int(ascensionsMatch.group(1)) if ascensionsMatch else 0,
        "num_trophies": int(trophiesMatch.group(1)) if trophiesMatch else 0,
        "num_tattoos": int(tattoosMatch.group(1)) if tattoosMatch else 0,
    }

    session.state.update(data)

    clanMatch = clan.search(html)
    if clanMatch:
        clan_id = int(clanMatch.group(1))
        clan_name = clanMatch.group(2)
        session.clan = Clan.Clan(session, id=clan_id, name=clan_name)

    return data


def user_profile(session: "Session", playerId: str) -> ClientResponse:
    payload = {"who": playerId}
    return session.request("showplayer.php", data=payload, parse=parse)
