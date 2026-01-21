"""
Debug script to check OPD queue entries created from appointments
"""

import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Appointment
from django.utils import timezone

print("=" * 80)
print("OPD QUEUE DEBUG - Checking Recent Entries")
print("=" * 80)

# Check recent OPD queue entries
print("\n📋 Recent OPD Queue Entries (Last 10):")
print("-" * 80)
recent_queue = OPDQueue.objects.all().order_by('-id')[:10]

if not recent_queue:
    print("❌ NO OPD QUEUE ENTRIES FOUND!")
else:
    for q in recent_queue:
        print(f"""
ID: {q.id}
Patient: {q.patient.full_name if q.patient else 'None'} (ID: {q.patient_id})
Doctor: {q.doctor.full_name if q.doctor else 'None'} (ID: {q.doctor_id})
Department: {q.department.name if q.department else 'None'} (ID: {q.department_id})
Token: #{q.token_number}
Status: {q.status}
Priority: {q.priority}
Check-in: {q.check_in_time}
Created: {q.created_at}
Updated: {q.updated_at}
Notes: {q.notes}
{'─' * 80}""")

# Check recent appointments
print("\n📅 Recent Appointments (Last 5):")
print("-" * 80)
recent_appointments = Appointment.objects.all().order_by('-appointment_id')[:5]

if not recent_appointments:
    print("❌ NO APPOINTMENTS FOUND!")
else:
    for apt in recent_appointments:
        print(f"""
ID: {apt.appointment_id}
Patient: {apt.patient.full_name if apt.patient else 'None'} (ID: {apt.patient_id})
Doctor ID: {apt.doctor_id}
Date: {apt.appointment_date}
Time: {apt.appointment_time}
Status: {apt.status}
Reason: {apt.reason_for_visit}
Created: {apt.created_at}
{'─' * 80}""")

# Check if today's appointments have corresponding OPD entries
print("\n🔍 Checking Today's Approved Appointments vs OPD Queue:")
print("-" * 80)
today = timezone.now().date()
today_appointments = Appointment.objects.filter(
    appointment_date=today,
    status__in=['Completed', 'Approved']
).order_by('-appointment_id')

print(f"Today's date: {today}")
print(f"Approved appointments for today: {today_appointments.count()}")

for apt in today_appointments:
    # Check if there's a corresponding OPD entry
    opd_entry = OPDQueue.objects.filter(
        patient_id=apt.patient_id,
        doctor_id=apt.doctor_id,
        check_in_time__date=today
    ).first()
    
    status_symbol = "✅" if opd_entry else "❌"
    print(f"""
{status_symbol} Appointment #{apt.appointment_id}
   Patient: {apt.patient.full_name if apt.patient else 'None'}
   Doctor ID: {apt.doctor_id}
   Status: {apt.status}
   OPD Entry: {'Found (ID: ' + str(opd_entry.id) + ', Token: #' + str(opd_entry.token_number) + ')' if opd_entry else 'NOT FOUND!'}
""")

print("=" * 80)
print("DEBUG COMPLETE")
print("=" * 80)
