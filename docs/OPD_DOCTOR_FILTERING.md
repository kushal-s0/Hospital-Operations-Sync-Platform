# OPD Queue Doctor Filtering - Implementation Summary

## Overview
Updated the OPD queue system to filter records based on the logged-in doctor. Each doctor now sees only the patients assigned to them in the OPD queue.

## Changes Made

### 1. Updated `OPDQueueViewSet` in `backend/apps/opd/views.py`

#### Added Import
```python
from rest_framework.permissions import IsAuthenticated
```

#### Added Permission Class
```python
class OPDQueueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication
```

#### Added `get_queryset()` Method
The core filtering logic that automatically filters queue entries based on the logged-in user's role:

```python
def get_queryset(self):
    """Filter queryset based on user role - doctors see only their patients."""
    queryset = OPDQueue.objects.all()
    
    # Check if user is authenticated
    if self.request.user and self.request.user.is_authenticated:
        # If user is a doctor, filter to show only patients assigned to them
        if self.request.user.role == 'Doctor':
            queryset = queryset.filter(doctor_id=self.request.user.staff_id)
    
    return queryset
```

#### Updated `list()` Method - No ML Predictions for Doctors
Doctors do NOT see ML wait time predictions to avoid unnecessary computation:

```python
def list(self, request, *args, **kwargs):
    """Override list to add ML-predicted wait times for each patient (except for doctors)."""
    queryset = self.filter_queryset(self.get_queryset())
    
    # Skip wait time calculation for doctors
    if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor'):
        # Calculate estimated wait time for each waiting patient (non-doctors only)
        for queue_entry in queryset:
            if queue_entry.status == 'waiting':
                estimated_wait = calculate_patient_wait_time(queue_entry)
                queue_entry.estimated_wait_time = estimated_wait
                OPDQueue.objects.filter(id=queue_entry.id).update(estimated_wait_time=estimated_wait)
    
    # Return serialized data
    ...
```

#### Updated `start_consultation()` and `end_consultation()` Actions
These actions no longer recalculate wait times for doctors:

```python
@action(detail=True, methods=['post'])
def start_consultation(self, request, pk=None):
    """Mark patient consultation as started (no wait time recalculation for doctors)."""
    queue_entry = self.get_object()
    queue_entry.status = 'in_consultation'
    queue_entry.consultation_start_time = timezone.now()
    queue_entry.save()
    
    # Skip wait time recalculation for doctors
    if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor'):
        # Recalculate for non-doctors only
        ...
    
    return Response({'status': 'consultation started'})
```

#### Added `my_queue()` Action
New endpoint specifically for doctors to get their queue with statistics:

```python
@action(detail=False, methods=['get'])
def my_queue(self, request):
    """Get the logged-in doctor's complete queue with statistics."""
    # Returns:
    # {
    #     "doctor_name": "Dr. John Smith",
    #     "statistics": {
    #         "waiting": 3,
    #         "in_consultation": 1,
    #         "completed_today": 10,
    #         "total_active": 4
    #     },
    #     "queue": [...]
    # }
```

## Database Schema Relationships

### The filtering works through these table relationships:

1. **StaffUser Table** (`staff_users`)
   - `staff_id` (Primary Key)
   - `role` (Doctor, Nurse, Admin, etc.)
   - `first_name`, `last_name`, `email`

2. **Doctor Table** (`doctors`)
   - `doctor_id` (Primary Key)
   - `admin_id` (Foreign Key to StaffUser.staff_id)
   - `specialization`

3. **OPDQueue Table** (`opd_queue`)
   - `id` (Primary Key)
   - `doctor_id` (Foreign Key to StaffUser.staff_id)
   - `patient_id` (Foreign Key to Patient.patient_id)
   - `status`, `priority`, etc.

### Filtering Logic:
```sql
-- When a doctor logs in with staff_id = 2
SELECT * FROM opd_queue WHERE doctor_id = 2;

-- This returns only patients assigned to that specific doctor
```

## API Endpoints

### 1. List All Queue Entries (Filtered)
**Endpoint:** `GET /api/opd/queue/`
**Authentication:** Required (JWT Token)
**Behavior:**
- Doctors: See only their assigned patients
- Other roles: See all patients

### 2. Current Active Queue (Filtered)
**Endpoint:** `GET /api/opd/queue/current_queue/`
**Authentication:** Required (JWT Token)
**Returns:** Today's waiting and in-consultation patients
**Behavior:**
- Doctors: See only their assigned patients
- Other roles: See all patients

