import re
from copy import copy
from itertools import groupby
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

import libkol

from .. import types
from ..Stat import Stat


def panel(html: str, title: str = "Results:") -> Optional[Tag]:
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all("b", text=title)
    header = next((h for h in headers), None)
    return None if header is None else header.parent.parent.next_sibling.td


def get_value(soup: Tag, key: str) -> Optional[Tag]:
    for k in soup.find_all("td", align="right"):
        if k.get_text() == f"{key}:":
            return k.next_sibling
    return None


def to_float(s: str) -> float:
    return float(s.replace(",", "").strip())


def to_int(s: str) -> int:
    return int(s.replace(",", "").strip())


def wrap_elements(wrapper: Tag, elements: List[Tag]):
    w = copy(wrapper)
    elements[0].wrap(w)
    for e in elements[1:]:
        w.append(e)
    return w


def split_by_br(element: Tag, wrapper: Tag = None):
    elements = [
        g
        for g in (
            list(g) for k, g in groupby(element.children, key=lambda e: e.name != "br")
        )
        if g[0].name != "br"
    ]

    return (
        elements if wrapper is None else [wrap_elements(wrapper, e) for e in elements]
    )


single_item_pattern = re.compile(
    r"<td[^>]*><img src=\"[^\"]*\" alt=\"[^\"]*\" title=\"[^\"]*\"[^>]*descitem\(([0-9]+)\)[^>]*><\/td><td[^>]*>You acquire an item"
)
multi_item_pattern = re.compile(
    r"<td[^>]*><img src=\"[^\"]*\" alt=\"[^\"]*\" title=\"[^\"]*\"[^>]*descitem\(([0-9]+)\)[^>]*><\/td><td[^>]*>You acquire <b>([0-9,]*)"
)

gain_meat_pattern = re.compile(
    r"<td><img src=\"[^\"]*meat\.gif\"[^>]*><\/td><td[^>]*>You gain ([0-9,]*?) Meat\.<\/td>"
)
lose_meat_pattern = re.compile(r"You (?:lose|spent) ([0-9,]+) Meat")

muscle_substats = "|".join(Stat.Muscle.substats)
mysticality_substats = "|".join(Stat.Mysticality.substats)
moxie_substats = "|".join(Stat.Moxie.substats)

substat_pattern = re.compile(
    rf"You (?P<sign>gain|lose) (?P<quantity>[0-9,]+) (?:(?P<muscle>{muscle_substats})|(?P<mysticality>{mysticality_substats})|(?P<moxie>{moxie_substats}))"
)
stat_pattern = re.compile(
    r"You (?P<sign>gain|lose) (?P<amount>a|some) (?P<stat>Muscle|Mysticality|Moxie) points?"
)
level_pattern = re.compile(r"You gain (a|some) (?:L|l)evels?")
hp_pattern = re.compile(r"You (gain|lose) ([0-9,]+) hit points?")
mp_pattern = re.compile(
    r"You (gain|lose) ([0-9,]+) (?:Muscularity|Mana|Mojo) (?:P|p)oints?"
)
inebriety_pattern = re.compile(r"You gain ([0-9]+) Drunkenness")
adventures_pattern = re.compile(r"You gain ([0-9,]+) Adventures")
effect_pattern = re.compile(
    r"<td valign=center class=effect>You acquire an effect: <b>(.*?)</b><br>\(duration: ([0-9,]+) Adventures\)</td>"
)


async def item(text: str) -> List["types.ItemQuantity"]:
    from .. import Item

    item_quantities = []  # type: List[types.ItemQuantity]

    for match in single_item_pattern.finditer(text):
        item = await Item.get_or_discover(desc_id=int(match.group(1)))
        item_quantities += [types.ItemQuantity(item, 1)]

    for match in multi_item_pattern.finditer(text):
        quantity = to_int(match.group(2))
        item = await Item.get_or_discover(desc_id=int(match.group(1)))
        item_quantities += [types.ItemQuantity(item, quantity)]

    return item_quantities


