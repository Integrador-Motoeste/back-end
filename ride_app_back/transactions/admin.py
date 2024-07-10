from django.contrib import admin

from .models import Invoice
from .models import Transaction

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Invoice)
