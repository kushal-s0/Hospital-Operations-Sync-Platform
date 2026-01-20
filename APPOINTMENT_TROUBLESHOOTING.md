# Appointment System - Troubleshooting Guide

## Current Issue: 500 Internal Server Error

### Steps to Fix:

1. **Restart Django Server with Debug Output**
   
   Open a terminal and run:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   python manage.py runserver
   ```
   
   Keep this terminal open to see error messages.

2. **Test the Backend Directly**
   
   Run the test script:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   python test_appointment_models.py
   ```
   
   This will verify database connectivity.

3. **Check the Error in Terminal**
   
   When you submit the appointment form, look at the Django terminal output. You'll see:
   - Validation errors (if any)
   - Database queries being executed
   - Stack trace of any errors
   
   The debug prints I added will show:
   - "Validated data: ..."
   - "Found existing patient: ..." OR "Creating new patient..."
   - "Next patient_id: ..."
   - "Patient created: ..."
   - "Next appointment_id: ..."
   - "Appointment created: ..."

4. **Common Issues and Solutions**

   **Issue: "created_at" or "updated_at" field error**
   - The Patient/Appointment tables might have these fields with `auto_now_add=True`
   - Solution: Remove these fields from the model or ensure they exist in MySQL

   **Issue: "managed = False" conflicts**
   - Django can't auto-generate IDs for unmanaged models
   - Solution: Already fixed - manually increment patient_id and appointment_id

   **Issue: Foreign key constraint**
   - doctor_id might not exist in staff_users table
   - Solution: Pass `None` or a valid doctor_id

   **Issue: Field mismatch**
   - Model fields might not match database columns
   - Solution: Check MySQL schema matches Django models

5. **Verify Database Schema**
   
   Check if these tables exist and have the correct structure:
   ```sql
   DESCRIBE patients;
   DESCRIBE appointments;
   DESCRIBE staff_users;
   DESCRIBE departments;
   ```

6. **Test API with curl (Alternative)**
   
   ```powershell
   curl -X POST http://localhost:8000/api/appointments/book/ `
     -H "Content-Type: application/json" `
     -d '{
       "first_name": "Test",
       "last_name": "Patient",
       "email": "test@example.com",
       "contact_number": "1234567890",
       "date_of_birth": "1990-01-01",
       "gender": "M",
       "address": "123 Test St",
       "appointment_date": "2026-01-25",
       "appointment_time": "10:00:00",
       "department_id": 1,
       "reason_for_visit": "Test appointment"
     }'
   ```

## Changes Made to Fix the Issue:

### 1. views.py
- ✅ Replaced `get_or_create()` with manual `get()` and `save()`
- ✅ Added manual ID increment for patient_id
- ✅ Added manual ID increment for appointment_id
- ✅ Added extensive debug logging
- ✅ Added try-except for better error handling

### 2. serializers.py
- ✅ Added try-except to all SerializerMethodField methods
- ✅ Handles None values gracefully

### 3. Frontend (Already Fixed)
- ✅ Replaced `getAuthToken()` with `localStorage.getItem('access_token')`

## Next Steps:

1. **Restart Django server** with virtual environment
2. **Try booking an appointment** from the landing page
3. **Check the Django terminal** for debug output
4. **Share the error message** if it still fails

The error message in the Django terminal will tell us exactly what's wrong!

## Expected Behavior:

When booking works correctly, you should see:
1. ✅ Form submission successful
2. ✅ Success message popup
3. ✅ New patient created (or existing updated)
4. ✅ New appointment created with "Scheduled" status
5. ✅ Admin can see it in Appointments management page

## Database Tables Used:

- `patients` - Patient information
- `appointments` - Appointment records  
- `staff_users` - Doctors and staff
- `departments` - Hospital departments
- `opd_queue` - OPD queue (after approval)
