from typing import List

from bs4 import BeautifulSoup

import libkol

from ..types import ItemQuantity
from ..Item import Item
from .request import Request


class hermit_menu(Request):
    def __init__(self, session: "libkol.Session") -> None:
        self.request = session.request("hermit.php")

    @staticmethod
    async def parser(content: str, **kwargs) -> List[ItemQuantity]:
        soup = BeautifulSoup(content, "html.parser")

        menu = []  # type: List[ItemQuantity]
        for item_image in soup.find_all("img", class_="hand"):
            desc_id = str(item_image["onclick"])[16:-1]
            item = await Item.get_or_discover(desc_id=desc_id)

            if item is None:
                print("Item in {} not recognised".format(item_image))
                continue

            item_name = item_image.parent.next_sibling.contents
            stock = (
                int(item_name[1].string[2:].split(" ")[0]) if len(item_name) > 1 else 0
            )
            menu += [ItemQuantity(item, stock)]

        return menu
