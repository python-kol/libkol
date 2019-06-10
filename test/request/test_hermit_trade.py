from libkol.Error import ItemNotFoundError, WrongKindOfItemError
from libkol.request import hermit_trade

from .test_base import TestCase


class HermitTradeTestCase(TestCase):
    request = "hermit_trade"

    def test_hermit_trade_clover(self):
        async def run_test(file):
            items = await hermit_trade.parser(file.read())
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].item.id, 24)
            self.assertEqual(items[0].quantity, 1)

        self.run_async("clover", run_test)

    def test_hermit_trade_doesnt_sell(self):
        async def run_test(file):
            try:
                await hermit_trade.parser(file.read())
            except WrongKindOfItemError:
                assert True
                return

            assert False

        self.run_async("doesnt_sell", run_test)

    def test_hermit_trade_insufficient(self):
        async def run_test(file):
            try:
                await hermit_trade.parser(file.read())
            except ItemNotFoundError as e:
                self.assertEqual(e.item, 43)
                return

            assert False

        self.run_async("insufficient", run_test)
