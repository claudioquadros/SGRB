from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    search_fields = ('name',)


admin.site.register(models.Category, CategoryAdmin)
