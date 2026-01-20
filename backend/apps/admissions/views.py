from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction, models
from apps.authentication.models import Admission, Bed, OPDQueue, Patient, Doctor
from .models import AdmissionRule
from .serializers import AdmissionSerializer, AdmissionRuleSerializer


class AdmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Admission CRUD operations."""
    
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get all current admissions."""
        current_admissions = Admission.objects.filter(status='Active')
        serializer = self.get_serializer(current_admissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def discharge(self, request, pk=None):
        """Discharge a patient."""
        admission = self.get_object()
        admission.status = 'Discharged'
        admission.discharge_time = timezone.now()
        admission.save()
        
        # Set bed to maintenance status after discharge
        if admission.bed:
            admission.bed.status = 'Maintenance'
            admission.bed.save()
        
        return Response({'status': 'patient discharged', 'bed_status': 'maintenance'})
    
    @action(detail=False, methods=['post'])
    def admit_from_opd(self, request):
        """
        Admit a patient from OPD queue.
        Pre-fills information from OPD and assigns a bed.
        """
        try:
            with transaction.atomic():
                # Get request data
                opd_queue_id = request.data.get('opd_queue_id')
                bed_id = request.data.get('bed_id')
                condition_level = request.data.get('condition_level')
                admission_notes = request.data.get('admission_notes', '')
                
                # Validate required fields
                if not opd_queue_id:
                    return Response({
                        'error': 'OPD queue ID is required'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not bed_id:
                    return Response({
                        'error': 'Bed ID is required'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Get OPD queue entry
                try:
                    opd_entry = OPDQueue.objects.get(id=opd_queue_id)
                except OPDQueue.DoesNotExist:
                    return Response({
                        'error': 'OPD queue entry not found'
                    }, status=status.HTTP_404_NOT_FOUND)
                
                # Get bed
                try:
                    bed = Bed.objects.get(bed_id=bed_id)
                except Bed.DoesNotExist:
                    return Response({
                        'error': 'Bed not found'
                    }, status=status.HTTP_404_NOT_FOUND)
                
                # Check if bed is available
                if bed.status != 'Available':
                    return Response({
                        'error': f'Bed {bed_id} is not available (Status: {bed.status})'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Get next admission ID
                max_admission_id = Admission.objects.all().aggregate(
                    models.Max('admission_id'))['admission_id__max']
                next_admission_id = (max_admission_id or 0) + 1
                
                # Get doctor_id from OPD entry
                doctor_id = opd_entry.doctor.staff_id
                
                # Create admission record
                admission = Admission(
                    admission_id=next_admission_id,
                    patient_id=opd_entry.patient.patient_id,
                    bed_id=bed_id,
                    doctor_id=doctor_id,
                    admission_time=timezone.now(),
                    condition_level=condition_level,
                    status='Active',
                    admin_id=request.user.staff_id if hasattr(request.user, 'staff_id') else None
                )
                admission.save()
                
                # Update bed status to Occupied
                bed.status = 'Occupied'
                bed.save()
                
                # Update OPD queue status to completed
                opd_entry.status = 'completed'
                opd_entry.consultation_end_time = timezone.now()
                opd_entry.notes = f"{opd_entry.notes}\n\nPatient admitted to bed {bed_id}. {admission_notes}".strip()
                opd_entry.save()
                
                # Return success response
                serializer = AdmissionSerializer(admission)
                return Response({
                    'message': 'Patient admitted successfully',
                    'admission': serializer.data,
                    'bed_id': bed_id,
                    'bed_status': 'Occupied'
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def match_bed(self, request):
        """Match patient requirements to available beds using rules."""
        patient_requirements = request.data
        
        # Get active rules sorted by priority
        rules = AdmissionRule.objects.filter(is_active=True)
        
        # Find matching beds based on rules
        recommended_beds = Bed.objects.filter(status='Available')
        
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
