"""
Add doctors to all departments that don't have one
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser, Department
from django.contrib.auth.hashers import make_password
from django.db import models

print("=" * 60)
print("ADDING DOCTORS TO ALL DEPARTMENTS")
print("=" * 60)

# Get all departments
departments = Department.objects.all()
print(f"\nTotal departments: {departments.count()}\n")

# For each department, check if it has doctors
for dept in departments:
    docs = StaffUser.objects.filter(department=dept, role='Doctor', is_active=True)
    doc_count = docs.count()
    
    print(f"Department: {dept.department_name} (ID: {dept.department_id})")
    print(f"  Existing doctors: {doc_count}")
    
    if doc_count == 0:
        # Get max staff_id
        max_staff_id = StaffUser.objects.aggregate(models.Max('staff_id'))['staff_id__max'] or 0
        new_staff_id = max_staff_id + 1
        
        # Create new doctor
        new_doctor = StaffUser.objects.create(
            staff_id=new_staff_id,
            first_name='Dr.',
            last_name=dept.department_name.replace(' ', ''),
            role='Doctor',
            email=f'doctor{new_staff_id}@hospital.com',
            phone_number='9999999999',
            department=dept,
            is_active=True,
            password_hash=make_password('doctor123')
        )
        print(f"  ✓ Added: {new_doctor.first_name} {new_doctor.last_name}")
    else:
        for doc in docs:
            print(f"  - {doc.first_name} {doc.last_name}")
    print()

# Verify all departments have doctors
print("\n" + "=" * 60)
print("VERIFICATION - DEPARTMENTS WITH DOCTORS")
print("=" * 60 + "\n")

for dept in Department.objects.all():
    docs = StaffUser.objects.filter(department=dept, role='Doctor', is_active=True)
    print(f"✓ {dept.department_name}: {docs.count()} doctor(s)")

print("\n" + "=" * 60)
print("✓ ALL DEPARTMENTS NOW HAVE DOCTORS")
print("=" * 60)
