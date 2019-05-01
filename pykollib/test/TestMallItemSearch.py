from . import TestData
from pykollib.request.MallItemSearchRequest import MallItemSearchRequest
import unittest


def printResults(response):
    """
    Print the Mall item search results from the response in a nice human-readable
    format.
    """
    results = response["results"]
    currentItemName = None
    for item in results:
        if currentItemName != item["name"]:
            currentItemName = item["name"]
            print(("==== {0} ====".format(currentItemName)))
        if "storeName" in item:
            limit = None
            if "limit" in item:
                limit = item["limit"]
            storeName = item["storeName"]
            if len(storeName) > 47:
                storeName = storeName[0:47] + "..."
            print(
                (
                    "  {0:50} {1:6} {2:>5} {3:10}".format(
                        storeName, item["quantity"], limit, item["price"]
                    )
                )
            )
    print(("{0} results found.".format(len(results))))
    print("")


def countShops(response):
    """
    Given a response for a single item, return how many shop-item combinations 
    are present.
    """
    return len(response["results"])


def isOrderedBy(field, response):
    """
    Given a response for a single item, return whether the shops are ordered
    by the specified field ('price' or 'stock').
    """
    if field == "price":
        previous = -1
    elif field == "stock":
        previous = 1000000000
    for shopItem in response["results"]:
        if field == "price":
            if shopItem["price"] < previous:
                return False
            if shopItem["price"] > previous:
                previous = shopItem["price"]
        elif field == "stock":
            if shopItem["quantity"] > previous:
                return False
            if shopItem["quantity"] < previous:
                previous = shopItem["quantity"]
        else:
            return False
    return True


def hasLimits(response):
    """
    Return whether the list of item-shop combos has a shop with purchase limits.
    """
    for shopItem in response["results"]:
        if "limit" in shopItem and shopItem["limit"] > 0:
            return True
    return False


def findPriceGap(response):
    """
    Return a tuple giving the location of a gap in prices between item-shop 
    combos, and a value that falls inside the gap.  This can be used to test 
    searching with a maximum price.
    """
    previous = response["results"][0]["price"]
    countBelowGap = 1
    for shopItem in response["results"][1:]:
        if shopItem["price"] - previous > 2:
            return (countBelowGap, previous + 1)
        countBelowGap = countBelowGap + 1
    return None


