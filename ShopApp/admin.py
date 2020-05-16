from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Ad)
admin.site.register(models.Profile)
admin.site.register(models.SubCategory)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(models.Sizes)
admin.site.register(models.Transactions)
admin.site.register(models.DropLocation)