# Appointment Approval Not Working - Troubleshooting Guide

## Symptoms
- Click "Approve" button
- Frontend shows "Completed" temporarily
- But after refresh, status goes back to "Scheduled"
- Patient doesn't appear in OPD queue
- No database changes persist

## Troubleshooting Steps

### Step 1: Check if Backend Server is Running
```bash
# Open browser and go to:
http://localhost:8000/admin/

# Should show Django admin login page
# If you get "Unable to connect" or "ERR_CONNECTION_REFUSED", backend is NOT running
```

### Step 2: Start Backend Server Properly

**Option A: Using Command Line**
```bash
cd C:\Users\Kushal\Desktop\rucici\backend
python manage.py runserver
```

**Option B: If you have a virtual environment**
```bash
cd C:\Users\Kushal\Desktop\rucici
venv\Scripts\activate
cd backend
python manage.py runserver
```

**Look for these messages:**
```
System check identified no issues (0 silenced).
January 21, 2026 - 12:30:00
Django version 4.2.x, using settings 'hospital_ops.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 3: Check Browser Console

1. Open browser (Chrome/Edge)
2. Press F12 to open DevTools
3. Go to Console tab
4. Click "Approve" button
5. Look for these logs:

**What you SHOULD see:**
```javascript
=== APPROVE APPOINTMENT ===
Appointment ID: 123
Token: Present
Calling URL: http://localhost:8000/api/appointments/appointments/123/approve/
Response status: 200
Response OK: true
Success response: {message: "Appointment approved...", token_number: 5, ...}
```

**If you see this (BACKEND NOT RUNNING):**
```javascript
=== APPROVE APPOINTMENT ===
Appointment ID: 123
Token: Present
Calling URL: http://localhost:8000/api/appointments/appointments/123/approve/
Network error details: TypeError: Failed to fetch
```

**If you see this (AUTHENTICATION ERROR):**
```javascript
Response status: 401
Response OK: false
Error response: {detail: "Authentication credentials were not provided"}
```

### Step 4: Check Backend Terminal

After clicking "Approve", the backend terminal should show:
```
=== APPROVE APPOINTMENT 123 ===
Current status: Scheduled
Appointment date: 2026-01-21
Today's date: 2026-01-21
Updated appointment 123 status to Completed
Found doctor: Dr. John Smith
Next token number: 5
Created OPD queue entry 42 with token 5
[21/Jan/2026 12:30:00] "POST /api/appointments/appointments/123/approve/ HTTP/1.1" 200 XX
```

**If you see NOTHING in backend terminal:**
- Backend server is not running
- Or request is not reaching the backend

**If you see an error:**
```
ERROR: ...
Traceback (most recent call last):
  ...
```
Read the error message - it will tell you what's wrong.

### Step 5: Verify Database Connection

Create a test file to check database:

**File: `backend/test_db_approve.py`**
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Appointment, OPDQueue
from django.db import connection

# Test 1: Check if we can read appointments
print("=" * 60)
print("TEST 1: Read Appointments")
print("=" * 60)
appointments = Appointment.objects.all()[:5]
for apt in appointments:
    print(f"Appointment {apt.appointment_id}: {apt.patient.full_name} - Status: {apt.status}")

# Test 2: Try to update an appointment using raw SQL
print("\n" + "=" * 60)
print("TEST 2: Update Appointment Status (DRY RUN)")
print("=" * 60)
test_apt_id = int(input("Enter an appointment ID to test: "))
with connection.cursor() as cursor:
    # First check current status
    cursor.execute("SELECT status FROM appointments WHERE appointment_id = %s", [test_apt_id])
    row = cursor.fetchone()
    if row:
        print(f"Current status: {row[0]}")
        
        # Try to update (will be rolled back)
        cursor.execute("UPDATE appointments SET status = %s WHERE appointment_id = %s", ['TEST', test_apt_id])
        cursor.execute("SELECT status FROM appointments WHERE appointment_id = %s", [test_apt_id])
        row = cursor.fetchone()
        print(f"After update: {row[0]}")
        
        # Rollback
        connection.rollback()
        print("Rolled back - no actual changes made")
    else:
        print(f"Appointment {test_apt_id} not found")

# Test 3: Check OPD Queue
print("\n" + "=" * 60)
print("TEST 3: Check OPD Queue")
print("=" * 60)
opd_entries = OPDQueue.objects.filter(check_in_time__date='2026-01-21')
print(f"Total OPD entries for today: {opd_entries.count()}")
for entry in opd_entries[:5]:
    print(f"Token #{entry.token_number}: {entry.patient.full_name} - Status: {entry.status}")
```

