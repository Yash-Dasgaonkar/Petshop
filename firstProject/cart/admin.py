from django.contrib import admin

# Register your models here.
from .models import order,OrderItem
# Register your models here.

class orderItemInline(admin.TabularInline):
  model=OrderItem

class OrderAdmin(admin.ModelAdmin):
  inlines=[orderItemInline]

admin.site.register(order,OrderAdmin)
admin.site. register(OrderItem)