def meat(text) -> int:
    match = gain_meat_pattern.search(text)
    if match:
        return to_int(match.group(1))

    match = lose_meat_pattern.search(text)
    if match:
        return -1 * to_int(match.group(1))

    return 0


def substat(text: str) -> Dict[Stat, int]:
    substats = {}

    for m in substat_pattern.finditer(text):
        g = m.groupdict()
        stat = (
            Stat.Muscle
            if g["muscle"]
            else Stat.Mysticality
            if g["mysticality"]
            else Stat.Moxie
        )
        quantity = to_int(g["quantity"])
        substats[stat] = quantity * (1 if g["sign"] == "gain" else -1)

    return substats


def stats(text: str) -> Dict[Stat, int]:
    """
    Returns a dictionary describing how many stat points the user gained or lost. Please note that
    the user interface does not say how many points were gained or lost if the number is greater
    than 1. This method will return '2' or '-2' in these situations. If your program needs a more
    exact number then you should request the user's character pane.
    """
    stats = {}

    for m in stat_pattern.finditer(text):
        g = m.groupdict()
        stat = Stat(g["stat"].lower())
        sign = 1 if g["sign"] == "gain" else -1
        quantity = 1 if g["amount"] == "a" else 2
        stats[stat] = quantity * sign

    return stats


def level(text: str) -> int:
    """
    Returns the number of levels gained by the user during the request. Please note that the user
    interface does not say how many levels were gained if the user gained more than 1. This method
    will return 2 if more than 1 level was gained. If your application needs a more fine-grained
    response, you should check the user's character pane.
    """
    m = level_pattern.search(text)
    return 0 if m is None else 1 if m.group(1) == "a" else 2


def hp(text: str) -> int:
    return sum(
        [
            to_int(m.group(2)) * (1 if m.group(1) == "gain" else -1)
            for m in hp_pattern.finditer(text)
        ]
    )


def mp(text: str) -> int:
    return sum(
        [
            to_int(m.group(2)) * (1 if m.group(1) == "gain" else -1)
            for m in mp_pattern.finditer(text)
        ]
    )


def inebriety(text: str) -> int:
    match = inebriety_pattern.search(text)
    return to_int(match.group(1)) if match else 0


def adventures(text: str) -> int:
    match = adventures_pattern.search(text)
    return to_int(match.group(1)) if match else 0


def effects(text: str) -> List[Dict[str, Any]]:
    return [
        {"name": match.group(1), "turns": to_int(match.group(2))}
        for match in effect_pattern.finditer(text)
    ]


@dataclass
class ResourceGain:
    items: List["types.ItemQuantity"]
    adventures: int
    inebriety: int
    substats: Dict[Stat, int]
    stats: Dict[Stat, int]
    levels: int
    effects: List[Dict[str, Any]]
    hp: int
    mp: int
    meat: int


async def resource_gain(
    html: str, session: Optional["libkol.Session"] = None, combat: bool = False
) -> ResourceGain:
    rg = ResourceGain(
        items=(await item(html)),
        adventures=adventures(html),
        inebriety=inebriety(html),
        substats=substat(html),
        stats=stats(html),
        levels=level(html),
        effects=effects(html),
        hp=hp(html),
        mp=mp(html),
        meat=meat(html),
    )

    if combat and "<!--WINWINWIN-->" in html:
        if "<!--FREEFREEFREE-->" not in html:
            rg.adventures -= 1

    if session:
        for iq in rg.items:
            session.state.inventory[iq.item] += iq.quantity
        session.state.adventures += rg.adventures
        session.state.inebriety += rg.inebriety

        for stat, change in rg.stats.items():
            session.state.stats[stat].base += change
            session.state.stats[stat].buffed += change

        session.state.level += rg.levels

        for effect in rg.effects:
            session.state.effects[effect["name"]] = (
                session.state.effects.get(effect["name"], 0) + effect["turns"]
            )

        session.state.meat += rg.meat

        session.state.current_hp += rg.hp
        session.state.current_mp += rg.mp

    return rg
