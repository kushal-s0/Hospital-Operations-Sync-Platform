"""
Test ML-predicted wait times for OPD queue with doctor availability
Run: python test_wait_time_predictions.py
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, StaffUser
from apps.opd.views import calculate_patient_wait_time

def test_wait_time_predictions():
    print("=" * 70)
    print("TESTING ML-PREDICTED WAIT TIMES WITH DOCTOR AVAILABILITY")
    print("=" * 70)
    
    # Get waiting patients
    waiting_patients = OPDQueue.objects.filter(status='waiting').order_by('check_in_time')
    
    if not waiting_patients.exists():
        print("\n❌ No waiting patients found in queue!")
        print("   Add some patients first to test wait time predictions.")
        return
    
    print(f"\n📊 Found {waiting_patients.count()} waiting patients\n")
    
    # Check doctor availability
    doctors = StaffUser.objects.filter(role='Doctor', is_active=True)
    print("👨‍⚕️ Doctor Status:")
    print("-" * 70)
    
    for doctor in doctors:
        busy_with = OPDQueue.objects.filter(
            doctor=doctor,
            status='in_consultation'
        ).first()
        
        waiting_count = OPDQueue.objects.filter(
            doctor=doctor,
            status='waiting'
        ).count()
        
        status = "🔴 BUSY" if busy_with else "🟢 FREE"
        print(f"  {status} Dr. {doctor.full_name}")
        if busy_with:
            print(f"       Currently with: {busy_with.patient.full_name} (Token #{busy_with.token_number})")
        print(f"       Waiting patients: {waiting_count}")
        print()
    
    # Calculate wait times for each waiting patient
    print("\n⏱️  Predicted Wait Times:")
    print("-" * 70)
    print(f"{'Token':<8} {'Patient':<20} {'Doctor':<20} {'Priority':<12} {'Wait Time'}")
    print("-" * 70)
    
    for patient in waiting_patients:
        estimated_wait = calculate_patient_wait_time(patient)
        
        # Update in database
        patient.estimated_wait_time = estimated_wait
        patient.save(update_fields=['estimated_wait_time'])
        
        doctor_name = patient.doctor.full_name if patient.doctor else "N/A"
        patient_name = patient.patient.full_name if patient.patient else "N/A"
        
        print(f"#{patient.token_number:<7} {patient_name:<20} {doctor_name:<20} {patient.priority:<12} {estimated_wait} min")
    
    print("-" * 70)
    
    # Show summary statistics
    print("\n📈 Wait Time Statistics:")
    avg_wait = sum([calculate_patient_wait_time(p) for p in waiting_patients]) / waiting_patients.count()
    min_wait = min([calculate_patient_wait_time(p) for p in waiting_patients])
    max_wait = max([calculate_patient_wait_time(p) for p in waiting_patients])
    
    print(f"  Average Wait: {avg_wait:.1f} minutes")
    print(f"  Minimum Wait: {min_wait} minutes")
    print(f"  Maximum Wait: {max_wait} minutes")
    
    # Show impact of doctor availability
    print("\n💡 Doctor Availability Impact:")
    print("  - Patients with FREE doctors: Shorter wait times")
    print("  - Patients with BUSY doctors: Wait includes current consultation")
    print("  - Emergency patients: 70% shorter wait (priority factor 0.3)")
    print("  - Urgent patients: 40% shorter wait (priority factor 0.6)")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE!")
    print("=" * 70)
    print("\n📝 Next Steps:")
    print("  1. Open OPD Queue page: http://localhost:3000/opd-queue")
    print("  2. Check 'Est. Wait' column - should show predicted times")
    print("  3. Click 'Start' on a patient - other patients' times should update")
    print("  4. Click 'Complete' - waiting patients' times should decrease")
    print("\n✨ Wait times will auto-update when queue refreshes!")

if __name__ == '__main__':
    try:
        test_wait_time_predictions()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
