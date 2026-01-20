from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction, models
from django.utils import timezone
from datetime import datetime, timedelta
import traceback

from apps.authentication.models import Appointment, Patient, StaffUser, OPDQueue, Department
from .serializers import AppointmentBookingSerializer, AppointmentSerializer, AppointmentStatusUpdateSerializer


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow public booking
def book_appointment(request):
    """
    Public API endpoint for booking appointments from landing page.
    Creates or updates patient record and creates appointment.
    """
    import traceback
    
    serializer = AppointmentBookingSerializer(data=request.data)
    
    if not serializer.is_valid():
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    print("Validated data:", data)
    
    try:
        with transaction.atomic():
            # Find existing patient by email
            patient = None
            try:
                patient = Patient.objects.get(email=data['email'])
                print(f"Found existing patient: {patient.patient_id}")
                # Update patient info if already exists
                patient.first_name = data['first_name']
                patient.last_name = data['last_name']
                patient.contact_number = data['contact_number']
                patient.date_of_birth = data['date_of_birth']
                patient.gender = data['gender']
                if data.get('address'):
                    patient.address = data['address']
                patient.save()
                created = False
            except Patient.DoesNotExist:
                print("Creating new patient...")
                # Create new patient
                max_patient_id = Patient.objects.aggregate(models.Max('patient_id'))['patient_id__max']
                next_patient_id = (max_patient_id or 0) + 1
                print(f"Next patient_id: {next_patient_id}")
                
                patient = Patient(
                    patient_id=next_patient_id,
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    contact_number=data['contact_number'],
                    date_of_birth=data['date_of_birth'],
                    gender=data['gender'],
                    address=data.get('address', ''),
                    registration_date=timezone.now().date(),
                )
                patient.save()
                print(f"Patient created: {patient.patient_id}")
                created = True
            
            # Get next appointment ID
            max_id = Appointment.objects.aggregate(models.Max('appointment_id'))['appointment_id__max']
            next_id = (max_id or 0) + 1
            print(f"Next appointment_id: {next_id}")
            
            # Create appointment with 'Scheduled' status (pending approval)
            appointment = Appointment(
                appointment_id=next_id,
                patient=patient,
                doctor_id=data.get('doctor_id'),
                appointment_date=data['appointment_date'],
                appointment_time=data['appointment_time'],
                reason_for_visit=data['reason_for_visit'],
                status='Scheduled',  # Pending approval
            )
            appointment.save()
            print(f"Appointment created: {appointment.appointment_id}")
            
            response_serializer = AppointmentSerializer(appointment)
            
            return Response({
                'message': 'Appointment booked successfully! You will be notified once it is approved.',
                'appointment': response_serializer.data,
                'patient_created': created
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"Error booking appointment: {str(e)}")
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing appointments (Admin/Nurse access).
    Supports listing, updating status, and approving appointments.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """Override list to add better error handling"""
        import traceback
        try:
            queryset = self.get_queryset()
            print(f"Queryset count: {queryset.count()}")
            
            serializer = self.get_serializer(queryset, many=True)
            print("Serialization successful")
            return Response(serializer.data)
        except Exception as e:
            print(f"Error in list: {str(e)}")
            traceback.print_exc()
            return Response({
                'error': str(e),
                'detail': 'Error fetching appointments'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_queryset(self):
        """Filter appointments based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            print(f"Filtering by status: {status_filter}")
        
        # Filter by date
        date_filter = self.request.query_params.get('date', None)
        if date_filter:
            queryset = queryset.filter(appointment_date=date_filter)
            print(f"Filtering by date: {date_filter}")
        
        # Filter by doctor
        doctor_id = self.request.query_params.get('doctor_id', None)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        # Get upcoming appointments by default
        show_all = self.request.query_params.get('all', None)
        if not show_all:
            queryset = queryset.filter(appointment_date__gte=timezone.now().date())
        
        return queryset.order_by('appointment_date', 'appointment_time')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve an appointment and add to OPD queue.
        """
        appointment = self.get_object()
        
        print("=" * 80)
        print(f"APPROVING APPOINTMENT #{appointment.appointment_id}")
        print("=" * 80)
        print(f"Patient: {appointment.patient.full_name} (ID: {appointment.patient_id})")
        print(f"Doctor ID: {appointment.doctor_id}")
        print(f"Appointment Date: {appointment.appointment_date}")
        print(f"Today's Date: {timezone.now().date()}")
        print(f"Current Status: {appointment.status}")
        print("=" * 80)
        
        if appointment.status == 'Cancelled':
            return Response({
                'error': 'Cannot approve a cancelled appointment'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if appointment.status in ['Completed', 'Approved']:
            return Response({
                'message': 'Appointment already processed'
            }, status=status.HTTP_200_OK)
        
        try:
            with transaction.atomic():
                # Update appointment status to Completed to prevent re-approval
                appointment.status = 'Completed'
                appointment.save()
                print("✅ Appointment status updated to 'Completed'")
                
                # Check if appointment is for today
                if appointment.appointment_date == timezone.now().date():
                    print("📅 Appointment is for TODAY - Adding to OPD queue...")
                    
                    # Get the doctor as StaffUser instance
                    if not appointment.doctor_id:
                        print("❌ ERROR: No doctor assigned!")
                        return Response({
                            'error': 'No doctor assigned to this appointment'
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    doctor = StaffUser.objects.get(staff_id=appointment.doctor_id)
                    print(f"👨‍⚕️ Doctor: {doctor.full_name} (ID: {doctor.staff_id})")
                    print(f"🏥 Department: {doctor.department.department_name if doctor.department else 'None'}")
                    
                    # Add to OPD Queue
                    # Get next token number for the doctor/department
                    today = timezone.now().date()
                    max_token = OPDQueue.objects.filter(
                        doctor_id=appointment.doctor_id,
                        check_in_time__date=today
                    ).aggregate(models.Max('token_number'))['token_number__max']
                    
                    next_token = (max_token or 0) + 1
                    print(f"🎫 Next Token Number: {next_token}")
                    
                    # Create OPD queue entry
                    current_time = timezone.now()
                    opd_entry = OPDQueue(
                        patient=appointment.patient,
                        doctor=doctor,
                        department=doctor.department,
                        token_number=next_token,
                        status='waiting',
                        priority='normal',
                        check_in_time=current_time,
                        notes=f"Appointment approved: {appointment.reason_for_visit}",
                        created_at=current_time,
                        updated_at=current_time
                    )
                    opd_entry.save()
                    
                    print("=" * 80)
                    print("✅ OPD QUEUE ENTRY CREATED SUCCESSFULLY!")
                    print(f"   OPD ID: {opd_entry.id}")
                    print(f"   Patient ID: {opd_entry.patient_id}")
                    print(f"   Doctor ID: {opd_entry.doctor_id}")
                    print(f"   Department ID: {opd_entry.department_id}")
                    print(f"   Token: #{opd_entry.token_number}")
                    print(f"   Status: {opd_entry.status}")
                    print(f"   Check-in: {opd_entry.check_in_time}")
                    print(f"   Created: {opd_entry.created_at}")
                    print(f"   Updated: {opd_entry.updated_at}")
                    print("=" * 80)
                    
                    return Response({
                        'message': 'Appointment approved and added to OPD queue',
                        'token_number': next_token,
                        'opd_queue_id': opd_entry.id
                    }, status=status.HTTP_200_OK)
                else:
                    print(f"📅 Appointment is for {appointment.appointment_date} (NOT today)")
                    print("   → Not adding to OPD queue yet")
                    return Response({
                        'message': 'Appointment approved. Patient will be added to queue on appointment date.'
                    }, status=status.HTTP_200_OK)
                    
        except Exception as e:
            print("=" * 80)
            print(f"❌ ERROR DURING APPROVAL: {str(e)}")
            print("=" * 80)
            import traceback
            traceback.print_exc()
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        
        if appointment.status == 'Completed':
            return Response({
                'error': 'Cannot cancel a completed appointment'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = 'Cancelled'
        appointment.save()
        
        return Response({
            'message': 'Appointment cancelled successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending appointments (status = Scheduled, awaiting approval)"""
        pending_appointments = self.get_queryset().filter(status='Scheduled')
        serializer = self.get_serializer(pending_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get appointment statistics"""
        today = timezone.now().date()
        
        stats = {
            'total_pending': Appointment.objects.filter(status='Scheduled', appointment_date__gte=today).count(),
            'today_appointments': Appointment.objects.filter(appointment_date=today).exclude(status='Cancelled').count(),
            'upcoming_appointments': Appointment.objects.filter(
                appointment_date__gt=today,
                appointment_date__lte=today + timedelta(days=7)
            ).exclude(status='Cancelled').count(),
        }
        
        return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_available_doctors(request):
    """Get list of available doctors for appointment booking"""
    department_id = request.query_params.get('department_id', None)
    
    doctors = StaffUser.objects.filter(role='Doctor', is_active=True).select_related('department')
    
    if department_id:
        doctors = doctors.filter(department_id=department_id)
    
    doctor_list = [{
        'id': doctor.staff_id,
        'name': f"Dr. {doctor.first_name} {doctor.last_name}",
        'department': doctor.department.department_name if doctor.department else None,
        'department_id': doctor.department.department_id if doctor.department else None
    } for doctor in doctors]
    
    return Response(doctor_list)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_departments(request):
    """Get list of departments for appointment booking"""
    departments = Department.objects.all()
    
    department_list = [{
        'id': dept.department_id,
        'name': dept.department_name
    } for dept in departments]
    
    return Response(department_list)