### 3. My Queue (Doctor-Only)
**Endpoint:** `GET /api/opd/queue/my_queue/`
**Authentication:** Required (JWT Token)
**Access:** Doctors only
**Returns:**
```json
{
    "doctor_name": "Dr. John Smith",
    "statistics": {
        "waiting": 2,
        "in_consultation": 1,
        "completed_today": 8,
        "total_active": 3
    },
    "queue": [
        {
            "id": 1,
            "token_number": 7,
            "patient_name": "Maria Garcia",
            "status": "waiting",
            "priority": "normal",
            "estimated_wait_time": 18
        }
    ]
}
```

### 4. Start Consultation
**Endpoint:** `POST /api/opd/queue/{id}/start_consultation/`
**Authentication:** Required
**Behavior:** Works only on entries accessible to the doctor

### 5. End Consultation
**Endpoint:** `POST /api/opd/queue/{id}/end_consultation/`
**Authentication:** Required
**Behavior:** Works only on entries accessible to the doctor

## Testing

### Database Test
Run the database-level test to verify filtering logic:
```bash
cd backend
python test_doctor_queue_filter.py
```

This will show:
- All doctors in the system
- Patient counts for each doctor
- Detailed queue breakdown by doctor
- Verification that filtering logic works correctly

### API Test
Run the API integration test:
```bash
cd backend
python test_doctor_api_filter.py
```

**Note:** Update the credentials in the script before running:
```python
DOCTOR_CREDENTIALS = {
    "email": "john.smith@hospital.com",
    "password": "your_password"
}
```

## Security Considerations

1. **Authentication Required:** All OPD queue endpoints now require JWT authentication
2. **Role-Based Access:** Filtering is automatic based on the user's role
3. **Data Isolation:** Doctors cannot access other doctors' patient queues
4. **Admin Access:** Non-doctor roles (Admin, Nurse, Receptionist) can still see all records

## Frontend Integration

When calling the API from the frontend:

```javascript
// Example: Fetch doctor's queue
const fetchDoctorQueue = async () => {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/opd/queue/', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    // Data will be automatically filtered for the logged-in doctor
    return data;
};

// Or use the dedicated my_queue endpoint for statistics
const fetchMyQueue = async () => {
    const token = localStorage.getItem('access_token');
    
    const response = await fetch('http://localhost:8000/api/opd/queue/my_queue/', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    
    const data = await response.json();
    return data; // Includes statistics + queue
};
```

## Backward Compatibility

- **Non-doctor users:** Continue to see all queue entries (unchanged behavior)
- **Existing API calls:** Work as before but with automatic filtering for doctors
- **Anonymous/Unauthenticated:** Will receive 401 Unauthorized (security improvement)

## Benefits

1. ✅ **Data Privacy:** Doctors only see their assigned patients
2. ✅ **Better UX:** Doctors see a focused view of their queue
3. ✅ **Automatic:** No need for manual filtering in frontend
4. ✅ **Secure:** Authentication enforced at the API level
5. ✅ **Flexible:** Admins and nurses still have full access
6. ✅ **Performance:** ML predictions disabled for doctors (faster response times)

## Migration Notes

No database migration required. This is a pure logic change in the API layer.

The filtering is based on existing relationships:
- `opd_queue.doctor_id` → `staff_users.staff_id`

## Troubleshooting

### Issue: Doctor sees no records
**Check:**
1. Are there records in `opd_queue` with matching `doctor_id`?
2. Is the doctor's `staff_id` correct?
3. Run: `python test_doctor_queue_filter.py` to verify data

### Issue: Doctor sees all records (not filtered)
**Check:**
1. Is authentication working? Check JWT token
2. Is `request.user.role` set to 'Doctor'?
3. Check server logs for errors

### Issue: 401 Unauthorized
**Check:**
1. Is the JWT token valid?
2. Is it properly included in Authorization header?
3. Has the token expired?

## Summary

print("""
The updated code now includes:

1. **list() method:**
   - Checks: `if not (request.user and request.user.is_authenticated and request.user.role == 'Doctor')`
   - Doctors: ML wait time calculation **SKIPPED** ⚡
   - Others: ML wait time calculation **PERFORMED** 📊

2. **start_consultation() method:**
   - Doctors: Wait time recalculation **SKIPPED**
   - Others: Wait time recalculation **PERFORMED**

3. **end_consultation() method:**
   - Doctors: Wait time recalculation **SKIPPED**
   - Others: Wait time recalculation **PERFORMED**

**Key Points:**
- ✅ Doctors will **NOT** see ML-predicted wait times (better performance)
- ✅ Doctors only see their assigned patients (data privacy)
- ✅ Admins, Nurses, Receptionists **WILL** see ML-predicted wait times
- ✅ Admins, Nurses, Receptionists can see all patients
""")
