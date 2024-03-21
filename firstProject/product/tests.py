from django.test import TestCase
from .models import Product

# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.product=Product.pm.create(product_name="TestProduct",
                          product_description="Product has been created for testing",
                          product_Brand="TestBrand",
                          product_price=500)
        
    def test_create_product(self):
       product= Product.pm.get(product_name="TestProduct")
       self.assertEqual(product.id,self.product.id)
        
    def test_update_user(self):
        product=Product.pm.get(product_name="TestProduct")
        product.product_price=5000
        product.save()

        self.assertNotEqual(product.product_price,self.product.product_price)

    def test_fetch_product(self):
        products=Product.pm.all()
        count=len(products)
        self.assertGreater(count,0)
        