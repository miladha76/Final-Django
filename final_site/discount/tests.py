from django.test import TestCase
from .models import Discount

class DiscountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.discount = Discount.objects.create(
            name='Test Discount',
            discount_percent=10
        )

    def test_discount_str_representation(self):
        discount = Discount.objects.get(id=self.discount.id)
        expected_discount_str = 'Test Discount'
        self.assertEqual(str(discount), expected_discount_str)

    def test_discount_percent_field(self):
        discount = Discount.objects.get(id=self.discount.id)
        expected_discount_percent = 10
        self.assertEqual(discount.discount_percent, expected_discount_percent)

    def test_discount_created_at_auto_now_add(self):
        discount = Discount.objects.get(id=self.discount.id)
        self.assertIsNotNone(discount.created_at)

    def test_discount_modified_at_auto_now(self):
        discount = Discount.objects.get(id=self.discount.id)
        self.assertIsNotNone(discount.modified_at)
