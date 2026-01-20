from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime, timedelta

from apps.authentication.models import Appointment
from .serializers import (
    AppointmentSerializer,
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


class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing appointments (accessible to patients and staff)"""
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = []  # Allow unauthenticated access for public booking
    
    def create(self, request, *args, **kwargs):
        """Create a new appointment from the booking form"""
        try:
            from apps.authentication.models import Patient
            from datetime import date
            
            # Create a mutable copy of request data
            appointment_data = dict(request.data)
            
            # Check if this is from the booking form with patient info
            if 'first_name' in appointment_data and 'patient' not in appointment_data:
                # Get the next patient ID
                cursor = connection.cursor()
                cursor.execute("SELECT MAX(patient_id) FROM patients")
                max_id = cursor.fetchone()[0]
                next_patient_id = (max_id or 0) + 1
                
                # Create a patient first with explicit ID
                patient_data = {
                    'patient_id': next_patient_id,
                    'first_name': appointment_data.get('first_name', ''),
                    'last_name': appointment_data.get('last_name', ''),
                    'contact_number': appointment_data.get('contact_number', ''),
                    'email': appointment_data.get('email', ''),
                    'gender': 'M',
                    'date_of_birth': date(2000, 1, 1),
                    'address': appointment_data.get('address', 'N/A'),
                    'registration_date': date.today()
                }
                
                # Create patient
                patient = Patient.objects.create(**patient_data)
                appointment_data['patient'] = patient.patient_id
            
            # Get the next appointment ID
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(appointment_id) FROM appointments")
            max_app_id = cursor.fetchone()[0]
            next_app_id = (max_app_id or 0) + 1
            appointment_data['appointment_id'] = next_app_id
            
            serializer = self.get_serializer(data=appointment_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        """Save the appointment"""
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def scheduled(self, request):
        """Get all scheduled appointments"""
        appointments = Appointment.objects.filter(status='Scheduled').order_by('appointment_date', 'appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments for today and future"""
        from datetime import date
        today = date.today()
        appointments = Appointment.objects.filter(
            appointment_date__gte=today,
            status__in=['Scheduled']
        ).order_by('appointment_date', 'appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept_to_opd(self, request, pk=None):
        """Accept an appointment and add it to OPD queue"""
        try:
            from apps.authentication.models import OPDQueue, StaffUser, Department
            from django.utils import timezone
            
            appointment = self.get_object()
            print(f"\n[ACCEPT_TO_OPD] Processing appointment {appointment.appointment_id}")
            print(f"[ACCEPT_TO_OPD] Current status: {appointment.status}")
            
            # Check if appointment is scheduled
            if appointment.status != 'Scheduled':
                return Response({
                    'error': f'Only scheduled appointments can be moved to OPD queue. Current status: {appointment.status}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parse the department from appointment reason
            # reason_for_visit might be like "Department: Dermatology" or "chest pain" etc
            reason_text = appointment.reason_for_visit if appointment.reason_for_visit else 'General'
            department_name = None
            
            # Try to extract department name if it contains "Department:"
            if 'Department:' in reason_text:
                # Extract text after "Department:"
                parts = reason_text.split('Department:')
                if len(parts) > 1:
                    department_name = parts[1].strip().split('-')[0].strip()
            
            print(f"[ACCEPT_TO_OPD] Reason: {reason_text}")
            print(f"[ACCEPT_TO_OPD] Department name extracted: {department_name}")
            
            # Try to find the department by name
            department = None
            if department_name:
                department = Department.objects.filter(department_name__iexact=department_name).first()
            
            # If no department found, try with generic search or use first available
            if not department:
                # Try with partial match
                if department_name:
                    department = Department.objects.filter(department_name__icontains=department_name).first()
                
                # Last resort: get first available department with available doctors
                if not department:
                    department = Department.objects.first()
            
            if not department:
                return Response({
                    'error': 'No department found in system'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"[ACCEPT_TO_OPD] Department found: {department.department_name}")
            
            # Get an available doctor from the department
            doctor = StaffUser.objects.filter(
                department=department,
                role='Doctor',
                is_active=True
            ).first()
            
            if not doctor:
                return Response({
                    'error': f'No available doctor found in {department.department_name} department'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"[ACCEPT_TO_OPD] Doctor found: {doctor.first_name} {doctor.last_name}")
            
            # Get next token number for this department
            cursor = connection.cursor()
            cursor.execute(
                "SELECT MAX(token_number) FROM opd_queue WHERE department_id = %s",
                [department.department_id]
            )
            max_token = cursor.fetchone()[0]
            next_token = (max_token or 0) + 1
            
            print(f"[ACCEPT_TO_OPD] Token number: {next_token}")
            
            # Create OPD queue entry
            opd_entry = OPDQueue.objects.create(
                patient=appointment.patient,
                doctor=doctor,
                department=department,
                token_number=next_token,
                status='waiting',
                priority=appointment.priority or 'normal',  # Use appointment priority
                check_in_time=timezone.now(),
                notes=f'From appointment #{appointment.appointment_id}: {appointment.reason_for_visit}',
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            
            print(f"[ACCEPT_TO_OPD] OPD entry created with ID: {opd_entry.id}")
            
            # Update appointment status
            appointment.status = 'In OPD Queue'
            appointment.save()
            
            print(f"[ACCEPT_TO_OPD] Appointment status updated to 'In OPD Queue'")
            
            return Response({
                'status': 'success',
                'message': f'Appointment moved to OPD queue',
                'token_number': next_token,
                'doctor': doctor.first_name + ' ' + doctor.last_name,
                'department': department.department_name,
                'opd_queue_id': opd_entry.id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

