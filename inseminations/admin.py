from django.contrib import admin
from .models import Insemination


@admin.register(Insemination)
class InseminationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'animal',
        'insemination_date',
        'expected_birth',
        'result',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'result',
        'animal__farm__company',
        'animal__breed',
        'animal__category',
        'insemination_date',
        'expected_birth',
    )
    search_fields = (
        'animal__name',
        'animal__farm__name',
    )
    date_hierarchy = 'insemination_date'

    readonly_fields = (
        'created_at',
        'updated_at',
    )
