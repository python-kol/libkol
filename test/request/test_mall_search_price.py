from .test_base import TestCase
from pykollib.request import mall_search_price


class MallSearchPriceTestCase(TestCase):
    request = "mall_search_price"

    def test_mall_search_price_basic(self):
        with self.open_test_data("basic") as file:
            r = mall_search_price.parser(file.read())
            self.assertEqual(len(r), 2)
            self.assertEqual(len(r.unlimited), 4)
            self.assertEqual(len(r.limited), 3)

    def test_mall_search_price_commas(self):
        """
        Only the cost gets commas, never the limit or stock
        """
        with self.open_test_data("commas") as file:
            r = mall_search_price.parser(file.read())
            self.assertEqual(len(r), 2)
            self.assertEqual(len(r.unlimited), 4)
            self.assertEqual(len(r.limited), 1)
