from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Admission, AdmissionRule
from .serializers import AdmissionSerializer, AdmissionRuleSerializer
from apps.beds.models import Bed


class AdmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Admission CRUD operations."""
    
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get all current admissions."""
        current_admissions = Admission.objects.filter(status='admitted')
        serializer = self.get_serializer(current_admissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def discharge(self, request, pk=None):
        """Discharge a patient."""
        admission = self.get_object()
        admission.status = 'discharged'
        admission.discharge_date = timezone.now()
        admission.save()
        
        # Free up the bed
        if admission.bed:
            admission.bed.status = 'available'
            admission.bed.save()
        
        return Response({'status': 'patient discharged'})
    
    @action(detail=False, methods=['post'])
    def match_bed(self, request):
        """Match patient requirements to available beds using rules."""
        patient_requirements = request.data
        
        # Get active rules sorted by priority
        rules = AdmissionRule.objects.filter(is_active=True)
        
        # Find matching beds based on rules
        recommended_beds = Bed.objects.filter(status='available')
        
        # Apply rule-based filtering (simplified)
        bed_type = patient_requirements.get('bed_type')
        if bed_type:
            recommended_beds = recommended_beds.filter(bed_type=bed_type)
        
        from apps.beds.serializers import BedSerializer
        serializer = BedSerializer(recommended_beds[:10], many=True)
        return Response(serializer.data)


class AdmissionRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for AdmissionRule CRUD operations."""
    
    queryset = AdmissionRule.objects.all()
    serializer_class = AdmissionRuleSerializer
