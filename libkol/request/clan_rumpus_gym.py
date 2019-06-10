from typing import Dict, NamedTuple

from yarl import URL

import libkol

from ..Stat import Stat
from ..util import parsing
from .request import Request

gym_stat_mapping = {
    Stat.Mysticality: 1,
    1: Stat.Mysticality,
    Stat.Moxie: 2,
    2: Stat.Moxie,
    Stat.Muscle: 3,
    3: Stat.Muscle,
}


class Response(NamedTuple):
    substats: Dict[str, int]
    stats: Dict[str, int]
    level: int


class clan_rumpus_gym(Request[Response]):
    """
    Visits the a gym in the clan rumpus room for a specified number of turns

    :param stat: The stat to train
    :param turns: The number of turns to train for
    """

    def __init__(self, session: "libkol.Session", stat: Stat, turns: int) -> None:
        super().__init__(session)

        params = {
            "preaction": "gym",
            "whichgym": gym_stat_mapping[stat],
            "numturns": turns,
        }
        self.request = session.request("clan_rumpus.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> Response:
        url = kwargs["url"]  # type: URL

        stat = gym_stat_mapping[int(url.query["whichgym"])]
        assert isinstance(stat, Stat)

        return Response(
            substats=parsing.substat(content, stat=stat),
            stats=parsing.stat(content, stat=stat),
            level=parsing.level(content),
        )
