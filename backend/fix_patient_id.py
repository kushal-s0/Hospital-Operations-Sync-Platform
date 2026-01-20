"""
Check and fix patient_id AUTO_INCREMENT
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

def fix_patient_id():
    """Make patient_id AUTO_INCREMENT."""
    try:
        with connection.cursor() as cursor:
            print("Checking patient_id column...")
            
            # Check current structure
            cursor.execute("SHOW COLUMNS FROM patients WHERE Field = 'patient_id'")
            result = cursor.fetchone()
            print(f"Current: {result}")
            
            # Check if already auto_increment
            if 'auto_increment' in str(result).lower():
                print("\n✅ patient_id is already AUTO_INCREMENT!")
                return
            
            # Modify patient_id to be AUTO_INCREMENT
            print("\n✓ Making patient_id AUTO_INCREMENT...")
            cursor.execute("""
                ALTER TABLE patients 
                MODIFY COLUMN patient_id INT(11) NOT NULL AUTO_INCREMENT
            """)
            
            print("\n✅ patient_id is now AUTO_INCREMENT!")
            
            # Verify
            cursor.execute("SHOW COLUMNS FROM patients WHERE Field = 'patient_id'")
            result = cursor.fetchone()
            print(f"Updated: {result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Fixing patient_id AUTO_INCREMENT ===\n")
    fix_patient_id()
