# HOW TO START THE BACKEND SERVER

## Problem
The backend server is NOT running, which is why appointments are not being saved and OPD queue is empty.

## Solution - Choose ONE option:

---

## OPTION 1: Use the start.bat script (EASIEST)

Just double-click the `start.bat` file in the main folder:
```
C:\Users\Kushal\Desktop\rucici\start.bat
```

This will open TWO windows:
- Backend window (Django server)
- Frontend window (React app)

**Important:** Keep both windows open!

---

## OPTION 2: Start manually with virtual environment

### Step 1: Activate virtual environment
```powershell
cd C:\Users\Kushal\Desktop\rucici
venv\Scripts\activate
```

### Step 2: Start backend
```powershell
cd backend
python manage.py runserver
```

### Step 3: In a NEW terminal, start frontend
```powershell
cd C:\Users\Kushal\Desktop\rucici\frontend
npm start
```

---

## OPTION 3: Install Django in base Conda environment

```powershell
pip install -r C:\Users\Kushal\Desktop\rucici\backend\requirements.txt
cd C:\Users\Kushal\Desktop\rucici\backend
python manage.py runserver
```

---

## How to verify backend is running:

1. Open browser
2. Go to: http://localhost:8000/admin/
3. You should see Django admin login page

If you see "Unable to connect" = Backend is NOT running!

---

## What you should see when backend starts:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 21, 2026 - 01:30:00
Django version 4.2.x, using settings 'hospital_ops.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## Current Status:

❌ Backend server is NOT running
❌ Django is not installed in your current Python environment
❌ Need to either:
   - Use start.bat (recommended)
   - Activate virtual environment
   - Install Django in base environment

---

## Quick Test:

After starting the backend, run this in browser console (F12):
```javascript
fetch('http://localhost:8000/admin/')
  .then(r => console.log('Backend is running!', r.status))
  .catch(e => console.log('Backend is NOT running!', e));
```

Should show: `Backend is running! 200`

---

## RECOMMENDED: Use start.bat

1. Double-click `C:\Users\Kushal\Desktop\rucici\start.bat`
2. Wait for both servers to start
3. Open browser to http://localhost:3000
4. Try approving appointment again
