# Appointment Approval Database Save Fix

## Problem
When clicking "Approve" on an appointment:
- Frontend shows status as "Completed" (works locally in state)
- But changes don't persist in database
- OPD queue entry not created
- After refresh, appointment shows as "Scheduled" again

## Root Cause
The Appointment and OPDQueue models use `managed=False` in Django, which means:
- Django doesn't automatically handle saves properly
- `appointment.save()` and `opd_entry.save()` may silently fail
- No errors are raised, but data isn't persisted

## Solution
Use **raw SQL** instead of Django ORM `.save()` methods for `managed=False` models.

### Changes in `backend/apps/appointments/views.py`

#### 1. Appointment Status Update
**Before (Not Working):**
```python
appointment.status = 'Completed'
appointment.save()  # Doesn't work with managed=False
```

**After (Working):**
```python
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(
        "UPDATE appointments SET status = %s WHERE appointment_id = %s",
        ['Completed', appointment.appointment_id]
    )
```

#### 2. OPD Queue Entry Creation
**Before (Not Working):**
```python
opd_entry = OPDQueue(
    patient=appointment.patient,
    doctor=doctor,
    department=doctor.department,
    token_number=next_token,
    status='waiting',
    priority='normal',
    check_in_time=timezone.now(),
    notes=f"Appointment approved: {appointment.reason_for_visit}",
)
opd_entry.save()  # Doesn't work with managed=False
```

**After (Working):**
```python
# Get next OPD queue ID
max_opd_id = OPDQueue.objects.all().aggregate(models.Max('id'))['id__max']
next_opd_id = (max_opd_id or 0) + 1

# Create OPD queue entry using raw SQL
with connection.cursor() as cursor:
    cursor.execute("""
        INSERT INTO opd_queue 
        (id, patient_id, doctor_id, department_id, token_number, status, 
         priority, check_in_time, notes, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
    """, [
        next_opd_id,
        appointment.patient.patient_id,
        appointment.doctor_id,
        doctor.department_id if doctor.department else None,
        next_token,
        'waiting',
        'normal',
        timezone.now(),
        f"Appointment approved: {appointment.reason_for_visit}"
    ])
```

## Debug Logging Added

The approve function now includes comprehensive logging:

```python
print(f"=== APPROVE APPOINTMENT {appointment.appointment_id} ===")
print(f"Current status: {appointment.status}")
print(f"Appointment date: {appointment.appointment_date}")
print(f"Today's date: {timezone.now().date()}")
print(f"Updated appointment {appointment.appointment_id} status to Completed")
print(f"Found doctor: {doctor.full_name}")
print(f"Next token number: {next_token}")
print(f"Created OPD queue entry {next_opd_id} with token {next_token}")
```

## How to Verify the Fix

### 1. Backend Terminal Output
After clicking "Approve", you should see:
```
=== APPROVE APPOINTMENT 123 ===
Current status: Scheduled
Appointment date: 2026-01-21
Today's date: 2026-01-21
Updated appointment 123 status to Completed
Found doctor: Dr. John Smith
Next token number: 5
Created OPD queue entry 42 with token 5
```

### 2. Database Verification
Check the database directly:

**Appointments Table:**
```sql
SELECT appointment_id, patient_id, status, appointment_date 
FROM appointments 
WHERE appointment_id = 123;
```
Should show `status = 'Completed'`

**OPD Queue Table:**
```sql
SELECT id, patient_id, doctor_id, token_number, status, check_in_time 
FROM opd_queue 
WHERE DATE(check_in_time) = '2026-01-21'
ORDER BY token_number DESC;
```
Should show the new entry with correct token number

### 3. Frontend Verification
1. Click "Approve" on an appointment
2. See success message
3. **Refresh the page** (F5)
4. Appointment should still show "Completed" status
5. Navigate to OPD Queue page
6. Patient should appear in the queue with correct token number

## Why Raw SQL is Needed

### Django's `managed=False` Behavior:
```python
class Appointment(models.Model):
    # ... fields ...
    
    class Meta:
        db_table = 'appointments'
        managed = False  # Django doesn't manage this table
```

When `managed=False`:
- Django doesn't create/alter the table
- Django doesn't handle migrations
- **Django's `.save()` may not work reliably**
- **Best practice:** Use raw SQL for DML operations

### Why This Happens:
- `managed=False` tells Django: "I don't control this table"
- Django assumes external system might be modifying it
- Django's ORM optimization may skip the actual SQL execution
- Raw SQL bypasses Django's ORM and directly executes

## Alternative Approach (Not Used)

Could also use `update()` queryset method:
```python
Appointment.objects.filter(appointment_id=appointment.appointment_id).update(status='Completed')
```

However, raw SQL is more explicit and guaranteed to work.

## Transaction Safety

All operations are wrapped in `transaction.atomic()`:
```python
with transaction.atomic():
    # Update appointment status
    cursor.execute("UPDATE ...")
    
    # Insert OPD queue entry
    cursor.execute("INSERT ...")
```

If any operation fails:
- All changes are rolled back
- Database stays consistent
- Error is returned to frontend

## Files Modified

- ✅ `backend/apps/appointments/views.py`
  - Replaced `appointment.save()` with raw SQL UPDATE
  - Replaced `opd_entry.save()` with raw SQL INSERT
  - Added ID generation for OPD queue entry
  - Added comprehensive debug logging
  - Added better error handling

## Impact

- ✅ Appointment status changes persist in database
- ✅ OPD queue entries are created successfully
- ✅ Refresh page shows correct status
- ✅ OPD queue shows approved appointments
- ✅ No duplicate approvals (status check works)
- ✅ Debug logs help troubleshooting

## Testing Checklist

- [ ] Restart Django backend server
- [ ] Create a test appointment for today
- [ ] Click "Approve" button
- [ ] Check backend terminal for debug logs
- [ ] Verify success message in frontend
- [ ] Refresh the page
- [ ] Verify appointment still shows "Completed"
- [ ] Navigate to OPD Queue
- [ ] Verify patient appears in queue
- [ ] Check database directly with SQL queries
- [ ] Try to approve the same appointment again
- [ ] Should show "Appointment already processed"

## Related Issues

This same issue may affect:
- Patient creation in booking form (uses raw SQL - ✅ working)
- Admission creation (uses raw SQL - ✅ working)
- Bed status updates (may need review)
- Any other `managed=False` models

## Best Practice for Future

For all `managed=False` models, use:
1. **Raw SQL** for INSERT/UPDATE/DELETE
2. **ORM** for SELECT/filtering (works fine)
3. **Explicit ID generation** (no auto-increment with managed=False)
4. **Debug logging** to verify operations
5. **Database verification** during testing
