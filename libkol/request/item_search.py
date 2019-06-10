from enum import Enum
from typing import List, Union
from bs4 import BeautifulSoup
import libkol

from ..Item import Item
from .request import Request


class Category(Enum):
    All = "allitems"
    Food = "food"
    Booze = "booze"
    OtherConsumables = "othercon"
    Weapons = "weapons"
    BackItem = "container"
    Hats = "hats"
    Shirts = "shirts"
    Pants = "pants"
    Accessories = "acc"
    OffHand = "offhand"
    FamiliarEquipment = "famequip"
    CombatItems = "combat"
    Potions = "potions"
    HpRestorers = "hprestore"
    MpRestorers = "mprestore"
    Familiars = "familiars"
    MrStore = "mrstore"
    Unlockers = "unlockers"
    New = "new"


class SortBy(Enum):
    Name = "name"
    LevelAsc = "levelreq"
    LevelDesc = "levelreqdesc"
    PowerAsc = "power"
    PowerDesc = "powerdesc"
    StatAsc = "statreq"
    StatDesc = "statreqdesc"
    Familiar = "fam"
    Price = "price"
    Stock = "stock"


class Tier(Enum):
    Crappy = 1
    Decent = 2
    Good = 3
    Awesome = 4
    Epic = 5


sortable_categories = [
    "food",
    "booze",
    "othercon",
    "hats",
    "shirts",
    "pants",
    "weapons",
    "acc",
    "offhand",
    "famequip",
]


class item_search(Request[List[Item]]):
    """
    Searches for an item by name using the mall justitems parameter

    :param session: The Pykol session
    :param query: The Item or string to search for. You can use % for a wildcard string. If you
                  supply an Item instance, it will search for exactly and only that item.
    :param category: The category to search in, such as 'food'.  The default is
                     to search in all categories.  Note the convenience constants
                     above.
    :param sort_items_by: How to sort the items listed in the output. Depending on the other
                          search parameters, not all of the possible values will be maningful.
    :param tiers: For food and booze, an array listing which quality levels to
                  include in the search results.
    :param consumable_by_me: For consumable items, whether to list only items that
                             are consumable by the session's character.
    :param weapon_attribute: For weapons, 1 to list only melee weapons, 2 to list
                             only ranged weapons, or 3 to list all weapons.
    :param weapon_hands: For weapons, 1 to list only one-handed weapons, 2 to
                         list only 2-handed weapons, or 3 to list all weapons.
    :param wearable_by_me: For wearable items, whether to list only items that can
                           be worn by the session's character.
    :param start: Not usually needed by the user. Tells which item in the list
                  of results is to be returned first.
    """

    def __init__(
        self,
        session: "libkol.Session",
        query: Union[str, Item],
        category: Category = Category.All,
        sort_items_by: SortBy = SortBy.Name,
        tiers: List[Tier] = [t for t in Tier],
        consumable_by_me: bool = False,
        weapon_attribute: int = 3,
        weapon_hands: int = 3,
        wearable_by_me: bool = False,
        start: int = 0,
    ) -> None:
        super().__init__(session)

        pudnuggler = '"{}"'.format(query.name) if isinstance(query, Item) else query

        params = {
            "didadv": 1,
            "pudnuggler": pudnuggler,
            "category": category.value,
            "consumable_byme": "1" if consumable_by_me else "0",
            "weaponattribute": weapon_attribute,
            "weaponhands": weapon_hands,
            "wearable_byme": "1" if wearable_by_me else "0",
            "justitems": "1",
            "start": start,
        }

        for cat in sortable_categories:
            if cat == category:
                params[cat + "_sortitemsby"] = sort_items_by.value
            else:
                params[cat + "_sortitemsby"] = SortBy.Name.value

        if category in ["food", "booze"]:
            for tier in Tier:
                params["consumable_tier_{}".format(tier.value)] = (
                    1 if tier in tiers else 0
                )

        self.request = session.request("mall.php", params=params)

    @staticmethod
    async def parser(content: str, **kwargs) -> List[Item]:
        soup = BeautifulSoup(content, "html.parser")

        return [
            await Item.get_or_discover(id=int(str(item["id"])[5:]))
            for item in soup.find_all("tr", id=lambda i: i and i.startswith("item_"))
        ]
