# Quick Database Check for OPD Queue

Run these SQL queries in your MySQL/MariaDB client to check the data:

## 1. Check today's OPD queue entries
```sql
SELECT id, patient_id, doctor_id, token_number, status, 
       check_in_time, created_at
FROM opd_queue 
WHERE DATE(check_in_time) = '2026-01-21'
ORDER BY created_at DESC;
```

## 2. Check the last inserted OPD queue entry
```sql
SELECT id, patient_id, doctor_id, token_number, status, 
       check_in_time, notes
FROM opd_queue 
ORDER BY id DESC 
LIMIT 5;
```

## 3. Check approved appointments
```sql
SELECT appointment_id, patient_id, doctor_id, status, 
       appointment_date, reason_for_visit
FROM appointments 
WHERE status = 'Completed' 
  AND appointment_date = '2026-01-21'
ORDER BY appointment_id DESC;
```

## 4. Check if patient_id exists in patients table
```sql
-- Replace XXX with the patient_id from the appointment
SELECT patient_id, first_name, last_name 
FROM patients 
WHERE patient_id = XXX;
```

## 5. Check table structure
```sql
DESCRIBE opd_queue;
```

## What to look for:

- If opd_queue has 0 rows for today → INSERT failed
- If appointment status = 'Completed' → UPDATE worked
- Check if patient_id, doctor_id are valid foreign keys
- Check if any constraints are preventing INSERT

## Common Issues:

1. **Foreign key constraint failure**: patient_id or doctor_id doesn't exist
2. **NULL constraint violation**: Required field is NULL
3. **Duplicate primary key**: ID already exists
4. **Transaction rollback**: If any error occurs, everything is rolled back

## Debug in Python:

You can also run this in Django shell:
```bash
cd backend
python manage.py shell
```

Then:
```python
from apps.authentication.models import OPDQueue, Appointment
from django.utils import timezone

# Check today's OPD queue
today = timezone.now().date()
opd_entries = OPDQueue.objects.filter(check_in_time__date=today)
print(f"Total OPD entries for today: {opd_entries.count()}")

for entry in opd_entries:
    print(f"ID: {entry.id}, Token: {entry.token_number}, Patient: {entry.patient.full_name if entry.patient else 'None'}")

# Check completed appointments
completed = Appointment.objects.filter(status='Completed', appointment_date=today)
print(f"\nTotal completed appointments: {completed.count()}")

for apt in completed:
    print(f"Appointment {apt.appointment_id}: {apt.patient.full_name if apt.patient else 'None'} - Doctor ID: {apt.doctor_id}")
```
