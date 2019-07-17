"""
This file shows how you can use adventure using libkol
"""

import asyncio
import os
from dotenv import load_dotenv
from libkol import Session
from libkol.request.combat import combat, CombatRound

load_dotenv()


async def do_combat(combat, start: CombatRound):
    monster_hp = start.monster.hp
    round = start

    while monster_hp > 0:
        round = await combat.attack()
        monster_hp -= round.damage

    return round


async def main():
    async with Session() as kol:
        await kol.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        result = await kol.adventure(92, combat_function=do_combat)
        print(result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
