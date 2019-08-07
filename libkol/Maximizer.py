from aioitertools import iter
from collections import defaultdict
from libkol import Bonus
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, LpStatusOptimal
from tortoise.query_utils import Q
from typing import DefaultDict, Dict, List, Optional, Tuple

import libkol


class Maximizer:
    def __init__(self, session):
        self.session = session
        self.maximize = []
        self.minimize = []
        self.must_equip = []
        self.must_not_equip = []
        self.weight = defaultdict(lambda: 1)
        self.minimum = {}
        self.maximum = {}

    def __iadd__(self, constraint):
        from libkol import Modifier, Item
        from libkol.Modifier import WeightedModifier

        if isinstance(constraint, Modifier):
            self.maximize.append(constraint)
        elif isinstance(constraint, WeightedModifier):
            if constraint.min is not None:
                self.minimum[constraint.modifier] = constraint.min
            else:
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
            if constraint.min is not None:
                self.maximum[constraint.modifier] = constraint.min
            else:
                self.minimize.append(constraint.modifier)
                self.weight[constraint.modifier] = constraint.weight
        elif isinstance(constraint, Item):
            self.must_not_equip.append(constraint)
        else:
            raise TypeError("You can only subtract a Modifier or Item")

        return self

    @staticmethod
    def calculate_smithsness(solution, smithsness) -> int:
        return sum(
            smithsness[id]
            for id, quantity in solution.items()
            if quantity != 0 and id in smithsness
        )

    @staticmethod
    def calculate_hobo_power(solution, hobo_power) -> int:
        return sum(
            hobo_power[id]
            for id, quantity in solution.items()
            if quantity != 0 and id in hobo_power
        )

    @staticmethod
    def enthroned_repr(familiar: "libkol.Familiar") -> str:
        return f"<Familiar(Enthroned): {familiar.id}>"

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

    async def solve(
        self
    ) -> Tuple[
        DefaultDict["libkol.Slot", Optional["libkol.Item"]],
        Optional["libkol.Familiar"],
        List["libkol.Familiar"],
    ]:
        from libkol import Modifier, Slot, Item, Familiar

        # Get variables for some specific items
        crown = await Item["Crown of Thrones"]
        bjorn = await Item["Buddy Bjorn"]

        # Load smithsness bonuses for tracking
        smithsness_bonuses = {
            s.item.id: await s.get_value()
            async for s in (
                Bonus.filter(
                    modifier=Modifier.Smithsness, item_id__not_isnull=True
                ).prefetch_related("item")
            )
        }

        # Load hobo power bonuses for tracking
        hobo_power_bonuses = {
            s.item.id: await s.get_value()
            async for s in (
                Bonus.filter(
                    modifier=Modifier.HoboPower, item_id__not_isnull=True
                ).prefetch_related("item")
            )
        }

        # Load relevant bonuses
        modifiers = set(
            self.maximize
            + self.minimize
            + list(self.maximum.keys())
            + list(self.minimum.keys())
        )

        bonuses = [
            b
            async for b in (
                Bonus.filter(effect_id__isnull=True, modifier__in=modifiers)
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
                .prefetch_related(
                    "familiar",
                    "item",
                    "outfit__variants__pieces",
                    "outfit__variants",
                    "outfit",
                    "throne_familiar",
                )
            )
        ]

        grouped_bonuses = {}  # type: Dict[libkol.Modifier, List[libkol.Bonus]]
        for b in bonuses:
            grouped_bonuses[b.modifier] = grouped_bonuses.get(b.modifier, []) + [b]

        possible_items = (
            [b.item for b in bonuses if isinstance(b.item, Item)]
            + self.must_equip
            + [bjorn, crown]
        )
        possible_familiars = [
            b.familiar for b in bonuses if isinstance(b.familiar, Familiar)
        ]
        possible_throne_familiars = [
            b.throne_familiar
            for b in bonuses
            if isinstance(b.throne_familiar, Familiar)
        ]



        # Define the problem
        prob = LpProblem(self.summarise(), LpMaximize)
        solution = LpVariable.dicts(
            "outfit",
            {repr(i) for i in possible_items + possible_familiars} | { self.enthroned_repr(f) for f in possible_throne_familiars },
            0,
            3,
            cat="Integer",
        )

        # Value of our Smithsness bonus
        smithsness = self.calculate_smithsness(solution, smithsness_bonuses)

        # Value of our Hobo Power bonus
        hobo_power = self.calculate_hobo_power(solution, hobo_power_bonuses)

        # Value of our familiar weight
        familiar_weight = next(
            (f.weight for f in possible_familiars if solution[repr(f)] == 1), 0
        )

        # Objective
        prob += lpSum(
            [
                m.sum(
                    [
                        await b.get_value(
                            smithsness=smithsness,
                            familiar_weight=familiar_weight,
                            hobo_power=hobo_power,
                        )
                        * (solution[repr(b.item)] if isinstance(b.item, Item) else 1)
                        * (
                            solution[repr(b.familiar)]
                            if isinstance(b.familiar, Familiar)
                            else 1
                        )
                        * (
                            solution[self.enthroned_repr(b.throne_familiar)]
                            if isinstance(b.throne_familiar, Familiar)
                            else 1
                        )
                        for b in bonuses
                        if b.outfit is None
                        or (
                            b.outfit
                            and await b.outfit.is_fulfilled(
                                [
                                    sb.item
                                    for sb in bonuses
                                    if isinstance(sb.item, Item)
                                    and solution[repr(sb.item)] >= 1
                                ]
                            )
                        )
                    ]
                )
                * self.weight[m]
                * (1 if m in self.maximize else -1 if m in self.minimize else 0)
                async for m, bonuses in iter(grouped_bonuses.items())
            ]
        )

        # Add minima and maxima
        for m, bonuses in grouped_bonuses.items():
            total = lpSum(
                [
                    await b.get_value(
                        smithsness=smithsness, familiar_weight=familiar_weight
                    )
                    * solution[repr(b.item)]
                    for b in bonuses
                    if b.item
                ]
            )
            if self.minimum.get(m) is not None:
                prob += total >= self.minimum[m]
            if self.maximum.get(m) is not None:
                prob += total <= self.maximum[m]

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
                lpSum([solution[repr(i)] for i in possible_items if getattr(i, slot)])
                <= size
            )

        # Only use one familiar
        prob += lpSum([solution[repr(f)] for f in possible_familiars]) <= 1

        # Do not use familiars we don't  have
        for f in possible_familiars:
            if f.have is False:
                prob += solution[repr(f)] == 0

        # Only throne familiars with throneable equips
        prob += (
            lpSum([solution[self.enthroned_repr(f)] for f in possible_throne_familiars])
            <= solution[repr(crown)] + solution[repr(bjorn)]
        )

        # Do not enthrone familiars we don't have
        for f in possible_throne_familiars:
            if f.have is False:
                prob += solution[self.enthroned_repr(f)] == 0

        # You've only got so many hands!
        prob += (
            lpSum(
                [
                    solution[repr(i)]
                    for i in possible_items
                    if (i.weapon and i.weapon_hands >= 2) or i.offhand
                ]
            )
            <= 1
        )

        # For each item...
        for i in possible_items:
            # Don't plan to equip things we can't wear
            if i.meet_requirements() is False:
                prob += solution[repr(i)] == 0

            # We can only equip as many as we have
            prob += solution[repr(i)] <= i.amount

            # We can only equip one single equip item
            if i.single_equip:
                prob += solution[repr(i)] <= 1

        # Forced equips
        for i in self.must_equip:
            prob += solution[repr(i)] >= 1

        # Forced non-equips
        for i in self.must_not_equip:
            prob += solution[repr(i)] == 0

        prob.writeLP("maximizer.lp")
        prob.solve()

        if prob.status is not LpStatusOptimal:
            raise ValueError(LpStatus[prob.status])

        familiar = None
        throne_familiars = []  # type: List[Familiar]
        result = defaultdict(lambda: None)  # type: DefaultDict[Slot, Optional[Item]]

        for v in prob.variables():
            index = v.name
            q = v.varValue
            index_parts = index.split("_")

            if q == 0 or q is None or len(index_parts) < 3:
                continue

            id = int(index_parts[2])

            if index_parts[1] == "<Familiar:":
                familiar = next(f for f in possible_familiars if f.id == id)
                continue

            if index_parts[1] == "<Familiar(Enthroned):":
                throne_familiars += next(f for f in possible_throne_familiars if f.id == id)
                continue

            item = next(i for i in possible_items if i.id == id)

            item_slot = item.slot  # type: Slot

            if item_slot == Slot.Acc1:
                if result[Slot.Acc1] is None:
                    item_slot = Slot.Acc1
                elif result[Slot.Acc2] is None:
                    item_slot = Slot.Acc2
                elif result[Slot.Acc3] is None:
                    item_slot = Slot.Acc3
                else:
                    raise Exception("Pulp has done something wrong")

            result[item_slot] = item

        return result, familiar, throne_familiars

    async def solve_and_equip(self):
        outfit, familiar, throne_familiars = await self.solve()

        await self.session.unequip()

        for slot, item in outfit.items():
            await item.equip(slot)

        return True
