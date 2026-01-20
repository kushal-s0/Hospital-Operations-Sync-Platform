import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

print("\nAdding priority column to appointments table...")
print("-" * 50)

cursor = connection.cursor()

try:
    # Add priority column if it doesn't exist
    cursor.execute("""
        ALTER TABLE appointments 
        ADD COLUMN priority ENUM('normal', 'urgent', 'emergency') 
        DEFAULT 'normal' 
        AFTER status
    """)
    connection.commit()
    print("✓ Successfully added priority column to appointments table")
except Exception as e:
    if "Duplicate column" in str(e):
        print("✓ Priority column already exists")
    else:
        print(f"✗ Error: {e}")
        connection.rollback()

# Verify the column was added
cursor.execute("DESCRIBE appointments")
columns = cursor.fetchall()
print("\nUpdated table structure:")
for col in columns:
    print(f"  {col[0]}: {col[1]}")

print("\n" + "-" * 50)
print("Done!")
