from libkol.request import charpane
from libkol import CharacterClass

from .test_base import TestCase


class CharpaneTestCase(TestCase):
    request = "charpane"

    def test_charpane_basic(self):
        async def run_test(file):
            parsed = await charpane.parser(file.read(), session=self.session)

            self.assertEqual(parsed["pwd"], "123")
            self.assertEqual(parsed["username"], "ASSistant")
            self.assertEqual(parsed["user_id"], 3270869)
            self.assertEqual(parsed["level"], 13)
            self.assertEqual(parsed["title"], "Accordion Thief")
            self.assertEqual(parsed["character_class"], CharacterClass.AccordionThief)
            self.assertEqual(parsed["current_hp"], 134)
            self.assertEqual(parsed["max_hp"], 134)
            self.assertEqual(parsed["current_mp"], 122)
            self.assertEqual(parsed["max_mp"], 122)
            self.assertEqual(parsed["meat"], 2975747)

            # self.assertEqual(parsed["drunkenness"], 0);
            self.assertEqual(
                parsed["familiar"], {"name": "Ass", "type": "Mosquito", "weight": 4}
            )

            self.assertEqual(parsed["adventures"], 200)
            self.assertEqual(parsed["base_muscle"], 118)
            self.assertEqual(parsed["buffed_muscle"], 71)
            self.assertEqual(parsed["base_moxie"], 154)
            self.assertEqual(parsed["buffed_moxie"], 77)
            self.assertEqual(parsed["base_mysticality"], 122)
            self.assertEqual(parsed["buffed_mysticality"], 61)

        self.run_async("basic", run_test)

    def test_charpane_custom_title(self):
        async def run_test(file):
            charpane_result = await charpane.parser(file.read(), session=self.session)

            effects = {
                "Favored by Lyle": 10,
                "Hustlin'": 10,
                "init.enh": 17,
                "Brother Flying Burrito's Blessing": 20,
                "Tomes of Opportunity": 20,
                "Billiards Belligerence": 20,
                "meat.enh": 50,
                "Thaumodynamic": 50,
                "Silent Running": 50,
                "items.enh": 50,
                "There's No N in Love": 100,
            }
            self.assertEqual(charpane_result["username"], "Username")
            self.assertEqual(charpane_result["user_id"], 123456)
            self.assertEqual(charpane_result["level"], 8)
            self.assertEqual(
                charpane_result["custom_title"], "The Electric Kool-Aid Acid Tester"
            )
            self.assertEqual(
                charpane_result.get("title"), None
            )  # custom title gives no level title information
            self.assertEqual(
                charpane_result.get("character_class"), None
            )  # or class information
            self.assertEqual(charpane_result["current_hp"], 122)
            self.assertEqual(charpane_result["max_hp"], 129)
            self.assertEqual(charpane_result["current_mp"], 0)
            self.assertEqual(charpane_result["max_mp"], 151)
            self.assertEqual(charpane_result["meat"], 11418)
            self.assertEqual(charpane_result["adventures"], 13)
            self.assertEqual(charpane_result["effects"], effects)
            self.assertEqual(charpane_result["buffed_muscle"], 59)
            self.assertEqual(charpane_result["base_muscle"], 44)
            self.assertEqual(charpane_result["buffed_moxie"], 62)
            self.assertEqual(charpane_result["base_moxie"], 47)
            self.assertEqual(charpane_result["buffed_mysticality"], 97)
            self.assertEqual(charpane_result["base_mysticality"], 62)

        self.run_async("custom_title", run_test)
