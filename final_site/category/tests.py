from django.test import TestCase
from .models import Categories

class CategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.category = Categories.objects.create(
            cat_name='Test Category',
            slug='test-category',
            description='Test category description'
        )

    def test_category_str_representation(self):
        category = Categories.objects.get(id=self.category.id)
        expected_category_str = 'Test Category'
        self.assertEqual(str(category), expected_category_str)

    def test_category_slug_field(self):
        category = Categories.objects.get(id=self.category.id)
        expected_slug = 'test-category'
        self.assertEqual(category.slug, expected_slug)

    def test_category_description_field(self):
        category = Categories.objects.get(id=self.category.id)
        expected_description = 'Test category description'
        self.assertEqual(category.description, expected_description)

    def test_category_blank_cat_image_field(self):
        category = Categories.objects.get(id=self.category.id)
        self.assertEqual(category.cat_image.name, '')



    def test_category_unique_cat_name_field(self):
        duplicate_category = Categories(cat_name='Test Category', slug='test-category2')
        self.assertRaises(Exception, duplicate_category.save)

    def test_category_unique_slug_field(self):
        duplicate_category = Categories(cat_name='Test Category 2', slug='test-category')
        self.assertRaises(Exception, duplicate_category.save)
