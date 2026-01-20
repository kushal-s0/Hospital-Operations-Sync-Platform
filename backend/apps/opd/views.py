from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, Count, Q, Max
from .models import OPDQueue, OPDStatistics
from .serializers import OPDQueueSerializer, OPDStatisticsSerializer, AppointmentSerializer
from apps.authentication.models import StaffUser, Patient, Doctor, Appointment
import joblib
import numpy as np
import os
from datetime import datetime

# Path to saved models
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models')


# =============================================================================
# HELPER FUNCTION: CALCULATE PATIENT ESTIMATED WAIT TIME
# =============================================================================

def calculate_patient_wait_time(patient_queue_entry):
    """
    Calculate ML-predicted wait time for a specific patient considering:
    - Their position in queue
    - Their priority level
    - Doctor availability
    - Current queue load
    
    Returns: estimated wait time in minutes
    """
    try:
        # Get current time and stats
        current_hour = timezone.now().hour
        is_weekend = timezone.now().weekday() >= 5
        
        # Get patient's doctor
        patient_doctor = patient_queue_entry.doctor
        
        # Check if doctor is currently busy (has patients in consultation)
        doctor_busy = False
        if patient_doctor:
            doctor_busy = OPDQueue.objects.filter(
                doctor=patient_doctor,
                status='in_consultation'
            ).exists()
        
        # Count patients waiting ahead of this patient (considering priority)
        priority_order = {'emergency': 0, 'urgent': 1, 'normal': 2}
        patient_priority_level = priority_order.get(patient_queue_entry.priority, 2)
        
        # Count patients with higher priority (emergency always ahead, urgent ahead of normal)
        if patient_priority_level == 2:  # Normal priority
            patients_ahead = OPDQueue.objects.filter(
                status='waiting',
                check_in_time__lt=patient_queue_entry.check_in_time
            ).filter(
                Q(priority='emergency') | Q(priority='urgent')
            ).count()
        elif patient_priority_level == 1:  # Urgent priority
            patients_ahead = OPDQueue.objects.filter(
                status='waiting',
                check_in_time__lt=patient_queue_entry.check_in_time,
                priority='emergency'
            ).count()
        else:  # Emergency priority
            patients_ahead = 0  # No one ahead of emergency
        
        # If same doctor, count only patients assigned to this doctor
        if patient_doctor:
            patients_ahead_same_doctor = OPDQueue.objects.filter(
                doctor=patient_doctor,
                status='waiting',
                check_in_time__lt=patient_queue_entry.check_in_time
            ).count()
        else:
            patients_ahead_same_doctor = patients_ahead
        
        # Average consultation time (default 15 minutes)
        avg_consultation = OPDStatistics.objects.aggregate(
            avg=Avg('average_consultation_time')
        )['avg'] or 15
        
        # Base wait time calculation
        if doctor_busy:
            # Doctor is busy, add current consultation time + queue
            base_wait = avg_consultation + (patients_ahead_same_doctor * avg_consultation)
        else:
            # Doctor is free, only queue ahead
            base_wait = patients_ahead_same_doctor * avg_consultation
        
        # Priority adjustment
        priority_multiplier = {
            'emergency': 0.3,  # Emergency patients wait less
            'urgent': 0.6,
            'normal': 1.0
        }.get(patient_queue_entry.priority, 1.0)
        
        # Time of day factor
        time_factor = 1.0
        if 9 <= current_hour <= 11:  # Peak morning
            time_factor = 1.2
        elif 14 <= current_hour <= 16:  # Peak afternoon
            time_factor = 1.15
        elif current_hour >= 18:  # Evening
            time_factor = 1.3
        
        # Weekend factor
        weekend_factor = 1.2 if is_weekend else 1.0
        
        # Calculate final wait time
        estimated_wait = base_wait * priority_multiplier * time_factor * weekend_factor
        
        # Minimum wait time is 5 minutes
        estimated_wait = max(5, int(estimated_wait))
        
        return estimated_wait
        
    except Exception as e:
        print(f"Error calculating wait time: {e}")
        return 15  # Default fallback


