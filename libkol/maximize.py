from libkol import Modifier
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from sympy.parsing.sympy_parser import parse_expr

def determine_value(modifier, base):
    if modifier.string_value:
        return 1

    if modifier.numeric_value:
        if modifier.percentage:
            return modifier.numeric_value * base

        return modifier.numeric_value

    if modifier.expression_value:
        try:
            expr = parse_expr(modifier.expression_value)
            print(expr)
        except:
            pass
        return 0


async def maximize(session, *args, modifier="Maximum HP", base=10, **kwargs):
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
    prob += lpSum([determine_value(map[i]["modifier"], base) * outfit[i] for i in outfit])

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
