"""
Script to create staff users with proper Django password hashing
Run this after inserting the dummy data OR to create users directly
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser, Hospital, Department
from django.contrib.auth.hashers import make_password
from django.db import connection

def ensure_hospital_and_departments():
    """Ensure at least one hospital and department exist"""
    cursor = connection.cursor()
    
    # Check if hospitals exist
    cursor.execute("SELECT COUNT(*) FROM hospitals")
    hospital_count = cursor.fetchone()[0]
    
    if hospital_count == 0:
        print("Creating default hospital...")
        cursor.execute("""
            INSERT INTO hospitals (hospital_id, hospital_name, region, facility_size_beds) 
            VALUES (1, 'City General Hospital', 'Urban', 500)
        """)
    
    # Check if departments exist
    cursor.execute("SELECT COUNT(*) FROM departments")
    dept_count = cursor.fetchone()[0]
    
    if dept_count == 0:
        print("Creating default departments...")
        cursor.execute("""
            INSERT INTO departments (department_id, hospital_id, department_name, total_beds, available_beds, emergency_beds) VALUES
            (1, 1, 'Emergency', 50, 10, 20),
            (2, 1, 'Cardiology', 40, 15, 5),
            (3, 1, 'Orthopedics', 35, 12, 3)
        """)
    
    connection.commit()

def create_staff_users():
    """Create staff users with proper password hashing"""
    
    staff_data = [
        {
            'staff_id': 1,
            'hospital_id': 1,
            'department_id': 1,
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'Admin',
            'phone_number': '9876543210',
            'email': 'admin@hospital.com',
            'password': 'admin123',
        },
        {
            'staff_id': 2,
            'hospital_id': 1,
            'department_id': 2,
            'first_name': 'John',
            'last_name': 'Smith',
            'role': 'Doctor',
            'phone_number': '9876543211',
            'email': 'john.smith@hospital.com',
            'password': 'doctor123',
        },
        {
            'staff_id': 3,
            'hospital_id': 1,
            'department_id': 2,
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'role': 'Nurse',
            'phone_number': '9876543212',
            'email': 'sarah.j@hospital.com',
            'password': 'nurse123',
        },
        {
            'staff_id': 4,
            'hospital_id': 1,
            'department_id': 1,
            'first_name': 'Emily',
            'last_name': 'Davis',
            'role': 'Receptionist',
            'phone_number': '9876543213',
            'email': 'emily.d@hospital.com',
            'password': 'reception123',
        },
        {
            'staff_id': 5,
            'hospital_id': 1,
            'department_id': 3,
            'first_name': 'Michael',
            'last_name': 'Brown',
            'role': 'Pharmacist',
            'phone_number': '9876543214',
            'email': 'michael.b@hospital.com',
            'password': 'pharma123',
        },
        {
            'staff_id': 6,
            'hospital_id': 2,
            'department_id': 5,
            'first_name': 'David',
            'last_name': 'Wilson',
            'role': 'Doctor',
            'phone_number': '9876543215',
            'email': 'david.w@hospital.com',
            'password': 'doctor123',
        },
        {
            'staff_id': 7,
            'hospital_id': 3,
            'department_id': 6,
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'role': 'Doctor',
            'phone_number': '9876543216',
            'email': 'lisa.a@hospital.com',
            'password': 'doctor123',
        },
        {
            'staff_id': 8,
            'hospital_id': 3,
            'department_id': 6,
            'first_name': 'Robert',
            'last_name': 'Taylor',
            'role': 'Nurse',
            'phone_number': '9876543217',
            'email': 'robert.t@hospital.com',
            'password': 'nurse123',
        },

    ]
    
    print("=" * 60)
    print("CREATING STAFF USERS WITH HASHED PASSWORDS")
    print("=" * 60)
    
    # First ensure hospital and departments exist
    ensure_hospital_and_departments()
    
    cursor = connection.cursor()
    
    for data in staff_data:
        password = data.pop('password')
        password_hash = make_password(password)
        
        # Check if user exists
        cursor.execute("SELECT COUNT(*) FROM staff_users WHERE staff_id = %s", [data['staff_id']])
        exists = cursor.fetchone()[0] > 0
        
        if exists:
            # Update existing user's password
            cursor.execute("""
                UPDATE staff_users 
                SET password_hash = %s 
                WHERE staff_id = %s
            """, [password_hash, data['staff_id']])
            action = "Updated"
        else:
            # Insert new user
            cursor.execute("""
                INSERT INTO staff_users 
                (staff_id, hospital_id, department_id, first_name, last_name, role, phone_number, email, password_hash, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, [
                data['staff_id'], data['hospital_id'], data['department_id'],
                data['first_name'], data['last_name'], data['role'],
                data['phone_number'], data['email'], password_hash
            ])
            action = "Created"
        
        print(f"✓ {action} {data['first_name']} {data['last_name']} ({data['email']})")
        print(f"  Login: {data['email']} or {data['phone_number']}")
        print(f"  Password: {password}")
        print()
    
    connection.commit()
    
    # Verify users exist
    cursor.execute("SELECT COUNT(*) FROM staff_users")
    count = cursor.fetchone()[0]
    
    print("=" * 60)
    print("STAFF USER CREDENTIALS")
    print("=" * 60)
    print(f"\nTotal staff users in database: {count}")
    print("\nYou can login with:")
    print("  Email: admin@hospital.com")
    print("  Phone: 9876543210")
    print("  Password: admin123")
    print()
    print("Other test accounts:")
    print("  john.smith@hospital.com / doctor123")
    print("  sarah.j@hospital.com / nurse123")
    print("  emily.d@hospital.com / reception123")
    print("  michael.b@hospital.com / pharma123")
    print()
    print("All staff users created/updated successfully!")
    print("=" * 60)

if __name__ == '__main__':
    create_staff_users()
