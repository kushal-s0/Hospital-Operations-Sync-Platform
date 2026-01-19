"""
Script to create staff users with proper Django password hashing
Run this after inserting the dummy data to set correct password hashes
"""
import os
import sys
import django
import MySQLdb

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser
from django.contrib.auth.hashers import make_password

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
    
    # Get database connection to use raw SQL
    from django.db import connection
    cursor = connection.cursor()
    
    for data in staff_data:
        password = data.pop('password')
        password_hash = make_password(password)
        
        # Update the password hash for existing staff
        cursor.execute("""
            UPDATE staff_users 
            SET password_hash = %s 
            WHERE staff_id = %s
        """, [password_hash, data['staff_id']])
        
        print(f"✓ Updated password for {data['first_name']} {data['last_name']} ({data['email']})")
        print(f"  Login: {data['email']} or {data['phone_number']}")
        print(f"  Password: {password}")
        print()
    
    connection.commit()
    
    print("=" * 60)
    print("STAFF USER CREDENTIALS")
    print("=" * 60)
    print("\nYou can login with:")
    print("  Email: admin@hospital.com")
    print("  Phone: 9876543210")
    print("  Password: admin123")
    print()
    print("Other test accounts:")
    print("  john.smith@hospital.com / 9876543211 / doctor123")
    print("  sarah.j@hospital.com / 9876543212 / nurse123")
    print("  emily.d@hospital.com / 9876543213 / reception123")
    print("  michael.b@hospital.com / 9876543214 / pharma123")
    print()
    print("All staff users created successfully!")
    print("=" * 60)

if __name__ == '__main__':
    create_staff_users()
