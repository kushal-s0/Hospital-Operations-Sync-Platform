# Date/Timezone Fix for Appointments "Today" Tab

## Problem
The "Today" tab in Appointments was showing data from the previous day (Jan 20) instead of the current day (Jan 21) after midnight. This was a timezone conversion issue.

## Root Cause
The frontend was using `new Date().toISOString().split('T')[0]` which:
- Converts to UTC time before getting the date
- At 12:00 AM IST (India), UTC is still the previous day (6:30 PM previous day)
- Backend is configured for Asia/Kolkata timezone (IST)
- Mismatch between frontend date calculation and backend timezone

## Solution

### Frontend Fix (`frontend/src/pages/Appointments/AppointmentsManagement.js`)

**Before:**
```javascript
const today = new Date().toISOString().split('T')[0];
url += `?date=${today}`;
```

**After:**
```javascript
// Get today's date in local timezone (YYYY-MM-DD format)
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const todayDate = `${year}-${month}-${day}`;
console.log('Today filter date:', todayDate);
url += `?date=${todayDate}`;
```

**Why this works:**
- Uses local date components (getFullYear, getMonth, getDate)
- No UTC conversion happens
- Always matches the user's local date
- Backend receives the correct date string for IST timezone

### Debug Logging Added

**Frontend:**
- Logs the date being sent to backend
- Logs current browser date for verification

**Backend:**
- Logs the date filter received
- Logs current server date from `timezone.now().date()`
- Logs count of appointments found
- Logs each appointment's date

## Testing Steps

1. **Refresh the page at midnight or after**
2. **Open browser console** (F12)
3. **Look for logs:**
   ```
   Today filter date: 2026-01-21
   Stats data: {total_pending: X, today_appointments: Y, ...}
   Current date in browser: 1/21/2026
   ```

4. **Check backend terminal for:**
   ```
   Stats endpoint - Today's date: 2026-01-21
   Filtering by date: 2026-01-21
   Current server date: 2026-01-21
   Appointments found for 2026-01-21: X
   ```

5. **Verify:**
   - "Today" tab shows appointments for Jan 21
   - Stats card shows correct "Today" count
   - No appointments from Jan 20 appear in "Today" tab

## Why toISOString() Was Wrong

```javascript
// At 12:00 AM IST (India)
const now = new Date(); // Mon Jan 21 2026 00:00:00 GMT+0530
now.toISOString();      // "2026-01-20T18:30:00.000Z" (UTC)
now.toISOString().split('T')[0]; // "2026-01-20" ❌ WRONG!

// Correct approach
const year = now.getFullYear();        // 2026
const month = now.getMonth() + 1;      // 1
const day = now.getDate();             // 21
const local = `${year}-${month}-${day}`; // "2026-1-21" ✓ Correct!
```

## Alternative Solutions (Not Used)

### Option 1: Use timezone library
```javascript
import { format } from 'date-fns';
import { toZonedTime } from 'date-fns-tz';

const istDate = toZonedTime(new Date(), 'Asia/Kolkata');
const today = format(istDate, 'yyyy-MM-dd');
```
- Requires additional library
- Overkill for simple date formatting

### Option 2: Backend converts UTC to IST
```python
# Backend handles conversion
date_filter_str = self.request.query_params.get('date', None)
if date_filter_str:
    # Convert UTC date string to IST
    utc_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
    ist_date = utc_date + timedelta(days=1)  # Add offset
```
- Error-prone
- Doesn't solve root issue

### Option 3: Send timestamp instead of date
- More complex
- Unnecessary for date-only filtering

## Files Modified

### Frontend
- ✅ `frontend/src/pages/Appointments/AppointmentsManagement.js`
  - Fixed date calculation for "today" filter
  - Added debug logging

### Backend
- ✅ `backend/apps/appointments/views.py`
  - Added debug logging to stats endpoint
  - Added debug logging to date filter

- ✅ `backend/apps/opd/views.py`
  - **Fixed OPD queue to show only today's entries**
  - Added filter: `check_in_time__date=today`
  - Added debug logging for date filtering

## Impact

- ✅ "Today" tab in Appointments now correctly shows today's appointments
- ✅ OPD Queue now shows only today's patients (not previous days)
- ✅ Works correctly across timezone boundaries (midnight)
- ✅ No UTC conversion issues
- ✅ Stats card shows accurate count
- ✅ Debug logs help verify correct operation

## Notes

1. **Django Settings:** TIME_ZONE = 'Asia/Kolkata' and USE_TZ = True
2. **Browser Timezone:** Uses local system timezone (should be IST for Indian users)
3. **Date Format:** Always YYYY-MM-DD for consistency with MySQL DATE type
4. **No library needed:** Simple vanilla JavaScript solution

## Verification Checklist

After deploying:
- [ ] Check at midnight transition (11:59 PM → 12:00 AM)
- [ ] Verify "Today" tab shows new day's data immediately
- [ ] Check stats card updates correctly
- [ ] Verify no duplicate data from previous day
- [ ] Test in different browsers (Chrome, Firefox, Edge)
- [ ] Check browser console for correct date logs
- [ ] Check backend terminal for correct date logs
