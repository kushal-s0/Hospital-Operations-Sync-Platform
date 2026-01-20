"""
Create a test appointment for TODAY to test the approval → OPD queue flow
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, Patient, StaffUser
from django.utils import timezone
from django.db import models

print("=" * 80)
print("Creating Test Appointment for TODAY")
print("=" * 80)

# Get today's date
today = timezone.now().date()
print(f"\nToday's Date: {today}")

# Get an existing patient
patient = Patient.objects.first()
print(f"Patient: {patient.full_name} (ID: {patient.patient_id})")

# Get a doctor
doctor = StaffUser.objects.filter(role='Doctor').first()
print(f"Doctor: {doctor.full_name} (ID: {doctor.staff_id})")
print(f"Department: {doctor.department.department_name if doctor.department else 'None'}")

# Get next appointment ID
max_id = Appointment.objects.aggregate(models.Max('appointment_id'))['appointment_id__max']
next_id = (max_id or 0) + 1

# Create appointment for TODAY
appointment = Appointment(
    appointment_id=next_id,
    patient=patient,
    doctor_id=doctor.staff_id,
    appointment_date=today,  # TODAY!
    appointment_time="10:00:00",
    reason_for_visit="TEST: Checking approval to OPD queue flow",
    status='Scheduled'  # Ready to be approved
)
appointment.save()

print("\n" + "=" * 80)
print("✅ TEST APPOINTMENT CREATED!")
print("=" * 80)
print(f"Appointment ID: {appointment.appointment_id}")
print(f"Patient: {patient.full_name}")
print(f"Doctor: {doctor.full_name}")
print(f"Date: {appointment.appointment_date} (TODAY!)")
print(f"Time: {appointment.appointment_time}")
print(f"Status: {appointment.status}")
print(f"Reason: {appointment.reason_for_visit}")
print("=" * 80)
print("\nNEXT STEPS:")
print(f"1. Restart your backend server")
print(f"2. Go to Appointments page in frontend")
print(f"3. Find appointment #{appointment.appointment_id}")
print(f"4. Click 'Approve & Add to Queue'")
print(f"5. Check OPD Queue page - patient should appear!")
print("=" * 80)
