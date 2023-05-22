from django.test import TestCase
from user.models import User
from category.models import Categories
from orders.models import Order, OrderItem, Payment
from store.models import Product, Variation

class OrderAppTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

        self.category = Categories.objects.create(
            cat_name='Test Category',
            slug='test-category',
            description='Test category description',
            cat_image='test.jpg'
        )

        self.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='Test description',
            price=10,
            images='test.jpg',
            stock=10,
            is_available=True,
            category=self.category
        )

        self.variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Red',
            is_active=True
        )

        self.order = Order.objects.create(
            user=self.user,
            first_name='milad',
            last_name='hatami',
            phone='123456789',
            address_line1='123 Test Street',
            address_line2='',
            country='Test Country',
            city='Test City',
            order_note='',
            order_total=10,
            tax=0,
            ip='',
            is_ordered=False
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            payment=None,
            user=self.user,  
            product=self.product,
            variations=self.variation,
            color='Red',
            size='',
            quantity=1,
            product_price=self.product.price,
            ordered=False
        )

        self.payment = Payment.objects.create(
            order=self.order,
            user=self.user, 
            payment_id='1234567890',
            payment_method='Credit Card',
            amount_paid='10',
            status='Pending'
        )


    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.first_name, 'milad')
        self.assertEqual(self.order.last_name, 'hatami')
        self.assertEqual(self.order.phone, '123456789')
        self.assertEqual(self.order.address_line1, '123 Test Street')
        self.assertEqual(self.order.address_line2, '')
        self.assertEqual(self.order.country, 'Test Country')
        self.assertEqual(self.order.city, 'Test City')
        self.assertEqual(self.order.order_note, '')
        self.assertEqual(self.order.order_total, 10)
        self.assertEqual(self.order.tax, 0)
        self.assertEqual(self.order.ip, '')
        self.assertEqual(self.order.is_ordered, False)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.payment, None)
        self.assertEqual(self.order_item.user, self.user)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.variations, self.variation)
        self.assertEqual(self.order_item.color, 'Red')
        self.assertEqual(self.order_item.size, '')
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.product_price, self.product.price)
        self.assertEqual(self.order_item.ordered, False)

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.payment_id, '1234567890')
        self.assertEqual(self.payment.payment_method, 'Credit Card')
        self.assertEqual(self.payment.amount_paid, '10')
        self.assertEqual(self.payment.status, 'Pending')

    def test_order_str_representation(self):
        order_str = str(self.order)
        expected_str = self.order.first_name
        self.assertEqual(order_str, expected_str)

    def test_orderitem_str_representation(self):
        orderitem_str = str(self.order_item)
        expected_str = self.order_item.product.product_name
        self.assertEqual(orderitem_str, expected_str)

   

