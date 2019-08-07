import libkol

from ..Stat import Stat
from ..util import parsing
from .request import Request

gym_stat_mapping = {
    Stat.Mysticality: 1,
    Stat.Moxie: 2,
    Stat.Muscle: 3,
}


class clan_rumpus_gym(Request[parsing.ResourceGain]):
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
    async def parser(content: str, **kwargs) -> parsing.ResourceGain:
        session = kwargs["session"]  # type: libkol.Session

        return await parsing.resource_gain(content, session)
