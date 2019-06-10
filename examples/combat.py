"""
This file shows how you can use adventure using libkol
"""

import asyncio

from libkol import Session


async def main():
    async with Session() as kol:
        await kol.login("username", "password")
        await kol.adventure(92)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
