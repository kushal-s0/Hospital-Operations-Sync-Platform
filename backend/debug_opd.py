import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Appointment
from datetime import datetime, timedelta

print("\n" + "="*60)
print("DEBUGGING OPD QUEUE AND APPOINTMENTS")
print("="*60)

# Check appointments
print("\n1. APPOINTMENTS IN DATABASE:")
print("-" * 60)
appointments = Appointment.objects.all().order_by('-appointment_id')[:5]
print(f"Total appointments: {Appointment.objects.count()}")
print(f"Latest 5 appointments:")
for a in appointments:
    patient_name = f"{a.patient.first_name} {a.patient.last_name}" if a.patient else "N/A"
    print(f"  ID: {a.appointment_id}, Patient: {patient_name}, Status: {a.status}, Priority: {a.priority}")

# Check OPD queue
print("\n2. OPD QUEUE ENTRIES:")
print("-" * 60)
queue_entries = OPDQueue.objects.all().order_by('-check_in_time')[:5]
print(f"Total OPD queue entries: {OPDQueue.objects.count()}")
print(f"Latest 5 entries:")
for q in queue_entries:
    patient_name = f"{q.patient.first_name} {q.patient.last_name}" if q.patient else "N/A"
    print(f"  Token: {q.token_number}, Patient: {patient_name}, Status: {q.status}, Priority: {q.priority}")

# Check appointments that are "In OPD Queue"
print("\n3. APPOINTMENTS WITH 'IN OPD QUEUE' STATUS:")
print("-" * 60)
in_opd_appointments = Appointment.objects.filter(status='In OPD Queue')
print(f"Count: {in_opd_appointments.count()}")
for a in in_opd_appointments:
    patient_name = f"{a.patient.first_name} {a.patient.last_name}" if a.patient else "N/A"
    print(f"  ID: {a.appointment_id}, Patient: {patient_name}")

# Check for recent entries (last 2 hours)
print("\n4. RECENTLY CREATED OPD ENTRIES (last 2 hours):")
print("-" * 60)
two_hours_ago = datetime.now() - timedelta(hours=2)
recent = OPDQueue.objects.filter(created_at__gte=two_hours_ago).order_by('-created_at')
print(f"Count: {recent.count()}")
for q in recent:
    patient_name = f"{q.patient.first_name} {q.patient.last_name}" if q.patient else "N/A"
    dept = q.department.department_name if q.department else "N/A"
    print(f"  Token: {q.token_number}, Patient: {patient_name}, Dept: {dept}, Created: {q.created_at}")

print("\n" + "="*60)
