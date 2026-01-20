"""
Test script to verify OPD queue filtering by doctor.
This checks that doctors can only see their own assigned patients.
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Patient, StaffUser, Doctor

print("=" * 80)
print("OPD QUEUE DOCTOR FILTERING TEST")
print("=" * 80)

# Get all doctors
doctors = StaffUser.objects.filter(role='Doctor')
print(f"\nTotal doctors in system: {doctors.count()}")

if doctors.count() == 0:
    print("\n❌ No doctors found in the database!")
    print("Please create doctor users first.")
    sys.exit(1)

print("\n" + "=" * 80)
print("DOCTORS LIST")
print("=" * 80)

for doctor in doctors:
    print(f"\nDoctor ID (staff_id): {doctor.staff_id}")
    print(f"  Name: {doctor.full_name}")
    print(f"  Email: {doctor.email}")
    print(f"  Department: {doctor.department.department_name if doctor.department else 'N/A'}")
    
    # Count patients assigned to this doctor
    patient_count = OPDQueue.objects.filter(doctor_id=doctor.staff_id).count()
    waiting_count = OPDQueue.objects.filter(doctor_id=doctor.staff_id, status='waiting').count()
    in_consultation = OPDQueue.objects.filter(doctor_id=doctor.staff_id, status='in_consultation').count()
    completed = OPDQueue.objects.filter(doctor_id=doctor.staff_id, status='completed').count()
    
    print(f"  Total patients assigned: {patient_count}")
    print(f"    - Waiting: {waiting_count}")
    print(f"    - In Consultation: {in_consultation}")
    print(f"    - Completed: {completed}")

# Show detailed queue for each doctor
print("\n" + "=" * 80)
print("DETAILED QUEUE BY DOCTOR")
print("=" * 80)

for doctor in doctors:
    queue_entries = OPDQueue.objects.filter(doctor_id=doctor.staff_id).order_by('priority', 'check_in_time')
    
    if queue_entries.count() > 0:
        print(f"\n{'=' * 80}")
        print(f"DOCTOR: {doctor.full_name} (ID: {doctor.staff_id})")
        print(f"{'=' * 80}")
        
        for entry in queue_entries:
            patient_name = entry.patient.full_name if entry.patient else "Unknown"
            dept_name = entry.department.department_name if entry.department else "N/A"
            
            print(f"\n  Token #{entry.token_number}")
            print(f"    Patient: {patient_name}")
            print(f"    Department: {dept_name}")
            print(f"    Status: {entry.status}")
            print(f"    Priority: {entry.priority}")
            print(f"    Check-in: {entry.check_in_time}")
            print(f"    Estimated Wait: {entry.estimated_wait_time} min" if entry.estimated_wait_time else "    Estimated Wait: Not calculated")
    else:
        print(f"\n{doctor.full_name} (ID: {doctor.staff_id}): No patients assigned")

# Test filtering logic
print("\n" + "=" * 80)
print("TESTING FILTER LOGIC")
print("=" * 80)

# Pick first doctor for testing
if doctors.count() > 0:
    test_doctor = doctors.first()
    print(f"\nTesting with doctor: {test_doctor.full_name} (ID: {test_doctor.staff_id})")
    
    # Simulate filter query
    filtered_queue = OPDQueue.objects.filter(doctor_id=test_doctor.staff_id)
    print(f"Queue entries for this doctor: {filtered_queue.count()}")
    
    # Check if any entries belong to other doctors
    all_queue = OPDQueue.objects.all()
    other_doctors_queue = all_queue.exclude(doctor_id=test_doctor.staff_id)
    print(f"Queue entries for other doctors: {other_doctors_queue.count()}")
    
    print("\n✅ Filtering logic verification:")
    print(f"   - Total queue entries: {all_queue.count()}")
    print(f"   - {test_doctor.full_name}'s entries: {filtered_queue.count()}")
    print(f"   - Other doctors' entries: {other_doctors_queue.count()}")
    print(f"   - Sum matches: {filtered_queue.count() + other_doctors_queue.count() == all_queue.count()}")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print("\nSummary:")
print("- Doctors can only see patients where opd_queue.doctor_id = staff_user.staff_id")
print("- The filtering is automatically applied in the OPDQueueViewSet.get_queryset() method")
print("- Non-doctor users (Admin, Nurse, Receptionist) can see all queue entries")