class Main(unittest.TestCase):
    def assertItemCount(self, response, target, what):
        """
        Given a response with items or item-shop combos in it and a target number,
        asserts that the number of results in the response is equal to the target,
        and causes an appropriate message to be raised if not.
        """
        self.assertEqual(
            target,
            len(response["results"]),
            "Expected {0} {1}, got {2}".format(target, what, len(response["results"])),
        )

    def runTest(self):
        s = TestData.data["session"]

        MISR = MallItemSearchRequest  # Tired of writing MallItemSearchRequest

        # Look up tiny barrel, ordered by price
        misr = MISR(s, "tiny barrel")
        response = misr.doRequest()
        countBelowGap, priceLimit = findPriceGap(response)
        self.assertTrue(
            isOrderedBy("price", response),
            "Results for tiny barrel not ordered by ascending price",
        )
        self.assertTrue(
            hasLimits(response), "Need shops with limits for the next test to work"
        )

        # Look up tiny barrel without limits
        misr = MISR(s, "tiny barrel", noLimits=True)
        response = misr.doRequest()
        self.assertFalse(
            hasLimits(response), "Search failed to eliminate shops with limits"
        )

        # Look up tiny barrel with price limit
        misr = MISR(s, "tiny barrel", maxPrice=priceLimit)
        response = misr.doRequest()
        self.assertTrue(
            countBelowGap == len(response["results"]),
            "Expected {0} items below ${1}, found {2}".format(
                countBelowGap, priceLimit, len(response["results"])
            ),
        )

        # Look up tiny barrel with limited number of results
        misr = MISR(s, "tiny barrel", numResults=7)
        response = misr.doRequest()
        self.assertItemCount(response, 7, "tiny barrel results")

        # Look up tiny barrel sorted by stock
        misr = MISR(s, "tiny barrel", sortShopsBy=MISR.SORT_BY_STOCK)
        response = misr.doRequest()
        self.assertTrue(
            isOrderedBy("stock", response),
            "Results for tiny barrel not ordered by descending stock",
        )

        # Look up Misty among back items, no stores
        misr = MISR(s, "misty", category=MISR.CATEGORY_BACK_ITEM, justItems=True)
        response = misr.doRequest()
        self.assertItemCount(response, 3, "Misty back items (items only)")

        # Look up katana and count items
        misr = MISR(s, "katana", justItems=True)
        response = misr.doRequest()
        self.assertItemCount(response, 6, "katana items")

        # Look up katana among weapons
        misr = MISR(s, "katana", justItems=True, category=MISR.CATEGORY_WEAPONS)
        response = misr.doRequest()
        self.assertItemCount(response, 3, "katana weapon items")

        # Look up katana among weapons filtered by 1-hand
        misr = MISR(
            s, "katana", justItems=True, category=MISR.CATEGORY_WEAPONS, weaponHands=1
        )
        response = misr.doRequest()
        self.assertItemCount(response, 2, "katana one-handed weapon items")

        # Look up katana among weapons filtered by 2-hand
        misr = MISR(
            s, "katana", justItems=True, category=MISR.CATEGORY_WEAPONS, weaponHands=2
        )
        response = misr.doRequest()
        self.assertItemCount(response, 1, "katana two-handed weapon item")

        # Look up bow, filter for weapon
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_WEAPONS)
        response = misr.doRequest()
        self.assertItemCount(response, 26, "bow weapon items")

        # Look up bow, filter for melee
        misr = MISR(
            s,
            "bow",
            justItems=True,
            category=MISR.CATEGORY_WEAPONS,
            weaponAttribute=MISR.MELEE_WEAPONS,
        )
        response = misr.doRequest()
        self.assertItemCount(response, 1, "bow melee weapon items")

        # Look up bow, filter for ranged
        misr = MISR(
            s,
            "bow",
            justItems=True,
            category=MISR.CATEGORY_WEAPONS,
            weaponAttribute=MISR.RANGED_WEAPONS,
        )
        response = misr.doRequest()
        self.assertItemCount(response, 25, "bow ranged weapon items")

        # Look up bow, filter for food
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_FOOD)
        response = misr.doRequest()
        self.assertItemCount(response, 11, "bow food items")

        # Look up bow, filter for booze
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_BOOZE)
        response = misr.doRequest()
        self.assertItemCount(response, 4, "bow booze items")

        # Look up bow, filter for hats
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_HATS)
        response = misr.doRequest()
        self.assertItemCount(response, 2, "bow hat items")

        # Look up bow, filter for pants
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_PANTS)
        response = misr.doRequest()
        self.assertItemCount(response, 1, "bow pants items")

        # Look up bow, filter for accessories
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_ACCESSORIES)
        response = misr.doRequest()
        self.assertItemCount(response, 9, "bow accessory items")

        # Look up bow, filter for off-hand
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_OFF_HAND)
        response = misr.doRequest()
        self.assertItemCount(response, 2, "bow off-hand items")

        # Look up bow, filter for familiar equipment
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_FAMILIAR_EQUIPMENT)
        response = misr.doRequest()
        self.assertItemCount(response, 9, "bow familiar equipment items")

        # Look up bow, filter for combat items
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_COMBAT_ITEMS)
        response = misr.doRequest()
        self.assertItemCount(response, 2, "bow combat items")

        # Look up bow, filter for potions
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_POTIONS)
        response = misr.doRequest()
        self.assertItemCount(response, 4, "bow potion items")

        # Look up bow, filter for familiars
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_FAMILIARS)
        response = misr.doRequest()
        self.assertItemCount(response, 2, "bow familiar items")

        # Look up bow, filter for Mr. Store items
        misr = MISR(s, "bow", justItems=True, category=MISR.CATEGORY_MR_STORE)
        response = misr.doRequest()
        self.assertItemCount(response, 2, "bow Mr. Store items")

        # Look up z among shirts
        misr = MISR(s, "z", justItems=True, category=MISR.CATEGORY_SHIRTS)
        response = misr.doRequest()
        self.assertItemCount(response, 1, "z shirt items")

        # Look up w among HP restorers
        misr = MISR(s, "w", justItems=True, category=MISR.CATEGORY_HP_RESTORERS)
        response = misr.doRequest()
        self.assertItemCount(response, 4, "w HP restorer items")

        # Look up w among MP restorers
        misr = MISR(s, "w", justItems=True, category=MISR.CATEGORY_MP_RESTORERS)
        response = misr.doRequest()
        self.assertItemCount(response, 9, "w MP restorer items")

        # Look up charter among content unlockers
        misr = MISR(s, "charter", justItems=True, category=MISR.CATEGORY_UNLOCKERS)
        response = misr.doRequest()
        self.assertItemCount(response, 3, "charter unlocker items")

        # Search for all wines
        misr = MISR(s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE)
        response = misr.doRequest()
        self.assertItemCount(response, 56, "wines")

        # Search for crappy wines
        misr = MISR(
            s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE, tiers=["crappy"]
        )
        response = misr.doRequest()
        self.assertItemCount(response, 2, "crappy wines")

        # Search for decent wines
        misr = MISR(
            s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE, tiers=["decent"]
        )
        response = misr.doRequest()
        self.assertItemCount(response, 8, "decent wines")

        # Search for good wines
        misr = MISR(
            s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE, tiers=["good"]
        )
        response = misr.doRequest()
        self.assertItemCount(response, 15, "good wines")

        # search for awesome wines
        misr = MISR(
            s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE, tiers=["awesome"]
        )
        response = misr.doRequest()
        self.assertItemCount(response, 21, "awesome wines")

        # search for epic wines
        misr = MISR(
            s, "wine", justItems=True, category=MISR.CATEGORY_BOOZE, tiers=["epic"]
        )
        response = misr.doRequest()
        self.assertItemCount(response, 10, "epic wines")

        # search for combination of the best wines
        misr = MISR(
            s,
            "wine",
            justItems=True,
            category=MISR.CATEGORY_BOOZE,
            tiers=["good", "awesome", "epic"],
        )
        response = misr.doRequest()
        self.assertItemCount(response, 46, "worthwhile (good, awesome, epic) wines")
