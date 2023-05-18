from django.db import models
from user.models import User
from store.models import Product

class OrderDetail(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    total= models.DecimalField( max_digits=10, decimal_places=2)
    created_at =models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return f'{self.user}'
    
class OrderItem(models.Model):
    order=models.ForeignKey(OrderDetail,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)   
    modified_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product}'
    
    
    
class Payment(models.Model):
    order=models.OneToOneField(OrderDetail,on_delete=models.CASCADE)
    amount =models.IntegerField()
    status =models.CharField(max_length=50,choices=[('d','done'),('f','failed'),('p','process')])   
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}s payment'