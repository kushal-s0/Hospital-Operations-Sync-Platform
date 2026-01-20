import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, Patient
from django.db import models

print("Testing Appointment queries...")
try:
    # Get all appointments
    all_appointments = Appointment.objects.all()
    print(f"Total appointments: {all_appointments.count()}")
    
    # Get scheduled appointments
    scheduled = Appointment.objects.filter(status='Scheduled')
    print(f"Scheduled appointments: {scheduled.count()}")
    
    # List details of scheduled appointments
    for appt in scheduled:
        print(f"\nAppointment ID: {appt.appointment_id}")
        print(f"  Patient ID: {appt.patient_id if hasattr(appt, 'patient_id') else 'N/A'}")
        print(f"  Doctor ID: {appt.doctor_id if hasattr(appt, 'doctor_id') else 'N/A'}")
        print(f"  Date: {appt.appointment_date}")
        print(f"  Time: {appt.appointment_time}")
        print(f"  Status: {appt.status}")
        print(f"  Reason: {appt.reason_for_visit}")
        
        # Try to access patient
        try:
            if appt.patient:
                print(f"  Patient: {appt.patient.first_name} {appt.patient.last_name}")
        except Exception as e:
            print(f"  Patient access error: {e}")
        
        # Try to access doctor
        try:
            if appt.doctor:
                print(f"  Doctor: {appt.doctor}")
        except Exception as e:
            print(f"  Doctor access error: {e}")
    
    print("\n✅ Query successful!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
