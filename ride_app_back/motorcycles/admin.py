from django.contrib import admin

from .models import Motorcycle

@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    list_display = ['model', 'color', 'year', 'owner']
    search_fields = ['model', 'brand', 'color', 'year','owner']
    list_filter = ['model', 'brand', 'color', 'year','owner']