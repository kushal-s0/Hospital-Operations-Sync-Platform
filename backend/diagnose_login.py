"""
Comprehensive diagnostic for login issues
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

print("=" * 70)
print("COMPREHENSIVE LOGIN DIAGNOSTIC")
print("=" * 70)

# 1. Check if staff_users table has data
print("\n[1] Checking staff_users table...")
try:
    staff_count = StaffUser.objects.count()
    print(f"   Total staff users in database: {staff_count}")
    
    if staff_count == 0:
        print("   ❌ ERROR: No staff users found!")
        print("   Run: python create_staff_users.py")
        sys.exit(1)
    else:
        print("   ✓ Staff users exist")
except Exception as e:
    print(f"   ❌ ERROR accessing staff_users table: {e}")
    sys.exit(1)

# 2. List all staff users
print("\n[2] All staff users in database:")
print("   " + "-" * 66)
print(f"   {'ID':<5} {'Name':<20} {'Email':<30} {'Active':<6}")
print("   " + "-" * 66)

for user in StaffUser.objects.all().order_by('staff_id'):
    print(f"   {user.staff_id:<5} {user.full_name:<20} {user.email or 'N/A':<30} {str(user.is_active):<6}")

# 3. Check specific test user (admin)
print("\n[3] Checking admin user...")
try:
    admin = StaffUser.objects.filter(Q(email='admin@hospital.com') | Q(staff_id=1)).first()
    
    if admin:
        print(f"   ✓ Admin user found:")
        print(f"     - Staff ID: {admin.staff_id}")
        print(f"     - Email: {admin.email}")
        print(f"     - Phone: {admin.phone_number}")
        print(f"     - Name: {admin.full_name}")
        print(f"     - Role: {admin.role}")
        print(f"     - Active: {admin.is_active}")
        print(f"     - Has password hash: {bool(admin.password_hash)}")
        print(f"     - Password hash length: {len(admin.password_hash) if admin.password_hash else 0}")
        
        # 4. Test password verification
        print("\n[4] Testing password verification...")
        test_password = 'admin123'
        
        if admin.password_hash:
            try:
                is_valid = admin.check_password(test_password)
                if is_valid:
                    print(f"   ✓ Password '{test_password}' is CORRECT")
                else:
                    print(f"   ❌ Password '{test_password}' is WRONG")
                    print(f"   Password hash: {admin.password_hash[:50]}...")
                    
                    # Try to fix it
                    print("\n   Attempting to fix password...")
                    admin.set_password(test_password)
                    admin.save()
                    
                    # Test again
                    if admin.check_password(test_password):
                        print(f"   ✓ Password fixed successfully!")
                    else:
                        print(f"   ❌ Still cannot verify password")
                        
            except Exception as e:
                print(f"   ❌ Error checking password: {e}")
                print(f"   Password hash might be invalid: {admin.password_hash[:50]}...")
        else:
            print("   ❌ No password hash set!")
            print("   Setting password now...")
            admin.set_password(test_password)
            admin.save()
            print(f"   ✓ Password set to '{test_password}'")
    else:
        print("   ❌ Admin user NOT found!")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# 5. Test login logic
print("\n[5] Testing login logic...")
test_cases = [
    ('admin@hospital.com', 'admin123'),
    ('9876543210', 'admin123'),
    ('1', 'admin123'),
]

for identifier, password in test_cases:
    print(f"\n   Testing: {identifier} / {password}")
    
    try:
        # Simulate login logic
        if identifier.isdigit():
            user = StaffUser.objects.filter(
                Q(phone_number=identifier) | Q(staff_id=identifier)
            ).first()
        else:
            user = StaffUser.objects.filter(email=identifier).first()
        
        if user:
            print(f"     ✓ User found: {user.full_name}")
            print(f"       Is active: {user.is_active}")
            
            if user.check_password(password):
                print(f"     ✓ Password CORRECT - Login would succeed!")
            else:
                print(f"     ❌ Password WRONG - Login would fail!")
        else:
            print(f"     ❌ User NOT found with identifier: {identifier}")
            
    except Exception as e:
        print(f"     ❌ Error: {e}")

# 6. Check database connection
print("\n[6] Checking database configuration...")
from django.conf import settings
db_config = settings.DATABASES['default']
print(f"   Database: {db_config.get('NAME', 'N/A')}")
print(f"   Engine: {db_config.get('ENGINE', 'N/A')}")
print(f"   Host: {db_config.get('HOST', 'N/A')}")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)

# Summary
print("\n🔍 SUMMARY:")
if staff_count > 0:
    print("✓ Database has staff users")
else:
    print("❌ No staff users found")

admin = StaffUser.objects.filter(email='admin@hospital.com').first()
if admin and admin.check_password('admin123'):
    print("✓ Admin credentials are working")
    print("\n✅ You should be able to login with:")
    print("   Email: admin@hospital.com")
    print("   Phone: 9876543210")
    print("   Password: admin123")
else:
    print("❌ Admin credentials need fixing")
    print("\n⚠️ Run these commands to fix:")
    print("   python create_staff_users.py")

print("\n" + "=" * 70)
