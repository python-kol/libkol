import pykollib.Error as Error
from .GenericRequest import GenericRequest
from pykollib.database import ItemDatabase
from pykollib.util import Report


class MallItemSearchRequest(GenericRequest):
    """
    Searches for an item at the mall.
    """

    CATEGORY_ALL = "allitems"
    CATEGORY_FOOD = "food"
    CATEGORY_BOOZE = "booze"
    CATEGORY_OTHER_CONSUMABLES = "othercon"
    CATEGORY_WEAPONS = "weapons"
    CATEGORY_BACK_ITEM = "container"
    CATEGORY_HATS = "hats"
    CATEGORY_SHIRTS = "shirts"
    CATEGORY_PANTS = "pants"
    CATEGORY_ACCESSORIES = "acc"
    CATEGORY_OFF_HAND = "offhand"
    CATEGORY_FAMILIAR_EQUIPMENT = "famequip"
    CATEGORY_COMBAT_ITEMS = "combat"
    CATEGORY_POTIONS = "potions"
    CATEGORY_HP_RESTORERS = "hprestore"
    CATEGORY_MP_RESTORERS = "mprestore"
    CATEGORY_FAMILIARS = "familiars"
    CATEGORY_MR_STORE = "mrstore"
    CATEGORY_UNLOCKERS = "unlockers"
    CATEGORY_NEW = "new"
    SORT_BY_NAME = "name"
    SORT_BY_LEVEL_ASC = "levelreq"
    SORT_BY_LEVEL_DESC = "levelreqdesc"
    SORT_BY_POWER_ASC = "power"
    SORT_BY_POWER_DESC = "powerdesc"
    SORT_BY_STAT_ASC = "statreq"
    SORT_BY_STAT_DESC = "statreqdesc"
    SORT_BY_FAMILIAR = "fam"
    SORT_BY_PRICE = "price"
    SORT_BY_STOCK = "stock"
    TIER_NAMES = ["crappy", "decent", "good", "awesome", "epic"]
    MELEE_WEAPONS = 1
    RANGED_WEAPONS = 2

    def __init__(
        self,
        session,
        searchQuery,
        category=CATEGORY_ALL,
        noLimits=False,
        maxPrice=0,
        numResults=0,
        # Below parameters added by me
        sortItemsBy=SORT_BY_NAME,
        sortShopsBy=SORT_BY_PRICE,
        justItems=False,
        tiers=TIER_NAMES,
        consumableByMe=0,
        weaponAttribute=3,
        weaponHands=3,
        wearableByMe=0,
        start=0,
    ):
        """
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

        super(MallItemSearchRequest, self).__init__(session)
        # Save parameters
        self.searchQuery = searchQuery
        self.category = category
        self.noLimits = noLimits
        self.maxPrice = maxPrice
        self.numResults = numResults
        self.sortItemsBy = sortItemsBy
        self.sortShopsBy = sortShopsBy
        self.justItems = justItems
        self.tiers = tiers
        self.start = start
        self.consumableByMe = consumableByMe
        self.weaponAttribute = weaponAttribute
        self.weaponHands = weaponHands
        self.wearableByMe = wearableByMe
        # Fill in GET request
        self.url = session.server_url + "mall.php"
        self.requestData["didadv"] = 1
        self.requestData["pudnuggler"] = searchQuery
        self.requestData["category"] = category
        for cat in [
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
        ]:
            if cat == category:
                self.requestData[cat + "_sortitemsby"] = sortItemsBy
            else:
                self.requestData[cat + "_sortitemsby"] = "name"
        self.requestData["consumable_byme"] = consumableByMe
        self.requestData["weaponattribute"] = weaponAttribute
        self.requestData["weaponhands"] = weaponHands
        self.requestData["wearable_byme"] = wearableByMe
        if noLimits:
            self.requestData["nolimits"] = "1"
        else:
            self.requestData["nolimits"] = "0"
        if justItems:
            self.requestData["justitems"] = "1"
        else:
            self.requestData["justitems"] = "0"
        self.requestData["sortresultsby"] = sortShopsBy
        self.requestData["max_price"] = maxPrice
        self.requestData["x_cheapest"] = numResults
        if category in ["food", "booze"]:
            for i in range(len(self.TIER_NAMES)):
                tiername = "consumable_tier_{0}".format(i + 1)
                if self.TIER_NAMES[i] in tiers:
                    self.requestData[tiername] = 1
                else:
                    self.requestData[tiername] = 0
        if start > 0:
            self.requestData["start"] = start

    def parseResponse(self):
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
        items = []
        itemMatchPattern = self.getPattern("mallItemSearchResult")
        itemDetailsPattern = self.getPattern("mallItemSearchDetails")
        itemHeaderPattern = self.getPattern("mallItemHeader")
        if self.justItems:
            for itemMatch in itemHeaderPattern.finditer(self.responseText):
                itemId = int(itemMatch.group(1))
                try:
                    item = ItemDatabase.getItemFromId(itemId)
                    items.append(item)
                except Error.Error as inst:
                    if inst.code == Error.ITEM_NOT_FOUND:
                        Report.info(
                            "itemdatabase",
                            "Unrecognized item found in mall search: {0}".format(
                                itemId
                            ),
                            inst,
                        )
                    else:
                        raise inst
        else:
            for itemMatch in itemMatchPattern.finditer(self.responseText):
                matchText = itemMatch.group(1)
                match = itemDetailsPattern.search(matchText)
                itemId = int(match.group("itemId"))
                try:
                    item = ItemDatabase.getItemFromId(itemId)
                    item["price"] = int(match.group("price").replace(",", ""))
                    item["storeId"] = int(match.group("storeId"))
                    storeName = match.group("storeName").replace("<br>", " ")
                    item["storeName"] = self.HTML_PARSER.unescape(storeName)
                    item["quantity"] = int(match.group("quantity").replace(",", ""))
                    limit = match.group("limit").replace(",", "")
                    if len(limit) > 0:
                        limit = int(limit)
                        item["limit"] = limit
                    if matchText.find('limited"') >= 0:
                        item["hitLimit"] = True
                    items.append(item)
                except Error.Error as inst:
                    if inst.code == Error.ITEM_NOT_FOUND:
                        Report.info(
                            "itemdatabase",
                            "Unrecognized item found in mall search: {0}".format(
                                itemId
                            ),
                            inst,
                        )
                    else:
                        raise inst
        nextlink = self.searchNamedPattern("nextLink")
        if nextlink is not None:
            # There's more.  We have to collect the info from subsequent pages.
            nextRequest = MallItemSearchRequest(
                session=self.session,
                searchQuery=self.searchQuery,
                category=self.category,
                noLimits=self.noLimits,
                maxPrice=self.maxPrice,
                numResults=self.numResults,
                sortBy=self.sortBy,
                sortResultsBy=self.sortResultsBy,
                justItems=self.justItems,
                tiers=self.tiers,
                consumableByMe=self.consumableByMe,
                weaponAttribute=self.weaponAttribute,
                weaponHands=self.weaponHands,
                wearableByMe=self.wearableByMe,
                start=nextlink.group(1),
            )
            resp = nextRequest.doRequest()
            items = items + resp["results"]
            self.responseText = self.responseText + nextRequest.responseText

        self.responseData["results"] = items
