from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'bill_id', 'razorpay_order_id', 'razorpay_payment_id', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['bill_id', 'razorpay_order_id', 'razorpay_payment_id']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
