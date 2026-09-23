from django.contrib import admin

from .models import Package, Treatment


admin.site.register(Treatment)
admin.site.register(Package)