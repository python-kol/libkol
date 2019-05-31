import unittest
from os import path

from pykollib.database import db

TEST_DATA = path.join(path.dirname(path.abspath(__file__)), "test_data")


class TestCase(unittest.TestCase):
    request: str

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        db_file = path.join(path.dirname(__file__), "../../pykollib/pykollib.db")
        db.init(db_file)
        db.connect()

    def open_test_data(self, variant: str):
        return open(path.join(TEST_DATA, "{}_{}.html".format(self.request, variant)))
