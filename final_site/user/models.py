from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, password, **extra_fields)
       
        

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    # address = models.ForeignKey('UserAddress', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin =models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True

class UserAddress(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)

class UserPayment(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    expiry_date = models.DateField()
    def __str__(self):
        return f"{self.user.username} - {self.payment_type}"
