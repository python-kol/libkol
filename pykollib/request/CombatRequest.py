from aiohttp import ClientResponse
from typing import Union, List, TYPE_CHECKING
from enum import Enum

from ..Error import InvalidActionError

if TYPE_CHECKING:
    from ..Session import Session


class Action(Enum):
    Attack = "attack"
    Item = "useitem"
    Skill = "skill"
    RunAway = "runaway"
    PickPocket = "steal"


def combatRequest(
    session: "Session",
    action: Action,
    skill: int = None,
    item: Union[int, List[int]] = None,
) -> ClientResponse:
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
    :param skill: If the Action is Skill, specifies the id of the skill to use
    :param item: If the Action is Item, either specifies the id of the item to use, or an array of
                 the items to funksling
    """
    params = {"action": action}

    if action == Action.Item:
        if isinstance(item, int):
            params["whichitem"] = item
        elif len(item) > 0:
            params["whichitem"] = item[0]
            if item[1]:
                params["whichitem2"] = item[1]
        else:
            raise InvalidActionError("You must specify an item(s) to use")

    if action == Action.Skill:
        if skill is None:
            raise InvalidActionError("You must specify a skill to use")

        params["whichskill"] = skill

    return session.request("fight.php", params=params)
