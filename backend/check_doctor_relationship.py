"""
Check the relationship between doctors and staff_users tables
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Check if doctor_id is a foreign key to staff_users
    cursor.execute("""
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE
            TABLE_NAME = 'doctors'
            AND REFERENCED_TABLE_NAME IS NOT NULL
    """)
    
    print("=== Foreign Keys in doctors table ===")
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"{row[1]} -> {row[3]}.{row[4]}")
    else:
        print("No foreign keys found")
    
    # Check sample data
    print("\n=== Sample doctor data ===")
    cursor.execute("SELECT * FROM doctors LIMIT 1")
    print(cursor.fetchone())
    
    print("\n=== Sample staff_users (doctors) ===")
    cursor.execute("SELECT staff_id, first_name, last_name, role FROM staff_users WHERE role='Doctor' LIMIT 3")
    for row in cursor.fetchall():
        print(row)
