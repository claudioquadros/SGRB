from django.contrib import admin
from .models import Insemination


@admin.register(Insemination)
class InseminationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'animal',
        'bull',
        'date_of_insemination',
        'expected_pregnancy',
        'pregnancy_check',
        'is_pregnant',
        'created_at',
    )
    list_filter = (
        'animal__farm__company',
        'animal__breed',
        'animal__category',
        'bull',
        'is_pregnant',
        'date_of_insemination',
        'expected_pregnancy',
    )
    search_fields = (
        'animal__name',
        'animal__earring',
        'animal__farm__name',
    )
    date_hierarchy = 'date_of_insemination'

    readonly_fields = (
        'created_at',
        'updated_at',
    )
