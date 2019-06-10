"""
This file shows how you can use Clan methods to determine
the ratio of monster kills in Dreadsylvania to skills
acquired from The Machine over all past and present raids
"""

import asyncio
import re
from tabulate import tabulate
from itertools import groupby
from tqdm import tqdm

from libkol import Session

kill_pattern = re.compile(r"^([^\(]+) \(#([0-9]+)\) defeated (.*) \(([0-9]+) turns?\)")
skill_pattern = re.compile(r"^([^\(]+) \(#([0-9]+)\)  used The Machine")


def events_for_player(raids, zones, pattern, get_count):
    events = [
        pattern.match(event)
        for raid in raids
        for zone, events in raid["events"]
        for event in events
        if zone.lower() in zones and pattern.match(event)
    ]

    events = sorted(events, key=lambda e: e.group(1))

    return {
        player: sum(get_count(e) for e in events)
        for player, events in groupby(events, key=lambda e: e.group(1))
    }


async def main():
    async with Session() as kol:
        await kol.login("username", "password")

        clan = kol.clan
        tasks = [asyncio.ensure_future(clan.get_raids())]
        tasks += [
            asyncio.ensure_future(clan.get_raid_log(raid_id=raid["id"]))
            for raid in await clan.get_previous_raids()
        ]

        current, *previous = [
            await t
            for t in tqdm(
                asyncio.as_completed(tasks),
                desc="Parsing raids",
                unit="raids",
                total=len(tasks),
            )
        ]
        raids = current + previous

        dreads = [raid for raid in raids if raid["name"] == "dreadsylvania"]

        kills = events_for_player(
            dreads,
            ["the village", "the castle", "the woods"],
            kill_pattern,
            lambda m: int(m.group(4)),
        )

        skills = events_for_player(
            dreads, ["miscellaneous"], skill_pattern, lambda m: 1
        )

        table = [
            {"player": player, "k/s": killcount / (skills.get(player, 0) + 0.5)}
            for player, killcount in kills.items()
        ]

        table = sorted(table, key=lambda r: -r["k/s"])

        print(tabulate(table))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
