from django.contrib import admin

from accounting import models

class PurchaseAdmin(admin.ModelAdmin):
    list_filter = ('product', 'amount', 'value')
    list_display = ('__str__', 'product', 'amount', 'value')

admin.site.register(models.Product)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Category)
admin.site.register(models.DepreciationInfo)
