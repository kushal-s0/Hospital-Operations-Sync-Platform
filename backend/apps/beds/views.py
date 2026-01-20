from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apps.authentication.models import Department, Bed, Admission
from .serializers import DepartmentSerializer, BedSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = None  # Disable pagination to show all departments

class BedViewSet(viewsets.ModelViewSet):
    """ViewSet for Bed CRUD operations."""
    
    queryset = Bed.objects.all()
    serializer_class = BedSerializer
    pagination_class = None  # Disable pagination to show all beds

    def _check_bed_assignment(self, bed_instance, new_status, old_status):
        """Check if bed is assigned to an active admission before allowing status change."""
        # Only check when changing FROM Occupied status
        if old_status == 'Occupied' and new_status != 'Occupied':
            # Check if bed is assigned to any active admission
            active_admission = Admission.objects.filter(
                bed=bed_instance,
                status='Active'
            ).first()
            
            if active_admission:
                raise ValidationError({
                    'status': f'Cannot change bed status. Bed is currently assigned to patient '
                             f'{active_admission.patient_name} (Admission #{active_admission.admission_id}). '
                             f'Please discharge the patient first before changing bed status.'
                })

    def update(self, request, *args, **kwargs):
        """Override update to add bed assignment validation."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_status = instance.status
        
        # Check if status is being changed
        new_status = request.data.get('status')
        if new_status and new_status != old_status:
            self._check_bed_assignment(instance, new_status, old_status)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Override partial_update to add bed assignment validation."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    
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

