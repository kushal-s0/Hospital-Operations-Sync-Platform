# 🔧 OPD QUEUE DATE FILTERING FIX

## Problem Identified

**Symptom**: 
- ML prediction shows "3 patients waiting" ✅
- Database has OPD entries with IST check-in times ✅
- BUT: Frontend OPD list shows 0 entries ❌

**Root Cause**:
```python
# OLD CODE (WRONG):
queryset = OPDQueue.objects.filter(check_in_time__date=today)
```

The `__date` lookup extracts the date portion **at the database level**, which uses **UTC timezone**, not IST!

### Example of the Problem:
```
Check-in time in DB: 2026-01-21 01:30:00+05:30 (IST)
Stored as UTC:       2026-01-20 20:00:00+00:00 (UTC)

Django filter:
- check_in_time__date extracts date in UTC → 2026-01-20
- Today (IST) = 2026-01-21
- Comparison: 2026-01-20 != 2026-01-21 → NOT INCLUDED ❌
```

## Solution Applied

### 1. Added New Utility Function
**File**: `backend/apps/utils.py`

```python
def get_ist_date_range():
    """
    Get datetime range for today in IST timezone.
    Returns start and end of today (midnight to midnight) in IST.
    """
    local_tz = pytz.timezone(settings.TIME_ZONE)
    today = get_ist_today()
    
    # Create start of day (00:00:00) in IST
    start_of_day = local_tz.localize(datetime.combine(today, datetime.min.time()))
    
    # Create end of day (23:59:59) in IST
    end_of_day = local_tz.localize(datetime.combine(today, datetime.max.time()))
    
    return start_of_day, end_of_day
```

### 2. Updated OPD Queue Filtering
**File**: `backend/apps/opd/views.py`

**Before (WRONG)**:
```python
def get_queryset(self):
    today = get_ist_today()
    queryset = OPDQueue.objects.filter(check_in_time__date=today)
    # Uses database-level date extraction (UTC) ❌
```

**After (CORRECT)**:
```python
def get_queryset(self):
    # Get today's datetime range in IST
    start_of_day, end_of_day = get_ist_date_range()
    
    # Filter using datetime range (preserves timezone)
    queryset = OPDQueue.objects.filter(
        check_in_time__gte=start_of_day,  # >= 2026-01-21 00:00:00+05:30
        check_in_time__lte=end_of_day     # <= 2026-01-21 23:59:59+05:30
    )
```

### How It Works Now:
```
Today (IST): 2026-01-21

IST Date Range:
- Start: 2026-01-21 00:00:00+05:30 (IST midnight)
- End:   2026-01-21 23:59:59+05:30 (IST midnight)

Converted to UTC for database:
- Start: 2026-01-20 18:30:00+00:00 (UTC)
- End:   2026-01-21 18:29:59+00:00 (UTC)

Database entry:
- check_in_time: 2026-01-21 01:30:00+05:30 (IST)
- Stored as:     2026-01-20 20:00:00+00:00 (UTC)

Filter check:
- Is 2026-01-20 20:00:00 >= 2026-01-20 18:30:00? YES ✅
- Is 2026-01-20 20:00:00 <= 2026-01-21 18:29:59? YES ✅
- Result: INCLUDED ✅
```

## Testing

### Check Backend Logs
When you refresh the OPD Queue page, you should see:
```
================================================================================
OPD Queue Filtering - IST Date Range
Start of day (IST): 2026-01-21 00:00:00+05:30
End of day (IST):   2026-01-21 23:59:59+05:30
Total queue entries for today: 3
================================================================================
```

### Expected Results
1. ✅ Frontend shows all 3 patients in the table
2. ✅ ML prediction matches: "3 patients waiting"
3. ✅ Check-in times display in IST
4. ✅ Token numbers are correct

## Files Modified

1. ✅ `backend/apps/utils.py`
   - Added `get_ist_date_range()` function
   - Added necessary imports

2. ✅ `backend/apps/opd/views.py`
   - Updated import to include `get_ist_date_range`
   - Changed `get_queryset()` to use datetime range filtering
   - Added detailed debug logging

## Why This Works

### The Key Difference:
- **`__date` lookup**: Extracts date at database level (UTC) ❌
- **Datetime range**: Compares full datetime with timezone (IST) ✅

### Django's Behavior:
```python
# BAD: Loses timezone info
.filter(check_in_time__date=today)
# SQL: WHERE DATE(check_in_time) = '2026-01-21'
# Problem: DATE() function uses database timezone (UTC)

# GOOD: Preserves timezone
.filter(check_in_time__gte=start, check_in_time__lte=end)
# SQL: WHERE check_in_time >= '2026-01-20 18:30:00+00:00' 
#      AND check_in_time <= '2026-01-21 18:29:59+00:00'
# Success: Full datetime comparison with timezone ✅
```

## Summary

**Root Cause**: Using `__date` lookup loses timezone information
**Solution**: Use datetime range (`__gte` and `__lte`) to preserve timezone
**Result**: OPD queue now shows all entries for today (IST) correctly!

Just restart the Django server and refresh the OPD Queue page! 🎉
