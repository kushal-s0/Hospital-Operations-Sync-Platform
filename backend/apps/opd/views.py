from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, Count
from .models import OPDQueue, OPDStatistics
from .serializers import OPDQueueSerializer, OPDStatisticsSerializer
import joblib
import numpy as np
import os
from datetime import datetime

# Path to saved models
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models')


# =============================================================================
# WAIT TIME PREDICTION ENDPOINT
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
            print(f"Successfully created: {serializer.data}")
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f"Error creating queue entry: {str(e)}")
            import traceback
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
        """Mark patient consultation as started."""
        queue_entry = self.get_object()
        queue_entry.status = 'in_consultation'
        queue_entry.consultation_start_time = timezone.now()
        queue_entry.save()
        return Response({'status': 'consultation started'})
    
    @action(detail=True, methods=['post'])
    def end_consultation(self, request, pk=None):
        """Mark patient consultation as completed."""
        queue_entry = self.get_object()
        queue_entry.status = 'completed'
        queue_entry.consultation_end_time = timezone.now()
        queue_entry.save()
        return Response({'status': 'consultation completed'})


class OPDStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for OPDStatistics read operations."""
    
    queryset = OPDStatistics.objects.all()
    serializer_class = OPDStatisticsSerializer
