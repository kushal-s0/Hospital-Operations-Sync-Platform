# OPD Queue Date Filtering Fix

## Problem
OPD Queue was showing patients from previous days instead of only today's patients. After midnight (Jan 21), it was still showing Jan 20 patients.

## Root Cause
The OPD Queue backend `get_queryset()` method was returning ALL queue entries from ALL days:

```python
queryset = OPDQueue.objects.all()  # ❌ Returns all days
```

This is different from a typical OPD queue which should reset daily and only show today's patients.

## Solution

### Backend Fix (`backend/apps/opd/views.py`)

**Before:**
```python
def get_queryset(self):
    """Filter queryset based on user role - doctors see only their patients."""
    queryset = OPDQueue.objects.all()  # Returns all days
    
    if self.request.user and self.request.user.is_authenticated:
        if self.request.user.role == 'Doctor':
            queryset = queryset.filter(doctor_id=self.request.user.staff_id)
    
    return queryset
```

**After:**
```python
def get_queryset(self):
    """Filter queryset based on user role and date - doctors see only their patients."""
    # Get today's date
    today = timezone.now().date()
    
    # Filter to show only today's queue entries
    queryset = OPDQueue.objects.filter(check_in_time__date=today)
    
    print(f"OPD Queue - Filtering for date: {today}")
    print(f"Total queue entries for today: {queryset.count()}")
    
    # Check if user is authenticated
    if self.request.user and self.request.user.is_authenticated:
        # If user is a doctor, filter to show only patients assigned to them
        if self.request.user.role == 'Doctor':
            queryset = queryset.filter(doctor_id=self.request.user.staff_id)
            print(f"Doctor filter applied - Showing only doctor's patients: {queryset.count()}")
    
    return queryset
```

## Changes Made

1. **Date Filter Added:**
   - Filters by `check_in_time__date=today`
   - Uses `timezone.now().date()` which respects Django's TIME_ZONE setting (Asia/Kolkata)

2. **Debug Logging:**
   - Logs today's date
   - Logs total queue entries for today
   - Logs count after doctor filter (if applicable)

3. **Behavior:**
   - At midnight (12:00 AM), the queue automatically shows only new day's patients
   - Previous day's patients no longer appear
   - Completed consultations from previous days are filtered out

## Database Schema

The `opd_queue` table has a `check_in_time` field (DATETIME) that stores when the patient checked in:
```sql
check_in_time DATETIME
```

The filter uses:
```python
check_in_time__date=today  # Extracts date part and compares
```

This is equivalent to SQL:
```sql
WHERE DATE(check_in_time) = '2026-01-21'
```

## Expected Behavior

### Before Fix:
- OPD Queue showed patients from Jan 20, Jan 19, Jan 18, etc.
- Queue never "reset" for new day
- Completed consultations from previous days still visible

### After Fix:
- OPD Queue shows ONLY patients who checked in today (Jan 21)
- At midnight, queue automatically filters to new day
- Previous days' patients are hidden (but still in database)

## Testing

### Backend Verification:
1. Restart Django server
2. Check terminal output when accessing OPD queue:
   ```
   OPD Queue - Filtering for date: 2026-01-21
   Total queue entries for today: X
   ```

### Frontend Verification:
1. Open OPD Queue page
2. Verify only today's patients are shown
3. Check patient check-in times are all from today
4. No patients from Jan 20 should appear

### Database Verification:
```sql
-- Check all OPD queue entries
SELECT id, token_number, patient_id, check_in_time, status, DATE(check_in_time) as check_in_date
FROM opd_queue
ORDER BY check_in_time DESC;

-- Today's entries only
SELECT COUNT(*) FROM opd_queue WHERE DATE(check_in_time) = '2026-01-21';
```

## Doctor Role Filter

The fix maintains the existing doctor role filter:
- **Doctors:** See only their patients from today
- **Nurses/Admins:** See all patients from today

```python
# For doctors
queryset = OPDQueue.objects.filter(
    check_in_time__date=today,
    doctor_id=current_user.staff_id
)

# For nurses/admins
queryset = OPDQueue.objects.filter(
    check_in_time__date=today
)
```

## Historical Data

**Important:** Previous days' data is NOT deleted, just filtered out.

To view historical OPD data, you would need:
- A separate "OPD History" page with date range filter
- Or modify the filter to accept date parameter from frontend
- Or add a "Show All" toggle button

Example for future enhancement:
```python
def get_queryset(self):
    queryset = OPDQueue.objects.all()
    
    # Allow date filter from query params
    date_filter = self.request.query_params.get('date', None)
    if date_filter:
        queryset = queryset.filter(check_in_time__date=date_filter)
    else:
        # Default to today
        today = timezone.now().date()
        queryset = queryset.filter(check_in_time__date=today)
    
    return queryset
```

## Related Files

### Modified:
- ✅ `backend/apps/opd/views.py` - OPDQueueViewSet.get_queryset()

### Related (Not Modified):
- `backend/apps/authentication/models.py` - OPDQueue model
- `frontend/src/pages/OPD/OPDQueue.js` - Frontend component
- `backend/apps/opd/serializers.py` - Serializers

## Impact

- ✅ OPD Queue shows only today's patients
- ✅ Automatic reset at midnight
- ✅ Cleaner queue management
- ✅ Better performance (fewer records to fetch)
- ✅ Matches real-world OPD workflow

## Notes

1. **Django Timezone:** TIME_ZONE = 'Asia/Kolkata', USE_TZ = True
2. **Date Boundary:** Midnight (00:00:00) IST is the cutoff
3. **Performance:** Filtering by date reduces query load
4. **Consistency:** Matches appointments "Today" tab behavior

## Verification Checklist

- [ ] Restart backend server
- [ ] Open OPD Queue page
- [ ] Check backend terminal shows correct date
- [ ] Verify only today's patients appear
- [ ] Check no Jan 20 patients are shown
- [ ] Test doctor role filter still works
- [ ] Test nurse/admin see all today's patients
- [ ] Add new patient - should appear immediately
- [ ] Wait until midnight - queue should auto-filter to new day
