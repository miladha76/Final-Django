from django.test import TestCase
from .models import Product, Categories, Discount,Variation

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.category = Categories.objects.create(
            cat_name='Test Category',
            slug='test-category',
            description='Test category description'
        )

        
        cls.discount = Discount.objects.create(
            name='Test Discount',
            discount_percent=10
        )

        
        cls.product = Product.objects.create(
            product_name='Test Product',
            slug='test-product',
            description='Test product description',
            price=100,
            stock=10,
            category=cls.category,
            discount=cls.discount
        )

    def test_product_str_representation(self):
        product = Product.objects.get(id=self.product.id)
        expected_product_str = 'Test Product'
        self.assertEqual(str(product), expected_product_str)

    def test_product_attributes(self):
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.description, 'Test product description')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.stock, 10)
        self.assertTrue(product.is_available)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.discount, self.discount)

    def test_product_created_date_auto_now_add(self):
        product = Product.objects.get(id=self.product.id)
        self.assertIsNotNone(product.created_date)

    def test_product_modified_date_auto_now(self):
        product = Product.objects.get(id=self.product.id)
        self.assertIsNotNone(product.modified_date)

    def test_variation_creation(self):
        variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Red',
            is_active=True
        )
        
        self.assertEqual(variation.product, self.product)
        self.assertEqual(variation.variation_category, 'color')
        self.assertEqual(variation.variation_value, 'Red')
        self.assertTrue(variation.is_active)

    def test_variation_str_representation(self):
        variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Red',
            is_active=True
        )
        
        variation_str = str(variation)
        expected_str = 'Red'
        self.assertEqual(variation_str, expected_str)