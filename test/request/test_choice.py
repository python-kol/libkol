from libkol.request import choice
from .test_base import TestCase


class ChoiceTestCase(TestCase):
    request = "choice"

    def test_choice_shore(self):
        async def run_test(file):
            c = await choice.parser(file.read(), session=self.session)
            self.assertEqual(c.id, 793)
            self.assertEqual(len(c.options), 4)
            self.assertEqual(c.options[0].id, 1)
            self.assertEqual(c.options[0].text, "Distant Lands Dude Ranch Adventure")

        self.run_async("shore", run_test)
