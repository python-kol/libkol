from pykollib.request import mall_price

from .test_base import TestCase


class MallSearchPriceTestCase(TestCase):
    request = "mall_price"

    def test_mall_price_basic(self):
        async def run_test(file):
            r = await mall_price.parser(file.read())
            self.assertEqual(len(r), 2)
            self.assertEqual(len(r.unlimited), 4)
            self.assertEqual(len(r.limited), 3)

        self.run_async("basic", run_test)

    def test_mall_price_commas(self):
        """
        Only the cost gets commas, never the limit or stock
        """
        async def run_test(file):
            r = await mall_price.parser(file.read())
            self.assertEqual(len(r), 2)
            self.assertEqual(len(r.unlimited), 4)
            self.assertEqual(len(r.limited), 1)

        self.run_async("commas", run_test)
