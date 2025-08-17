from django.contrib import admin
from . import models


class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'created_at', 'updated_at',)
    search_fields = ('name', 'company__name',)


admin.site.register(models.Farm, FarmAdmin)
