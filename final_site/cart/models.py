from django.db import models
from accounts.models import Account
from store.models import Product

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    cart_no = models.CharField(max_length=255)

    def __str__(self):
        return self.cart_no

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product} - {self.cart}"


