from django.contrib import admin
from .models import Item, HSNCode, PurchaseBill, PurchaseItem, SellBill, SellItem

# Register your models here.
admin.site.register(Item)
admin.site.register(HSNCode)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseBill)
admin.site.register(SellItem)
admin.site.register(SellBill)