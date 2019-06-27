from libkol.request import charpane
from libkol import CharacterClass, Stat
from libkol.Session import State

from .test_base import TestCase


class CharpaneTestCase(TestCase):
    request = "charpane"

    def test_charpane_basic(self):
        async def run_test(file):
            result = await charpane.parser(file.read(), session=self.session)

            state = self.session.state

            self.assertEqual(result, True)
            self.assertEqual(state.pwd, "123")
            self.assertEqual(state.username, "ASSistant")
            self.assertEqual(state.user_id, 3270869)
            self.assertEqual(state.level, 13)
            self.assertEqual(state.title, "Accordion Thief")
            self.assertEqual(state.character_class, CharacterClass.AccordionThief)
            self.assertEqual(state.current_hp, 134)
            self.assertEqual(state.max_hp, 134)
            self.assertEqual(state.current_mp, 122)
            self.assertEqual(state.max_mp, 122)
            self.assertEqual(state.meat, 2975747)
            self.assertEqual(state.inebriety, 0)
            self.assertGreaterEqual(state.familiar, "Mosquito")
            self.assertEqual(state.familiars[state.familiar].nickname, "Ass")
            self.assertEqual(state.familiars[state.familiar].weight, 4)
            self.assertEqual(state.adventures, 200)
            self.assertEqual(state.stats[Stat.Muscle].base, 118)
            self.assertEqual(state.stats[Stat.Muscle].buffed, 71)
            self.assertEqual(state.stats[Stat.Moxie].base, 154)
            self.assertEqual(state.stats[Stat.Moxie].buffed, 77)
            self.assertEqual(state.stats[Stat.Mysticality].base, 122)
            self.assertEqual(state.stats[Stat.Mysticality].buffed, 61)

        self.run_async("basic", run_test)

    def test_charpane_custom_title(self):
        async def run_test(file):
            self.session.state = State()

            result = await charpane.parser(file.read(), session=self.session)

            state = self.session.state

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

            self.assertEqual(result, True)
            self.assertEqual(state.username, "Username")
            self.assertEqual(state.user_id, 123456)
            self.assertEqual(state.level, 8)
            self.assertEqual(state.custom_title, "The Electric Kool-Aid Acid Tester")
            self.assertEqual(
                state.title, None
            )  # custom title gives no level title information
            self.assertEqual(state.character_class, None)  # or class information
            self.assertEqual(state.current_hp, 122)
            self.assertEqual(state.max_hp, 129)
            self.assertEqual(state.current_mp, 0)
            self.assertEqual(state.max_mp, 151)
            self.assertEqual(state.meat, 11418)
            self.assertEqual(state.adventures, 13)
            self.assertEqual(state.effects, effects)
            self.assertEqual(state.stats[Stat.Muscle].buffed, 59)
            self.assertEqual(state.stats[Stat.Muscle].base, 44)
            self.assertEqual(state.stats[Stat.Moxie].buffed, 62)
            self.assertEqual(state.stats[Stat.Moxie].base, 47)
            self.assertEqual(state.stats[Stat.Mysticality].buffed, 97)
            self.assertEqual(state.stats[Stat.Mysticality].base, 62)

        self.run_async("custom_title", run_test)
