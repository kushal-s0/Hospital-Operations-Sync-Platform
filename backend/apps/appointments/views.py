from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction, models
from django.utils import timezone
from datetime import datetime, timedelta

from apps.authentication.models import Appointment, Patient, StaffUser, OPDQueue, Department
from .serializers import AppointmentBookingSerializer, AppointmentSerializer, AppointmentStatusUpdateSerializer
from apps.utils import get_ist_now, get_ist_today


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
                    registration_date=get_ist_today(),
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
            print(f"Current server date (IST): {get_ist_today()}")
            print(f"Appointments found for {date_filter}: {queryset.count()}")
            for apt in queryset:
                print(f"  - Appointment {apt.appointment_id}: {apt.appointment_date}")
        
        # Filter by doctor
        doctor_id = self.request.query_params.get('doctor_id', None)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        # Get upcoming appointments by default
        show_all = self.request.query_params.get('all', None)
        if not show_all:
            queryset = queryset.filter(appointment_date__gte=get_ist_today())
        
        return queryset.order_by('appointment_date', 'appointment_time')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve an appointment and add to OPD queue.
        """
        from django.db import connection
        
        appointment = self.get_object()
        
        print("=" * 80)
        print(f"APPROVE APPOINTMENT CALLED - ID: {appointment.appointment_id}")
        print(f"Current status: {appointment.status}")
        print(f"Appointment date: {appointment.appointment_date}")
        print(f"Today's date (IST): {get_ist_today()}")
        print("=" * 80)
        
        if appointment.status == 'Cancelled':
            print("ERROR: Cannot approve cancelled appointment")
            return Response({
                'error': 'Cannot approve a cancelled appointment'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if appointment.status in ['Completed', 'Approved']:
            print("INFO: Appointment already processed")
            return Response({
                'message': 'Appointment already processed'
            }, status=status.HTTP_200_OK)
        
        try:
            # Step 1: Update appointment status
            print(f"\nSTEP 1: Updating appointment status to Completed...")
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE appointments SET status = %s WHERE appointment_id = %s",
                    ['Completed', appointment.appointment_id]
                )
                affected_rows = cursor.rowcount
                print(f"SUCCESS: Updated {affected_rows} row(s)")
            
            # Step 2: Check if appointment is for today (IST)
            today = get_ist_today()
            apt_date = appointment.appointment_date
            
            print(f"\nSTEP 2: Date comparison")
            print(f"  UTC time:         {timezone.now()}")
            print(f"  IST time:         {get_ist_now()}")
            print(f"  Appointment date: {apt_date} (type: {type(apt_date)})")
            print(f"  Today's date:     {today} (type: {type(today)})")
            print(f"  Are they equal?   {apt_date == today}")
            
            if apt_date != today:
                print(f"\nINFO: Appointment is NOT for today - skipping OPD queue")
                return Response({
                    'message': 'Appointment approved. Patient will be added to queue on appointment date.'
                }, status=status.HTTP_200_OK)
            
            print(f"\nSTEP 2: Appointment is for today - creating OPD queue entry...")
            
            # Step 3: Validate doctor
            if not appointment.doctor_id:
                print("ERROR: No doctor assigned")
                return Response({
                    'error': 'No doctor assigned to this appointment'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                doctor = StaffUser.objects.get(staff_id=appointment.doctor_id)
                print(f"SUCCESS: Found doctor: {doctor.full_name} (ID: {doctor.staff_id})")
            except StaffUser.DoesNotExist:
                print(f"ERROR: Doctor {appointment.doctor_id} not found")
                return Response({
                    'error': f'Doctor with staff_id {appointment.doctor_id} not found'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Step 4: Get next token number
            print(f"\nSTEP 3: Calculating next token number...")
            # Use IST date for token calculation
            today = get_ist_today()
            max_token = OPDQueue.objects.filter(
                doctor_id=appointment.doctor_id,
                check_in_time__date=today
            ).aggregate(models.Max('token_number'))['token_number__max']
            
            next_token = (max_token or 0) + 1
            print(f"SUCCESS: Next token number: {next_token}")
            
            # Step 5: Get next OPD queue ID
            print(f"\nSTEP 4: Getting next OPD queue ID...")
            max_opd_id = OPDQueue.objects.all().aggregate(models.Max('id'))['id__max']
            next_opd_id = (max_opd_id or 0) + 1
            print(f"SUCCESS: Next OPD queue ID: {next_opd_id}")
            
            # Step 6: Insert into OPD queue
            print(f"\nSTEP 5: Inserting into opd_queue table...")
            print(f"  - Patient ID: {appointment.patient.patient_id}")
            print(f"  - Doctor ID: {appointment.doctor_id}")
            print(f"  - Department ID: {doctor.department_id if doctor.department else 'None'}")
            print(f"  - Token: {next_token}")
            
            # Get current time in IST for check_in_time
            check_in_time_ist = get_ist_now()
            print(f"  - Check-in time (IST): {check_in_time_ist}")
            
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO opd_queue 
                    (id, patient_id, doctor_id, department_id, token_number, status, 
                     priority, check_in_time, notes, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, [
                    next_opd_id,
                    appointment.patient.patient_id,
                    appointment.doctor_id,
                    doctor.department_id if doctor.department else None,
                    next_token,
                    'waiting',
                    'normal',
                    check_in_time_ist,
                    f"Appointment approved: {appointment.reason_for_visit}"
                ])
                affected_rows = cursor.rowcount
                print(f"SUCCESS: Inserted {affected_rows} row(s) into opd_queue")
            
            print(f"\n{'=' * 80}")
            print(f"COMPLETE: Created OPD queue entry #{next_opd_id} with token #{next_token}")
            print(f"{'=' * 80}\n")
            
            return Response({
                'message': 'Appointment approved and added to OPD queue',
                'token_number': next_token,
                'opd_queue_id': next_opd_id
            }, status=status.HTTP_200_OK)
                
        except Exception as e:
            print(f"\n{'!' * 80}")
            print(f"ERROR OCCURRED: {str(e)}")
            print(f"{'!' * 80}")
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
        print(f"Stats endpoint - Today's date: {today}")
        print(f"Current timezone: {timezone.now()}")
        
        stats = {
            'total_pending': Appointment.objects.filter(status='Scheduled', appointment_date__gte=today).count(),
            'today_appointments': Appointment.objects.filter(appointment_date=today).exclude(status='Cancelled').count(),
            'upcoming_appointments': Appointment.objects.filter(
                appointment_date__gt=today,
                appointment_date__lte=today + timedelta(days=7)
            ).exclude(status='Cancelled').count(),
        }
        
        print(f"Stats: {stats}")
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
