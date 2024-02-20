from django.test import TestCase
from datetime import datetime
from .models import ModelForTest

# Create your tests here.
class Test(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = ModelForTest.objects.create(
            first_name = 'John',
            last_name = 'McDonald'
        )

    def test_fields(self):
        self.assertIsInstance(self.data.first_name,str)
        self.assertIsInstance(self.data.last_name,str)

    def test_timestamps(self):
        self.assertIsInstance(self.data.booking_time,datetime)