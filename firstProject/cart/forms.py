from django import forms
from .models import order

class OrderForm(forms.ModelForm):
     class Meta:
          model=order
          fields="__all__"

          exclude=["order_id","user","paid"]