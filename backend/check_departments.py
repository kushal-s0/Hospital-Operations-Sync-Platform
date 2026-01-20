import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Department, StaffUser

print("\n" + "="*60)
print("DEPARTMENTS IN DATABASE")
print("="*60)

departments = Department.objects.all()
for d in departments:
    print(f"ID: {d.department_id}, Name: {d.department_name}")

print("\n" + "="*60)
print("DOCTORS IN DATABASE")
print("="*60)

doctors = StaffUser.objects.filter(role='Doctor')
for d in doctors:
    dept_name = d.department.department_name if d.department else "No Dept"
    print(f"ID: {d.staff_id}, Name: {d.first_name} {d.last_name}, Dept: {dept_name} (ID: {d.department_id})")

print("\n" + "="*60)
print("CREATING MISSING DEPARTMENTS AND DOCTORS")
print("="*60)

# Check if Dermatology department exists
derma_dept = Department.objects.filter(department_name__iexact='Dermatology').first()
if not derma_dept:
    print("\n✓ Creating Dermatology department...")
    cursor = __import__('django.db').db.connection.cursor()
    cursor.execute("SELECT MAX(department_id) FROM departments")
    max_id = cursor.fetchone()[0] or 0
    next_id = max_id + 1
    
    derma_dept = Department.objects.create(
        department_id=next_id,
        hospital_id=1,
        department_name='Dermatology',
        total_beds=20,
        available_beds=20,
        emergency_beds=0
    )
    print(f"  Created: Dermatology (ID: {derma_dept.department_id})")
else:
    print(f"✓ Dermatology department exists (ID: {derma_dept.department_id})")

# Check if there's a doctor in Dermatology
derma_doctors = StaffUser.objects.filter(department=derma_dept, role='Doctor')
if derma_doctors.count() == 0:
    print("\n✓ Creating doctor for Dermatology...")
    cursor = __import__('django.db').db.connection.cursor()
    cursor.execute("SELECT MAX(staff_id) FROM staff_users")
    max_id = cursor.fetchone()[0] or 0
    next_id = max_id + 1
    
    doctor = StaffUser.objects.create(
        staff_id=next_id,
        hospital_id=1,
        department=derma_dept,
        first_name='Dr. Skin',
        last_name='Specialist',
        role='Doctor',
        phone_number='9999999999',
        email='derma.doctor@hospital.com',
        password_hash='hashed_password',
        is_active=True
    )
    print(f"  Created: Dr. Skin Specialist (ID: {doctor.staff_id})")
else:
    print(f"✓ Dermatology has {derma_doctors.count()} doctor(s)")

print("\n" + "="*60)
