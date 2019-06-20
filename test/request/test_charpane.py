from libkol import CharacterClass
from libkol.request import charpane

from .test_base import TestCase


class CharpaneTestCase(TestCase):
    request = "charpane"

    def test_charpane_basic(self):
        async def run_test(file):
            parsed = await charpane.parser(file.read(), session=self.session)

            self.assertEqual(parsed["pwd"], "123");
            self.assertEqual(parsed["username"], "ASSistant");
            self.assertEqual(parsed["user_id"], 3270869);
            self.assertEqual(parsed["level"], 13);
            self.assertEqual(parsed["level_title"], "Accordion Thief");
            self.assertEqual(parsed["character_class"], CharacterClass.AccordionThief);
            self.assertEqual(parsed["current_hP"], 134);
            self.assertEqual(parsed["max_hp"], 134);
            self.assertEqual(parsed["current_mp"], 122);
            self.assertEqual(parsed["max_mp"], 122);
            self.assertEqual(parsed["meat"], 2975747);

            # self.assertEqual(parsed["drunkenness"], 0);
            self.assertEqual(parsed["familiar"], {
                "name": "Ass",
                "type": "Mosquito",
                "weight": 4,
            })

            self.assertEqual(parsed["adventures"], 200)
            self.assertEqual(parsed["base_muscle"], 71)
            self.assertEqual(parsed["buffed_muscle"], 118)
            self.assertEqual(parsed["base_moxie"], 77)
            self.assertEqual(parsed["buffed_moxie"], 154)
            self.assertEqual(parsed["base_mysticality"], 61)
            self.assertEqual(parsed["buffed_mysticality"], 122)

        self.run_async("basic", run_test)
