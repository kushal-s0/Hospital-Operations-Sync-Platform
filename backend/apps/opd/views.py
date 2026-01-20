from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, Count, Q
from .models import OPDQueue, OPDStatistics
from .serializers import OPDQueueSerializer, OPDStatisticsSerializer
from apps.authentication.models import StaffUser
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
    
    queryset = OPDQueue.objects.all()
    serializer_class = OPDQueueSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def get_queryset(self):
        """Filter queryset based on user role - doctors see only their patients."""
        queryset = OPDQueue.objects.all()
        
        # Check if user is authenticated
        if self.request.user and self.request.user.is_authenticated:
            # If user is a doctor, filter to show only patients assigned to them
            if self.request.user.role == 'Doctor':
                queryset = queryset.filter(doctor_id=self.request.user.staff_id)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Override list to add ML-predicted wait times for each patient (except for doctors)."""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Skip wait time calculation for doctors
        if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor'):
            # Calculate estimated wait time for each waiting patient (non-doctors only)
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
        """Get current active queue (filtered by doctor if logged-in user is a doctor)."""
        today = timezone.now().date()
        queue = OPDQueue.objects.filter(
            created_at__date=today,
            status__in=['waiting', 'in_consultation']
        )
        
        # Filter by doctor if user is a doctor
        if request.user and request.user.is_authenticated:
            if request.user.role == 'Doctor':
                queue = queue.filter(doctor_id=request.user.staff_id)
        
        queue = queue.order_by('priority', 'check_in_time')
        serializer = self.get_serializer(queue, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start_consultation(self, request, pk=None):
        """Mark patient consultation as started (no wait time recalculation for doctors)."""
        queue_entry = self.get_object()
        queue_entry.status = 'in_consultation'
        queue_entry.consultation_start_time = timezone.now()
        queue_entry.estimated_wait_time = None  # Clear wait time when consultation starts
        queue_entry.save()
        
        # Skip wait time recalculation for doctors
        # (Only recalculate for non-doctor roles)
        if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor'):
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
        """Mark patient consultation as completed (no wait time recalculation for doctors)."""
        queue_entry = self.get_object()
        doctor = queue_entry.doctor
        queue_entry.status = 'completed'
        queue_entry.consultation_end_time = timezone.now()
        queue_entry.estimated_wait_time = None  # Clear wait time when completed
        queue_entry.save()
        
        # Skip wait time recalculation for doctors
        # (Only recalculate for non-doctor roles)
        if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor'):
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
    
    @action(detail=False, methods=['get'])
    def my_queue(self, request):
        """Get the logged-in doctor's complete queue with statistics."""
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if request.user.role != 'Doctor':
            return Response(
                {'error': 'This endpoint is only available for doctors'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get doctor's queue
        doctor_queue = OPDQueue.objects.filter(doctor_id=request.user.staff_id)
        
        # Calculate statistics
        waiting_count = doctor_queue.filter(status='waiting').count()
        in_consultation_count = doctor_queue.filter(status='in_consultation').count()
        completed_today = doctor_queue.filter(
            status='completed',
            created_at__date=timezone.now().date()
        ).count()
        
        # Get current active queue
        active_queue = doctor_queue.filter(
            status__in=['waiting', 'in_consultation']
        ).order_by('priority', 'check_in_time')
        
        serializer = self.get_serializer(active_queue, many=True)
        
        return Response({
            'doctor_name': request.user.full_name,
            'statistics': {
                'waiting': waiting_count,
                'in_consultation': in_consultation_count,
                'completed_today': completed_today,
                'total_active': waiting_count + in_consultation_count
            },
            'queue': serializer.data
        })


class OPDStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for OPDStatistics read operations."""
    
    queryset = OPDStatistics.objects.all()
    serializer_class = OPDStatisticsSerializer
