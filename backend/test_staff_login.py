"""
Test login with staff_users table
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser

print("=" * 60)
print("TESTING STAFF USER AUTHENTICATION")
print("=" * 60)

# Test data
test_credentials = [
    ('admin@hospital.com', 'admin123'),
    ('9876543210', 'admin123'),
    ('john.smith@hospital.com', 'doctor123'),
    ('9876543211', 'doctor123'),
]

for identifier, password in test_credentials:
    print(f"\nTesting login with: {identifier}")
    
    # Find user
    if identifier.isdigit():
        user = StaffUser.objects.filter(phone_number=identifier).first()
    else:
        user = StaffUser.objects.filter(email=identifier).first()
    
    if user:
        print(f"  ✓ User found: {user.full_name} ({user.role})")
        
        if user.check_password(password):
            print(f"  ✓ Password correct!")
            print(f"    Staff ID: {user.staff_id}")
            print(f"    Email: {user.email}")
            print(f"    Phone: {user.phone_number}")
            print(f"    Role: {user.role}")
            print(f"    Active: {user.is_active}")
        else:
            print(f"  ✗ Password incorrect!")
    else:
        print(f"  ✗ User not found!")

print("\n" + "=" * 60)
print("ALL STAFF USERS IN DATABASE")
print("=" * 60)

for user in StaffUser.objects.all().order_by('staff_id'):
    print(f"{user.staff_id:3d} | {user.full_name:20s} | {user.role:15s} | {user.email:30s} | {user.phone_number}")

print("=" * 60)
