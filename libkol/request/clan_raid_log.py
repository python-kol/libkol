import re
from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import date
from bs4 import BeautifulSoup, Tag
from yarl import URL
from dataclasses import dataclass
import libkol

from ..Error import UnknownError
from ..util import parsing
from .request import Request

previous_run_pattern = re.compile(r"^(.+?) run, ([A-Za-z]+) ([0-9]{2}), ([0-9]{4})$")
user_p = r"(?P<username>.*?) \(#(?P<user_id>[0-9]+)\)"
turns_p = r"\((?P<turns>[0-9]+) turns?\)"
raid_log_pattern = re.compile(r"^{} +(?P<event>.*)$".format(user_p))


class RaidAction(Enum):
    Defeat = "Defeat"
    Distribute = "Distribute"
    DreadBanishElement = "DreadBanishElement"
    DreadBanishType = "DreadBanishType"
    DreadBloodKiwitini = "DreadBloodKiwitini"
    DreadBoneFlour = "DreadBoneFlour"
    DreadBuffCold = "DreadBuffCold"
    DreadBuffDefence = "DreadBuffDefence"
    DreadBuffHot = "DreadBuffHot"
    DreadBuffHP = "DreadBuffHP"
    DreadBuffMP = "DreadBuffMP"
    DreadBuffSleaze = "DreadBuffSleaze"
    DreadBuffSpooky = "DreadBuffSpooky"
    DreadBuffStench = "DreadBuffStench"
    DreadCarriageman = "DreadCarriageman"
    DreadClockworkBird = "DreadClockworkBird"
    DreadComplicatedKey = "DreadComplicatedKey"
    DreadCoolIronItem = "DreadCoolIronItem"
    DreadFreddy = "DreadFreddy"
    DreadGhostShawl = "DreadGhostShawl"
    DreadGotItem = "DreadGotItem"
    DreadHangee = "DreadHangee"
    DreadHanger = "DreadHanger"
    DreadKiwiKnock = "DreadKiwiKnock"
    DreadKiwiWaste = "DreadKiwiWaste"
    DreadLockImpression = "DreadLockImpression"
    DreadMachineFix = "DreadMachineFix"
    DreadMachineUse = "DreadMachineUse"
    DreadMoonAmber = "DreadMoonAmber"
    DreadMoonAmberNecklace = "DreadMoonAmberNecklace"
    DreadMP = "DreadMP"
    DreadPencil = "DreadPencil"
    DreadShepherdsPie = "DreadShepherdsPie"
    DreadStatAll = "DreadStatAll"
    DreadStatMoxieForest = "DreadStatMoxieForest"
    DreadStatMoxieVillage = "DreadStatMoxieVillage"
    DreadStatMuscleForest = "DreadStatMuscleForest"
    DreadStatMuscleCastle = "DreadStatMuscleCastle"
    DreadStatMuscleVillage = "DreadStatMuscleVillage"
    DreadStatMysticalityForest = "DreadStatMysticalityForest"
    DreadStatMysticalityCastle = "DreadStatMysticalityCastle"
    DreadStatMysticalityVillage = "DreadStatMysticalityVillage"
    DreadTwirl = "DreadTwirl"
    DreadUnlock = "DreadUnlock"
    HoboColdFreezer = "HoboColdFreezer"
    HoboColdMeat = "HoboColdMeat"
    HoboColdPipeBreak = "HoboColdPipeBreak"
    HoboColdPipeTurnFirst = "HoboColdPipeTurnFirst"
    HoboColdPipeTurnSecond = "HoboColdPipeTurnSecond"
    HoboColdYodel = "HoboColdYodel"
    HoboHotDoor = "HoboHotDoor"
    HoboHotMeat = "HoboHotMeat"
    HoboHotPipeTurn = "HoboHotPipeTurn"
    HoboHotTireBuild = "HoboHotTireBuild"
    HoboHotTireCollapse = "HoboHotTireCollapse"
    HoboRichard = "HoboRichard"
    HoboSewerCageFree = "HoboSewerCageFree"
    HoboSewerCageGnaw = "HoboSewerCageGnaw"
    HoboSewerCageStare = "HoboSewerCageStare"
    HoboSewerClear = "HoboSewerClear"
    HoboSewerExplore = "HoboSewerExplore"
    HoboSewerGrates = "HoboSewerGrates"
    HoboSewerWaterLevel = "HoboSewerWaterLevel"
    HoboSleazeBamboozle = "HoboSleazeBamboozle"
    HoboSleazeBarfight = "HoboSleazeBarfight"
    HoboSleazeFlimflam = "HoboSleazeFlimflam"
    HoboSleazeMeat = "HoboSleazeMeat"
    HoboSleazePickNose = "HoboSleazePickNose"
    HoboSleazyTrash = "HoboSleazyTrash"
    HoboSpookyDanceFailure = "HoboSpookyDanceFailure"
    HoboSpookyDanceSuccess = "HoboSpookyDanceSuccess"
    HoboSpookyFlowers = "HoboSpookyFlowers"
    HoboSpookyMeat = "HoboSpookyMeat"
    HoboSpookyWatch = "HoboSpookyWatch"
    HoboSquareBusk = "HoboSquareBusk"
    HoboSquareLeave = "HoboSquareLeave"
    HoboSquareMarketBooze = "HoboSquareMarketBooze"
    HoboSquareMarketFood = "HoboSquareMarketFood"
    HoboSquareMarketShop = "HoboSquareMarketShop"
    HoboSquareMosh = "HoboSquareMosh"
    HoboSquarePerform = "HoboSquarePerform"
    HoboStenchCompost = "HoboStenchCompost"
    HoboStenchEruption = "HoboStenchEruption"
    HoboStenchTreasure = "HoboStenchTreasure"
    SlimeSqueeze = "SlimeSqueeze"
    SlimeTickle = "SlimeTickle"
    SororityBoombox = "SororityBoombox"
    SororityCostume = "SororityCostume"
    SororityDownWindows = "SororityDownWindows"
    SororityFogMachine = "SororityFogMachine"
    SororityItemGhost = "SororityItemGhost"
    SororityItemSkeleton = "SororityItemSkeleton"
    SororityItemWerewolf = "SororityItemWerewolf"
    SororityItemZombie = "SororityItemZombie"
    SororityKillGhosts = "SororityKillGhosts"
    SororityKillGuides = "SororityKillGuides"
    SororityKillSkeletons = "SororityKillSkeletons"
    SororityKillVampires = "SororityKillVampires"
    SororityKillWerewolves = "SororityKillWerewolves"
    SororityKillZombies = "SororityKillZombies"
    Unknown = "Unknown"
    Victory = "Victory"


