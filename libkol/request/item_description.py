from bs4 import BeautifulSoup, Comment
from yarl import URL
from typing import Optional, List

from ..util import parsing
from .request import Request


class item_description(Request):
    """
    Gets the description of an item and then parses various information from the response.
    """

    def __init__(self, session, descid):
        super().__init__(session)

        params = {"whichitem": descid}

        self.request = session.request("desc_item.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs):
        soup = BeautifulSoup(content, "html.parser")

        container = soup.find(id="description")
        main = container.blockquote
        lines = parsing.split_by_br(container.blockquote)

        id = int(main.find(string=lambda text: isinstance(text, Comment))[9:])
        name = container.center.img["alt"]
        image = URL(container.center.img["src"]).parts[-1]
        autosell = next(
            (
                int(line[1].string.split(" ")[0].replace(",", ""))
                for line in lines
                if line[0] == "Selling Price: "
            ),
            None,
        )
        level_required = next(
            (int(line[1].string) for line in lines if line[0] == "Level required: "),
            None,
        )
        type: Optional[List[str]] = next(
            (line[1].string.split(" ") for line in lines if line[0] == "Type: "), None
        )
        power = next(
            (int(line[1].string) for line in lines if line[0] == "Power: "), None
        )

        food = type and type[0] == "food"
        booze = type and type[0] == "booze"
        spleen = type and type[0] == "spleen"

        return {
            "id": id,
            "name": name,
            "image": image,
            "autosell": autosell,
            "level_required": level_required,
            "food": food,
            "booze": booze,
            "spleen": spleen,
            "quality": type[1][1:-1] if type and (food or booze or spleen) else None,
            "hat": type and type[0] == "hat",
            "power": power,
        }
