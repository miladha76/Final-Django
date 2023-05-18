from django.test import TestCase
from django.utils import timezone
from user.models import User
from store.models import Categories, Product
from .models import OrderDetail, OrderItem, Payment

class OrderDetailModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.order_detail = OrderDetail.objects.create(user=self.user, total=100.00)

    def test_order_detail_str_representation(self):
        self.assertEqual(str(self.order_detail), str(self.user))

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.category = Categories.objects.create(cat_name='TestCategory', slug='test-category')
        self.product = Product.objects.create(product_name='Test Product', price=50.00, category=self.category)
        self.order_detail = OrderDetail.objects.create(user=self.user, total=100.00)
        self.order_item = OrderItem.objects.create(order=self.order_detail, product=self.product)

    def test_order_item_str_representation(self):
        self.assertEqual(str(self.order_item), str(self.product))

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.order_detail = OrderDetail.objects.create(user=self.user, total=100.00)
        self.payment = Payment.objects.create(order=self.order_detail, amount=100, status='d')

    def test_payment_str_representation(self):
        self.assertEqual(str(self.payment), f'{self.order_detail.user.username}s payment')

    def test_payment_status_choices(self):
        choices = dict(self.payment._meta.get_field('status').choices)
        self.assertEqual(choices['d'], 'done')
        self.assertEqual(choices['f'], 'failed')
        self.assertEqual(choices['p'], 'process')

    def test_payment_created_at(self):
        now = timezone.now()
        self.assertLess(self.payment.created_at, now)
