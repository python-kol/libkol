from typing import List
import re
from bs4 import BeautifulSoup, Tag

import libkol

from .request import Request
from ..util import parsing
from ..Error import UnknownError

stat_pattern = re.compile(
    r"^(?:, the )?(?P<weight>[0-9]+)-pound (?P<name>.*?) \((?P<experience>[0-9,]+) exp(?:erience)?, (?P<kills>[0-9,]+) kills\)$"
)


class familiar(Request):
    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)
        self.request = session.request("familiar.php")

    @staticmethod
    async def make_familiar_state(
        img: Tag, name: Tag, info: str
    ) -> "libkol.types.FamiliarState":
        from libkol import Familiar
        from libkol.types import FamiliarState

        id = int(img["onclick"][4:-1])
        familiar = await Familiar[id]

        match = stat_pattern.match(info.strip())

        if match is None:
            raise UnknownError("Could not parse familiar stats")

        stats = match.groupdict()

        return FamiliarState(
            familiar=familiar,
            nickname=name.get_text(),
            weight=int(stats["weight"]),
            experience=parsing.to_int(stats["experience"]),
            kills=parsing.to_int(stats["kills"]),
        )

    @classmethod
    async def parser(cls, content: str, **kwargs) -> List["libkol.types.FamiliarState"]:
        soup = BeautifulSoup(content, "html.parser")

        familiar_states = []  # type: List["libkol.types.FamiliarState"]

        for c in soup.find_all("center"):
            if c.contents[0] == "Current Familiar:":
                familiar_states += [
                    await cls.make_familiar_state(
                        c.contents[2], c.contents[4], c.contents[6]
                    )
                ]
                break

        terrarium = soup.find_all("img", class_="fam")

        for f in terrarium:
            info = f.parent.next_sibling.b
            familiar_states += [
                await cls.make_familiar_state(f, info, info.next_sibling.string)
            ]

        session = kwargs["session"]  # type: libkol.Session

        session.state.familiars = {f.familiar: f for f in familiar_states}

        return familiar_states
