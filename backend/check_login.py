"""
Simple script to check if admin user exists and test authentication
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')

try:
    django.setup()
    from django.contrib.auth import authenticate
    from django.contrib.auth.models import User
    
    print("=" * 50)
    print("CHECKING AUTHENTICATION")
    print("=" * 50)
    
    # Check if admin exists
    try:
        admin_user = User.objects.get(username='admin')
        print(f"\n✓ Admin user exists:")
        print(f"  - Username: {admin_user.username}")
        print(f"  - Email: {admin_user.email}")
        print(f"  - Is active: {admin_user.is_active}")
        print(f"  - Is staff: {admin_user.is_staff}")
        print(f"  - Is superuser: {admin_user.is_superuser}")
    except User.DoesNotExist:
        print("\n✗ Admin user does NOT exist!")
        print("  Run: python create_test_users.py")
        sys.exit(1)
    
    # Test authentication
    print("\n" + "=" * 50)
    print("TESTING AUTHENTICATION")
    print("=" * 50)
    
    user = authenticate(username='admin', password='admin123')
    if user is not None:
        print("\n✓ SUCCESS! Authentication works!")
        print(f"  Authenticated as: {user.username}")
    else:
        print("\n✗ FAILED! Authentication did not work")
        print("  Possible issues:")
        print("  1. Password is incorrect")
        print("  2. User is not active")
        print("  3. Database issue")
        
        # Check password
        if admin_user.check_password('admin123'):
            print("\n  Password 'admin123' is CORRECT")
        else:
            print("\n  Password 'admin123' is WRONG")
            print("  Resetting password to 'admin123'...")
            admin_user.set_password('admin123')
            admin_user.save()
            print("  ✓ Password reset complete!")
    
    print("\n" + "=" * 50)
    print("ALL USERS IN DATABASE:")
    print("=" * 50)
    for u in User.objects.all():
        print(f"  - {u.username} ({u.email}) - Active: {u.is_active}")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
