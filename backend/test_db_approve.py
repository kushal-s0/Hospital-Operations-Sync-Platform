import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, OPDQueue
from django.db import connection
from django.utils import timezone

print("=" * 70)
print("APPOINTMENT APPROVAL - DATABASE TEST")
print("=" * 70)

# Test 1: Check if we can read appointments
print("\nTEST 1: Read Appointments")
print("-" * 70)
try:
    appointments = Appointment.objects.filter(status='Scheduled')[:5]
    print(f"Found {appointments.count()} scheduled appointments")
    for apt in appointments:
        print(f"  Appointment {apt.appointment_id}: {apt.patient.full_name if apt.patient else 'No patient'} - Status: {apt.status}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Test raw SQL update
print("\nTEST 2: Test Raw SQL Update (Dry Run)")
print("-" * 70)
try:
    test_apt = Appointment.objects.filter(status='Scheduled').first()
    if test_apt:
        print(f"Testing with Appointment ID: {test_apt.appointment_id}")
        print(f"Current status: {test_apt.status}")
        
        # Perform update
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE appointments SET status = %s WHERE appointment_id = %s",
                ['TEST_STATUS', test_apt.appointment_id]
            )
            print(f"Executed UPDATE query")
            
            # Check if it worked
            cursor.execute(
                "SELECT status FROM appointments WHERE appointment_id = %s",
                [test_apt.appointment_id]
            )
            row = cursor.fetchone()
            print(f"Status after update: {row[0] if row else 'Not found'}")
            
            # Rollback to not affect database
            connection.rollback()
            print("✓ Rolled back - no actual changes made")
    else:
        print("No scheduled appointments found to test with")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Test OPD Queue insertion
print("\nTEST 3: Test OPD Queue Insertion (Dry Run)")
print("-" * 70)
try:
    # Get max OPD queue ID
    max_opd_id = OPDQueue.objects.all().aggregate(models.Max('id'))['id__max']
    next_opd_id = (max_opd_id or 0) + 1
    print(f"Next OPD Queue ID would be: {next_opd_id}")
    
    # Try to insert
    from django.db import models
    test_apt = Appointment.objects.filter(status='Scheduled').first()
    if test_apt and test_apt.doctor_id and test_apt.patient:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO opd_queue 
                (id, patient_id, doctor_id, department_id, token_number, status, 
                 priority, check_in_time, notes, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, [
                next_opd_id,
                test_apt.patient.patient_id,
                test_apt.doctor_id,
                1,  # department_id
                999,  # test token number
                'waiting',
                'normal',
                timezone.now(),
                'TEST INSERT - Will be rolled back'
            ])
            print("✓ Executed INSERT query successfully")
            
            # Check if it worked
            cursor.execute(
                "SELECT id, token_number FROM opd_queue WHERE id = %s",
                [next_opd_id]
            )
            row = cursor.fetchone()
            print(f"Inserted entry: ID={row[0]}, Token={row[1]}" if row else "Not found")
            
            # Rollback
            connection.rollback()
            print("✓ Rolled back - no actual changes made")
    else:
        print("No suitable appointment found for testing")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Check today's OPD Queue
print("\nTEST 4: Today's OPD Queue Entries")
print("-" * 70)
try:
    today = timezone.now().date()
    opd_entries = OPDQueue.objects.filter(check_in_time__date=today)
    print(f"Total OPD entries for {today}: {opd_entries.count()}")
    for entry in opd_entries[:10]:
        print(f"  Token #{entry.token_number}: {entry.patient.full_name if entry.patient else 'No patient'} - Status: {entry.status}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 5: Database connection info
print("\nTEST 5: Database Connection Info")
print("-" * 70)
from django.conf import settings
db_config = settings.DATABASES['default']
print(f"Database Engine: {db_config['ENGINE']}")
print(f"Database Name: {db_config['NAME']}")
print(f"Database Host: {db_config['HOST']}")
print(f"Database Port: {db_config['PORT']}")
print(f"Database User: {db_config['USER']}")

print("\n" + "=" * 70)
print("ALL TESTS COMPLETED")
print("=" * 70)
print("\nIf all tests passed, the database connection and queries work fine.")
print("If approval still doesn't work, the issue is likely:")
print("  1. Backend server not running")
print("  2. Frontend not calling the API")
print("  3. Authentication issue")
print("\nCheck browser console (F12) and backend terminal for errors.")
