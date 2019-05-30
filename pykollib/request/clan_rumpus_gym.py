from typing import Any, Coroutine, NamedTuple, Dict

from aiohttp import ClientResponse
from yarl import URL

import pykollib

from ..Stat import Stat
from ..util import parsing

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


def parse(url: URL, html: str, **kwargs) -> Response:
    stat = gym_stat_mapping[int(url.query["whichgym"])]
    assert isinstance(stat, Stat)

    return Response(
        substats=parsing.substat(html, stat=stat),
        stats=parsing.stat(html, stat=stat),
        level=parsing.level(html),
    )


def clan_rumpus_gym(session: "pykollib.Session", stat: Stat, turns: int) -> Coroutine[Any, Any, ClientResponse]:
    """
    Visits the a gym in the clan rumpus room for a specified number of turns

    :param stat: The stat to train
    :param turns: The number of turns to train for
    """

    params = {"preaction": "gym", "whichgym": gym_stat_mapping[stat], "numturns": turns}
    return session.request("clan_rumpus.php", params=params, parse=parse)
