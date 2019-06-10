from libkol.request import mall_search

from .test_base import TestCase


class MallSearchTestCase(TestCase):
    request = "mall_search"

    def test_mall_search_lime(self):
        async def run_test(file):
            listings = await mall_search.parser(file.read())
            self.assertEqual(len(listings), 174)

        self.run_async("lime", run_test)

    def test_mall_search_limited_include(self):
        async def run_test(file):
            listings = await mall_search.parser(file.read(), include_limit_reached=True)
            self.assertEqual(listings[3].limit_reached, True)

        self.run_async("limited", run_test)

    def test_mall_search_limited_exclude(self):
        async def run_test(file):
            listings = await mall_search.parser(file.read())
            self.assertEqual(listings[3].limit_reached, False)

        self.run_async("limited", run_test)
