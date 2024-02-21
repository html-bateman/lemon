from django.test import TestCase
from django.urls import reverse
from ..models import Menu
from ..serializers import MenuSerializer


class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            name='Menu1', description='Description1', price=11.11)
        Menu.objects.create(
            name='Menu2', description='Description2', price=22.22)

    def test_getall(self):
        response = self.client.get(reverse('api-menu'))
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
