from libkol.request import hermit_menu
from .test_base import TestCase


class HermitMenuTestCase(TestCase):
    request = "hermit_menu"

    def test_hermit_menu_clovers(self):
        async def run_test(file):
            menu = await hermit_menu.parser(file.read())

            self.assertEqual([menu[0].item.id, menu[0].quantity], [2, 0])
            self.assertEqual([menu[1].item.id, menu[1].quantity], [2285, 0])
            self.assertEqual([menu[2].item.id, menu[2].quantity], [2284, 0])
            self.assertEqual([menu[3].item.id, menu[3].quantity], [55, 0])
            self.assertEqual([menu[4].item.id, menu[4].quantity], [52, 0])
            self.assertEqual([menu[5].item.id, menu[5].quantity], [47, 0])
            self.assertEqual([menu[6].item.id, menu[6].quantity], [46, 0])
            self.assertEqual([menu[7].item.id, menu[7].quantity], [106, 0])
            self.assertEqual([menu[8].item.id, menu[8].quantity], [107, 0])
            self.assertEqual([menu[9].item.id, menu[9].quantity], [527, 0])
            self.assertEqual([menu[10].item.id, menu[10].quantity], [24, 4])

        self.run_async("clovers", run_test)

    def test_hermit_menu_unrecognised(self):
        async def run_test(file):
            menu = await hermit_menu.parser(file.read())

            discovered_item = menu[8].item
            self.assertEqual(discovered_item.id, 1517)
            self.assertEqual(discovered_item.name, "test case")

        request_mocks = {"desc_item.php": "unrecognised_desc"}

        self.run_async("unrecognised", run_test, request_mocks=request_mocks)
