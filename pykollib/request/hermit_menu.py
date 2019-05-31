from typing import List

from .request import Request
from bs4 import BeautifulSoup

import pykollib

from ..Item import Item, ItemQuantity


class hermit_menu(Request):
    def __init__(self, session: "pykollib.Session") -> None:
        self.request = session.request("hermit.php")

    @staticmethod
    def parser(html: str, **kwargs) -> List[ItemQuantity]:
        soup = BeautifulSoup(html, "html.parser")

        menu = []  # type: List[ItemQuantity]
        for item_image in soup.find_all("img", class_="hand"):
            desc_id = str(item_image["onclick"])[16:-1]
            item = Item.get_or_none(desc_id=desc_id)

            if item is None:
                print("Item in {} not recognised".format(item_image))
                continue

            item_name = item_image.parent.next_sibling.contents
            stock = int(item_name[1].string[2:].split(" ")[0]) if len(item_name) > 1 else 0
            menu += [ItemQuantity(item, stock)]

        return menu
