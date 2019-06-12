from collections import Counter
from tortoise.models import Model

from libkol.request import charpane

from .test_base import TestCase


class CharpaneTestCase(TestCase):
    request = "charpane"

    def test_charpane_basic(self):
        async def run_test(file):
            charpane_result = await charpane.parser(file.read(), session=Model.kol)

            self.assertEqual(charpane_result["userName"], "Username")
            self.assertEqual(charpane_result["userId"], 123456)
            self.assertEqual(charpane_result["level"], 9)
            self.assertEqual(charpane_result["levelTitle"], "Disco Bandit")
            self.assertEqual(charpane_result["title"], "Disco Bandit")
            self.assertEqual(charpane_result["class"], "Disco Bandit")
            self.assertEqual(charpane_result["currentHP"], 41)
            self.assertEqual(charpane_result["maxHP"], 41)
            self.assertEqual(charpane_result["currentMP"], 37)
            self.assertEqual(charpane_result["maxMP"], 37)
            self.assertEqual(charpane_result["meat"], 0)
            self.assertEqual(charpane_result["adventures"], 200)
            self.assertEqual(charpane_result["effects"], [])
            self.assertEqual(charpane_result["buffedMuscle"], 38)
            self.assertEqual(charpane_result["baseMuscle"], 34)
            self.assertEqual(charpane_result["buffedMoxie"], 72)
            self.assertEqual(charpane_result["baseMoxie"], 68)
            self.assertEqual(charpane_result["buffedMysticality"], 37)
            self.assertEqual(charpane_result["baseMysticality"], 33)

        self.run_async("basic", run_test)

    def test_charpane_custom_title(self):
        async def run_test(file):
            charpane_result = await charpane.parser(file.read(), session=Model.kol)

            effects = [
                {"name": "Favored by Lyle", "turns": 10},
                {"name": "Hustlin'", "turns": 10},
                {"name": "init.enh", "turns": 17},
                {"name": "Brother Flying Burrito's Blessing", "turns": 20},
                {"name": "Tomes of Opportunity", "turns": 20},
                {"name": "Billiards Belligerence", "turns": 20},
                {"name": "meat.enh", "turns": 50},
                {"name": "Thaumodynamic", "turns": 50},
                {"name": "Silent Running", "turns": 50},
                {"name": "items.enh", "turns": 50},
                {"name": "There's No N in Love", "turns": 100},
            ]
            self.assertEqual(charpane_result["userName"], "Username")
            self.assertEqual(charpane_result["userId"], 123456)
            self.assertEqual(charpane_result["level"], 8)
            self.assertEqual(
                charpane_result["title"], "The Electric Kool-Aid Acid Tester"
            )
            self.assertEqual(
                charpane_result.get("levelTitle"), None
            )  # custom title gives no level title information
            self.assertEqual(charpane_result.get("class"), None)  # or class information
            self.assertEqual(charpane_result["currentHP"], 122)
            self.assertEqual(charpane_result["maxHP"], 129)
            self.assertEqual(charpane_result["currentMP"], 0)
            self.assertEqual(charpane_result["maxMP"], 151)
            self.assertEqual(charpane_result["meat"], 11418)
            self.assertEqual(charpane_result["adventures"], 13)
            self.assertEqual(charpane_result["effects"], effects)
            self.assertEqual(charpane_result["buffedMuscle"], 59)
            self.assertEqual(charpane_result["baseMuscle"], 44)
            self.assertEqual(charpane_result["buffedMoxie"], 62)
            self.assertEqual(charpane_result["baseMoxie"], 47)
            self.assertEqual(charpane_result["buffedMysticality"], 97)
            self.assertEqual(charpane_result["baseMysticality"], 62)

        self.run_async("custom_title", run_test)
