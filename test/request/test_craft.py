from yarl import URL

from libkol.Error import ItemNotFoundError, RecipeNotFoundError
from libkol.request import craft

from .test_base import TestCase


class CraftTestCase(TestCase):
    request = "craft"

    def test_craft_combine_meatpaste_error(self):
        async def run_test(file):
            url = URL.build(query={"mode": "combine"})
            try:
                await craft.parser(file.read(), url=url)
            except ItemNotFoundError:
                assert True
                return

            assert False

        self.run_async("combine_meatpaste_error", run_test)

    def test_craft_cook_recipe_error(self):
        async def run_test(file):
            url = URL.build(query={"mode": "cook"})
            try:
                await craft.parser(file.read(), url=url)
            except RecipeNotFoundError:
                assert True
                return

            assert False

        self.run_async("cook_recipe_error", run_test)
