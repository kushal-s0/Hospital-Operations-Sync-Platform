import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("DESCRIBE appointments")
columns = cursor.fetchall()

print("\nAppointment Table Columns:")
print("-" * 50)
for col in columns:
    print(f"{col[0]}: {col[1]}")
