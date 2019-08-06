from dataclasses import dataclass
from typing import List, Union
from bs4 import BeautifulSoup
import libkol

from .request import Request

@dataclass
class Option:
    id: int
    text: str

@dataclass
class Choice:
    id: int
    options: List[Option]


class choice(Request[Choice]):
    """
    Submit a given option in response to a give choice

    :param session: KoL session
    :param choice: The id of the choice
    :param option: The number option to submit
    """

    def __init__(self, session: "libkol.Session", choice: Union[Choice, int], option: Union[Option, int]) -> None:
        super().__init__(session)
        data = {"whichchoce": choice, "option": option}
        self.request = session.request("choice.php", data=data, pwd=True)

    @staticmethod
    async def parser(content: str, **kwargs) -> Choice:
        soup = BeautifulSoup(content, "html.parser")

        choice = Choice(0, [])

        for option in soup.find_all("form", action="choice.php"):
            choice_id = option.find("input", attrs={"name": "whichchoice"})["value"]
            option_id = option.find("input", attrs={"name": "option"})["value"]
            option_text = option.find("input", type="submit")["value"]

            choice.id = int(choice_id)
            choice.options += [Option(int(option_id), option_text)]

        return choice
