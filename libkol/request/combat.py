from enum import Enum
from typing import List, Optional, Union
from dataclasses import dataclass
from bs4 import BeautifulSoup
from yarl import URL
import re

import libkol

from ..Error import InvalidActionError
from ..Skill import Skill
from ..Monster import Monster
from .request import Request


@dataclass
class CombatRound:
    monster: str
    turn: int


class Action(Enum):
    Attack = "attack"
    Item = "useitem"
    Skill = "skill"
    RunAway = "runaway"
    PickPocket = "steal"


turn_pattern = re.compile("<script>var onturn = (\d+);</script>")


class combat(Request[CombatRound]):
    """
    A request used for a single round of combat. The user may attack, use an item or skill, or
    attempt to run away.

    In this constructor, action should be set to CombatRequest.ATTACK, CombatRequest.USE_ITEM,
    CombatRequest.USE_SKILL, CombatRequest.RUN_AWAY, or CombatRequest.PICK_POCKET. If a skill
    or item is to be used, the caller should also specify param to be the number of the item or
    skill the user wishes to use.

    Submit a given option in response to a give choice

    :param session: KoL session
    :param action: The Action to carry out in this combat round
    :param skill: If the action is Action.Skill, specifies the skill to use
    :param item: If the action is Action.Item, either specifies an item to use, or an array of
                 items to funksling
    """

    def __init__(
        self,
        session: "libkol.Session",
        action: Action,
        skill: Optional[Skill] = None,
        item: Union["libkol.Item", List["libkol.Item"]] = None,
    ) -> None:
        super().__init__(session)

        from libkol import Item

        params = {"action": action.value}

        if action == Action.Item:
            if item is None:
                raise InvalidActionError("You must specify at least one item to use")

            if isinstance(item, Item):
                params["whichitem"] = item.id
            else:
                if len(item) == 0:
                    raise InvalidActionError(
                        "You must specify at least one item to use"
                    )

                params["whichitem"] = item[0].id
                if item[1]:
                    params["whichitem2"] = item[1].id

        if action == Action.Skill:
            if skill is None:
                raise InvalidActionError("You must specify a skill to use")

            params["whichskill"] = skill.id

        self.request = session.request("fight.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> CombatRound:
        turn_match = turn_pattern.search(content)
        turn = int(turn_match.group(1)) if turn_match else 1

        soup = BeautifulSoup(content, "html.parser")

        img = soup.find("img", id="monpic")
        image = URL(img["src"]).parts[-1]
        monster = await Monster.identify(
            name=soup.find("span", id="monname"), image=image
        )

        return CombatRound(turn=turn, monster=monster)
