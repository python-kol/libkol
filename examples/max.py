from libkol import Session, run, Modifier, Maximizer


async def main():
    async with Session() as kol:
        problem = Maximizer(kol)
        problem += Modifier.Moxie
        problem -= Modifier.CombatRate
        items = await problem.solve()

        for i in items:
            print(f"{i.type}: {i.name}")


if __name__ == "__main__":
    run(main)
