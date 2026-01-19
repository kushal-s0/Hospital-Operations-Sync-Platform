from rest_framework import serializers
from django.db import connection


class BillingSerializer(serializers.Serializer):
    """Serializer for Billing data from database"""
    bill_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    treatment_id = serializers.IntegerField()
    bill_date = serializers.DateField()
    amount = serializers.FloatField()
    payment_method = serializers.CharField()
    payment_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class FinancialTransactionSerializer(serializers.Serializer):
    """Serializer for Financial Transactions data from database"""
    transaction_id = serializers.IntegerField()
    hospital_id = serializers.IntegerField()
    reference_type = serializers.CharField()
    reference_id = serializers.IntegerField()
    transaction_type = serializers.CharField()
    amount = serializers.FloatField()
    payment_method = serializers.CharField()
    description = serializers.CharField()
    transaction_date = serializers.DateTimeField()
    created_at = serializers.DateTimeField()


class TreatmentSerializer(serializers.Serializer):
    """Serializer for Treatment data from database"""
    treatment_id = serializers.IntegerField()
    appointment_id = serializers.IntegerField()
    treatment_type = serializers.CharField()
    description = serializers.CharField()
    cost = serializers.FloatField()
    treatment_date = serializers.DateField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class DashboardSummarySerializer(serializers.Serializer):
    """Summary data for receptionist dashboard"""
    total_billing_amount = serializers.FloatField()
    total_transactions_amount = serializers.FloatField()
    total_treatments = serializers.IntegerField()
    pending_bills_count = serializers.IntegerField()
    paid_bills_count = serializers.IntegerField()
    failed_bills_count = serializers.IntegerField()
    income_transactions = serializers.FloatField()
    expense_transactions = serializers.FloatField()
    total_income = serializers.FloatField()
    total_expenses = serializers.FloatField()
    predicted_profit = serializers.FloatField()
    predicted_loss_area = serializers.CharField()
    profit_confidence = serializers.FloatField()
    loss_confidence = serializers.FloatField()
    recommendations = serializers.ListField()
