from .test_base import TestCase
from ...request.hermit_trade import parse
from ...Error import WrongKindOfItemError, ItemNotFoundError


class HermitTradeTestCase(TestCase):
    request = "hermit_trade"

    def test_hermit_trade_clover(self):
        with self.open_test_data("clover") as file:
            items = parse(file.read())
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].item.id, 24)
            self.assertEqual(items[0].quantity, 1)

    def test_hermit_trade_doesnt_sell(self):
        with self.open_test_data("doesnt_sell") as file:
            try:
                parse(file.read())
            except WrongKindOfItemError:
                assert True
                return

            assert False

    def test_hermit_trade_insufficient(self):
        with self.open_test_data("insufficient") as file:
            try:
                parse(file.read())
            except ItemNotFoundError as e:
                self.assertEqual(e.item, 43)
                return

            assert False
