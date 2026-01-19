"""
Script to list all users in the database
Run this script with: python list_users.py
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

def list_users():
    """List all users in the database"""
    
    users = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    
    if not users.exists():
        print("No users found in the database.")
        print("\nRun 'python create_test_users.py' to create test users.")
        return
    
    print("\n" + "=" * 80)
    print(" " * 30 + "USER LIST")
    print("=" * 80)
    print(f"{'Username':<20} {'Name':<25} {'Email':<25} {'Role':<10}")
    print("-" * 80)
    
    for user in users:
        name = f"{user.first_name} {user.last_name}".strip() or "N/A"
        email = user.email or "N/A"
        
        if user.is_superuser:
            role = "Admin"
        elif user.is_staff:
            role = "Staff"
        else:
            role = "User"
        
        print(f"{user.username:<20} {name:<25} {email:<25} {role:<10}")
    
    print("=" * 80)
    print(f"\nTotal users: {users.count()}")
    print()

if __name__ == '__main__':
    try:
        list_users()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
