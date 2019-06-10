from libkol import Session, run
from libkol.maximize import maximize


async def main():
    async with Session() as kol:
        items = await maximize(kol)
        for i in items:
            print(i.name)

if __name__ == "__main__":
    run(main)
