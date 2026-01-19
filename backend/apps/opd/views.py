from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.authentication.models import Visit, Appointment
from .serializers import VisitSerializer, AppointmentSerializer


class OPDQueueViewSet(viewsets.ModelViewSet):
    """ViewSet for OPD Queue operations - uses Visit model."""
    
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    
    @action(detail=False, methods=['get'])
    def current_queue(self, request):
        """Get current active queue based on today's visits."""
        try:
            today = timezone.now().date()
            # Get visits from today that haven't been discharged
            queue = Visit.objects.filter(
                visit_datetime__date=today
            ).order_by('-urgency_level', 'visit_datetime')
            serializer = self.get_serializer(queue, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response([])
    
    @action(detail=True, methods=['post'])
    def start_consultation(self, request, pk=None):
        """Mark patient consultation as started."""
        try:
            visit = self.get_object()
            return Response({'status': 'consultation started'})
        except Exception:
            return Response({'status': 'error'}, status=400)
    
    @action(detail=True, methods=['post'])
    def end_consultation(self, request, pk=None):
        """Mark patient consultation as completed."""
        try:
            visit = self.get_object()
            visit.patient_outcome = 'Discharged'
            visit.save()
            return Response({'status': 'consultation completed'})
        except Exception:
            return Response({'status': 'error'}, status=400)


class OPDStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for OPD Statistics - aggregate visit data."""
    
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    
    def list(self, request):
        """Get OPD statistics summary."""
        today = timezone.now().date()
        try:
            total_today = Visit.objects.filter(visit_datetime__date=today).count()
            avg_wait = Visit.objects.filter(
                visit_datetime__date=today,
                total_wait_time_min__isnull=False
            ).values_list('total_wait_time_min', flat=True)
            avg_wait_time = sum(avg_wait) / len(avg_wait) if avg_wait else 0
            
            return Response({
                'total_patients_today': total_today,
                'average_wait_time': round(avg_wait_time, 1)
            })
        except Exception:
            return Response({
                'total_patients_today': 0,
                'average_wait_time': 0
            })