**Run it:**
```bash
cd backend
python test_db_approve.py
```

### Step 6: Common Issues and Solutions

#### Issue: "Network error. Check if backend server is running"
**Solution:** Backend server is not running. Start it using Step 2.

#### Issue: Backend server starts but crashes immediately
**Check for:**
- Missing dependencies: `pip install -r requirements.txt`
- Database connection issues in `settings.py`
- Port 8000 already in use: Change port or kill the process

#### Issue: "Authentication credentials were not provided"
**Solution:** 
```javascript
// Check if token exists
console.log(localStorage.getItem('access_token'));

// If null, you need to login again
```

#### Issue: Backend shows error about managed=False
**This is expected!** The code uses raw SQL specifically for this reason.

#### Issue: Status updates in UI but not in database
**This was the original problem - fixed by using raw SQL**
- Make sure you've pulled the latest code
- Restart backend server
- Clear browser cache

### Step 7: Manual Database Check

Open MySQL/MariaDB command line:
```sql
-- Check appointment status
SELECT appointment_id, patient_id, status, appointment_date 
FROM appointments 
WHERE appointment_id = 123;  -- Replace with your appointment ID

-- Check OPD queue
SELECT id, patient_id, token_number, status, check_in_time 
FROM opd_queue 
WHERE DATE(check_in_time) = '2026-01-21'
ORDER BY token_number DESC;

-- If status is not 'Completed', the UPDATE didn't work
-- If OPD entry doesn't exist, the INSERT didn't work
```

### Step 8: Test with curl

Test the API directly without the frontend:
```bash
# Replace with your actual token and appointment ID
curl -X POST \
  http://localhost:8000/api/appointments/appointments/123/approve/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "message": "Appointment approved and added to OPD queue",
  "token_number": 5,
  "opd_queue_id": 42
}
```

### Step 9: Enable Django Debug Mode

In `backend/hospital_ops/settings.py`:
```python
DEBUG = True

# And add this for more detailed errors:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### Quick Checklist

- [ ] Backend server is running (check http://localhost:8000/admin/)
- [ ] Frontend can connect to backend (check browser console)
- [ ] Authentication token exists (check localStorage)
- [ ] Backend terminal shows the debug logs when clicking approve
- [ ] Database connection works (use test script)
- [ ] Latest code is pulled from git
- [ ] Browser cache is cleared
- [ ] No Python errors in backend terminal
- [ ] No JavaScript errors in browser console

### Most Likely Causes (in order)

1. **Backend server not running** (90% of cases)
   - Solution: Start it with `python manage.py runserver`

2. **Old code running** (if server was already running)
   - Solution: Restart backend server (Ctrl+C, then start again)

3. **Authentication token expired**
   - Solution: Logout and login again

4. **Database connection issue**
   - Solution: Check `settings.py` database config

5. **Port 8000 already in use**
   - Solution: Kill the process or use different port

### Still Not Working?

If none of the above works, provide:
1. Backend terminal output (copy the entire error)
2. Browser console output (F12 > Console tab, screenshot)
3. Result of: `SELECT * FROM appointments WHERE appointment_id = XXX;`
4. Django version: `python manage.py version`
5. Python version: `python --version`
