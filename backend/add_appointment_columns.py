"""
Add age and time_slot columns to appointments table
Run this script to update the database schema
Uses Django settings for database credentials
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

def add_appointment_columns():
    """Add age and time_slot columns to appointments table."""
    try:
        with connection.cursor() as cursor:
            print("Connected to MySQL database")
            
            # Check current table structure
            print("\n=== Current table structure ===")
            cursor.execute("DESCRIBE appointments")
            columns = cursor.fetchall()
            existing_columns = [col[0] for col in columns]
            print(f"Existing columns: {existing_columns}")
            
            # Add age column if it doesn't exist
            if 'age' not in existing_columns:
                print("\n✓ Adding 'age' column...")
                cursor.execute("""
                    ALTER TABLE appointments 
                    ADD COLUMN age INT NULL COMMENT 'Patient age at time of appointment'
                """)
                print("✓ 'age' column added successfully")
            else:
                print("\n✓ 'age' column already exists")
            
            # Add time_slot column if it doesn't exist
            if 'time_slot' not in existing_columns:
                print("\n✓ Adding 'time_slot' column...")
                cursor.execute("""
                    ALTER TABLE appointments 
                    ADD COLUMN time_slot VARCHAR(50) NULL COMMENT 'Time slot (e.g., 09:00-09:30)'
                """)
                print("✓ 'time_slot' column added successfully")
            else:
                print("\n✓ 'time_slot' column already exists")
            
            # Verify the changes
            print("\n=== Updated table structure ===")
            cursor.execute("DESCRIBE appointments")
            columns = cursor.fetchall()
            for col in columns:
                nullable = 'NULL' if col[2] == 'YES' else 'NOT NULL'
                print(f"  {col[0]}: {col[1]} {nullable}")
            
            print("\n✅ Database schema updated successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Adding Appointment Columns ===\n")
    add_appointment_columns()
