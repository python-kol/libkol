from . import TestData

import unittest


class Main(unittest.TestCase):
    def runTest(self):
        s = TestData.data["session"]
        s.logout()
        self.assertTrue(s.is_connected == False)
