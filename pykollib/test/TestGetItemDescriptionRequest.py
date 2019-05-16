from . import TestData
from pykollib.old_database import ItemDatabase
from pykollib.request.ItemDescriptionRequest import ItemDescriptionRequest

import unittest


class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]

        item = ItemDatabase.getItemFromName("olive")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEqual(itemData["isCookingIngredient"], True)
        self.assertEqual(itemData["isCocktailcraftingIngredient"], True)
        self.assertEqual(itemData["image"], "olive.gif")
        self.assertEqual(itemData["autosell"], 35)
        self.assertEqual(itemData["type"], "food")

        item = ItemDatabase.getItemFromName("furry fur")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEqual(itemData["isMeatsmithingComponent"], True)
        self.assertEqual(itemData["image"], "furfur.gif")
        self.assertEqual(itemData["autosell"], 129)

        item = ItemDatabase.getItemFromName("baconstone")
        r = ItemDescriptionRequest(s, item["descId"])
        itemData = r.doRequest()
        self.assertEqual(itemData["image"], "baconstone.gif")
        self.assertEqual(itemData["autosell"], 500)

        # Test a haiku item -- these description pages are formatted differently.
        r = ItemDescriptionRequest(s, 435365663)
        itemData = r.doRequest()
        self.assertEqual(itemData["name"], "little round pebble")
        self.assertEqual(itemData["autosell"], 45)
        self.assertEqual(itemData["type"], "off-hand item")
