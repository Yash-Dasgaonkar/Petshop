from django.db import models
from django.contrib.auth.models import User 
from product.models import Product

# Create your models here.
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,through="CartItem")

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    Products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

class order(models.Model):
   order_id=models.CharField(max_length=200,primary_key=True,default="OrderXYZ")
   user=models.ForeignKey(User ,on_delete=models.CASCADE)
   first_name=models.CharField(max_length=100)
   last_name=models.CharField( max_length=100 )
   address=models.CharField(max_length=200)
   city=models.CharField(max_length=100)
   state=models.CharField(max_length=100)
   pincode=models.IntegerField()
   phoneno=models.CharField(max_length=10)
   created_at=models.DateTimeField(auto_now_add=True)
   updated_at=models.DateTimeField(auto_now=True)
   paid=models.BooleanField(default=False)

   def __str__(self):
    return f"{self.first_name}-{self.created_at}"

class OrderItem(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    total=models.IntegerField()
