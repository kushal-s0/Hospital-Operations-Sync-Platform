"""
Update appointments table status column length
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

try:
    print("Updating appointments table status column...")
    cursor.execute('''
        ALTER TABLE appointments 
        MODIFY COLUMN status VARCHAR(50) NULL
    ''')
    connection.commit()
    print("✓ Status column updated to VARCHAR(50)")
except Exception as e:
    print(f"Error: {e}")
    connection.rollback()
finally:
    cursor.close()
