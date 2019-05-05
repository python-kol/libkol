"""
This file shows how you can use Clan methods to determine
"""

import asyncio
import re

from pykollib.Session import Session

kill_pattern = re.compile(r"^([^\(]+) \(#([0-9]+)\) defeated (.*) \(([0-9]+) turns?\)")
skill_pattern = re.compile(r"^^([^\(]+) \(#([0-9]+)\)  used The Machine")


def events_for_player(raids, zones, pattern, get_turns):
    per_player = {}

    events = [
        event
        for raid in raids
        for zone, events in raid["events"]
        for event in events
        if zone.lower() in zones and pattern.match(event)
    ]

    for event in events:
        m = pattern.match(event)
        player = m.group(1)
        per_player[player] = per_player.get(player, 0) + get_turns(m)

    return per_player


async def main():
    async with Session() as kol:
        await kol.login("username", "password")

        tasks = [kol.clan.get_raids()]
        tasks += [
            kol.clan.get_raid_log(raid_id=raid["id"])
            for raid in await kol.clan.get_previous_raids()
        ]

        current, *previous = await asyncio.gather(*tasks)

        raids = [raid for raid in current + previous if raid["name"] == "dreadsylvania"]

        kills = events_for_player(
            raids,
            ["the village", "the castle", "the woods"],
            kill_pattern,
            lambda m: int(m.group(4)),
        )

        skills = events_for_player(raids, ["miscellaneous"], skill_pattern, lambda m: 1)

        for player, killcount in kills.items():
            ranking = killcount / (skills.get(player, 0) + 0.5)
            print("{}: {}".format(player, ranking))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
