from django.db import models
from accounts.models import Account
from store.models import Product,Variation

class Cart(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    cart_id = models.CharField(max_length=255)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


