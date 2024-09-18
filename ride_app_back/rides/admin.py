from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Ride

# Register your models here.
@admin.register(Ride)
class RideAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['pilot', 'client', 'timeStart', 'status']
    search_fields = ['value', 'distance', 'pilot', 'client', 'stopPlace', 'status', 'timeStart', 'timeEnd']
    list_filter = ['value', 'distance', 'pilot', 'client', 'stopPlace', 'status', 'timeStart', 'timeEnd']
    history_list_display = ["history_type"]

@admin.register(Ride.history.model)
class RideHistoryAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ['history_type', 'history_date', 'history_user']