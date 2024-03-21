from django.db import models
from django.db.models.query import QuerySet

class ProductManager(models.Manager):
    
    def get_queryset(self):
        return  ProductQuerySet(self.model)
    
    def get_queryset(self):
        return ProductQuerySet(self.model).getPawsIndia()
    
    def sortByPrice(self):
        return super().get_queryset().order_by('product_price')


class ProductQuerySet(models.QuerySet):

    def getPawsIndia(self):
        return self.filter(product_Brand="Pawsup")
    

    def catProducts(self):
        return self.filter(product_name__icontains="cat")
    

        
    
    
    

    