@dataclass
class Event:
    user_id: int
    username: str
    action: RaidAction
    data: Dict[str, str]


@dataclass
class Raid:
    id: int
    name: str
    start: Optional[date]
    end: Optional[date]
    summary: List[str]
    events: Optional[List[Tuple[str, List[Event]]]]


class clan_raid_log(Request[Raid]):
    """
    Retrieves on a previous raid.
    """

    def __init__(self, session: "libkol.Session", raid_id: int) -> None:
        super().__init__(session)

        params = {"viewlog": raid_id}

        self.request = session.request("clan_viewraidlog.php", params=params)

    @staticmethod
    def center_with_no_link(tag):
        return tag.name == "center" and tag.a is None

    log_patterns = {
        re.compile(
            r"^got the carriageman ([0-9]+) sheet\(s\) drunker$"
        ): RaidAction.DreadCarriageman,
        re.compile(
            r"^used The Machine, assisted by (?P<left_chamber>.*?) and (?P<right_chamber>.*?)$"
        ): RaidAction.DreadMachineUse,
        # There are different standards for showing an individual monster victory/defeat
        # Luckily they are either double space or use the indefinite article
        re.compile(
            r"^was defeated by +(?:a )?(?P<monster>.*?) \((?P<turns>1) turn\)$"
        ): RaidAction.Defeat,
        re.compile(
            r"^was defeated by +(?:a )?(?P<monster>.*?) x [0-9,]+ {}$".format(turns_p)
        ): RaidAction.Defeat,
        re.compile(
            r"^defeated +(?:a )?(?P<monster>.*?) \((?P<turns>1) turn\)$"
        ): RaidAction.Victory,
        re.compile(
            r"^defeated +(?:a )?(?P<monster>.*?) x [0-9,]+ {}$".format(turns_p)
        ): RaidAction.Victory,
        re.compile(
            r"^unlocked the (?P<location>.*?) \(1 turn\)"
        ): RaidAction.DreadUnlock,
        re.compile(r"^fixed The Machine"): RaidAction.DreadMachineFix,
        re.compile(r"^raided a (?P<location>dresser)"): RaidAction.DreadFreddy,
        re.compile(
            r"^drove some (?P<type>.*?) out of the (?P<location>.*?) \(1 turn\)"
        ): RaidAction.DreadBanishType,
        re.compile(r"^sifted through some (?P<location>ashes)"): RaidAction.DreadFreddy,
        re.compile(
            r"^(acquired|got) (some|a) (?P<item>.*?) \(1 turn\)"
        ): RaidAction.DreadGotItem,
        re.compile(r"^made a shepherd's pie"): RaidAction.DreadShepherdsPie,
        re.compile(
            r"^looted the blacksmith's (?P<location>till)"
        ): RaidAction.DreadFreddy,
        re.compile(r"^looted the tinker's (?P<location>shack)"): RaidAction.DreadFreddy,
        re.compile(r"^robbed some (?P<location>graves)"): RaidAction.DreadFreddy,
        re.compile(
            r"^made the (?P<location>.*?) less (?P<element>.*?) \(1 turn\)$"
        ): RaidAction.DreadBanishElement,
        re.compile(r"^recycled some (?P<location>newspapers)"): RaidAction.DreadFreddy,
        re.compile(
            r"^found and sold a rare (?P<location>baseball card)"
        ): RaidAction.DreadFreddy,
        re.compile(
            r"^made an impression of a complicated lock"
        ): RaidAction.DreadLockImpression,
        re.compile(r"^lowered the water level"): RaidAction.HoboSewerWaterLevel,
        re.compile(
            r"^gnawed through (?:[0-9]+|a) C. H. U. M. cages? {}$".format(turns_p)
        ): RaidAction.HoboSewerCageGnaw,
        re.compile(
            r"^made it through the sewer \((?P<turns>[0-9]+) turns?\)$"
        ): RaidAction.HoboSewerClear,
        re.compile(
            r"^explored (a|[0-9]+) dark sewer tunnels? {}$".format(turns_p)
        ): RaidAction.HoboSewerExplore,
        re.compile(
            r"^went shopping in the Marketplace {}$".format(turns_p)
        ): RaidAction.HoboSquareMarketShop,
        re.compile(
            r"^squeezed a Slime gall bladder \(1 turn\)"
        ): RaidAction.SlimeSqueeze,
        re.compile(
            r"^distributed (?P<item>.*?) to {}$".format(user_p)
        ): RaidAction.Distribute,
        re.compile(
            r"^rifled through a (?P<location>footlocker)"
        ): RaidAction.DreadFreddy,
        re.compile(r"^made some bone flour"): RaidAction.DreadBoneFlour,
        re.compile(r"^knocked some fruit loose"): RaidAction.DreadKiwiKnock,
        re.compile(r"^made a complicated key"): RaidAction.DreadComplicatedKey,
        re.compile(r"^collected a ghost pencil \(1 turn\)"): RaidAction.DreadPencil,
        re.compile(r"^made a ghost shawl"): RaidAction.DreadGhostShawl,
        re.compile(r"^made a blood kiwitini"): RaidAction.DreadBloodKiwitini,
        re.compile(r"^twirled on the dance floor \(1 turn\)$"): RaidAction.DreadTwirl,
        re.compile(r"^frolicked in a freezer \(1 turn\)$"): RaidAction.DreadBuffCold,
        re.compile(r"^polished some moon-amber \(1 turn\)$"): RaidAction.DreadMoonAmber,
        re.compile(r"^read an old diary \(1 turn\)$"): RaidAction.DreadBuffSpooky,
        re.compile(
            r"^got intimate with some hot coals \(1 turn\)$"
        ): RaidAction.DreadBuffHot,
        re.compile(
            r"^learned to make a moon-amber necklace \(1 turn\)$"
        ): RaidAction.DreadMoonAmberNecklace,
        re.compile(r"^got magically fingered \(1 turn\)$"): RaidAction.DreadBuffMP,
        re.compile(
            r"^made (a|some) cool iron (?P<item>.*?) \(1 turn\)$"
        ): RaidAction.DreadCoolIronItem,
        re.compile(
            r"^read some lurid epitaphs \(1 turn\)$"
        ): RaidAction.DreadBuffSleaze,
        re.compile(r"^was hung by a clanmate \(1 turn\)$"): RaidAction.DreadHangee,
        re.compile(r"^hung a clanmate \(1 turn\)$"): RaidAction.DreadHanger,
        re.compile(
            r"^lifted some weights \(1 turn\)$"
        ): RaidAction.DreadStatMuscleForest,
        re.compile(
            r"^rolled around in some mushrooms \(1 turn\)$"
        ): RaidAction.DreadBuffDefence,
        re.compile(
            r"^drank some nutritious forest goo \(1 turn\)$"
        ): RaidAction.DreadBuffHP,
        re.compile(r"^made a clockwork bird"): RaidAction.DreadClockworkBird,
        re.compile(
            r"^stared at (?:an|[0-9]+) empty cages? for (?:a|[0-9]+) whiles? {}$".format(
                turns_p
            )
        ): RaidAction.HoboSewerCageStare,
        re.compile(
            r"^rescued (?P<other_user>.*?) from a C. H. U. M. cage {}$".format(turns_p)
        ): RaidAction.HoboSewerCageFree,
        re.compile(
            r"^opened (?:a|[0-9]+) sewer grates? {}$".format(turns_p)
        ): RaidAction.HoboSewerGrates,
        re.compile(
            r"^helped Richard make (?:a|[0-9,]+) (?P<item>protein shake|grenade|bandage)s? {}$".format(
                turns_p
            )
        ): RaidAction.HoboRichard,
        re.compile(
            r"^threw (a|[0-9]+) tires? on the fire {}$".format(turns_p)
        ): RaidAction.HoboHotTireBuild,
        re.compile(
            r"^started (?:a|[0-9]+) tirevalanches? {}$".format(turns_p)
        ): RaidAction.HoboHotTireCollapse,
        re.compile(
            r"^got burned by (?:a|[0-9]+) hot doors? {}$".format(turns_p)
        ): RaidAction.HoboHotDoor,
        re.compile(
            r"^raided (a|[0-9]+) freezers? {}$".format(turns_p)
        ): RaidAction.HoboColdFreezer,
        re.compile(
            r"^yodeled (?P<amount>a little bit|quite a bit|like crazy) {}$".format(
                turns_p
            )
        ): RaidAction.HoboColdYodel,
        re.compile(
            r"^busted (a|[0-9]+) moves? {}$".format(turns_p)
        ): RaidAction.HoboSpookyDanceSuccess,
        re.compile(
            r"^watched some zombie hobos dance {}$".format(turns_p)
        ): RaidAction.HoboSpookyWatch,
        re.compile(
            r"^bamboozled some hobos {}$".format(turns_p)
        ): RaidAction.HoboSleazeBamboozle,
        re.compile(
            r"^flimflammed some hobos {}$".format(turns_p)
        ): RaidAction.HoboSleazeFlimflam,
        re.compile(
            r"^danced like a superstar {}$".format(turns_p)
        ): RaidAction.HoboSleazePickNose,
        re.compile(
            r"^started (a|[0-9]+) barfights? {}$".format(turns_p)
        ): RaidAction.HoboSleazeBarfight,
        re.compile(
            r"^started (a|[0-9]+) trashcano eruptions? {}$".format(turns_p)
        ): RaidAction.HoboStenchEruption,
        re.compile(
            r"^searched for buried treasure {}$".format(turns_p)
        ): RaidAction.HoboStenchTreasure,
        re.compile(r"^swam in a sewer \(1 turn\)$"): RaidAction.DreadBuffStench,
        re.compile(
            r"^listened to the forest's heart \(1 turn\)$"
        ): RaidAction.DreadStatMysticalityForest,
        re.compile(r"^relaxed in a furnace \(1 turn\)$"): RaidAction.DreadStatAll,
        re.compile(r"^tickled a Slime uvula \(1 turn\)$"): RaidAction.SlimeTickle,
        re.compile(
            r"^did a whole bunch of pushups \(1 turn\)$"
        ): RaidAction.DreadStatMuscleCastle,
        re.compile(
            r"^moved some bricks around \(1 turn\)$"
        ): RaidAction.DreadStatMuscleVillage,
        re.compile(
            r"^flipped through a photo album \(1 turn\)$"
        ): RaidAction.DreadStatMoxieForest,
        re.compile(
            r"^diverted some cold water out of Exposure Esplanade {}$".format(turns_p)
        ): RaidAction.HoboColdPipeTurnFirst,
        re.compile(
            r"^diverted some cold water to Burnbarrel Blvd. {}$".format(turns_p)
        ): RaidAction.HoboColdPipeTurnSecond,
        re.compile(
            r"^broke (?:a|[0-9]+) water pipes? {}$".format(turns_p)
        ): RaidAction.HoboColdPipeBreak,
        re.compile(r"^wasted some fruit \(1 turn\)$"): RaidAction.DreadKiwiWaste,
        re.compile(
            r"^\(unknown action\: (?P<action>.*?)\) {}$".format(turns_p)
        ): RaidAction.Unknown,
        re.compile(r"^{}$".format(turns_p)): RaidAction.Unknown,
        re.compile(
            r"^raided some naughty cabinets \(1 turn\)$"
        ): RaidAction.DreadStatMoxieVillage,
        re.compile(
            r"^read some naughty carvings \(1 turn\)$"
        ): RaidAction.DreadStatMysticalityVillage,
        re.compile(
            r"^sent some trash to The Heap {}$".format(turns_p)
        ): RaidAction.HoboSleazyTrash,
        re.compile(
            r"^sent (?:some|[0-9]+ bunches of) flowers to The Heap {}$".format(turns_p)
        ): RaidAction.HoboSpookyFlowers,
        re.compile(
            r"^sent (?:a|[0-9]+) batch(?:es)? of compost to the Burial Ground {}$".format(
                turns_p
            )
        ): RaidAction.HoboStenchCompost,
        re.compile(
            r"^found (?:a|[0-9]+) caches? of Meat for the clan coffer {}$".format(
                turns_p
            )
        ): RaidAction.HoboHotMeat,
        re.compile(
            r"^diverted some steam away from Burnbarrel Blvd. {}$".format(turns_p)
        ): RaidAction.HoboHotPipeTurn,
        re.compile(
            r"^raided (?:a|[0-9]+) dumpsters? {}$".format(turns_p)
        ): RaidAction.HoboSleazeMeat,
        re.compile(
            r"^raided (?:a|[0-9]+) fridges? {}$".format(turns_p)
        ): RaidAction.HoboColdMeat,
        re.compile(
            r"^raided (?:a|[0-9]+) tombs? {}$".format(turns_p)
        ): RaidAction.HoboSpookyMeat,
        re.compile(r"^took a nap on a prison cot \(1 turn\)$"): RaidAction.DreadMP,
        re.compile(
            r"^slew some vampires {}$".format(turns_p)
        ): RaidAction.SororityKillVampires,
        re.compile(
            r"^took care of some werewolves {}$".format(turns_p)
        ): RaidAction.SororityKillWerewolves,
        re.compile(
            r"^took out some zombies {}$".format(turns_p)
        ): RaidAction.SororityKillZombies,
        re.compile(
            r"^took out some skeletons {}$".format(turns_p)
        ): RaidAction.SororityKillSkeletons,
        re.compile(
            r"^trapped some ghosts {}$".format(turns_p)
        ): RaidAction.SororityKillGhosts,
        re.compile(
            r"^picked up some staff guides {}$".format(turns_p)
        ): RaidAction.SororityKillGuides,
        re.compile(
            r"^snagged a ghost trap {}$".format(turns_p)
        ): RaidAction.SororityItemGhost,
        re.compile(
            r"^snagged a funhouse mirror {}$".format(turns_p)
        ): RaidAction.SororityItemSkeleton,
        re.compile(
            r"^made a silver shotgun shell {}$".format(turns_p)
        ): RaidAction.SororityItemWerewolf,
        re.compile(
            r"^grabbed a chainsaw chain {}$".format(turns_p)
        ): RaidAction.SororityItemZombie,
        re.compile(
            r"^grabbed a sexy costume {}$".format(turns_p)
        ): RaidAction.SororityCostume,
        re.compile(
            r"^turned (?P<direction>up|down) the fog machine {}$".format(turns_p)
        ): RaidAction.SororityFogMachine,
        re.compile(
            r"^(?:cranked|turned) (?P<direction>up|down) the spooky noise volume {}$".format(
                turns_p
            )
        ): RaidAction.SororityBoombox,
        re.compile(
            r"^(?P<direction>opened|closed)(?: up)? some windows {}$".format(turns_p)
        ): RaidAction.SororityDownWindows,
        re.compile(
            r"^passed (?:the|[0-9]+) hats? in the tent {}$".format(turns_p)
        ): RaidAction.HoboSquareBusk,
        re.compile(
            r"^took the stage {}$".format(turns_p)
        ): RaidAction.HoboSquarePerform,
        re.compile(
            r"^failed to impress as a dancer {}$".format(turns_p)
        ): RaidAction.HoboSpookyDanceFailure,
        re.compile(
            r"^started (?:a|[0-9]+) mosh pits? in the tent {}$".format(turns_p)
        ): RaidAction.HoboSquareMosh,
        re.compile(
            r"^ruined (?:the|[0-9]+) shows? {}$".format(turns_p)
        ): RaidAction.HoboSquareLeave,
        re.compile(
            r"^had a drink in the Marketplace {}$".format(turns_p)
        ): RaidAction.HoboSquareMarketBooze,
        re.compile(
            r"^had some food in the Marketplace {}$".format(turns_p)
        ): RaidAction.HoboSquareMarketFood,
        re.compile(
            r"^read some ancient secrets \(1 turn\)$"
        ): RaidAction.DreadStatMysticalityCastle,
    }

    @classmethod
    def parse_raid_log(cls, raw_log: str) -> Optional[Event]:
        if raw_log == "(none yet)":
            return None

        raid_log_match = raid_log_pattern.match(raw_log)

        if raid_log_match is None:
            # There are occasionally logs with no user attached
            return None

        username = raid_log_match.group(1)
        user_id = int(raid_log_match.group(2))
        event = raid_log_match.group(3)

        for pattern, action in cls.log_patterns.items():
            m = pattern.match(event)

            if m is None:
                continue

            data = m.groupdict()

            return Event(action=action, username=username, user_id=user_id, data=data)

        raise UnknownError("Unrecognised event: {}".format(raw_log))

    @classmethod
    def parse_raid(cls, name: str, id: int, raid: Tag) -> Raid:
        """
        Parse a single raid's HTML tree
        """
        # They throw random <p>s everywhere, so get rid of them
        for p in raid.find_all("p", recursive=True):
            p.unwrap()

        summary = raid.find_all(clan_raid_log.center_with_no_link)

        events_categories = []

        # In the old days there were no summaries
        if len(summary) == 0:
            section = raid.find("b")
        else:
            section = summary[-1].find_next_sibling("b")

        # We now look for subsection titles, these are zones or
        # sections like "Loot Distribution"
        while section is not None:
            title = section.text
            section = section.find_next_sibling("blockquote")

            # This just traverses the list of HTML elements,
            # breaking it up by <br /> tag
            events = [
                event
                for event in (
                    cls.parse_raid_log("".join([e.text if e.name else e for e in g]))
                    for g in parsing.split_by_br(section)
                )
                if event is not None
            ]

            events_categories.append((title, events))

            section = section.find_next_sibling("b")

        return Raid(
            id=id,
            start=None,
            end=None,
            name=name.lower(),
            summary=[s.text for s in summary],
            events=events_categories,
        )

    @classmethod
    async def parser(cls, content: str, **kwargs) -> Raid:
        url = kwargs["url"]  # type: URL
        soup = BeautifulSoup(content, "html.parser")

        title = soup.find("b", text=previous_run_pattern)

        m = previous_run_pattern.match(title.text)

        if m is None:
            raise UnknownError("Cannot parse previous run")

        name = m.group(1)
        id = int(url.query["viewlog"])
        first = title.parent
        raid = first.parent
        first.decompose()
        return cls.parse_raid(name, id, raid)
