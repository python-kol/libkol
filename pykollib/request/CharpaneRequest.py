import re
from aiohttp import ClientResponse

from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Session import Session

accountPwd = re.compile(r"var pwdhash = \"([0-9a-f]+)\";")
accountId = re.compile(r"var playerid = ([0-9]+);")
accountName = re.compile(r"<a [^<>]*href=\"charsheet\.php\">(?:<b>)?([^<>]+)<")
characterLevel = re.compile(r"<br>Level ([0-9]+)<br>(.*?)<table")
characterMuscle = re.compile(
    r"Muscle:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>"
)
characterMoxie = re.compile(
    r"Moxie:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>"
)
characterMysticality = re.compile(
    r"Mysticality:</td><td align=left><b>(?:<font color=blue>([0-9]+)</font>)?(?:&nbsp;)?\(?([0-9]+)\)?</b>"
)
characterHP = re.compile(
    r"onclick=\'doc\(\"hp\"\);\'[^<>]*><br><span class=[^>]+>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>"
)
characterMP = re.compile(
    r"onclick=\'doc\(\"mp\"\);\'[^<>]*><br><span class=[^>]+>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>"
)
characterMeat = re.compile(
    r"onclick=\'doc\(\"meat\"\);\'[^<>]*><br><span class=black>([0-9,]+)</span>"
)
characterAdventures = re.compile(
    r"onclick=\'doc\(\"adventures\"\);\'[^<>]*><br><span class=black>([0-9]+)</span>"
)
currentFamiliar = re.compile(
    r"href=\"familiar.php\">(?:<b>)?<font size=[0-9]+>(.*?)</a>(?:</b>)?, the  ([0-9]+)-pound (.*?)</font></td></tr></table>"
)
characterEffect = re.compile(
    r"eff\(\"[a-fA-F0-9]+\"\);\'.*?></td><td valign=center><font size=[0-9]+>(.*?) ?\(([0-9]+)\)</font><br></td>"
)
characterRonin = re.compile(r">Ronin</a>: <b>([0-9]+)</b>")
characterMindControl = re.compile(r">Mind Control</a>: <b>([0-9]{1,2})</b>")
characterDrunk = re.compile(
    r">(?:Inebriety|Temulency|Tipsiness|Drunkenness):</td><td><b>([0-9]{1,2})</b>"
)


def titleToClass(title: str) -> str:
    if title == "Astral Spirit":
        return "Astral Spirit"

    if title in [
        "Lemming Trampler",
        "Tern Slapper",
        "Puffin Intimidator",
        "Ermine Thumper",
        "Penguin Frightener",
        "Malamute Basher",
        "Narwhal Pummeler",
        "Otter Crusher",
        "Caribou Smacker",
        "Moose Harasser",
        "Reindeer Threatener",
        "Ox Wrestler",
        "Walrus Bludgeoner",
        "Whale Boxer",
        "Seal Clubber",
    ]:
        return "Seal Clubber"

    if title in [
        "Toad Coach",
        "Skink Trainer",
        "Frog Director",
        "Gecko Supervisor",
        "Newt Herder",
        "Frog Boss",
        "Iguana Driver",
        "Salamander Subduer",
        "Bullfrog Overseer",
        "Rattlesnake Chief",
        "Crocodile Lord",
        "Cobra Commander",
        "Alligator Subjugator",
        "Asp Master",
        "Turtle Tamer",
    ]:
        return "Turtle Tamer"

    if title in [
        "Dough Acolyte",
        "Yeast Scholar",
        "Noodle Neophyte",
        "Starch Savant",
        "Carbohydrate Cognoscenti",
        "Spaghetti Sage",
        "Macaroni Magician",
        "Vermicelli Enchanter",
        "Linguini Thaumaturge",
        "Ravioli Sorcerer",
        "Manicotti Magus",
        "Spaghetti Spellbinder",
        "Cannelloni Conjurer",
        "Angel-Hair Archmage",
        "Pastamancer",
    ]:
        return "Pastamancer"

    if title in [
        "Allspice Acolyte",
        "Cilantro Seer",
        "Parsley Enchanter",
        "Sage Sage",
        "Rosemary Diviner",
        "Thyme Wizard",
        "Tarragon Thaumaturge",
        "Oreganoccultist",
        "Basillusionist",
        "Coriander Conjurer",
        "Bay Leaf Brujo",
        "Sesame Soothsayer",
        "Marinara Mage",
        "Alfredo Archmage",
        "Sauceror",
    ]:
        return "Sauceror"

    if title in [
        "Funk Footpad",
        "Rhythm Rogue",
        "Chill Crook",
        "Jiggy Grifter",
        "Beat Snatcher",
        "Sample Swindler",
        "Move Buster",
        "Jam Horker",
        "Groove Filcher",
        "Vibe Robber",
        "Boogie Brigand",
        "Flow Purloiner",
        "Jive Pillager",
        "Rhymer And Stealer",
        "Disco Bandit",
    ]:
        return "Disco Bandit"

    if title in [
        "Polka Criminal",
        "Mariachi Larcenist",
        "Zydeco Rogue",
        "Chord Horker",
        "Chromatic Crook",
        "Squeezebox Scoundrel",
        "Concertina Con Artist",
        "Button Box Burglar",
        "Hurdy-Gurdy Hooligan",
        "Sub-Sub-Apprentice Accordion Thief",
        "Sub-Apprentice Accordion Thief",
        "Pseudo-Apprentice Accordion Thief",
        "Hemi-Apprentice Accordion Thief",
        "Apprentice Accordion Thief",
        "Accordion Thief",
    ]:
        return "Accordion Thief"

    return None


