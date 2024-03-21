from django.db import models

from .managers import ProductManager
from autoslug import AutoSlugField

# Create your models here.
class Category(models.Model):
    category_name =models.CharField(max_length=12)
    slug=AutoSlugField(populate_from="category_name")


    def __str__(self):  
     return self.category_name


class Product(models.Model):
    
    product_name=models.CharField(max_length=100,default="ProductName")
    product_description=models.TextField(default = "description")
    product_price=models.IntegerField(default=0)
    product_Brand=models.CharField(max_length=75,default="Paws")
    product_picture=models.ImageField(upload_to="images/",default="")
    #category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    #category=models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)


    pm =models.Manager()
    cm=ProductManager()

    def __str__(self):
        return self.product_name
    
    #def __str__(self):
       # return self.product_Brand
    
