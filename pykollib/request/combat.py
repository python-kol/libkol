from enum import Enum
from typing import Any, Coroutine, List, Union

from aiohttp import ClientResponse

import pykollib

from ..Error import InvalidActionError
from ..Item import Item


class Action(Enum):
    Attack = "attack"
    Item = "useitem"
    Skill = "skill"
    RunAway = "runaway"
    PickPocket = "steal"


def combat(
    session: "pykollib.Session",
    action: Action,
    skill: int = None,
    item: Union[Item, List[Item]] = None,
) -> Coroutine[Any, Any, ClientResponse]:
    """
    A request used for a single round of combat. The user may attack, use an item or skill, or
    attempt to run away.

    In this constructor, action should be set to CombatRequest.ATTACK, CombatRequest.USE_ITEM,
    CombatRequest.USE_SKILL, CombatRequest.RUN_AWAY, or CombatRequest.PICK_POCKET. If a skill
    or item is to be used, the caller should also specify param to be the number of the item or
    skill the user wishes to use.
    """
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param action: The Action to carry out in this combat round
    :param skill: If the action is Action.Skill, specifies the id of the skill to use
    :param item: If the action is Action.Item, either specifies an item to use, or an array of
                 items to funksling
    """
    params = {"action": action.value}

    if action == Action.Item:
        if item is None or len(item) == 0:
            raise InvalidActionError("You must specify an item(s) to use")

        if isinstance(item, Item):
            params["whichitem"] = item.id
        else:
            params["whichitem"] = item[0].id
            if item[1]:
                params["whichitem2"] = item[1].id

    if action == Action.Skill:
        if skill is None:
            raise InvalidActionError("You must specify a skill to use")

        params["whichskill"] = skill

    return session.request("fight.php", params=params)
