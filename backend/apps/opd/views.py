from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import OPDQueue, OPDStatistics
from .serializers import OPDQueueSerializer, OPDStatisticsSerializer


class OPDQueueViewSet(viewsets.ModelViewSet):
    """ViewSet for OPDQueue CRUD operations."""
    
    queryset = OPDQueue.objects.all()
    serializer_class = OPDQueueSerializer
    
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
