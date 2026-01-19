# Login Troubleshooting Guide

## Quick Diagnosis Steps

### Step 1: Check if Backend is Running
```bash
# The backend should be running on http://localhost:8000
# Open browser and go to: http://localhost:8000/admin
```
If you see Django admin page → Backend is running ✓
If you get "Can't reach this page" → Backend is NOT running ✗

### Step 2: Install Dependencies (if not done)
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run Migrations
```bash
cd backend
python manage.py migrate
```

### Step 4: Create Test Users
```bash
cd backend
python create_test_users.py
```

### Step 5: Check if Users Exist
```bash
cd backend
python check_login.py
```

This will:
- Check if admin user exists
- Test authentication
- List all users
- Reset password if needed

### Step 6: Start Backend (if not running)
```bash
cd backend
python manage.py runserver
```

### Step 7: Check Browser Console
1. Open login page: http://localhost:3000/login
2. Press F12 (open Developer Tools)
3. Go to "Console" tab
4. Try to login
5. Check for errors (red text)

Common errors:
- `ERR_CONNECTION_REFUSED` → Backend not running
- `401 Unauthorized` → Wrong credentials
- `CORS error` → Backend CORS settings issue

### Step 8: Check Network Tab
1. Open Developer Tools (F12)
2. Go to "Network" tab
3. Try to login
4. Look for the request to `/api/auth/login/`
5. Click on it and check:
   - **Status Code**: Should be 200 (success) or 401 (wrong password)
   - **Response**: Shows error message
   - **Request Payload**: Shows what was sent

## Common Issues and Solutions

### Issue 1: "Invalid username or password"

**Possible Causes:**
1. User doesn't exist in database
2. Password is wrong
3. Backend not properly configured

**Solution:**
```bash
cd backend
python check_login.py
```

If admin doesn't exist:
```bash
python create_test_users.py
```

### Issue 2: Backend Not Running

**Symptoms:**
- Can't reach http://localhost:8000
- "Network Error" in browser
- ERR_CONNECTION_REFUSED

**Solution:**
```bash
cd backend
python manage.py runserver
```

### Issue 3: Dependencies Not Installed

**Symptoms:**
- ModuleNotFoundError when running scripts
- Backend won't start

**Solution:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python create_test_users.py
```

### Issue 4: Database Not Migrated

**Symptoms:**
- "no such table: auth_user"
- Backend errors about missing tables

**Solution:**
```bash
cd backend
python manage.py migrate
python create_test_users.py
```

### Issue 5: CORS Errors

**Symptoms:**
- "CORS policy" errors in browser console
- Requests blocked

**Solution:**
Check `backend/hospital_ops/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

Restart backend after changes.

### Issue 6: Frontend Not Connecting to Backend

**Check:**
1. Is backend running on port 8000?
2. Is frontend running on port 3000?
3. Check `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
   ```

## Testing Authentication Manually

### Using Browser
1. Go to: http://localhost:8000/admin
2. Try logging in with: admin / admin123
3. If this works, Django is fine

### Using Postman or curl
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Expected Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1...",
  "access": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@hospital.com",
    ...
  }
}
```

## Reset Everything (Nuclear Option)

If nothing works, try this:

```bash
# 1. Stop all servers (Ctrl+C)

# 2. Delete database (if using SQLite)
cd backend
del db.sqlite3

# 3. Delete all migrations (optional)
# cd backend/apps/*/migrations
# Delete all files except __init__.py

# 4. Reinstall dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create users
python create_test_users.py

# 7. Start backend
python manage.py runserver

# 8. In new terminal, start frontend
cd frontend
npm start
```

## Still Not Working?

### Collect This Information:

1. **Backend Status:**
   ```bash
   cd backend
   python manage.py runserver
   # Copy any error messages
   ```

2. **Check Login Script:**
   ```bash
   cd backend
   python check_login.py
   # Copy the output
   ```

3. **Browser Console:**
   - Open http://localhost:3000/login
   - Press F12
   - Try to login
   - Copy any red error messages

4. **Network Tab:**
   - Open Network tab in DevTools
   - Try to login
   - Find the `/api/auth/login/` request
   - Copy the Response

Share all this information for further help!

## Quick Test Command

Run this single command to test everything:
```bash
cd backend && python check_login.py
```
