from libkol import Modifier
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from sympy import functions
from sympy.parsing.sympy_parser import parse_expr

def determine_value(modifier, state):
    if modifier.string_value:
        return 1

    if modifier.numeric_value:
        if modifier.percentage:
            base = 1
            multiplier = modifier.numeric_value / 100

            if modifier.key == "Maximum HP":
                base = state["buffed_muscle"] + 3
                multiplier += 1.5 if state["class"] in ["Seal Clubber", "Turtle Tamer"] else 1
            elif modifier.key == "Maximum MP":
                base = state["buffed_mysticality"]
                multiplier = 1.5 if state["class"] in ["Pastamancer", "Sauceror"] else 1
            elif modifier.key == "Muscle":
                base = state["base_muscle"]
            elif modifier.key == "Mysticality":
                base = state["base_mysticality"]
            elif modifier.key == "Moxie":
                base = state["base_moxie"]

            return multiplier * base

        return modifier.numeric_value

    if modifier.expression_value:
        local_dict = {
            "D": state["inebriety"],
            "L": state["level"],
            "W": state["familiar"]["weight"],
            "abs": functions.Abs,
            "min": functions.Min,
            "max": functions.Max,
            "sqrt": functions.sqrt,
            "ceil": functions.ceiling,
            "floor": functions.floor,
        }

        try:
            expr = parse_expr(modifier.expression_value, local_dict=local_dict)
            if expr.is_number:
                return expr
            else:
                print("Unknown symbols {}".format(expr.free_symbols))
        except:
            print("Could not parse {}".format(modifier.expression_value))

    return 0


async def maximize(session, *args, modifier="Maximum HP", **kwargs):
    modifiers = await Modifier.Modifier.filter(key=modifier, item_id__not_isnull=True).all()

    map = {}

    state = session.state

    for m in modifiers:
        await m.fetch_related('item')
        map[m.item.id] = {"item": m.item, "modifier": m}

    keys = map.keys()

    # Define the problem
    prob = LpProblem(modifier, LpMaximize)
    outfit = LpVariable.dicts("outfit", keys, 0, 1, cat="Integer")

    # Objective
    prob += lpSum([determine_value(map[i]["modifier"], state) * outfit[i] for i in outfit])

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
