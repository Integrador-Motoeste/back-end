from django.contrib import admin

from .models import Ride

# Register your models here.
@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['pilot', 'client', 'start', 'timeStart', 'status']
    search_fields = ['value', 'distance', 'pilot', 'client', 'start', 'end', 'stopPlace', 'status', 'timeStart', 'timeEnd']
    list_filter = ['value', 'distance', 'pilot', 'client', 'start', 'end', 'stopPlace', 'status', 'timeStart', 'timeEnd']
