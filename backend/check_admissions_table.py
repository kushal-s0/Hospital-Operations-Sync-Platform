import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute('DESCRIBE admissions')
columns = cursor.fetchall()

print('Admissions table columns:')
for col in columns:
    print(f'  {col[0]} - {col[1]}')
