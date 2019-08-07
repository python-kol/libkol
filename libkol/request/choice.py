from dataclasses import dataclass
from typing import Any, Dict, List, Union
from bs4 import BeautifulSoup, Tag
import libkol

from ..Error import UnknownError
from .request import Request
from ..util import parsing

@dataclass
class Option:
    id: int
    text: str

@dataclass
class Choice:
    session: "libkol.Session"
    id: int
    options: List[Option]

    async def choose(self, option_id: int, extra: Dict[str, Any] = {}):
        return await choice(self.session, self.id, option_id, extra).parse()


class choice(Request[Union[Tag, Choice]]):
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param choice: The id of the choice
    :param option: The number option to submit
    """

    def __init__(
        self, session: "libkol.Session",
        choice: Union[Choice, int],
        option: Union[Option, int],
        extra: Dict[str, Any] = {},
    ) -> None:
        super().__init__(session)
        data = {"whichchoice": choice, "option": option, **extra}
        self.request = session.request("choice.php", data=data, pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> Union[Tag, Choice]:
        session = kwargs["session"]  # type: libkol.Session
        soup = BeautifulSoup(content, "html.parser")

        choice = Choice(session, 0, [])

        options = soup.find_all("form", action="choice.php")

        if len(options) == 0:
            results = parsing.panel(content)

            if results is None:
                raise UnknownError("Choice rendered no new options and no results")

            return results

        for option in options:
            choice_id = option.find("input", attrs={"name": "whichchoice"})["value"]
            option_id = option.find("input", attrs={"name": "option"})["value"]
            option_text = option.find("input", type="submit")["value"]

            choice.id = int(choice_id)
            choice.options += [Option(int(option_id), option_text)]

        return choice
