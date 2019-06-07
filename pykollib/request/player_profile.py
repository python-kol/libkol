import re
from typing import Any, Dict

import pykollib

from .. import Clan
from ..Error import UnknownError
from .request import Request

username = re.compile(
    r"<td valign=\"?center\"?>(?:<center>)?(?:<span [^>]+>)?<b>([^<>]+)<\/b> \(#[0-9]+\)<br>"
)
clan = re.compile(
    r"Clan: <b><a class=nounder href=\"showclan\.php\?whichclan=([0-9]+)\">(.*?)<\/a>"
)
numAscensions = re.compile(r"Ascensions<\/a>:<\/b><\/td><td>([0-9,]+)<\/td>")
numTrophies = re.compile(r"Trophies Collected:<\/b><\/td><td>([0-9,]+)<\/td>")
numTattoos = re.compile(r"Tattoos Collected:<\/b><\/td><td>([0-9,]+)<\/td>")


class player_profile(Request):
    def __init__(self, session: "pykollib.Session", player_id: int) -> None:
        super().__init__(session)
        payload = {"who": player_id}
        self.request = session.request("showplayer.php", data=payload)

    @staticmethod
    async def parser(html: str, url, session: "pykollib.Session", **kwargs) -> Dict[str, Any]:
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
            session.clan = Clan(session, id=clan_id, name=clan_name)

        return data
