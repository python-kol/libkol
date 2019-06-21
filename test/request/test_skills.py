from libkol.request import skills
from libkol import Skill

from .test_base import TestCase


class SkillsTestCase(TestCase):
    request = "skills"

    def test_skills_lots(self):
        async def run_test(file):
            knowledge = await skills.parser(file.read(), session=self.session)
            self.assertEqual(len(knowledge), 306)
            self.assertIn(await Skill["Blood Bubble"], knowledge)

        self.run_async("lots", run_test)
