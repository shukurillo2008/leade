from django.contrib import admin
from . import models

admin.site.register(models.Status)
admin.site.register(models.Lead)
admin.site.register(models.LeadHistory)
admin.site.register(models.LeadType)
admin.site.register(models.Board)
