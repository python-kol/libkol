from libkol.request import item_description
from .test_base import TestCase


class ItemDescriptionTestCase(TestCase):
    request = "item_description"

    def test_item_description_food(self):
        async def run_test(file):
            description = await item_description.parser(file.read())

            self.assertEqual(description["id"], 333)
            self.assertEqual(description["name"], "lime")
            self.assertEqual(description["image"], "lime.gif")
            self.assertEqual(description["autosell"], 60)
            self.assertEqual(description["level_required"], 2)
            self.assertEqual(description["food"], True)
            self.assertEqual(description["booze"], False)
            self.assertEqual(description["spleen"], False)
            self.assertEqual(description["quality"], "decent")

        self.run_async("food", run_test)

    def test_item_description_hat(self):
        async def run_test(file):
            description = await item_description.parser(file.read())

            self.assertEqual(description["id"], 638)
            self.assertEqual(description["name"], "asshat")
            self.assertEqual(description["image"], "asshat.gif")
            self.assertEqual(description["autosell"], 45)
            self.assertEqual(description["food"], False)
            self.assertEqual(description["booze"], False)
            self.assertEqual(description["spleen"], False)
            self.assertEqual(description["quality"], None)
            self.assertEqual(description["hat"], True)
            self.assertEqual(description["power"], 30)

        self.run_async("hat", run_test)
