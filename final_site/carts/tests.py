from django.test import TestCase
from accounts.models import Account
from store.models import Product
from category.models import Categories
from discount.models import Discount
from .models import Cart, CartItem

class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = Account.objects.create(username='testuser')

        
        cls.category = Categories.objects.create(cat_name='Test Category', slug='test-category')

        cls.discount = Discount.objects.create(name='Test Discount', discount_percent=10)

        cls.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='Test product description',
            price=100,
            images='test_image.jpg',
            stock=10,
            is_available=True,
            category=cls.category,
            discount=cls.discount
        )

        
        cls.cart = Cart.objects.create(user=cls.user, cart_no='test-cart')

    
        cls.cart_item = CartItem.objects.create(cart=cls.cart, product=cls.product, quantity=2, is_active=True)

    def test_cart_str_representation(self):
        cart = Cart.objects.get(id=self.cart.id)
        expected_cart_str = 'test-cart'
        self.assertEqual(str(cart), expected_cart_str)

    def test_cartitem_str_representation(self):
        cart_item = CartItem.objects.get(id=self.cart_item.id)
        expected_cartitem_str = f"{self.product} - {self.cart}"
        self.assertEqual(str(cart_item), expected_cartitem_str)

    def test_cart_item_quantity(self):
        cart_item = CartItem.objects.get(id=self.cart_item.id)
        expected_quantity = 2
        self.assertEqual(cart_item.quantity, expected_quantity)

    def test_cart_item_is_active(self):
        cart_item = CartItem.objects.get(id=self.cart_item.id)
        self.assertTrue(cart_item.is_active)

    def test_cart_user_relation(self):
        cart = Cart.objects.get(id=self.cart.id)
        self.assertEqual(cart.user, self.user)

    def test_cart_item_product_relation(self):
        cart_item = CartItem.objects.get(id=self.cart_item.id)
        self.assertEqual(cart_item.product, self.product)
