from aiohttp import ClientSession, ClientResponse
import re

async def load_mafia_data(session: ClientSession, key: str) -> ClientResponse:
    response = await session.get(
        "https://svn.code.sf.net/p/kolmafia/code/src/data/{}.txt".format(key)
    )
    return response


range_pattern = re.compile(r"(-?[0-9]+)(?:-(-?[0-9]+))?")


def split_range(range: str):
    m = range_pattern.match(range)

    if m is None:
        raise ValueError("Cannot split range: {}".format(range))

    start = int(m.group(1))
    return start, int(m.group(2)) if m.group(2) else start


id_duplicate_pattern = re.compile(r"\[([0-9]+)\].+")


def mafia_dedupe(name: str):
    if name[0] != "[":
        return {"name": name}

    m = id_duplicate_pattern.match(name)

    if m is None:
        return {"name": name}

    return {"id": int(m.group(1))}
