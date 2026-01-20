"""
Fix appointment_id to be AUTO_INCREMENT
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

def fix_appointment_id():
    """Make appointment_id AUTO_INCREMENT."""
    try:
        with connection.cursor() as cursor:
            print("Checking appointment_id column...")
            
            # Check current structure
            cursor.execute("SHOW COLUMNS FROM appointments WHERE Field = 'appointment_id'")
            result = cursor.fetchone()
            print(f"Current: {result}")
            
            # Check if already auto_increment
            if 'auto_increment' in str(result).lower():
                print("\n✅ appointment_id is already AUTO_INCREMENT!")
                return
            
            # Modify appointment_id to be AUTO_INCREMENT without dropping primary key
            print("\n✓ Making appointment_id AUTO_INCREMENT...")
            cursor.execute("""
                ALTER TABLE appointments 
                MODIFY COLUMN appointment_id INT(11) NOT NULL AUTO_INCREMENT
            """)
            
            print("\n✅ appointment_id is now AUTO_INCREMENT!")
            
            # Verify
            cursor.execute("SHOW COLUMNS FROM appointments WHERE Field = 'appointment_id'")
            result = cursor.fetchone()
            print(f"Updated: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Fixing appointment_id AUTO_INCREMENT ===\n")
    fix_appointment_id()
