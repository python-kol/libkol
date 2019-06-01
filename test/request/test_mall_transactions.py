from pykollib.request import mall_transactions

from .test_base import TestCase


class MallTransactionsTestCase(TestCase):
    request = "mall_transactions"

    def test_mall_transactions_short(self):
        with self.open_test_data("short") as file:
            logs = mall_transactions.parser(file)
            self.assertEqual(len(logs), 24)

            # Ensure we got the one with the internal brackets
            self.assertEqual(logs[18].username, "kutzputter")
            self.assertEqual(logs[18].user_id, 688802)
            self.assertEqual(logs[18].item.id, 2528)
            self.assertEqual(logs[18].quantity, 2)
            self.assertEqual(logs[18].meat, 4830)
