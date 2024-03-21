from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,HttpResponse
from product.models import Product
from .models import Cart,CartItem
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.

#add to cart button
def add_to_cart(request,productId):
    # logic for adding cart 

    product=get_object_or_404(Product,id=productId)

    print(product.product_name)

    #Fetching current user 
    currentUser=request.user

    cart,created= Cart.objects.get_or_create(user=currentUser)

    print(created)
    
    item,item_created= CartItem.objects.get_or_create(cart=cart,Products=product)

    quantity=request.GET.get("quantity")
    
    if not item_created:
        item.quantity+=int(quantity)
    else:
        item.quantity=1

    item.save()

    return HttpResponseRedirect("/product/productlookup/")


#================================================

#View Cart
#===============================================
#update Cart
#==============================================

def update_cart(request,cartItemId):

    cartItem=get_object_or_404(CartItem,pk=cartItemId)
    quantity=request.GET.get("quantity")
    cartItem.quantity=int(quantity)
    cartItem.save()


    return HttpResponseRedirect("/cart/")


def view_cart(request):
    currentUser=request.user
    cart,created=Cart.objects.get_or_create(user=currentUser)
    cartItems=cart.cartitem_set.all()
    print(cartItems)

    finalAmount=0

    for item in cartItems:
        finalAmount+=item.quantity*item.Products.product_price


    return render(request,"cart.html",{"items":cartItems,"finalAmount" : finalAmount})



#==================================================
# delete cart item
#===================================================

def delete_cart(request,cartItemId):
    cartItem=get_object_or_404(CartItem,pk=cartItemId)
    cartItem.delete()
    return HttpResponseRedirect("/cart/")


     #============================================

   #               Check Out

   #=============================================
from .forms import OrderForm
from .models import order,OrderItem
import uuid
def check_out(request):

    currentUser = request.user
    initial = {
         "user":currentUser ,
         "first_name":currentUser.get_short_name(),
         "last_name":currentUser.last_name
    }
    print(initial['user'])
    print(initial['first_name'])
    form = OrderForm(initial = initial )

    currentUser = request.user
    cart,created = Cart.objects.get_or_create(user=currentUser)
    cartItems = cart.cartitem_set.all()
    print(cartItems)
    finalAmount = 0

    for item in cartItems:
        finalAmount += item.quantity*item.Products.product_price


        if request.method=="POST":
            form=OrderForm(request.POST)
            if form .is_valid():
             user=request.user
             firstName=form.cleaned_data['first_name']
             lastName=form.cleaned_data['last_name']
             address=form.cleaned_data['address']
             city=form.cleaned_data['city']
             state=form.cleaned_data['state']
             pincode=form.cleaned_data['pincode']
             phoneno=form.cleaned_data['phoneno']

             orderId=str(uuid.uuid4())
            
            Order=order.objects.create(user=user,
                                 first_name=firstName,
                                 last_name=lastName,
                                 address=address,
                                 city=city,
                                 state=state,
                                 pincode=pincode,
                                 phoneno=phoneno,
                                 order_id=orderId[:8]
                                 )
            for item in cartItems:
                OrderItem.objects.create(
                   order=Order,
                   products=item.Products,
                   quantity=item.quantity,
                   total=item.quantity*item.Products.product_price
                )
                    
            return HttpResponseRedirect("/payment/"+orderId[:8]) 
    
    return render(request,"checkout.html", {"form":form,"items":cartItems,"finalAmount":finalAmount})

#=========================================================
# make payment 
#=============================================================
import razorpay
def make_payment(request,orderId):
    #print(orderId)

     Order=order.objects.get(pk=orderId)
     OrderItems=Order.orderitem_set.all()
     amount=0

     for item in OrderItems:
        amount+=item.total

     print(amount)
     
     client = razorpay.Client(auth=("rzp_test_ul2Jla4RQ8Ul48","v2mc1lKr3QnXgDHlbwZl95CI"))
     data = { "amount": amount*100, "currency": "INR", "receipt": orderId ,"payment_capture" :1 }
     payment = client.order.create(data=data)

     return render(request,"payment.html",{"payment":payment})

#=========================================================
#  success Page
#============================================================
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
@csrf_exempt
def success(request ,orderId):
    if request.method=="POST":
          client = razorpay.Client(auth=("rzp_test_ul2Jla4RQ8Ul48","v2mc1lKr3QnXgDHlbwZl95CI"))
          check = client.utility.verify_payment_signature({
                         'razorpay_order_id': request.POST.get("razorpay_order_id"),
                         'razorpay_payment_id': request.POST.get("razorpay_payment_id"),
                         'razorpay_signature':request.POST.get("razorpay_signature")
                       })
          if check:
              Order=order.objects.get(pk=orderId)
              Order.paid=True
              Order.save()
              cart=Cart.objects.get(user=request.user)
              orderItems=Order.orderitem_set.all()
              cart.delete()
              send_mail(
                  "Order Placed..",#Subject
                  " ",#message
                    settings.EMAIL_HOST_USER,
                  ["priyanka.vibhute@itvedant.com","yash.dasgaonkar83@gmail.com"],
                  fail_silently=False,
                  html_message=render_to_string("email.html" ,{"items":orderItems})
              )


              return render(request,"success.html",{})
            



            
    
     
