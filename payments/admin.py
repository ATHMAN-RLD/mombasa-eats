from django.contrib import admin
from .models import MpesaTransaction


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ("checkout_request_id", "order", "status", "amount", "mpesa_receipt_number", "created_at")
    list_filter = ("status",)
    search_fields = ("checkout_request_id", "phone_number")  