from enum import Enum
from typing import List, NamedTuple

from bs4 import BeautifulSoup
from yarl import URL

import pykollib

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


class Listing(NamedTuple):
    item: Item
    price: int
    store_id: int
    store_name: str
    stock: int
    limit: int


class mall_search(Request):
    """
    Searches for an item at the mall

    :param session: The Pykol session
    :param query: The string to search for.  You can use % for a wildca:param d
    :param category: The category to search in, such as 'food'.  The default is
                     to search in all categories.  Note the convenience constants
                     above.
    :param no_limits: Whether to exclude shops that have daily purchase limits.
    :param max_price: The maximum price to show.  Defaults to 0, which shows all
                      prices.
    :param num_results: The number of shops to show per item.  The default is 0,
                        which shows a number of shops depending on the number of items
                        returned.
    :param sort_items_by: How to sort the items listed in the output. Depending on the other
                          search parameters, not all of the possible values will be maningful.
    :param sort_shops_by: How to sort the shops within each individual item.
    :param just_items: Whether to suppress the shops and just show a list of items.
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
        session: "pykollib.Session",
        query: str,
        category: Category = Category.All,
        no_limits: bool = False,
        max_price: int = 0,
        num_results: int = 0,
        sort_items_by: SortBy = SortBy.Name,
        sort_shops_by: SortBy = SortBy.Price,
        just_items: bool = False,
        tiers: List[Tier] = [t for t in Tier],
        consumable_by_me: bool = False,
        weapon_attribute: int = 3,
        weapon_hands: int = 3,
        wearable_by_me: bool = False,
        start: int = 0,
    ) -> None:
        super().__init__(session)

        params = {
            "didadv": 1,
            "pudnuggler": query,
            "category": category.value,
            "consumable_byme": "1" if consumable_by_me else "0",
            "weaponattribute": weapon_attribute,
            "weaponhands": weapon_hands,
            "wearable_byme": "1" if wearable_by_me else "0",
            "nolimits": "1" if no_limits else "0",
            "justitems": "1" if just_items else "0",
            "sortresultsby": sort_shops_by.value,
            "max_price": max_price,
            "x_cheapest": num_results,
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
    def parser(html: str, url: URL, **kwargs) -> List[Listing]:
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr", id=lambda i: i and i.startswith("stock_"))

        if len(rows) == 0:
            return [
                Item[int(str(item["id"])[5:])]
                for item in soup.find_all(
                    "tr", id=lambda i: i and i.startswith("item_")
                )
            ]

        return [
            Listing(
                Item[int(url.query["searchitem"])],
                int(url.query["searchprice"]),
                int(url.query["whichstore"]),
                store_name,
                int(stock.replace(",", "")),
                (
                    0
                    if limit == "\xa0"
                    else int(limit.replace("\xa0", "").replace("/day", ""))
                ),
            )
            for url, store_name, stock, limit in (
                (
                    URL(row.contents[1].a["href"]),
                    row.contents[1].a.string,
                    row.contents[2].string,
                    row.contents[3].string,
                )
                for row in rows
            )
        ]


""" NOTES ON THE KOL MALL SEARCH PARAMETERS:
category: One of food,booze,othercon,weapons,hats,shirts,container,
    pants,acc,offhand,famequip,combat,potions,hprestore,mprestore,familiars,
    mrstore,unlockers,new
food_sortitemsby (food)
    name
    levelreq (level requirement)
    levelreqdesc (highest to lowest)
booze_sortitemsby (booze)
    name
    levelreq (level requirement)
    levelreqdesc (highest to lowest)
othercon_sortitemsby (othercon)
    name
    levelreq (level requirement)
    levelreqdesc (highest to lowest)
consumable_byme (0 or 1) (food, booze, othercon)
hats_sortitemsby (hats)
    name
    power
    powerdesc
    statreq
    statreqdesc
shirts_sortitemsby (shirts)
    name
    power
    powerdesc
    statreq
    statreqdesc
pants_sortitemsby (pants)
    name
    power
    powerdesc
    statreq
    statreqdesc
weapons_sortitemsby (weapons)
    name
    power
    powerdesc
    statreq
    statreqdesc
weaponattribute (weapons)
    1: melee, 2: ranged, 3: both
weaponhands (weapons)
    1, 2, 3: both
acc_sortitemsby (accessories)
    name
    statreq
    statreqdesc
offhand_sortitemsby (offhand)
    name
    statreq
    statreqdesc
wearable_byme (shirts hats weapons pants accessories offhand)
famequip_sortitemsby (famequip)
    name
    fam (applicable familiar)
nolimits (0 or 1)
justitems (0 or 1)
sortresultsby
    price (lowest to highest)
    stock (highest to lowest)
max_price
x_cheapest
consumable_tier_1 (0 or 1) (crappy)
consumable_tier_2 (0 or 1) (decent)
consumable_tier_3 (0 or 1) (good)
consumable_tier_4 (0 or 1) (awesome)
consumable_tier_5 (0 or 1) (epic)
"""
