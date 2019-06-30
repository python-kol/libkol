import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Effect

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Effect]]

    async for bytes in (await load_mafia_data(session, "statuseffects")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if "\t" not in line or line[0] == "#":
            continue

        parts = line.split("\t")

        if len(parts) < 4:
            continue

        effect = Effect(
            id=int(parts[0]), name=parts[1], image=parts[2], desc_id=parts[3]
        )
        tasks += [effect.save()]

    return await asyncio.gather(*tasks)
