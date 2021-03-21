from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Publisher)
admin.site.register(models.ComposerScore)
admin.site.register(models.Score)
admin.site.register(models.User)