# =============================================================================
# WAIT TIME PREDICTION ENDPOINT (UNCHANGED - FOR PREDICTOR PANEL)
# =============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public access for predictions
def predict_wait_time(request):
    """
    Predict OPD wait time for a patient.
    
    Request body (optional - will auto-calculate if not provided):
    {
        "urgency_level": "normal",  // normal, urgent, emergency
        "department": "General Medicine",
        "time_of_day": "morning"  // morning, afternoon, evening
    }
    
    Response:
    {
        "predicted_wait_time_minutes": 25,
        "confidence": "medium",
        "factors": {...}
    }
    """
    try:
        # Get current queue stats
        today = timezone.now()
        current_hour = today.hour
        is_weekend = today.weekday() >= 5
        
        # Count patients in queue (all active, not just today)
        # This gives better predictions based on actual queue
        waiting_count = OPDQueue.objects.filter(
            status='waiting'
        ).count()
        
        in_consultation = OPDQueue.objects.filter(
            status='in_consultation'
        ).count()
        
        # Get average consultation time from recent data
        avg_consultation = OPDStatistics.objects.aggregate(
            avg=Avg('average_consultation_time')
        )['avg'] or 15  # Default 15 minutes
        
        # Get request data (optional overrides)
        urgency = request.data.get('urgency_level', 'normal')
        department = request.data.get('department', 'General')
        
        # Priority multiplier
        priority_multiplier = {
            'emergency': 0.2,  # Emergency patients wait less
            'urgent': 0.5,
            'normal': 1.0
        }.get(urgency, 1.0)
        
        # Time of day factor
        time_factor = 1.0
        if 9 <= current_hour <= 11:  # Peak morning
            time_factor = 1.3
        elif 14 <= current_hour <= 16:  # Peak afternoon
            time_factor = 1.2
        elif current_hour >= 18:  # Evening (less staff)
            time_factor = 1.4
        
        # Weekend factor
        weekend_factor = 1.3 if is_weekend else 1.0
        
        # Try to use ML model if available
        try:
            model = joblib.load(os.path.join(MODELS_DIR, 'wait_time_prediction_model.pkl'))
            scaler = joblib.load(os.path.join(MODELS_DIR, 'wait_time_scaler.pkl'))
            
            # Prepare features for ML model
            features = np.array([[
                waiting_count,
                in_consultation,
                current_hour,
                1 if is_weekend else 0,
                {'emergency': 0, 'urgent': 1, 'normal': 2}.get(urgency, 2),
                avg_consultation
            ]])
            
            features_scaled = scaler.transform(features)
            predicted_time = max(0, model.predict(features_scaled)[0])
            prediction_source = 'ml_model'
            
        except (FileNotFoundError, ValueError, Exception) as e:
            # Fallback: Simple calculation when model not available or features mismatch
            print(f"Using fallback calculation: {e}")
            base_wait = waiting_count * avg_consultation / max(in_consultation + 1, 1)
            predicted_time = base_wait * priority_multiplier * time_factor * weekend_factor
            # Add minimum wait time
            predicted_time = max(5, predicted_time)
            prediction_source = 'calculation'
        
        # Determine confidence level
        if waiting_count < 3:
            confidence = 'high'
        elif waiting_count < 10:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        return Response({
            'predicted_wait_time_minutes': round(predicted_time, 0),
            'confidence': confidence,
            'prediction_source': prediction_source,
            'current_queue_status': {
                'patients_waiting': waiting_count,
                'patients_in_consultation': in_consultation,
                'avg_consultation_time': round(avg_consultation, 1)
            },
            'factors_considered': {
                'urgency_level': urgency,
                'time_of_day': 'peak' if time_factor > 1 else 'normal',
                'is_weekend': is_weekend,
                'priority_multiplier': priority_multiplier
            },
            'recommendation': get_wait_recommendation(predicted_time)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_wait_recommendation(wait_time):
    """Generate recommendation based on wait time."""
    if wait_time < 10:
        return "Short wait expected. Patient will be seen soon."
    elif wait_time < 30:
        return "Moderate wait. Patient can be seated in waiting area."
    elif wait_time < 60:
        return "Long wait expected. Consider offering refreshments or updates."
    else:
        return "Extended wait. Recommend rescheduling or priority review."


class OPDQueueViewSet(viewsets.ModelViewSet):
    """ViewSet for OPDQueue CRUD operations."""
    
    queryset = OPDQueue.objects.all().order_by('-created_at')
    serializer_class = OPDQueueSerializer
    pagination_class = None  # Disable pagination to show all entries
    
    def list(self, request, *args, **kwargs):
        """Override list to add ML-predicted wait times for each patient."""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Calculate estimated wait time for each waiting patient
        for queue_entry in queryset:
            if queue_entry.status == 'waiting':
                estimated_wait = calculate_patient_wait_time(queue_entry)
                queue_entry.estimated_wait_time = estimated_wait
                # Update in database
                OPDQueue.objects.filter(id=queue_entry.id).update(estimated_wait_time=estimated_wait)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Override create to add better error logging."""
        print("=" * 60)
        print("CREATE OPD QUEUE ENTRY")
        print("=" * 60)
        print(f"Request data: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            self.perform_create(serializer)
            
            # Calculate initial estimated wait time
            created_entry = OPDQueue.objects.get(id=serializer.data['id'])
            estimated_wait = calculate_patient_wait_time(created_entry)
            created_entry.estimated_wait_time = estimated_wait
            created_entry.save(update_fields=['estimated_wait_time'])
            
            print(f"Successfully created with estimated wait time: {estimated_wait} minutes")
            
            # Re-serialize with updated wait time
            updated_serializer = self.get_serializer(created_entry)
            headers = self.get_success_headers(updated_serializer.data)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Error creating queue entry: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            traceback.print_exc()
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def current_queue(self, request):
        """Get current active queue."""
        today = timezone.now().date()
        queue = OPDQueue.objects.filter(
            created_at__date=today,
            status__in=['waiting', 'in_consultation']
        ).order_by('priority', 'check_in_time')
        serializer = self.get_serializer(queue, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_consultation(self, request, pk=None):
        """Mark patient consultation as started and recalculate wait times."""
        queue_entry = self.get_object()
        queue_entry.status = 'in_consultation'
        queue_entry.consultation_start_time = timezone.now()
        queue_entry.estimated_wait_time = None  # Clear wait time when consultation starts
        queue_entry.save()
        
        # Recalculate wait times for other waiting patients with same doctor
        if queue_entry.doctor:
            waiting_patients = OPDQueue.objects.filter(
                doctor=queue_entry.doctor,
                status='waiting'
            )
            for patient in waiting_patients:
                estimated_wait = calculate_patient_wait_time(patient)
                patient.estimated_wait_time = estimated_wait
                patient.save(update_fields=['estimated_wait_time'])
        
        return Response({'status': 'consultation started'})
    
    @action(detail=True, methods=['post'])
    def end_consultation(self, request, pk=None):
        """Mark patient consultation as completed and recalculate wait times."""
        queue_entry = self.get_object()
        doctor = queue_entry.doctor
        queue_entry.status = 'completed'
        queue_entry.consultation_end_time = timezone.now()
        queue_entry.estimated_wait_time = None  # Clear wait time when completed
        queue_entry.save()
        
        # Recalculate wait times for waiting patients with same doctor (doctor now free)
        if doctor:
            waiting_patients = OPDQueue.objects.filter(
                doctor=doctor,
                status='waiting'
            )
            for patient in waiting_patients:
                estimated_wait = calculate_patient_wait_time(patient)
                patient.estimated_wait_time = estimated_wait
                patient.save(update_fields=['estimated_wait_time'])
        
        return Response({'status': 'consultation completed'})


class OPDStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for OPDStatistics read operations."""
    
    queryset = OPDStatistics.objects.all()
    serializer_class = OPDStatisticsSerializer


# =============================================================================
# APPOINTMENT VIEWS FOR OPD SCHEDULING
# =============================================================================

from apps.authentication.models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Appointment CRUD operations and listing."""
    
    queryset = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """List all appointments or filter by status."""
        queryset = self.get_queryset()
        
        # Filter by status if provided
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range if provided
        from_date = request.query_params.get('from_date', None)
        to_date = request.query_params.get('to_date', None)
        
        if from_date:
            from datetime import datetime
            queryset = queryset.filter(appointment_date__gte=from_date)
        if to_date:
            from datetime import datetime
            queryset = queryset.filter(appointment_date__lte=to_date)
        
        # Filter by doctor if provided
        doctor_id = request.query_params.get('doctor_id', None)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        # Filter by patient if provided
        patient_id = request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments for today and future."""
        from django.utils import timezone
        today = timezone.now().date()
        
        appointments = Appointment.objects.filter(
            appointment_date__gte=today,
            status='Scheduled'
        ).order_by('appointment_date', 'appointment_time')
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get appointments for today only."""
        from django.utils import timezone
        today = timezone.now().date()
        
        appointments = Appointment.objects.filter(
            appointment_date=today,
            status='Scheduled'
        ).order_by('appointment_time')
        
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_to_queue(self, request, pk=None):
        """
        Add appointment to OPD queue when patient checks in.
        Convert appointment to active queue entry.
        """
        appointment = self.get_object()
        
        if appointment.status == 'Completed' or appointment.status == 'Cancelled':
            return Response(
                {'error': f'Cannot add {appointment.status} appointment to queue'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create OPD queue entry from appointment
            from django.db.models import Max
            
            # Generate token number
            max_token = OPDQueue.objects.aggregate(Max('token_number'))['token_number__max']
            token_number = (max_token or 0) + 1
            
            # Determine priority from urgency or appointment details
            priority = request.data.get('priority', 'normal')
            notes = request.data.get('notes', f'From appointment: {appointment.reason_for_visit}')
            
            # Get next ID for opd_queue (in case managed=False causes issues)
            from django.db.models import Max
            max_id = OPDQueue.objects.aggregate(Max('id'))['id__max']
            next_id = (max_id or 0) + 1
            
            # Create queue entry with explicit ID
            queue_entry = OPDQueue(
                id=next_id,
                patient=appointment.patient,
                doctor=appointment.doctor.staff if appointment.doctor else None,
                department=appointment.doctor.staff.department if (appointment.doctor and appointment.doctor.staff) else None,
                token_number=token_number,
                status='waiting',
                priority=priority,
                check_in_time=timezone.now(),
                notes=notes,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            queue_entry.save()
            
            # Update appointment status to Completed (or you can use a custom status)
            appointment.status = 'Completed'
            appointment.visit = None  # or link to the visit if needed
            appointment.save()
            
            # Calculate initial wait time
            estimated_wait = calculate_patient_wait_time(queue_entry)
            queue_entry.estimated_wait_time = estimated_wait
            queue_entry.save(update_fields=['estimated_wait_time'])
            
            # Serialize and return both queue entry and updated appointment
            queue_serializer = OPDQueueSerializer(queue_entry)
            appointment_serializer = self.get_serializer(appointment)
            
            return Response({
                'message': 'Patient added to OPD queue successfully',
                'queue_entry': queue_serializer.data,
                'appointment': appointment_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error adding appointment to queue: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Failed to add to queue: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment."""
        appointment = self.get_object()
        appointment.status = 'Cancelled'
        appointment.save()
        
        serializer = self.get_serializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)


# =============================================================================
# PUBLIC APPOINTMENT BOOKING ENDPOINT
# =============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def public_book_appointment(request):
    """
    Public endpoint for patients to book appointments without authentication.
    
    Request body:
    {
        "patient_first_name": "John",
        "patient_last_name": "Doe",
        "contact_number": "1234567890",
        "age": 30,
        "doctor_id": 1,
        "appointment_date": "2026-01-25",
        "appointment_time": "10:00:00",
        "time_slot": "10:00-10:30",
        "reason_for_visit": "Regular checkup"
    }
    """
    try:
        # Validate required fields
        required_fields = ['patient_first_name', 'patient_last_name', 'age', 'doctor_id', 
                          'appointment_date', 'appointment_time']
        
        for field in required_fields:
            if field not in request.data or not request.data.get(field):
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get doctor
        doctor_id = request.data.get('doctor_id')
        try:
            doctor = Doctor.objects.get(staff_id=doctor_id)
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create or get patient
        patient_first_name = request.data.get('patient_first_name')
        patient_last_name = request.data.get('patient_last_name')
        contact_number = request.data.get('contact_number', '')
        
        # Get the next patient_id
        max_patient_id = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
        next_patient_id = (max_patient_id or 0) + 1
        
        # Create new patient (only use valid Patient model fields)
        patient = Patient.objects.create(
            patient_id=next_patient_id,
            first_name=patient_first_name,
            last_name=patient_last_name,
            contact_number=contact_number,
            date_of_birth=None,
            gender=None,
            address=None,
            email=None,
            registration_date=timezone.now().date(),
            admin_id=None
        )
        
        # Get the next appointment_id
        max_appointment_id = Appointment.objects.aggregate(Max('appointment_id'))['appointment_id__max']
        next_appointment_id = (max_appointment_id or 0) + 1
        
        # Create appointment
        appointment = Appointment.objects.create(
            appointment_id=next_appointment_id,
            patient=patient,
            doctor=doctor,
            appointment_date=request.data.get('appointment_date'),
            appointment_time=request.data.get('appointment_time'),
            time_slot=request.data.get('time_slot', ''),
            age=request.data.get('age'),
            reason_for_visit=request.data.get('reason_for_visit', ''),
            status='Scheduled',
            admin_id=None
        )
        
        # Serialize response
        serializer = AppointmentSerializer(appointment)
        
        return Response({
            'message': 'Appointment booked successfully!',
            'appointment': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Error creating public appointment: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'Failed to book appointment: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
