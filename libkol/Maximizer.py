from libkol import Bonus
from aioitertools import groupby
from tortoise.query_utils import Q
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, LpStatusOptimal
from collections import defaultdict


class Maximizer:
    def __init__(self, session):
        self.session = session
        self.maximize = []
        self.minimize = []
        self.must_equip = []
        self.must_not_equip = []
        self.weight = defaultdict(lambda: 1)
        self.minimum = defaultdict(int)
        self.maximum = defaultdict(int)

    def __iadd__(self, constraint):
        from libkol import Modifier, Item
        from libkol.Modifier import WeightedModifier

        if isinstance(constraint, Modifier):
            self.maximize.append(constraint)
        elif isinstance(constraint, WeightedModifier):
            self.maximize.append(constraint.modifier)
            self.weight[constraint.modifier] = constraint.weight
            self.minimum[constraint.modifier] = constraint.min
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
            self.maximum[constraint.modifier] = constraint.min
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
        smithsness_bonuses = {
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
                .filter(
                    Q(item_id__isnull=True)
                    | Q(item__hat=True)
                    | Q(item__shirt=True)
                    | Q(item__weapon=True)
                    | Q(item__offhand=True)
                    | Q(item__pants=True)
                    | Q(item__accessory=True)
                    | Q(item__familiar_equipment=True)
                )
                .prefetch_related("item", "outfit", "outfit__pieces")
            )
        ]

        grouped_bonuses = groupby(bonuses, lambda m: m.modifier)

        possible_items = [b.item for b in bonuses if b.item] + self.must_equip

        # Define the problem
        prob = LpProblem(self.summarise(), LpMaximize)
        solution = LpVariable.dicts(
            "outfit", {i.id for i in possible_items}, 0, 3, cat="Integer"
        )

        # Value of our Smithsness bonus
        smithsness = self.calculate_smithsness(solution, smithsness_bonuses)

        # Objective
        prob += lpSum(
            [
                m.sum(
                    [
                        await b.get_value(smithsness=smithsness)
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

        # Add minima and maxima
        async for m, bonuses in grouped_bonuses:
            prob += (
                this.minimum(m)
                <= lpSum([await b.get_value(smithsness=smithsness) for b in bonuses])
                <= this.maximum(m)
            )

        # Maximum slot sizes
        slot_sizes = [
            ("hat", 1),
            ("shirt", 1),
            ("weapon", 1),
            ("offhand", 1),
            ("pants", 1),
            ("accessory", 3),
            ("familiar_equipment", 1),
        ]

        for slot, size in slot_sizes:
            prob += (
                lpSum(
                    [
                        solution[b.item.id]
                        for b in bonuses
                        if b.item and getattr(b.item, slot)
                    ]
                )
                <= size
            )

        # For each item...
        for i in possible_items:
            # Don't plan to equip things we can't wear
            if i.meet_requirements() is False:
                prob += solution[i.id] == 0

            # We can only equip as many as we have
            prob += solution[i.id] <= i.amount()

            # We can only equip one single equip item
            if i.single_equip:
                prob += solution[i.id] <= 1

        # Forced equips
        for i in self.must_equip:
            prob += solution[i.id] >= 1

        # Forced non-equips
        for i in self.must_not_equip:
            prob += solution[i.id] == 0

        prob.writeLP("maximizer.lp")
        prob.solve()

        if prob.status is not LpStatusOptimal:
            raise ValueError(LpStatus[prob.status])

        result = []

        for v in prob.variables():
            index = v.name
            q = v.varValue

            if q == 0 or q is None:
                continue

            id = int(index[7:])

            for _ in range(int(q)):
                result.append(next(i for i in possible_items if i.id == id))

        return result
