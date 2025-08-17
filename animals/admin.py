from django.contrib import admin
from . import models


class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm', 'breed', 'category',)
    search_fields = ('name', 'farm__name',)


admin.site.register(models.Animal, AnimalAdmin)
