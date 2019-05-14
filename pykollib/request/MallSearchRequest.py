from enum import Enum
from yarl import URL
from bs4 import BeautifulSoup
from pykollib.Error import Error, ItemNotFoundError
from pykollib.database import ItemDatabase


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


MELEE_WEAPONS = 1
RANGED_WEAPONS = 2

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


def parse(html: str, **kwargs):
    """
    Returns a dict in which 'results' references an array of dicts.  If the
    search included items only, each dict would have the following item keys:
        descId (always)
        id (always)
        image (always)
        name (always)
    and sometime, depending on the kind of item,
        adventuresGained
        autosell
        drunkenness
        fullness
        isBounty
        isCandy
        isCombatReusable
        isCombatUsable
        isMultiUsable
        isReusable
        isSphere
        isUsable
        isUsableOnOthers
        isZappable
        moxieGained
        muscleGained
        mysticalityGained
        npcPrice
        npcStoreId
        numPackageItems
        plural
        power
        quality
        requiredMoxie
        requiredMuscle
        requiredMysticality
        spleen
        type
    If the search included shops, the dicts would have the following
    additional keys:
        hitLimit (if the item's limit has been hit by the session character)
        limit (if the item is limited per day)
        price
        quantity
        storeId
        storeName
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr", id=lambda i: i and i.startswith("stock_"))

    if len(rows) == 0:
        return [
            ItemDatabase.getItemFromId(int(item["id"][5:]))
            for item in soup.find_all("tr", id=lambda i: i and i.startswith("item_"))
        ]

    return [
        {
            **ItemDatabase.getItemFromId(int(url.query["searchitem"])),
            "price": int(url.query["searchprice"]),
            "store_id": int(url.query["whichstore"]),
            "store_name": store_name,
            "stock": int(stock.replace(",", "")),
            "limit": 0
            if limit == "\xa0"
            else int(limit.replace("\xa0", "").replace("/day", "")),
        }
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


def mallSearchRequest(
    session,
    searchQuery,
    category=Category.All,
    noLimits=False,
    maxPrice=0,
    numResults=0,
    sortItemsBy=SortBy.Name,
    sortShopsBy=SortBy.Price,
    justItems=False,
    tiers=[t for t in Tier],
    consumableByMe=0,
    weaponAttribute=3,
    weaponHands=3,
    wearableByMe=0,
    start=0,
):
    """
    Searches for an item at the mall
    Arguments:
        session: The Pykol session
        searchQuery: The string to search for.  You can use % for a wildcard.
        category: The category to search in, such as 'food'.  The default is
            to search in all categories.  Note the convenience constants
            above.
        noLimits: Whether to exclude shops that have daily purchase limits.
            Defaults to False.
        maxPrice: The maximum price to show.  Defaults to 0, which shows all
            prices.
        numResults: The number of shops to show per item.  The default is 0,
            which shows a number of shops depending on the number of items
            returned.
        sortItemsBy: How to sort the items listed in the output.  Can be 'name'
            (the default), 'levelreq', 'levelreqdesc', 'power', 'powerdesc',
            'statreq', 'statreqdesc', or 'fam'.  Depending on the other
            search parameters, not all of these values will be maningful.
        sortShopsBy: How to sort the shops within each individual item.
            Can be 'price' (the default) or 'stock'.
        justItems: Whether to suppress the shops and just show a list of items.
            Defaults to False.
        tiers: For food and booze, an array listing which quality levels to
            include in the search results.  Each item in the array can be one
            of 'crappy', 'decent', 'good', 'awesome', and 'epic'.  Defaults
            to an array of all five qualities.
        consumableByMe: For consumable items, whether to list only items that
            are consumable by the session's character.  Defaults to False.
        weaponAttribute: For weapons, 1 to list only melee weapons, 2 to list
            only ranged weapons, or 3 (the default) to list all weapons.
        weaponHands: For weapons, 1 to list only one-handed weapons, 2 to
            list only 2-handed weapons, or 3 (the default) to list all weapons.
        wearableByMe: For wearable items, whether to list only items that can
            be worn by the session's character.  Defaults to False.
        start: Not usually needed by the user.  Tells which item in the list
            of results is to be returned first.  Defaults to 0 (the first item).
    """

    # NOTES ON THE KOL MALL SEARCH PARAMETERS:
    # category: One of food,booze,othercon,weapons,hats,shirts,container,
    #     pants,acc,offhand,famequip,combat,potions,hprestore,mprestore,familiars,
    #     mrstore,unlockers,new
    # food_sortitemsby (food)
    #     name
    #     levelreq (level requirement)
    #     levelreqdesc (highest to lowest)
    # booze_sortitemsby (booze)
    #     name
    #     levelreq (level requirement)
    #     levelreqdesc (highest to lowest)
    # othercon_sortitemsby (othercon)
    #     name
    #     levelreq (level requirement)
    #     levelreqdesc (highest to lowest)
    # consumable_byme (0 or 1) (food, booze, othercon)
    # hats_sortitemsby (hats)
    #     name
    #     power
    #     powerdesc
    #     statreq
    #     statreqdesc
    # shirts_sortitemsby (shirts)
    #     name
    #     power
    #     powerdesc
    #     statreq
    #     statreqdesc
    # pants_sortitemsby (pants)
    #     name
    #     power
    #     powerdesc
    #     statreq
    #     statreqdesc
    # weapons_sortitemsby (weapons)
    #     name
    #     power
    #     powerdesc
    #     statreq
    #     statreqdesc
    # weaponattribute (weapons)
    #     1: melee, 2: ranged, 3: both
    # weaponhands (weapons)
    #     1, 2, 3: both
    # acc_sortitemsby (accessories)
    #     name
    #     statreq
    #     statreqdesc
    # offhand_sortitemsby (offhand)
    #     name
    #     statreq
    #     statreqdesc
    # wearable_byme (shirts hats weapons pants accessories offhand)
    # famequip_sortitemsby (famequip)
    #     name
    #     fam (applicable familiar)
    # nolimits (0 or 1)
    # justitems (0 or 1)
    # sortresultsby
    #     price (lowest to highest)
    #     stock (highest to lowest)
    # max_price
    # x_cheapest
    # consumable_tier_1 (0 or 1) (crappy)
    # consumable_tier_2 (0 or 1) (decent)
    # consumable_tier_3 (0 or 1) (good)
    # consumable_tier_4 (0 or 1) (awesome)
    # consumable_tier_5 (0 or 1) (epic)

    params = {
        "didadv": 1,
        "pudnuggler": searchQuery,
        "category": category.value,
        "consumable_byme": consumableByMe,
        "weaponattribute": weaponAttribute,
        "weaponhands": weaponHands,
        "wearable_byme": wearableByMe,
        "nolimits": "1" if noLimits else "0",
        "justitems": "1" if justItems else "0",
        "sortresultsby": sortShopsBy.value,
        "max_price": maxPrice,
        "x_cheapest": numResults,
        "start": start,
    }

    for cat in sortable_categories:
        if cat == category:
            params[cat + "_sortitemsby"] = sortItemsBy.value
        else:
            params[cat + "_sortitemsby"] = SortBy.Name.value

    if category in ["food", "booze"]:
        for tier in Tier:
            params["consumable_tier_{}".format(tier.value)] = 1 if tier in tiers else 0

    return session.request("mall.php", params=params, parse=parse)