def parse(html: str, session: "Session", **kwargs) -> Dict[str, Any]:
    data = {
        "pwd": accountPwd.search(html).group(1),
        "userName": accountName.search(html).group(1),
        "userId": int(accountId.search(html).group(1)),
    }

    match = characterLevel.search(html)
    if match:
        title = str(match.group(2))
        data["level"] = int(match.group(1))
        data["levelTitle"] = title
        data["class"] = titleToClass(title)

    match = characterHP.search(html)
    if match:
        data["currentHP"] = int(match.group(1))
        data["maxHP"] = int(match.group(2))

    match = characterMP.search(html)
    if match:
        data["currentMP"] = int(match.group(1))
        data["maxMP"] = int(match.group(2))

    match = characterMeat.search(html)
    if match:
        data["meat"] = int(match.group(1).replace(",", ""))

    match = characterAdventures.search(html)
    if match:
        data["adventures"] = int(match.group(1))

    match = characterDrunk.search(html)
    if match:
        data["drunkenness"] = int(match.group(1))

    match = currentFamiliar.search(html)
    if match:
        data["familiar"] = {
            "name": str(match.group(1)),
            "type": str(match.group(3)),
            "weight": int(match.group(2)),
        }

    data["effects"] = []
    for match in characterEffect.finditer(html):
        data["effects"].append(
            {"name": str(match.group(1)), "turns": int(match.group(2))}
        )

    match = characterMuscle.search(html)
    if match:
        if match.group(1) and len(str(match.group(1))) > 0:
            data["buffedMuscle"] = int(match.group(1))
        data["baseMuscle"] = int(match.group(2))

    match = characterMoxie.search(html)
    if match:
        if match.group(1) and len(str(match.group(1))) > 0:
            data["buffedMoxie"] = int(match.group(1))
        data["baseMoxie"] = int(match.group(2))

    match = characterMysticality.search(html)
    if match:
        if match.group(1) and len(str(match.group(1))) > 0:
            data["buffedMysticality"] = int(match.group(1))
        data["baseMysticality"] = int(match.group(2))

    match = characterRonin.search(html)
    if match:
        data["roninLeft"] = int(match.group(1))

    match = characterMindControl.search(html)
    if match:
        data["mindControl"] = int(match.group(1))

    session.state.update(data)

    return data


def charpaneRequest(session: "Session") -> ClientResponse:
    "Requests the user's character pane."
    return session.request("charpane.php", parse=parse)
