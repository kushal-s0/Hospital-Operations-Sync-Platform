"""
Check all records in opd_queue table
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue
from django.utils import timezone

print("=" * 80)
print("ALL OPD QUEUE RECORDS")
print("=" * 80)

all_entries = OPDQueue.objects.all().order_by('-check_in_time')
print(f"\nTotal Records: {all_entries.count()}")

if all_entries.count() == 0:
    print("\n❌ NO RECORDS FOUND IN OPD_QUEUE TABLE")
    print("\nThis is why the OPD Queue page is empty!")
    print("\nTo test:")
    print("1. Restart backend server")
    print("2. Approve appointment #10 (for today)")
    print("3. Check again")
else:
    print("\n" + "-" * 80)
    for entry in all_entries[:20]:  # Show first 20
        print(f"\nID: {entry.id}")
        print(f"  Patient: {entry.patient.full_name} (ID: {entry.patient_id})")
        print(f"  Doctor: {entry.doctor.full_name if entry.doctor else 'N/A'} (ID: {entry.doctor_id})")
        print(f"  Department: {entry.department.department_name if entry.department else 'N/A'}")
        print(f"  Token: #{entry.token_number}")
        print(f"  Status: {entry.status}")
        print(f"  Priority: {entry.priority}")
        print(f"  Check-in: {entry.check_in_time}")
        print(f"  Created: {entry.created_at}")
        print(f"  Notes: {entry.notes or 'N/A'}")
        print("-" * 80)

print("\n" + "=" * 80)
