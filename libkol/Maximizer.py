from libkol import Bonus
from aioitertools import groupby
from tortoise.query_utils import Q
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus
from collections import defaultdict


class Maximizer:
    def __init__(self, session):
        self.session = session
        self.maximize = []
        self.minimize = []
        self.must_equip = []
        self.must_not_equip = []
        self.weight = defaultdict(lambda: 1)

    def __iadd__(self, constraint):
        from libkol import Modifier, Item
        from libkol.Modifier import WeightedModifier

        if isinstance(constraint, Modifier):
            self.maximize.append(constraint)
        elif isinstance(constraint, WeightedModifier):
            self.maximize.append(constraint.modifier)
            self.weight[constraint.modifier] = constraint.weight
        elif isinstance(constraint, Item):
            self.must_equip.append(constraint)
        else:
            raise TypeError("You can only add a Modifier or Item")

        return self

    def __isub__(self, constraint):
        from libkol import Modifier, Item
        from libkol.Modifier import WeightedModifier

        if isinstance(constraint, Modifier):
            self.minimize.append(constraint)
        elif isinstance(constraint, WeightedModifier):
            self.minimize.append(constraint.modifier)
            self.weight[constraint.modifier] = constraint.weight
        elif isinstance(constraint, Item):
            self.must_not_equip.append(constraint)
        else:
            raise TypeError("You can only subtract a Modifier or Item")

        return self

    @staticmethod
    def calculate_smithsness(outfit, smithsness) -> int:
        return sum(
            smithsness[id]
            for id, quantity in outfit.items()
            if quantity != 0 and id in smithsness
        )

    def summarise(self) -> str:
        return ", ".join(
            [
                constraint
                for sublist in [
                    [m.value for m in self.maximize],
                    [f"-{m.value}" for m in self.minimize],
                    [f"equip {i.name}" for i in self.must_equip],
                    [f"-equip {i.name}" for i in self.must_not_equip],
                ]
                for constraint in sublist
            ]
        )

    async def solve(self):
        from libkol import Modifier

        # Load smithsness bonuses for tracking smithsness
        smithsness = {
            s.item.id: await s.get_value()
            async for s in (
                Bonus.filter(
                    modifier=Modifier.Smithsness, item_id__not_isnull=True
                ).prefetch_related("item")
            )
        }

        # Load relevant bonuses
        modifiers = self.maximize + self.minimize

        bonuses = [
            b
            async for b in (
                Bonus.filter(
                    Q(item_id__not_isnull=True) | Q(outfit_id__not_isnull=True)
                )
                .filter(modifier__in=modifiers)
                .prefetch_related("item", "outfit", "outfit__pieces")
            )
            if b.outfit or (b.item and b.item.have())
        ]

        grouped_bonuses = groupby(bonuses, lambda m: m.modifier)

        # Define the problem
        prob = LpProblem(self.summarise(), LpMaximize)
        solution = LpVariable.dicts(
            "outfit", [b.item.id for b in bonuses if b.item], 0, 3, cat="Integer"
        )

        # Objective
        prob += lpSum(
            [
                m.sum(
                    [
                        await b.get_value(
                            smithsness=self.calculate_smithsness(solution, smithsness)
                        )
                        * (solution[b.item.id] if b.item else 1)
                        for b in bonuses
                        if b.item
                        or (
                            b.outfit
                            and b.outfit.is_fulfilled(
                                [
                                    sb.item
                                    for sb in bonuses
                                    if sb.item and solution[sb.item.id] >= 1
                                ]
                            )
                        )
                    ]
                )
                * self.weight[m]
                * (1 if m in self.maximize else -1 if m in self.minimize else 0)
                async for m, bonuses in grouped_bonuses
            ]
        )

        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.hat]) <= 1
        )
        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.shirt])
            <= 1
        )
        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.weapon])
            <= 1
        )
        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.offhand])
            <= 1
        )
        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.pants])
            <= 1
        )
        prob += (
            lpSum([solution[b.item.id] for b in bonuses if b.item and b.item.accessory])
            <= 3
        )
        prob += (
            lpSum(
                [
                    solution[b.item.id]
                    for b in bonuses
                    if b.item and b.item.familiar_equipment
                ]
            )
            <= 1
        )
        prob += (
            lpSum(
                [
                    solution[b.item.id]
                    for b in bonuses
                    if b.item
                    and b.item.type
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

        for b in bonuses:
            if b.item and b.item.single_equip:
                prob += solution[b.item.id] <= 1

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
                result.append(
                    next(b.item for b in bonuses if b.item and b.item.id == id)
                )

        return result
