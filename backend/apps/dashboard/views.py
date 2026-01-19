from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from apps.beds.models import Bed, Department
from apps.opd.models import OPDQueue
from apps.admissions.models import Admission
from apps.inventory.models import InventoryItem


class DashboardSummaryView(APIView):
    """API view for operational command dashboard."""
    
    def get(self, request):
        """Get dashboard summary metrics."""
        today = timezone.now().date()
        
        # Bed metrics
        total_beds = Bed.objects.count()
        available_beds = Bed.objects.filter(status='available').count()
        occupied_beds = Bed.objects.filter(status='occupied').count()
        occupancy_rate = round((occupied_beds / total_beds * 100), 2) if total_beds > 0 else 0
        
        # OPD metrics
        total_opd_today = OPDQueue.objects.filter(created_at__date=today).count()
        waiting_patients = OPDQueue.objects.filter(
            created_at__date=today,
            status='waiting'
        ).count()
        
        # Admission metrics
        current_admissions = Admission.objects.filter(status='admitted').count()
        
        # Inventory metrics
        low_stock_items = InventoryItem.objects.filter(
            current_stock__lte=models.F('minimum_stock')
        ).count()
        
        return Response({
            'total_beds': total_beds,
            'available_beds': available_beds,
            'occupied_beds': occupied_beds,
            'occupancy_rate': occupancy_rate,
            'total_opd_patients_today': total_opd_today,
            'waiting_patients': waiting_patients,
            'current_admissions': current_admissions,
            'low_stock_items': low_stock_items,
        })


class DepartmentSummaryView(APIView):
    """API view for department-wise summary."""
    
    def get(self, request):
        """Get department-wise metrics."""
        departments = Department.objects.all()
        summary = []
        
        for dept in departments:
            total = dept.beds.count()
            available = dept.beds.filter(status='available').count()
            occupied = dept.beds.filter(status='occupied').count()
            
            summary.append({
                'department': dept.name,
                'floor': dept.floor,
                'total_beds': total,
                'available': available,
                'occupied': occupied,
                'occupancy_rate': round((occupied / total * 100), 2) if total > 0 else 0
            })
        
        return Response(summary)
