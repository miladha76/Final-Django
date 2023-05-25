from django.db import models
from django.urls import reverse

class Categories(models.Model):
    cat_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)
    
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])
    def __str__(self):
        return self.cat_name
    
        
