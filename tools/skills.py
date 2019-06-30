import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Skill

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Skill]]

    async for bytes in (await load_mafia_data(session, "classskills")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) == 0 or line[0] == "#":
            continue

        parts = line.split("\t")
        if len(parts) < 5:
            continue

        type = int(parts[3])

        skill = Skill(
            id=int(parts[0]),
            name=parts[1],
            image=parts[2],
            passive=type in [0, 8],
            noncombat=type in [1, 2, 3, 4, 6, 7, 9, 10],
            shruggable=type == 4,
            combat=type in [5, 7, 8],
            healing=type in [2, 7],
            summon=type == 1,
            expression=type == 9,
            walk=type == 10,
            mutex_song=type == 6,
            mp_cost=int(parts[4]),
            level_required=int(parts[5]) if len(parts) > 5 else 0,
        )

        tasks += [skill.save()]

    return await asyncio.gather(*tasks)
