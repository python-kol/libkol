import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession
from sympy import Symbol

from typing import Any, Coroutine, List
from libkol import Familiar, Item, Bonus, Modifier

from util import load_mafia_data

W = Symbol("W")
ML = Symbol("ML")

volleyball = 2 + (W / 5)
sombrero = (ML / 4) * (0.1 + 0.005 * W)
fairy = ((55 * W) ** 0.5) + W - 3
leprechaun = fairy * 2


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Familiar]]

    async for bytes in (await load_mafia_data(session, "familiars")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) == 0 or line[0] == "#":
            continue

        parts = line.split("\t")
        if len(parts) < 2:
            continue

        fam_type = {t.strip() for t in parts[3].split(",")}
        attributes = (
            [t.strip() for t in parts[10].split(",")] if len(parts) > 10 else []
        )

        familiar = Familiar(
            id=int(parts[0]),
            name=parts[1],
            image=parts[2],
            physical_attack="combat0" in fam_type,
            elemental_attack="combat1" in fam_type,
            drop="drop" in fam_type,
            block="block" in fam_type,
            delevel="delevel" in fam_type,
            combat_hp="hp0" in fam_type,
            combat_mp="mp0" in fam_type,
            combat_meat="meat1" in fam_type,
            combat_stat="stat2" in fam_type,
            combat_other="other0" in fam_type,
            post_hp="hp1" in fam_type,
            post_mp="mp1" in fam_type,
            post_stat="stat3" in fam_type,
            post_other="other" in fam_type,
            passive={"passive", "stat0", "stat1", "item0", "meat0"} & fam_type,
            underwater="underwater" in fam_type,
            variable="variable" in fam_type,
            cave_match_skill=int(parts[6]),
            scavenger_hunt_skill=int(parts[7]),
            obstacle_course_skill=int(parts[8]),
            hide_and_seek_skill=int(parts[9]),
            pokefam="pokefam" in attributes,
            bites="UNKNOWN" in attributes,
            has_eyes="eyes" in attributes,
            has_hands="hands" in attributes,
            has_wings="wings" in attributes,
            is_animal="animal" in attributes,
            is_bug="bug" in attributes,
            is_flying="UNKNOWN" in attributes,
            is_hot="UNKNOWN" in attributes,
            is_mechanical="mechanical" in attributes,
            is_quick="UNKNOWN" in attributes,
            is_slayer="slayer" in attributes,
            is_sleazy="sleazy" in attributes,
            is_undead="undead" in attributes,
            wears_clothes="clothes" in attributes,
        )

        if parts[4] != "":
            familiar.hatchling = await Item[parts[4]]

        if parts[5] != "":
            familiar.equipment = await Item[parts[5]]

        tasks += [familiar.save()]

        if "stat0" in fam_type:
            # Volleyball-like
            b = Bonus(familiar_id=familiar.id, modifier=Modifier.Experience)
            b.expression_value = volleyball
            tasks += [b.save()]

        if "stat1" in fam_type:
            # Sombrero-like
            b = Bonus(familiar_id=familiar.id, modifier=Modifier.Experience)
            b.expression_value = sombrero
            tasks += [b.save()]

        if "item0" in fam_type:
            # Fairy-like
            b = Bonus(familiar_id=familiar.id, modifier=Modifier.ItemDrop)
            b.expression_value = fairy
            tasks += [b.save()]

        if "meat0" in fam_type:
            # Leprechaun-like
            b = Bonus(familiar_id=familiar.id, modifier=Modifier.MeatDrop)
            b.expression_value = leprechaun
            tasks += [b.save()]

    return await asyncio.gather(*tasks)
