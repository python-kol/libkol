from libkol import Modifier
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus


async def maximize(session, *args, modifier="Maximum HP", **kwargs):
    modifiers = await Modifier.Modifier.filter(key=modifier, item_id__not_isnull=True).all()

    map = {}

    for m in modifiers:
        await m.fetch_related('item')
        map[m.item.id] = {"item": m.item, "modifier": m}

    keys = map.keys()

    # Define the problem
    prob = LpProblem(modifier, LpMaximize)
    outfit = LpVariable.dicts("outfit", keys, 0, 1, cat="Integer")

    # Objective
    prob += lpSum([map[i]["modifier"].get_value() * outfit[i] for i in outfit])

    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].hat]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].shirt]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].weapon]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].offhand]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].pants]) <= 1
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].accessory]) <= 3
    prob += lpSum([outfit[i] for i in outfit if map[i]["item"].familiar_equipment]) <= 1

    prob.writeLP("maximizer.lp")
    prob.solve()

    print("Status: ", LpStatus[prob.status])
    result = []

    for v in prob.variables():
        index = v.name
        q = v.varValue
        if (q == 0 or q is None):
            continue

        id = int(index[7:])
        result.append(map[id]["item"])

    return result
