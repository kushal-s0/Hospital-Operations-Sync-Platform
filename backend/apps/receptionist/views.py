from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.core.paginator import Paginator
from django.utils.timezone import now
from datetime import datetime, timedelta

from .serializers import (
    BillingSerializer,
    FinancialTransactionSerializer,
    TreatmentSerializer,
    DashboardSummarySerializer
)
from .profit_loss_predictor import get_profit_loss_predictions


class ReceptionistDashboardViewSet(viewsets.ViewSet):
    """ViewSet for Receptionist Dashboard - View-only access to billing, transactions, and treatments"""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get dashboard summary data"""
        return self.get_dashboard_summary(request)
    
    def get_dashboard_summary(self, request):
        """Get summary statistics for the receptionist dashboard"""
        cursor = connection.cursor()
        
        try:
            # Get billing summary
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(amount), 0) as total_billing,
                    SUM(CASE WHEN payment_status = 'Paid' THEN 1 ELSE 0 END) as paid_count,
                    SUM(CASE WHEN payment_status = 'Pending' THEN 1 ELSE 0 END) as pending_count,
                    SUM(CASE WHEN payment_status = 'Failed' THEN 1 ELSE 0 END) as failed_count
                FROM billing
            """)
            billing_summary = cursor.fetchone()
            
            # Get financial transactions summary - dynamically calculated
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN transaction_type = 'INCOME' THEN amount ELSE 0 END), 0) as income,
                    COALESCE(SUM(CASE WHEN transaction_type = 'EXPENSE' THEN amount ELSE 0 END), 0) as expense
                FROM financial_transactions
            """)
            transaction_summary = cursor.fetchone()
            
            # Get treatments count
            cursor.execute("SELECT COUNT(*) FROM treatments")
            treatments_count = cursor.fetchone()[0]
            
            # Convert Decimal to float
            total_billing = float(billing_summary[0]) if billing_summary and billing_summary[0] else 0.0
            paid_count = billing_summary[1] if billing_summary and billing_summary[1] else 0
            pending_count = billing_summary[2] if billing_summary and billing_summary[2] else 0
            failed_count = billing_summary[3] if billing_summary and billing_summary[3] else 0
            
            income = float(transaction_summary[0]) if transaction_summary and transaction_summary[0] else 0.0
            expense = float(transaction_summary[1]) if transaction_summary and transaction_summary[1] else 0.0
            
            # Get profit/loss predictions from ML models
            predictions = get_profit_loss_predictions()
            
            data = {
                'total_billing_amount': total_billing,
                'paid_bills_count': paid_count,
                'pending_bills_count': pending_count,
                'failed_bills_count': failed_count,
                'income_transactions': income,
                'expense_transactions': expense,
                'total_income': income,  # Dynamic from financial_transactions INCOME
                'total_expenses': expense,  # Dynamic from financial_transactions EXPENSE
                'total_treatments': treatments_count,
                'total_transactions_amount': income + expense,
                'predicted_profit': predictions['predicted_profit'],
                'predicted_loss_area': predictions['loss_area'],
                'profit_confidence': predictions['profit_confidence'],
                'loss_confidence': predictions['loss_confidence'],
                'recommendations': predictions['recommendations']
            }
            
            serializer = DashboardSummarySerializer(data)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def billing_list(self, request):
        """Get all billing records"""
        cursor = connection.cursor()
        
        try:
            # Get pagination parameters
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM billing")
            total_count = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get paginated data
            cursor.execute("""
                SELECT 
                    bill_id, patient_id, treatment_id, bill_date, 
                    amount, payment_method, payment_status, 
                    created_at, updated_at
                FROM billing
                ORDER BY bill_date DESC
                LIMIT %s OFFSET %s
            """, [page_size, offset])
            
            columns = [col[0] for col in cursor.description]
            billing_data = []
            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                # Convert Decimal to float
                if record['amount']:
                    record['amount'] = float(record['amount'])
                billing_data.append(record)
            
            # Serialize data
            serializer = BillingSerializer(billing_data, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def financial_transactions_list(self, request):
        """Get all financial transactions"""
        cursor = connection.cursor()
        
        try:
            # Get pagination parameters
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM financial_transactions")
            total_count = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get paginated data
            cursor.execute("""
                SELECT 
                    transaction_id, hospital_id, reference_type, reference_id,
                    transaction_type, amount, payment_method, description,
                    transaction_date, created_at
                FROM financial_transactions
                ORDER BY transaction_date DESC
                LIMIT %s OFFSET %s
            """, [page_size, offset])
            
            columns = [col[0] for col in cursor.description]
            transaction_data = []
            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                # Convert Decimal to float
                if record['amount']:
                    record['amount'] = float(record['amount'])
                transaction_data.append(record)
            
            # Serialize data
            serializer = FinancialTransactionSerializer(transaction_data, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def treatments_list(self, request):
        """Get all treatments"""
        cursor = connection.cursor()
        
        try:
            # Get pagination parameters
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM treatments")
            total_count = cursor.fetchone()[0]
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get paginated data
            cursor.execute("""
                SELECT 
                    treatment_id, appointment_id, treatment_type, description,
                    cost, treatment_date, created_at, updated_at
                FROM treatments
                ORDER BY treatment_date DESC
                LIMIT %s OFFSET %s
            """, [page_size, offset])
            
            columns = [col[0] for col in cursor.description]
            treatment_data = []
            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                # Convert Decimal to float
                if record['cost']:
                    record['cost'] = float(record['cost'])
                treatment_data.append(record)
            
            # Serialize data
            serializer = TreatmentSerializer(treatment_data, many=True)
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def billing_statistics(self, request):
        """Get billing statistics by status and method"""
        cursor = connection.cursor()
        
        try:
            # Get billing by status
            cursor.execute("""
                SELECT payment_status, COUNT(*) as count, SUM(amount) as total
                FROM billing
                GROUP BY payment_status
            """)
            
            status_data = [
                {
                    'status': row[0],
                    'count': row[1],
                    'total': float(row[2]) if row[2] else 0.0
                }
                for row in cursor.fetchall()
            ]
            
            # Get billing by payment method
            cursor.execute("""
                SELECT payment_method, COUNT(*) as count, SUM(amount) as total
                FROM billing
                GROUP BY payment_method
            """)
            
            method_data = [
                {
                    'method': row[0],
                    'count': row[1],
                    'total': float(row[2]) if row[2] else 0.0
                }
                for row in cursor.fetchall()
            ]
            
            return Response({
                'status': 'success',
                'by_status': status_data,
                'by_method': method_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def transaction_statistics(self, request):
        """Get financial transaction statistics by type"""
        cursor = connection.cursor()
        
        try:
            # Get transactions by type
            cursor.execute("""
                SELECT transaction_type, COUNT(*) as count, SUM(amount) as total
                FROM financial_transactions
                GROUP BY transaction_type
            """)
            
            type_data = [
                {
                    'type': row[0],
                    'count': row[1],
                    'total': float(row[2]) if row[2] else 0.0
                }
                for row in cursor.fetchall()
            ]
            
            # Get transactions by reference type
            cursor.execute("""
                SELECT reference_type, COUNT(*) as count, SUM(amount) as total
                FROM financial_transactions
                GROUP BY reference_type
            """)
            
            reference_data = [
                {
                    'reference_type': row[0],
                    'count': row[1],
                    'total': float(row[2]) if row[2] else 0.0
                }
                for row in cursor.fetchall()
            ]
            
            return Response({
                'status': 'success',
                'by_type': type_data,
                'by_reference_type': reference_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
