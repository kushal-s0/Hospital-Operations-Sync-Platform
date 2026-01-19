"""
Script to set passwords for existing staff users
Run this to activate user accounts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser


def set_passwords():
    """Set default passwords for all users without a password"""
    users_without_password = StaffUser.objects.filter(password_hash__isnull=True)
    
    print(f"Found {users_without_password.count()} users without passwords")
    print("-" * 60)
    
    for user in users_without_password:
        # Set a default password (you can customize this)
        default_password = "hospital123"  # Default password for all users
        user.set_password(default_password)
        user.save()
        print(f"✓ Set password for {user.email} (Staff ID: {user.staff_id})")
        print(f"  Login with: email={user.email}, password={default_password}")
    
    print("-" * 60)
    print(f"\nPassword set successfully for {users_without_password.count()} users")
    print(f"Default password: {default_password}")
    print("\nYou can now login with any user's email and the default password.")
    print("IMPORTANT: Change passwords after first login!")


if __name__ == "__main__":
    set_passwords()
