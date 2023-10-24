from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Campaign)
admin.site.register(models.Donation)
admin.site.register(models.Rate)
admin.site.register(models.Report)
