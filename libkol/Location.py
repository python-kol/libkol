from typing import Any, Callable, Dict, Union, List, Optional

import libkol

from libkol import request
from .request.combat import CombatAction, CombatRound
from .request.choice import Choice, Option


class Combat:
    def __init__(self, session):
        self.session = session

    async def attack(self):
        return await request.combat(self.session, CombatAction.Attack).parse()

    async def item(self, items=Union["libkol.Item", List["libkol.Item"]]):
        return await request.combat(self.session, CombatAction.Item, item=items).parse()

    async def skill(self, skill: "libkol.Skill"):
        return await request.combat(
            self.session, CombatAction.Skill, skill=skill
        ).parse()


class Location:
    """
    This class represents a Location
    """

    def __init__(self, session, id):
        self.session = session
        self.id = id

    async def visit(
        self,
        combat_function: Callable[[Combat, CombatRound], Any],
        choices: Union[Dict[int, int], Callable[[Choice], Union[Option, int]]] = {},
    ):
        adventure = await request.adventure(self.session, self.id).parse()

        while adventure is not None:
            if isinstance(adventure, CombatRound) and combat_function is not None:
                combat = Combat(self.session)
                combat_result = await combat_function(combat, adventure)

                if combat_result.finished:
                    return combat_result
            elif isinstance(adventure, Choice):
                if isinstance(choices, dict):
                    option = choices.get(adventure.id)
                elif callable(choices):
                    o = choices(adventure)
                    if isinstance(o, Option):
                        option = o.id
                    else:
                        option = o

                if option is None:
                    return None

                return await request.choice(self.session, adventure.id, option).parse()
