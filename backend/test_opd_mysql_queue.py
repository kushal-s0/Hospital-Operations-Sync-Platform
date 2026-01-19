"""
Test script to verify OPD Queue MySQL integration
Run: python test_opd_mysql_queue.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Patient, StaffUser, Department
from django.db.models import Max
from django.utils import timezone

def test_opd_queue():
    print("=" * 60)
    print("TESTING OPD QUEUE MYSQL INTEGRATION")
    print("=" * 60)
    
    # 1. Check if we have doctors
    print("\n1. Checking for doctors...")
    doctors = StaffUser.objects.filter(role='Doctor')
    if not doctors.exists():
        print("❌ No doctors found in staff_users table!")
        print("   Please create at least one doctor first.")
        return
    
    doctor = doctors.first()
    print(f"✅ Found doctor: {doctor.full_name} (ID: {doctor.staff_id})")
    
    # 2. Check if we have departments
    print("\n2. Checking for departments...")
    departments = Department.objects.all()
    if not departments.exists():
        print("❌ No departments found in departments table!")
        print("   Please create at least one department first.")
        return
    
    department = departments.first()
    print(f"✅ Found department: {department.department_name} (ID: {department.department_id})")
    
    # 3. Check existing queue entries
    print("\n3. Checking existing queue entries...")
    existing_queue = OPDQueue.objects.all()
    print(f"📊 Found {existing_queue.count()} existing queue entries")
    
    if existing_queue.exists():
        print("\nSample queue entries:")
        for entry in existing_queue[:3]:
            print(f"  Token #{entry.token_number}:")
            print(f"    Patient: {entry.patient.full_name if entry.patient else 'N/A'}")
            print(f"    Doctor: {entry.doctor.full_name if entry.doctor else 'N/A'}")
            print(f"    Department: {entry.department.department_name if entry.department else 'N/A'}")
            print(f"    Status: {entry.status}")
            print()
    
    # 4. Test creating a new queue entry
    print("\n4. Testing new queue entry creation...")
    
    # Create a test patient
    max_patient = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
    next_patient_id = (max_patient or 0) + 1
    
    test_patient = Patient.objects.create(
        patient_id=next_patient_id,
        first_name="Test",
        last_name="Patient",
        contact_number="9999999999",
        registration_date=timezone.now().date()
    )
    print(f"✅ Created test patient: {test_patient.full_name} (ID: {test_patient.patient_id})")
    
    # Get next token number
    max_token = OPDQueue.objects.aggregate(Max('token_number'))['token_number__max']
    next_token = (max_token or 0) + 1
    
    # Create queue entry
    queue_entry = OPDQueue.objects.create(
        patient=test_patient,
        doctor=doctor,
        department=department,
        token_number=next_token,
        status='waiting',
        priority='normal',
        check_in_time=timezone.now(),
        created_at=timezone.now(),
        estimated_wait_time=15,
        notes="Test queue entry from integration test"
    )
    
    print(f"✅ Created queue entry:")
    print(f"   Token #: {queue_entry.token_number}")
    print(f"   Patient: {queue_entry.patient.full_name}")
    print(f"   Doctor: {queue_entry.doctor.full_name}")
    print(f"   Department: {queue_entry.department.department_name}")
    print(f"   Status: {queue_entry.status}")
    print(f"   Priority: {queue_entry.priority}")
    
    # 5. Test updating queue entry (start consultation)
    print("\n5. Testing consultation start...")
    queue_entry.status = 'in_consultation'
    queue_entry.consultation_start_time = timezone.now()
    queue_entry.save()
    print(f"✅ Updated status to: {queue_entry.status}")
    print(f"   Start time: {queue_entry.consultation_start_time}")
    
    # 6. Test completing consultation
    print("\n6. Testing consultation completion...")
    queue_entry.status = 'completed'
    queue_entry.consultation_end_time = timezone.now()
    queue_entry.save()
    print(f"✅ Updated status to: {queue_entry.status}")
    print(f"   End time: {queue_entry.consultation_end_time}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\n📝 Summary:")
    print(f"   - Doctors available: {doctors.count()}")
    print(f"   - Departments available: {departments.count()}")
    print(f"   - Total queue entries: {OPDQueue.objects.count()}")
    print(f"   - Waiting: {OPDQueue.objects.filter(status='waiting').count()}")
    print(f"   - In consultation: {OPDQueue.objects.filter(status='in_consultation').count()}")
    print(f"   - Completed: {OPDQueue.objects.filter(status='completed').count()}")
    print("\n✨ OPD Queue MySQL integration is working correctly!")

if __name__ == '__main__':
    try:
        test_opd_queue()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
