from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Account


class AccountModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            first_name='milad',
            last_name='hatami',
            username='miladha',
            email='miladha@example.com',
            password='testpass123'
        )
        self.superuser = self.User.objects.create_superuser(
            first_name='Admin',
            last_name='User',
            username='adminuser',
            email='admin@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'miladha@example.com')
        self.assertEqual(self.user.username, 'miladha')
        self.assertEqual(self.user.first_name, 'milad')
        self.assertEqual(self.user.last_name, 'hatami')
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_superadmin)
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.full_name(), 'milad hatami')
        self.assertEqual(str(self.user), 'miladha@example.com')
        self.assertFalse(self.user.has_perm('some_permission'))
        self.assertTrue(self.user.has_module_perms('some_module'))

    def test_superuser_creation(self):
        self.assertEqual(self.superuser.email, 'admin@example.com')
        self.assertEqual(self.superuser.username, 'adminuser')
        self.assertEqual(self.superuser.first_name, 'Admin')
        self.assertEqual(self.superuser.last_name, 'User')
        self.assertTrue(self.superuser.is_admin)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_superadmin)
        self.assertTrue(self.superuser.check_password('testpass123'))
        self.assertEqual(self.superuser.full_name(), 'Admin User')
        self.assertEqual(str(self.superuser), 'admin@example.com')
        self.assertTrue(self.superuser.has_perm('some_permission'))
        self.assertTrue(self.superuser.has_module_perms('some_module'))
