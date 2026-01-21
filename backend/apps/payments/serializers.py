from rest_framework import serializers
from .models import PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """Serializer for Payment Transaction model"""
    
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'bill_id', 'razorpay_order_id', 'razorpay_payment_id',
            'razorpay_signature', 'amount', 'currency', 'status',
            'payment_method', 'error_code', 'error_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating Razorpay order"""
    bill_id = serializers.IntegerField()


class VerifyPaymentSerializer(serializers.Serializer):
    """Serializer for verifying Razorpay payment"""
    razorpay_order_id = serializers.CharField(max_length=100)
    razorpay_payment_id = serializers.CharField(max_length=100)
    razorpay_signature = serializers.CharField(max_length=255)
