import re
from aiohttp import ClientResponse

from typing import Dict, Any, TYPE_CHECKING, Coroutine, Any

if TYPE_CHECKING:
    from ..Session import Session

from .. import Clan
from ..Error import UnknownError

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
    username_match = username.search(html)
    ascensions_match = numAscensions.search(html)
    trophies_match = numTrophies.search(html)
    tattoos_match = numTattoos.search(html)

    if username_match is None:
        raise UnknownError("Cannot match username")

    data = {
        "username": username_match.group(1),
        "num_ascensions": int(ascensions_match.group(1)) if ascensions_match else 0,
        "num_trophies": int(trophies_match.group(1)) if trophies_match else 0,
        "num_tattoos": int(tattoos_match.group(1)) if tattoos_match else 0,
    }

    session.state.update(data)

    clanMatch = clan.search(html)
    if clanMatch:
        clan_id = int(clanMatch.group(1))
        clan_name = clanMatch.group(2)
        session.clan = Clan.Clan(session, id=clan_id, name=clan_name)

    return data


def player_profile(
    session: "Session", player_id: int
) -> Coroutine[Any, Any, ClientResponse]:
    payload = {"who": player_id}
    return session.request("showplayer.php", data=payload, parse=parse)
