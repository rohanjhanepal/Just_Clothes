from django.contrib import admin
from django.contrib.auth.models import Group
from . import models


admin.site.site_header = "Just clothes control panel"
admin.site.unregister(Group)

admin.site.register(models.Category)
admin.site.register(models.Ad)
admin.site.register(models.Profile)
admin.site.register(models.SubCategory)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)

admin.site.register(models.Transactions)
admin.site.register(models.DropLocation)
admin.site.register(models.Frontal_images)