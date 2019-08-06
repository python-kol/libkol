"""
This file shows how you can use adventure using libkol
"""

import os
from dotenv import load_dotenv
from libkol import run, Session
from libkol.request.combat import CombatRound

load_dotenv()


async def do_combat(combat, start: CombatRound):
    raise Exception("There shouldn't be a combat here!")


async def main():
    async with Session() as kol:
        await kol.login(os.getenv("KOL_USERNAME"), os.getenv("KOL_PASSWORD"))
        await kol.adventure(355, do_combat, choices={793: 3})


if __name__ == "__main__":
    run(main)
