from django.test import TestCase
from ..models import CapstoneMenu


class CapstoneMenuTest(TestCase):
    def test_get_item(self):
        CapstoneMenu.objects.create(
            Title="Ice Cream", Price=6, Inventory=10)
        saved_item = CapstoneMenu.objects.get(Title="Ice Cream")
        self.assertEqual(saved_item.Title, 'Ice Cream')
        self.assertEqual(saved_item.Price, 6)
        self.assertEqual(saved_item.Inventory, 10)
