from django.contrib import admin

from accounting import models


admin.site.register(models.Product)
admin.site.register(models.Purchase)
admin.site.register(models.Category)
admin.site.register(models.DepreciationInfo)
