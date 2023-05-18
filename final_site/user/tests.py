from django.test import TestCase
from .models import User, UserAddress, UserPayment

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )

    def test_user_str_representation(self):
        user = User.objects.get(id=self.user.id)
        expected_user_str = 'testuser'
        self.assertEqual(str(user), expected_user_str)

    def test_user_attributes(self):
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '1234567890')

    def test_user_default_permissions(self):
        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)

    def test_user_address_creation(self):
        user = User.objects.get(id=self.user.id)
        address = UserAddress.objects.create(
            user=user,
            address_line1='Address Line 1',
            city='City',
            postal_code='12345',
            country='Country',
            telephone='123456',
            mobile='789012345'
        )
        self.assertEqual(user.addresses.count(), 1)
        self.assertIn(address, user.addresses.all())

    def test_user_payment_creation(self):
        user = User.objects.get(id=self.user.id)
        payment = UserPayment.objects.create(
            user=user,
            payment_type='Payment Type',
            account_no='1234567890',
            expiry_date='2023-01-01'
        )
        self.assertEqual(user.payments.count(), 1)
        self.assertIn(payment, user.payments.all())
