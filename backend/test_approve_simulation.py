"""
Simulate what happens when approving appointment #9
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, OPDQueue
from django.utils import timezone

print("=" * 80)
print("SIMULATING APPROVAL OF APPOINTMENT #9")
print("=" * 80)

apt = Appointment.objects.get(appointment_id=9)
today = timezone.now().date()

print(f"\nBEFORE APPROVAL:")
print(f"  Appointment Status: {apt.status}")
print(f"  Appointment Date: {apt.appointment_date}")
print(f"  Today: {today}")

# Check OPD queue entries for this patient
opd_entries = OPDQueue.objects.filter(patient_id=apt.patient_id)
print(f"\n  OPD Queue Entries for Patient #{apt.patient_id}: {opd_entries.count()}")
for entry in opd_entries:
    print(f"    - Token #{entry.token_number}, Doctor: {entry.doctor_id}, Status: {entry.status}")

print(f"\n{'─' * 80}")
print("WHAT WILL HAPPEN WHEN YOU APPROVE:")
print("─" * 80)

if apt.appointment_date == today:
    print("✅ Date matches TODAY → Will update appointment AND create OPD queue entry")
    print("   - appointments table: status = 'Completed'")
    print("   - opd_queue table: NEW entry created with token number")
else:
    print("⚠️  Date is FUTURE → Will update appointment ONLY")
    print("   - appointments table: status = 'Completed'")
    print("   - opd_queue table: NO entry created (not today)")
    print(f"\n   Patient will be added to OPD queue on {apt.appointment_date}")

print("\n" + "=" * 80)
