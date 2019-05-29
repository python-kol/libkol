from .test_base import TestCase
from ...request.hermit_menu import parse


class HermitMenuTestCase(TestCase):
    request = "hermit_menu"

    def test_hermit_menu_clovers(self):
        with self.open_test_data("clovers") as file:
            menu = parse(file.read())
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
