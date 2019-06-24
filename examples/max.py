from libkol import Session, run, Modifier, Maximizer, Item


async def main():
    async with Session() as kol:
        problem = Maximizer(kol)
        problem += Modifier.HotResistance
        problem += await Item["high-temperature mining drill"]

        try:
            items = await problem.solve()

            for slot, i in items.items():
                print(f"{slot.value}: {i.name}")
        except ValueError as e:
            print(f"Not possible ({e})")


if __name__ == "__main__":
    run(main)
