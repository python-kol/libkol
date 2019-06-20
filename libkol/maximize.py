from libkol import Modifier
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus


def calculate_smithsness(outfit, smithsness) -> int:
    return sum(
        smithsness[id]
        for id, quantity in outfit.items()
        if quantity != 0 and id in smithsness
    )


async def maximize(session, *args, modifier: str = None, **kwargs):
    if modifier is None:
        return []

    modifiers = await Modifier.Modifier.filter(
        key=modifier, item_id__not_isnull=True
    ).all()
    smiths_modifiers = await Modifier.Modifier.filter(
        key="Smithsness", item_id__not_isnull=True
    ).all()

    smithsness = {}
    for s in smiths_modifiers:
        await s.fetch_related("item")
        smithsness[s.item.id] = await s.get_value()

    map = {}
    for m in modifiers:
        await m.fetch_related("item")

        if m.item.have():
            map[m.item.id] = {"item": m.item, "modifier": m}

    # Define the problem
    prob = LpProblem(modifier, LpMaximize)
    outfit = LpVariable.dicts("outfit", map.keys(), 0, 3, cat="Integer")

    # Objective
    prob += lpSum(
        [
            await map[i]["modifier"].get_value(
                smithsness=calculate_smithsness(outfit, smithsness)
            )
            * outfit[i]
            for i in outfit
        ]
    )

    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].hat]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].shirt]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].weapon]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].offhand]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].pants]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].accessory]) <= 3
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].familiar_equipment]) <= 1
    prob += (
        lpSum(
            [
                outfit[i]
                for i in outfit
                if map[i]["item"].type
                not in [
                    "hat",
                    "shirt",
                    "weapon",
                    "offhand",
                    "pants",
                    "accessory",
                    "familiar_equipment",
                ]
            ]
        )
        == 0
    )

    for i in outfit:
        if map[i]["item"].single_equip:
            prob += outfit[i] <= 1

    prob.writeLP("maximizer.lp")
    prob.solve()

    print("Status: ", LpStatus[prob.status])
    result = []

    for v in prob.variables():
        index = v.name
        q = v.varValue
        if q == 0 or q is None:
            continue

        id = int(index[7:])
        for _ in range(int(q)):
            result.append(map[id]["item"])

    return result
