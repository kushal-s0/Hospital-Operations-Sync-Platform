from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Hospital, CapacitySnapshot
from .serializers import HospitalSerializer, CapacitySnapshotSerializer


class HospitalViewSet(viewsets.ModelViewSet):
    """ViewSet for Hospital CRUD operations."""
    
    queryset = Hospital.objects.filter(is_active=True)
    serializer_class = HospitalSerializer


class CapacitySnapshotViewSet(viewsets.ModelViewSet):
    """ViewSet for CapacitySnapshot operations."""
    
    queryset = CapacitySnapshot.objects.all()
    serializer_class = CapacitySnapshotSerializer
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest capacity snapshot for all hospitals."""
        hospitals = Hospital.objects.filter(is_active=True)
        snapshots = []
        
        for hospital in hospitals:
            latest = hospital.capacity_snapshots.first()
            if latest:
                snapshots.append(latest)
        
        serializer = self.get_serializer(snapshots, many=True)
        return Response(serializer.data)


class CityDashboardAPIView(APIView):
    """
    Public API for city health dashboard.
    Returns anonymized bed availability data.
    """
    
    def get(self, request):
        """Get anonymized capacity data for all hospitals."""
        hospitals = Hospital.objects.filter(is_active=True)
        data = []
        
        for hospital in hospitals:
            latest = hospital.capacity_snapshots.first()
            if latest:
                occupied = latest.total_beds - latest.available_beds
                occupancy_rate = round((occupied / latest.total_beds * 100), 2) if latest.total_beds > 0 else 0
                
                data.append({
                    'hospital_code': hospital.code,
                    'city': hospital.city,
                    'available_beds': latest.available_beds,
                    'icu_beds_available': latest.icu_beds_available,
                    'occupancy_rate': occupancy_rate,
                    'last_updated': latest.timestamp
                })
        
        return Response(data)
