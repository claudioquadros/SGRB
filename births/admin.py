from django.contrib import admin
from .models import Birth


@admin.register(Birth)
class BirthAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'animal',
        'insemination',
        'expected_birth',
        'birth',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'animal__farm__company',
        'animal__breed',
        'animal__category',
        'expected_birth',
        'birth',
    )
    search_fields = (
        'animal__name',
        'insemination__animal__name',
    )
    date_hierarchy = 'birth'

    readonly_fields = (
        'created_at',
        'updated_at',
    )
