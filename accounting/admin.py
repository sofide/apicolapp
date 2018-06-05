from django.contrib import admin

from accounting.models import Product, Purchase, Inventary, InventaryProduct


admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Inventary)
admin.site.register(InventaryProduct)
