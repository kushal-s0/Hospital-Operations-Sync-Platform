# 🐛 OPD Queue Issue - Debugging Guide

## Problem
When approving appointments, the popup shows success but:
- ❌ Patient doesn't appear in OPD Queue page
- ❌ Data not being updated in opd_queue table

## Changes Made

### 1. Fixed `created_at` and `updated_at` fields
**File:** `backend/apps/appointments/views.py`

**Issue:** The OPDQueue model has `managed = False`, so Django doesn't auto-populate timestamp fields.

**Fix:** Explicitly set `created_at` and `updated_at` when creating OPD entry:
```python
current_time = timezone.now()
opd_entry = OPDQueue(
    # ... other fields ...
    created_at=current_time,
    updated_at=current_time
)
```

### 2. Added Extensive Logging
Added detailed console logging to track:
- Appointment details being approved
- Whether appointment is for today
- OPD queue entry creation
- All field values being saved

## How to Test

### Step 1: Create a Test Appointment for TODAY
1. Go to landing page
2. Book appointment for **today's date**
3. Fill in all details
4. Submit

### Step 2: Approve the Appointment
1. Login as Admin/Nurse
2. Go to Appointments page
3. Click "Approve & Add to Queue"
4. **Watch the terminal/console output**

### Step 3: Check Backend Terminal
You should see detailed logs like:
```
================================================================================
APPROVING APPOINTMENT #123
================================================================================
Patient: John Doe (ID: 45)
Doctor ID: 12
Appointment Date: 2026-01-21
Today's Date: 2026-01-21
Current Status: Scheduled
================================================================================
✅ Appointment status updated to 'Completed'
📅 Appointment is for TODAY - Adding to OPD queue...
👨‍⚕️ Doctor: Dr. Smith (ID: 12)
🏥 Department: General Medicine
🎫 Next Token Number: 105
================================================================================
✅ OPD QUEUE ENTRY CREATED SUCCESSFULLY!
   OPD ID: 234
   Patient ID: 45
   Doctor ID: 12
   Department ID: 5
   Token: #105
   Status: waiting
   Check-in: 2026-01-21 14:30:00
   Created: 2026-01-21 14:30:00
   Updated: 2026-01-21 14:30:00
================================================================================
```

### Step 4: Check OPD Queue Page
1. Navigate to OPD Queue page
2. Patient should now appear with Token #105
3. Status should be "waiting"

### Step 5: Debug if Still Not Showing

Run the debug script:
```bash
cd backend
python debug_opd_queue.py
```

This will show:
- All recent OPD queue entries
- All recent appointments
- Match between today's appointments and OPD entries

## Common Issues & Solutions

### Issue 1: Entry created but not visible in frontend
**Check:** OPD Queue page filtering
- If logged in as Doctor, you only see YOUR patients
- Check `doctor_id` matches logged-in doctor

**Solution:** Login as Nurse or Admin to see all patients

### Issue 2: Appointment not for today
**Check:** Appointment date vs today's date
- OPD entry only created if appointment is for TODAY
- Future appointments won't appear until that date

**Solution:** Create appointment for today's date

### Issue 3: Database connection issues
**Check:** Backend terminal for errors

**Solution:** 
```bash
python manage.py shell -c "from apps.authentication.models import OPDQueue; print(OPDQueue.objects.count())"
```

### Issue 4: Missing doctor or department
**Check:** Logs will show if doctor or department is null

**Solution:** Ensure appointment has valid doctor_id

## Verification Queries

### Check OPD Queue Table Directly
```python
python manage.py shell -c "
from apps.authentication.models import OPDQueue
from django.utils import timezone

today = timezone.now().date()
entries = OPDQueue.objects.filter(check_in_time__date=today)
print(f'OPD entries for today: {entries.count()}')
for e in entries:
    print(f'  Token #{e.token_number}: {e.patient.full_name} - {e.status}')
"
```

### Check Appointment Status
```python
python manage.py shell -c "
from apps.authentication.models import Appointment
from django.utils import timezone

today = timezone.now().date()
apts = Appointment.objects.filter(appointment_date=today, status='Completed')
print(f'Approved appointments for today: {apts.count()}')
for a in apts:
    print(f'  #{a.appointment_id}: {a.patient.full_name} - Dr.ID {a.doctor_id}')
"
```

## Expected Behavior After Fix

1. **Approve Appointment** → Logs show detailed creation process
2. **OPD Entry Created** → Logs confirm all fields set
3. **Frontend Refreshes** → Patient appears in OPD Queue
4. **Database Updated** → Entry visible with all timestamps

## Files Modified

- ✅ `backend/apps/appointments/views.py` - Fixed timestamp fields & added logging
- ✅ `backend/debug_opd_queue.py` - NEW debug script

## Next Steps

1. **Restart backend server** to apply changes
2. **Create new appointment for TODAY**
3. **Approve appointment** and watch logs
4. **Check OPD Queue page**
5. **Run debug script** if issues persist

---

**Status:** 🔧 Fixed - Ready for Testing
**Date:** January 21, 2026
