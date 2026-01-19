# OPD Queue MySQL Table Migration

## Summary
Updated the OPD Queue system to use the MySQL `opd_queue` table instead of the Django-managed local table.

## Key Changes

### 1. **Database Structure**
The new `opd_queue` table uses ForeignKeys instead of CharField for doctor and department:

**Old Structure (Django Local):**
- `doctor_name` - CharField (text)
- `department` - CharField (text)

**New Structure (MySQL):**
- `doctor` - ForeignKey to `staff_users` table
- `department` - ForeignKey to `departments` table
- `admin_id` - Integer field

### 2. **Backend Changes**

#### `backend/apps/authentication/models.py`
- ✅ Added `OPDQueue` model mapped to MySQL `opd_queue` table
- ✅ Uses `managed = False` to prevent Django migrations
- ✅ ForeignKeys to Patient, StaffUser (doctor), and Department

#### `backend/apps/opd/models.py`
- ✅ Removed local `OPDQueue` model definition
- ✅ Now imports `OPDQueue` from `authentication.models`

#### `backend/apps/opd/serializers.py`
- ✅ Added `doctor_name` and `department_name` as SerializerMethodField (read-only)
- ✅ Added write-only fields: `doctor_id`, `department_id`, `doctor_name_input`, `department_name_input`
- ✅ Enhanced `create()` method to:
  - Accept doctor/department by ID or name
  - Auto-find matching records from database
  - Auto-generate token numbers
  - Set timestamps automatically

### 3. **Frontend Changes**

#### `frontend/src/pages/OPD/OPDQueue.js`
- ✅ Fixed `queue.filter is not a function` error by ensuring queue is always an array
- ✅ Updated API data submission to use `doctor_name_input` and `department_name_input`
- ✅ Updated table columns to display `doctor_name` and `department_name` from serializer
- ✅ Added fallbacks for missing data (N/A display)

## API Usage

### Creating a New Queue Entry

**Request Body:**
```json
{
  "patient_first_name": "John",
  "patient_last_name": "Doe",
  "contact_number": "9876543210",
  "doctor_name_input": "Dr. Smith",
  "department_name_input": "Cardiology",
  "priority": "normal",
  "notes": "Regular checkup"
}
```

**OR with IDs:**
```json
{
  "patient_first_name": "John",
  "patient_last_name": "Doe",
  "contact_number": "9876543210",
  "doctor_id": 2,
  "department_id": 2,
  "priority": "urgent"
}
```

### Response Format
```json
{
  "id": 1,
  "token_number": 101,
  "patient": {
    "patient_id": 20,
    "first_name": "John",
    "last_name": "Doe",
    "contact_number": "9876543210"
  },
  "patient_name": "John Doe",
  "doctor_name": "John Smith",
  "department_name": "Cardiology",
  "status": "waiting",
  "priority": "normal",
  "check_in_time": "2026-01-19T10:30:00Z",
  "estimated_wait_time": 15,
  "notes": "Regular checkup"
}
```

## Data Requirements

### Before Adding Queue Entries
Ensure the following exist in your MySQL database:

1. **Departments** - At least one department in `departments` table
2. **Doctors** - At least one staff user with `role='Doctor'` in `staff_users` table
3. **Patients** - Will be auto-created if new

## Testing

### Test Adding a Patient to Queue
```python
# backend/test_opd_mysql_queue.py
from apps.authentication.models import OPDQueue, Patient, StaffUser, Department
from django.utils import timezone

# Get a doctor and department
doctor = StaffUser.objects.filter(role='Doctor').first()
department = Department.objects.first()

# Create a new patient
max_patient = Patient.objects.aggregate(Max('patient_id'))['patient_id__max']
patient = Patient.objects.create(
    patient_id=(max_patient or 0) + 1,
    first_name="Test",
    last_name="Patient",
    contact_number="9999999999",
    registration_date=timezone.now().date()
)

# Create queue entry
queue_entry = OPDQueue.objects.create(
    patient=patient,
    doctor=doctor,
    department=department,
    token_number=999,
    status='waiting',
    priority='normal',
    check_in_time=timezone.now(),
    created_at=timezone.now()
)

print(f"✅ Created queue entry: Token #{queue_entry.token_number}")
print(f"   Patient: {queue_entry.patient.full_name}")
print(f"   Doctor: {queue_entry.doctor.full_name}")
print(f"   Department: {queue_entry.department.department_name}")
```

## Troubleshooting

### Issue: "Cannot assign 'string': expected ForeignKey instance"
**Solution:** Use the serializer's `doctor_name_input` and `department_name_input` fields instead of `doctor` and `department` when submitting via API.

### Issue: "Queue data not showing in frontend"
**Solution:** Check that the serializer is returning `doctor_name` and `department_name` fields. The frontend expects these fields.

### Issue: "Invalid doctor or department"
**Solution:** Ensure doctors and departments exist in the database. Check:
```sql
SELECT staff_id, first_name, last_name, role FROM staff_users WHERE role='Doctor';
SELECT department_id, department_name FROM departments;
```

## Migration Path

If you have existing data in the old Django `opd_opdqueue` table:

1. **Export existing data** (if needed for backup)
2. **Clear old Django table** (optional)
3. **Use new MySQL table** - All new entries go to `opd_queue`
4. **No migration needed** - Models use `managed=False`, Django won't touch MySQL table

## Next Steps

1. ✅ Restart Django server to load new models
2. ✅ Test adding patients via the frontend nurse interface
3. ✅ Verify Start/Complete consultation buttons work
4. ✅ Check that doctor and department names display correctly
5. ⏳ Add more doctors and departments as needed

---
**Updated:** January 19, 2026
**Status:** ✅ Complete - Ready for testing
