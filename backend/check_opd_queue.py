"""
Script to check OPD queue entries in the database
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Patient

print("=" * 70)
print("OPD QUEUE DATABASE CHECK")
print("=" * 70)

total = OPDQueue.objects.count()
print(f"\nTotal OPD Queue entries: {total}")

if total > 0:
    print("\n" + "=" * 70)
    print("LATEST 10 ENTRIES (ordered by ID descending)")
    print("=" * 70)
    
    latest = OPDQueue.objects.all().order_by('-id')[:10]
    for q in latest:
        patient_name = q.patient.full_name if q.patient else "N/A"
        doctor_name = f"{q.doctor.first_name} {q.doctor.last_name}" if q.doctor else "N/A"
        dept_name = q.department.department_name if q.department else "N/A"
        
        print(f"\nID: {q.id}")
        print(f"  Token: {q.token_number}")
        print(f"  Patient: {patient_name}")
        print(f"  Doctor: {doctor_name}")
        print(f"  Department: {dept_name}")
        print(f"  Status: {q.status}")
        print(f"  Priority: {q.priority}")
        print(f"  Check-in Time: {q.check_in_time}")
        print(f"  Created At: {q.created_at}")
        print(f"  Wait Time: {q.estimated_wait_time} min")
else:
    print("\nNo entries found in OPD queue!")

print("\n" + "=" * 70)
print("PATIENTS IN DATABASE")
print("=" * 70)
print(f"Total patients: {Patient.objects.count()}")

if Patient.objects.count() > 0:
    print("\nLatest 5 patients:")
    for p in Patient.objects.all().order_by('-patient_id')[:5]:
        print(f"  ID: {p.patient_id}, Name: {p.full_name}, Contact: {p.contact_number}")
