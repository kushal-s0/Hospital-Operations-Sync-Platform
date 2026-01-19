"""
Script to create test users for the Hospital Information System
Run this script with: python create_test_users.py
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_test_users():
    """Create test users with different roles"""
    
    test_users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@hospital.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        },
        {
            'username': 'doctor1',
            'password': 'doctor123',
            'email': 'doctor1@hospital.com',
            'first_name': 'Dr. John',
            'last_name': 'Smith',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'nurse1',
            'password': 'nurse123',
            'email': 'nurse1@hospital.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'is_staff': True,
            'is_superuser': False,
        },
        {
            'username': 'receptionist',
            'password': 'reception123',
            'email': 'reception@hospital.com',
            'first_name': 'Emily',
            'last_name': 'Davis',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'pharmacist',
            'password': 'pharma123',
            'email': 'pharma@hospital.com',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'Sagar',
            'password': 'Sagar123',
            'email': 'sagar@hospital.com',
            'first_name': 'Sagar',
            'last_name': 'Shetty',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'Kushal',
            'password': 'Kushal123',
            'email': 'kushal@hospital.com',
            'first_name': 'Kushal',
            'last_name': 'Soni',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'Kartik',
            'password': 'Kartik123',
            'email': 'kartik@hospital.com',
            'first_name': 'Kartik',
            'last_name': 'verma',
            'is_staff': False,
            'is_superuser': False,
        },
        {
            'username': 'Bhavana',
            'password': 'Bhavana123',
            'email': 'Bhavana@hospital.com',
            'first_name': 'Bhavana',
            'last_name': 'Suthar',
            'is_staff': False,
            'is_superuser': False,
        }
    ]
    
    print("Creating test users...")
    print("-" * 60)
    
    for user_data in test_users:
        username = user_data['username']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"✓ User '{username}' already exists - skipping")
            continue
        
        # Create user
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=user_data['is_staff'],
            is_superuser=user_data['is_superuser'],
        )
        
        role = "Admin" if user.is_superuser else "Staff" if user.is_staff else "User"
        print(f"✓ Created {role}: {username} (password: {user_data['password']})")
    
    print("-" * 60)
    print("\n✅ Test users creation completed!")
    print("\nLogin Credentials:")
    print("-" * 60)
    for user_data in test_users:
        print(f"Username: {user_data['username']:<15} | Password: {user_data['password']}")
    print("-" * 60)

if __name__ == '__main__':
    try:
        create_test_users()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
