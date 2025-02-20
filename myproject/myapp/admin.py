from django.contrib import admin
from .models import Feedback,Demart,Ordernow
# Register your models here.

admin.site.register(Demart)
admin.site.register(Feedback)

# class OrdernowAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'product_name', 'quantity', 'total_price', 'status', 'order_date')
#     list_filter = ('status', 'order_date')
#     search_fields = ('name', 'email', 'product_name')
#     ordering = ('-order_date',)

admin.site.register(Ordernow)