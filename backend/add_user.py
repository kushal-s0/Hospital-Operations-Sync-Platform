"""
Quick script to add a single user to the database
Usage: python add_user.py <username> <password> [--admin]
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

def add_user(username, password, is_admin=False):
    """Add a single user to the database"""
    
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        return False
    
    user = User.objects.create_user(
        username=username,
        password=password,
        is_staff=is_admin,
        is_superuser=is_admin,
    )
    
    role = "Admin" if is_admin else "User"
    print(f"✅ Successfully created {role}: {username}")
    print(f"   Password: {password}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python add_user.py <username> <password> [--admin]")
        print("\nExample:")
        print("  python add_user.py testuser password123")
        print("  python add_user.py admin admin123 --admin")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    is_admin = '--admin' in sys.argv
    
    try:
        add_user(username, password, is_admin)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
