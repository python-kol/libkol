from libkol import Session, run
from libkol.maximize import maximize


async def main():
    async with Session() as kol:
        items = await maximize(kol, modifier="Spooky Damage")

        for i in items:
            print(f"{i.type}: {i.name}")


if __name__ == "__main__":
    run(main)
