import asyncio
import json
from tortoise.transactions import atomic
from aiohttp import ClientSession

from libkol import Trophy

@atomic()
async def load(session: ClientSession):
    trophies = [Trophy(**trophy) for trophy in json.load(open("./trophies.json"))]
    tasks = [trophy._insert_instance() for trophy in trophies]
    return await asyncio.gather(*tasks)
