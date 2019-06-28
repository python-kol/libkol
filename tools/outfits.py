import asyncio
from tortoise.transactions import atomic
from html import unescape
from aiohttp import ClientSession

from typing import Any, Coroutine, List
from libkol import Item, Outfit, OutfitVariant

from util import load_mafia_data


@atomic()
async def load(session: ClientSession):
    tasks = []  # type: List[Coroutine[Any, Any, Item]]

    async for bytes in (await load_mafia_data(session, "outfits")).content:
        line = unescape(bytes.decode("utf-8")).strip()

        if len(line) < 2:
            continue

        parts = line.split("\t")

        if len(parts) < 4:
            continue

        outfit, _created = await Outfit.get_or_create(
            id=int(parts[0]), name=parts[1], image=parts[2]
        )

        variant = OutfitVariant(outfit_id=outfit.id)
        await variant.save()

        items = await Item.filter(name__in=[i.strip() for i in parts[3].split(",")])

        for item in items:
            tasks += [item.outfit_variants.add(variant)]

        # Manually add outfit variant for Meteor Masquerade
        if outfit.name == "Meteor Masquerade":
            guard = await Item["meteorite guard"]
            variant = OutfitVariant(outfit_id=outfit.id)
            await variant.save()
            for item in items:
                if item.name == "meteorb":
                    item = guard

                tasks += [item.outfit_variants.add(variant)]

    return await asyncio.gather(*tasks)
