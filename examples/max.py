import os
from dotenv import load_dotenv
from libkol import Session, run, Modifier, Maximizer, Item

load_dotenv()


async def main():
    async with Session() as kol:
        await kol.login(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        problem = Maximizer(kol)
        problem += Modifier.HotResistance
        problem += await Item["high-temperature mining drill"]

        try:
            items, familiar = await problem.solve()

            if familiar:
                print(f"Familiar: {familiar.name}")

            for slot, i in items.items():
                print(f"{slot.value}: {i.name}")
        except ValueError as e:
            print(f"Not possible ({e})")


if __name__ == "__main__":
    run(main)
