from yarl import URL

from .test_base import TestCase
from pykollib.request import craft
from pykollib.Error import ItemNotFoundError, RecipeNotFoundError


class CraftTestCase(TestCase):
    request = "craft"

    def test_craft_combine_meatpaste_error(self):
        url = URL.build(query={"mode": "combine"})

        with self.open_test_data("combine_meatpaste_error") as file:
            try:
                craft.parser(file.read(), url=url)
            except ItemNotFoundError:
                assert True
                return

            assert False

    def test_craft_cook_recipe_error(self):
        url = URL.build(query={"mode": "cook"})

        with self.open_test_data("cook_recipe_error") as file:
            try:
                craft.parser(file.read(), url=url)
            except RecipeNotFoundError:
                assert True
                return

            assert False
