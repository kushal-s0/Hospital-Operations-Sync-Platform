from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.authentication.models import Department, Bed
from .serializers import DepartmentSerializer, BedSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class BedViewSet(viewsets.ModelViewSet):
    """ViewSet for Bed CRUD operations."""
    
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available beds."""
        available_beds = Bed.objects.filter(status='Available')
        serializer = self.get_serializer(available_beds, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def occupancy_summary(self, request):
        """Get bed occupancy summary by department."""
        departments = Department.objects.all()
        summary = []
        for dept in departments:
            beds = Bed.objects.filter(department=dept)
            total = beds.count()
            available = beds.filter(status='Available').count()
            occupied = beds.filter(status='Occupied').count()
            summary.append({
                'department': dept.department_name,
                'total_beds': total,
                'available': available,
                'occupied': occupied,
                'occupancy_rate': round((occupied / total * 100), 2) if total > 0 else 0
            })
        return Response(summary)

