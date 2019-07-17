from enum import Enum
from typing import List, Optional, Union
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag, NavigableString
from yarl import URL
import re

import libkol

from ..util import parsing
from ..Error import InvalidActionError
from ..Skill import Skill
from ..Monster import Monster
from .request import Request


@dataclass
class CombatEvent:
    log: str
    damage: int


@dataclass
class CombatRound:
    monster: str
    turn: int
    events: List[CombatEvent]
    resource_gain: parsing.ResourceGain
    damage: int
    finished: bool
    choice_follows: bool
    fight_follows: bool


class CombatAction(Enum):
    Attack = "attack"
    Item = "useitem"
    Skill = "skill"
    RunAway = "runaway"
    PickPocket = "steal"


turn_pattern = re.compile(r"<script>\s*var onturn = (\d+);\s*</script>")
physical_damage_pattern = re.compile(
    r"(?P<prefix>your blood, to the tune of|stabs you for|sown|You lose|You gain|strain your neck|approximately|roughly)?\s*"
    r"#?(?P<damage>\d[\d,]*) (?P<bonus>\([^.]*\) |)(?P<suffix>(?:[^\s]+ ){0,3})"
    r"(?:\"?damage|points?|bullets|hollow|notch(?:es)?|to your opponent|to the foul demon|force damage|tiny holes|like this, it's bound|from the power)"
)
elemental_damage_pattern = re.compile(
    r"(?P<prefix>sown)? \+?(?P<damage>[\d,]+) (?P<bonus>\([^.]*\) |)"
    r"(?:months worth of concentrated palm sweat|(?:slimy, (?:clammy|gross) |hotsy-totsy |)damage|points|HP worth)"
)
bonus_damage_pattern = re.compile(r"\+(?P<damage>[\d,]+)")


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
    :param action: The CombatAction to carry out in this combat round
    :param skill: If the action is CombatAction.Skill, specifies the skill to use
    :param item: If the action is CombatAction.Item, either specifies an item to use, or an array of
                 items to funksling
    """

    def __init__(
        self,
        session: "libkol.Session",
        action: CombatAction,
        skill: Optional[Skill] = None,
        item: Union["libkol.Item", List["libkol.Item"]] = None,
    ) -> None:
        super().__init__(session)

        from libkol import Item

        params = {"action": action.value}

        if action == CombatAction.Item:
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

        if action == CombatAction.Skill:
            if skill is None:
                raise InvalidActionError("You must specify a skill to use")

            params["whichskill"] = skill.id

        self.request = session.request("fight.php", params=params)

    @staticmethod
    def parse_damage(log: str) -> int:
        """
        Parse damage dealt from a combat log string

        This is entirely modeled on FightRequest.java from KoLmafia
        """
        m = None

        physical_match = physical_damage_pattern.search(log)
        if physical_match:
            m = physical_match.groupdict()
            # Remove some false positives (due to number scroll or poorly named familiars)
            if m["suffix"] in ["shambles up ", "scroll "]:
                return 0
        else:
            elemental_match = elemental_damage_pattern.search(log)
            if elemental_match:
                m = elemental_match.groupdict()

        if m is None:
            return 0

        # Exclude damage done to player
        if m["prefix"] is not None:
            return 0

        return parsing.to_int(m["damage"]) + sum(
            [
                parsing.to_int(b.group("damage"))
                for b in bonus_damage_pattern.finditer(m["bonus"])
            ]
        )

    @classmethod
    def parse_event(cls, line: Tag) -> CombatEvent:
        log = line.get_text()
        return CombatEvent(log=log, damage=cls.parse_damage(log))

    @classmethod
    async def parser(cls, content: str, **kwargs) -> CombatRound:
        turn_match = turn_pattern.search(content)
        turn = int(turn_match.group(1)) if turn_match else 0

        resource_gain = await parsing.resource_gain(content)

        panel = parsing.panel(content, "Combat!")

        # Remove action interface, just intercase
        actions = panel.find("a", attrs={"name": "end"}).parent.extract()

        # Intro
        intro = panel.find("blockquote")
        if intro:
            intro.extract()

        # Monster Info
        monster_info = panel.table.table

        img = monster_info.find("img", id="monpic")
        image = URL(img["src"]).parts[-1]

        monster = await Monster.identify(
            name=monster_info.find("span", id="monname"), image=image
        )

        # Events
        events = [
            cls.parse_event(e)
            for e in panel.find_all("p")
            if isinstance(e.contents[0], NavigableString)
        ]

        damage = sum(e.damage for e in events)

        finished = "<!--WINWINWIN-->" in content or "action=fight.php" not in content
        choice_follows = finished and 'href="choice.php' in content
        fight_follows = finished and 'href="fight.php' in content

        return CombatRound(
            turn=turn,
            monster=monster,
            events=events,
            damage=damage,
            resource_gain=resource_gain,
            finished=finished,
            choice_follows=choice_follows,
            fight_follows=fight_follows,
        )
