from bs4 import BeautifulSoup
from typing import List, Dict, Any
from pykollib.pattern import PatternManager

from ..Item import Item, ItemQuantity
from ..Stat import Stat


def panel(html: str, title: str = "Results:") -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all("b", text=title)
    header = next((h for h in headers), None)
    return header.parent.parent.next_sibling.td


def item(text: str) -> List[ItemQuantity]:
    itemQuantities = []

    singleItemPattern = PatternManager.getOrCompilePattern("acquireSingleItem")
    for match in singleItemPattern.finditer(text):
        item = Item.get_or_none(desc_id=int(match.group(1)))
        itemQuantities += [ItemQuantity(item, 1)]

    multiItemPattern = PatternManager.getOrCompilePattern("acquireMultipleItems")
    for match in multiItemPattern.finditer(text):
        quantity = int(match.group(2).replace(",", ""))
        item = Item.get_or_none(desc_id=int(match.group(1)))
        itemQuantities += [ItemQuantity(item, quantity)]

    return itemQuantities


def meat(text) -> int:
    meatPattern = PatternManager.getOrCompilePattern("gainMeat")
    match = meatPattern.search(text)
    if match:
        return int(match.group(1).replace(",", ""))
    meatPattern = PatternManager.getOrCompilePattern("loseMeat")
    match = meatPattern.search(text)
    if match:
        return -1 * int(match.group(1).replace(",", ""))

    return 0


def substat(text: str, stat: Stat = None) -> Dict[str, int]:
    substats = {}

    if stat in [Stat.Muscle, None]:
        muscPattern = PatternManager.getOrCompilePattern("muscleGainLoss")
        muscMatch = muscPattern.search(text)
        if muscMatch:
            muscle = int(muscMatch.group(2).replace(",", ""))
            substats["muscle"] = muscle * (1 if muscMatch.group(1) == "gain" else -1)

    if stat in [Stat.Mysticality, None]:
        mystPattern = PatternManager.getOrCompilePattern("mysticalityGainLoss")
        mystMatch = mystPattern.search(text)
        if mystMatch:
            myst = int(mystMatch.group(2).replace(",", ""))
            substats["mysticality"] = myst * (1 if mystMatch.group(1) == "gain" else -1)

    if stat in [Stat.Moxie, None]:
        moxPattern = PatternManager.getOrCompilePattern("moxieGainLoss")
        moxMatch = moxPattern.search(text)
        if moxMatch:
            moxie = int(moxMatch.group(2).replace(",", ""))
            substats["moxie"] = moxie * (1 if moxMatch.group(1) == "gain" else -1)

    return substats


def stat(text: str, stat: Stat = None) -> Dict[str, int]:
    """
    Returns a dictionary describing how many stat points the user gained or lost. Please note that
    the user interface does not say how many points were gained or lost if the number is greater
    than 1. This method will return '2' or '-2' in these situations. If your program needs a more
    exact number then you should request the user's character pane.
    """
    statPoints = {}

    if stat in [Stat.Muscle, None]:
        muscPattern = PatternManager.getOrCompilePattern("musclePointGainLoss")
        muscMatch = muscPattern.search(text)
        if muscMatch:
            modifier = 1
            if muscMatch.group(1) == "lose":
                modifier = -1
            if muscMatch.group(2) == "a":
                statPoints["muscle"] = 1 * modifier
            else:
                statPoints["muscle"] = 2 * modifier

    if stat in [Stat.Mysticality, None]:
        mystPattern = PatternManager.getOrCompilePattern("mystPointGainLoss")
        mystMatch = mystPattern.search(text)
        if mystMatch:
            modifier = 1
            if mystMatch.group(1) == "lose":
                modifier = -1
            if mystMatch.group(2) == "a":
                statPoints["mysticality"] = 1 * modifier
            else:
                statPoints["mysticality"] = 2 * modifier

    if stat in [Stat.Moxie, None]:
        moxPattern = PatternManager.getOrCompilePattern("moxiePointGainLoss")
        moxMatch = moxPattern.search(text)
        if moxMatch:
            modifier = 1
            if moxMatch.group(1) == "lose":
                modifier = -1
            if moxMatch.group(2) == "a":
                statPoints["moxie"] = 1 * modifier
            else:
                statPoints["moxie"] = 2 * modifier

    return statPoints


def level(text: str) -> int:
    """
    Returns the number of levels gained by the user during the request. Please note that the user
    interface does not say how many levels were gained if the user gained more than 1. This method
    will return 2 if more than 1 level was gained. If your application needs a more fine-grained
    response, you should check the user's character pane.
    """
    levelPattern = PatternManager.getOrCompilePattern("levelGain")
    levelMatch = levelPattern.search(text)
    if levelMatch is None:
        return 0

    return 1 if levelMatch.group(1) == "a" else 2


def hp(text: str) -> int:
    hp = 0
    hpPattern = PatternManager.getOrCompilePattern("hpGainLoss")
    # Need to do an iteration because it may happen multiple times in combat.
    for hpMatch in hpPattern.finditer(text):
        hpChange = int(hpMatch.group(2).replace(",", ""))
        hp += hpChange * (1 if hpMatch.group(1) == "gain" else -1)

    return hp


def mp(text: str) -> int:
    mp = 0
    mpPattern = PatternManager.getOrCompilePattern("mpGainLoss")
    # Need to do an iteration because it may happen multiple times in combat
    for mpMatch in mpPattern.finditer(text):
        mpChange = int(mpMatch.group(2).replace(",", ""))
        mp += mpChange * (1 if mpMatch.group(1) == "gain" else -1)

    return mp


def inebriety(text: str) -> int:
    drunkPattern = PatternManager.getOrCompilePattern("gainDrunk")
    match = drunkPattern.search(text)
    return int(match.group(1).replace(",", "")) if match else 0


def adventures(text: str) -> int:
    adventurePattern = PatternManager.getOrCompilePattern("gainAdventures")
    match = adventurePattern.search(text)
    return int(match.group(1).replace(",", "")) if match else 0


def effects(text: str) -> List[Dict[str, Any]]:
    effects = []
    effectPattern = PatternManager.getOrCompilePattern("gainEffect")
    for match in effectPattern.finditer(text):
        effects += [
            {"name": match.group(1), "turns": int(match.group(2).replace(",", ""))}
        ]

    return effects
