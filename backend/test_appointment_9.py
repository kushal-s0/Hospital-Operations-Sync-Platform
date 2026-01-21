"""
Test script to check if approve function works
"""

import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, StaffUser, OPDQueue
from django.utils import timezone

print("=" * 80)
print("Testing Appointment Approval")
print("=" * 80)

# Get appointment #9
try:
    apt = Appointment.objects.get(appointment_id=9)
    print(f"\n✅ Found Appointment #9")
    print(f"   Patient: {apt.patient.full_name} (ID: {apt.patient_id})")
    print(f"   Doctor ID: {apt.doctor_id}")
    print(f"   Date: {apt.appointment_date}")
    print(f"   Status: {apt.status}")
    print(f"   Reason: {apt.reason_for_visit}")
    
    # Check if doctor exists
    print(f"\n🔍 Checking Doctor...")
    if not apt.doctor_id:
        print("   ❌ ERROR: No doctor_id assigned!")
    else:
        try:
            doctor = StaffUser.objects.get(staff_id=apt.doctor_id)
            print(f"   ✅ Doctor found: {doctor.full_name}")
            print(f"   Department: {doctor.department.department_name if doctor.department else 'NONE - ERROR!'}")
            
            if not doctor.department:
                print("   ❌ ERROR: Doctor has no department!")
        except StaffUser.DoesNotExist:
            print(f"   ❌ ERROR: Doctor with staff_id={apt.doctor_id} does not exist!")
    
    # Check if appointment is for today
    today = timezone.now().date()
    print(f"\n📅 Date Check:")
    print(f"   Today: {today}")
    print(f"   Appointment: {apt.appointment_date}")
    
    if apt.appointment_date == today:
        print("   ✅ Appointment is for TODAY - will add to OPD queue")
    else:
        print(f"   ℹ️  Appointment is for {apt.appointment_date} - NOT today")
        print("   → Won't add to OPD queue yet")

except Appointment.DoesNotExist:
    print("❌ ERROR: Appointment #9 not found!")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("Test Complete")
print("=" * 80)
