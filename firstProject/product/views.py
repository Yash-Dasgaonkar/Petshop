from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.db.models import Q
from .models import Product,Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url="/login/"),name="dispatch")
# Create your views here.
class ProductView(ListView):
      model=Product
      template_name="products.html"


class ProductDetailView(DetailView):
      model = Product
      template_name="Product_detail.html"
      context_object_name="p"
      #context['object_list']objectlist
def field_lookup(request):
     #products=Product.pm.all()
     #products=Product.pm.all(). filter (Q(product_price__lt="700" )& Q(product_name__icontains="cat"))
     #products=Product.pm.all().filter(Q(id=7)  | Q(id=6))
     products=Product.pm.all().filter(~Q(product_Brand="PawsUp"))
     
     #products = Product.objects.filter(product_Brand = "PawsUp")
     #products = Product.objects.filter(product_price__lt = "600")
     #products = Product.objects.filter(product_price__lte = "200")
     #products = Product.objects.filter(product_price__gt = "600")
     #products = Product.objects.filter(product_name__contains = "cat")#case sensitive
     #products = Product.objects.filter(product_name__icontains = "CAT")#case insensitive
     # products = Product.objects.filter(product_Brand__startswith = "P")#case sensitive
     # products = Product.objects.filter(product_Brand__istartswith = "p")#case insensitive (i is basically used for insensitive )
     #products = Product.objects.filter(product_name__endswith = "D")#case insensitive (i is basically used for insensitive )
     #products = Product.objects.filter(product_name__iendswith = "d")#case sensitive 
     #products = Product.objects.filter(id__in = [5,6,7])#case sensitive
      
      




     return render(request,"productLookup.html",{"product":products})

class CategoryDetailView(DetailView):
      model=Category
      template_name="category.html"
      context_object_name="category"
      slug_field = "slug"

