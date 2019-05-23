from os import path
import unittest

TEST_DATA = path.join(path.dirname(path.abspath(__file__)), "test_data")


class TestCase(unittest.TestCase):
    def open_test_data(self, variant: str):
        return open(path.join(TEST_DATA, "{}_{}.html".format(self.request, variant)))
