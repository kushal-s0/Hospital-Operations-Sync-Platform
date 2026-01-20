"""
Fix: Add a doctor to Emergency department
"""
import os
import sys
import django
from django.db import models

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser, Department
from django.contrib.auth.hashers import make_password

# Find Emergency department
emergency = Department.objects.filter(department_name__icontains='Emergency').first()

if not emergency:
    print("ERROR: Emergency department not found")
    sys.exit(1)

print(f"Found Emergency Department: {emergency.department_name} (ID: {emergency.department_id})")

# Check existing doctors in Emergency
existing_docs = StaffUser.objects.filter(department=emergency, role='Doctor')
print(f"Existing Emergency doctors: {existing_docs.count()}")

if existing_docs.count() > 0:
    for doc in existing_docs:
        print(f"  - {doc.first_name} {doc.last_name}")
else:
    # Add a new doctor to Emergency department
    print("\nAdding new doctor to Emergency department...")
    
    # Get max staff_id
    max_staff_id = StaffUser.objects.aggregate(models.Max('staff_id'))['staff_id__max'] or 0
    new_staff_id = max_staff_id + 1
    
    new_doctor = StaffUser.objects.create(
        staff_id=new_staff_id,
        first_name='Dr. Emergency',
        last_name='Specialist',
        role='Doctor',
        email=f'dr.emergency{new_staff_id}@hospital.com',
        phone_number='9999999999',
        department=emergency,
        is_active=True,
        password_hash=make_password('doctor123')
    )
    
    print(f"✓ Created doctor: {new_doctor.first_name} {new_doctor.last_name}")
    print(f"  Email: {new_doctor.email}")
    print(f"  Department: {new_doctor.department.department_name}")

# Verify
final_docs = StaffUser.objects.filter(department=emergency, role='Doctor')
print(f"\nFinal Emergency doctors: {final_docs.count()}")
for doc in final_docs:
    print(f"  - {doc.first_name} {doc.last_name}")
