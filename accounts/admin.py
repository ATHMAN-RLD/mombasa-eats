from django.contrib import admin
from .models import Rider


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "is_available")
    list_filter = ("is_available",)  