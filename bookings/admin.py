from django.contrib import admin

from .models import Booking, CancellationRecord


admin.site.register(Booking)
admin.site.register(CancellationRecord)