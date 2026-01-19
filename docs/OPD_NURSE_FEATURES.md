# OPD Queue - Nurse Features Implementation ✅

## Features Implemented

### 1. **Role-Based Access Control**
- ✅ "Add Patient" button only visible to **Nurse** role
- Checks user role from localStorage: `currentUser.role === 'Nurse'`

### 2. **Add Patient Form**
- ✅ Modal form with basic patient information
- ✅ Fields included:
  - First Name (required)
  - Last Name (required)
  - Contact Number (required)
  - Department (dropdown)
  - Doctor Name (required)
  - Priority (normal/urgent/emergency)
  - Notes (optional)

### 3. **Patient Creation**
- ✅ Creates new patient in database
- ✅ Automatically generates patient_id
- ✅ Adds patient to OPD queue
- ✅ Shows success/error messages
- ✅ Refreshes queue list after adding

### 4. **Start Consultation Button**
- ✅ Visible when status = 'waiting'
- ✅ On click:
  - Changes status from 'waiting' to 'in_consultation'
  - Sets consultation_start_time
  - Removes estimated wait time from display
  - Shows success message

### 5. **Complete Consultation Button**
- ✅ Visible when status = 'in_consultation'
- ✅ On click:
  - Changes status to 'completed'
  - Sets consultation_end_time
  - Shows success message
  - Refreshes queue list

## Files Modified

### Frontend:
1. **`frontend/src/pages/OPD/OPDQueue.js`**
   - Added role-based button visibility
   - Added patient form modal
   - Added form state management
   - Added API calls for CRUD operations
   - Added Start/Complete button handlers
   - Added success/error message display

2. **`frontend/src/pages/OPD/OPDQueue.css`**
   - Added modal overlay styles
   - Added form styling
   - Added alert message styles
   - Added responsive design

### Backend:
1. **`backend/apps/opd/serializers.py`**
   - Updated OPDQueueSerializer
   - Added patient creation fields
   - Added create() method to handle new patients
   - Auto-generates patient_id

2. **`backend/apps/opd/views.py`** (already had these)
   - `start_consultation` action
   - `end_consultation` action

## How It Works

### For Nurses Only:

1. **Login as Nurse**
   ```
   Email: sarah.j@hospital.com
   Password: hospital123
   ```

2. **Navigate to OPD Queue page**

3. **Click "+ Add Patient" button**
   - Button only visible if user role is 'Nurse'

4. **Fill Patient Form:**
   ```
   First Name: John
   Last Name: Doe
   Contact: 9876543210
   Department: General Medicine
   Doctor: Dr. Smith
   Priority: normal
   Notes: First visit
   ```

5. **Click "Add to Queue"**
   - Creates patient in database
   - Adds to queue with status 'waiting'
   - Shows in list below

6. **Manage Queue:**
   - **For waiting patients:** Click "Start" button
     - Status changes to 'in_consultation'
     - Estimated wait time disappears
   - **For patients in consultation:** Click "Complete" button
     - Status changes to 'completed'
     - Patient removed from active queue

## API Endpoints Used

### 1. Get Queue
```http
GET /api/opd/queue/
```

### 2. Create Patient & Queue Entry
```http
POST /api/opd/queue/
Content-Type: application/json

{
  "patient_first_name": "John",
  "patient_last_name": "Doe",
  "contact_number": "9876543210",
  "department": "General Medicine",
  "doctor_name": "Dr. Smith",
  "priority": "normal",
  "status": "waiting",
  "notes": "First visit"
}
```

### 3. Start Consultation
```http
POST /api/opd/queue/{id}/start_consultation/
```

### 4. Complete Consultation
```http
POST /api/opd/queue/{id}/end_consultation/
```

## Database Tables Used

### 1. **patients** (MySQL)
- `patient_id` (PK, auto-generated)
- `first_name`
- `last_name`
- `contact_number`
- `registration_date`

### 2. **opd_opdqueue** (Local Django)
- `id` (PK)
- `patient_id` (FK to patients)
- `token_number` (auto-generated)
- `department`
- `doctor_name`
- `status` (waiting/in_consultation/completed/cancelled)
- `priority` (normal/urgent/emergency)
- `check_in_time`
- `consultation_start_time`
- `consultation_end_time`
- `estimated_wait_time`
- `notes`

## Status Flow

```
waiting → [Click "Start"] → in_consultation → [Click "Complete"] → completed
```

## UI Components

### Add Patient Button (Nurses Only)
```jsx
{isNurse && (
  <button 
    className="btn btn-primary"
    onClick={() => setShowAddPatientForm(true)}
  >
    + Add Patient
  </button>
)}
```

### Action Buttons in Table
```jsx
{row.status === 'waiting' && (
  <button 
    className="btn btn-primary btn-sm"
    onClick={() => handleStartConsultation(row)}
  >
    Start
  </button>
)}
{row.status === 'in_consultation' && (
  <button 
    className="btn btn-success btn-sm"
    onClick={() => handleCompleteConsultation(row)}
  >
    Complete
  </button>
)}
```

## Validation

### Frontend Validation:
- ✅ First Name (required)
- ✅ Last Name (required)
- ✅ Contact Number (required, tel type)
- ✅ Department (required, dropdown)
- ✅ Doctor Name (required)
- ✅ Priority (required, dropdown)
- ✅ Notes (optional, textarea)

### Backend Validation:
- ✅ Creates new patient if data provided
- ✅ Auto-generates patient_id
- ✅ Auto-generates token_number
- ✅ Sets check_in_time to current time
- ✅ Sets status to 'waiting' by default

## Success Messages

- ✅ "Patient added to queue successfully!"
- ✅ "Started consultation for Token #101"
- ✅ "Completed consultation for Token #102"

## Error Handling

- ✅ Form validation errors
- ✅ API error messages
- ✅ Network error handling
- ✅ Auto-dismiss after 3 seconds

## Testing

### Test as Nurse:
1. Login with nurse credentials
2. Verify "Add Patient" button is visible
3. Click and fill form
4. Submit and verify patient appears in list
5. Click "Start" on a waiting patient
6. Verify status changes to 'in_consultation'
7. Verify estimated wait time is removed
8. Click "Complete"
9. Verify status changes to 'completed'

### Test as Other Roles:
1. Login with non-nurse account (Doctor/Admin)
2. Navigate to OPD Queue
3. Verify "Add Patient" button is NOT visible
4. Start/Complete buttons should still work (for queue management)

## Styling Features

- ✅ Modal overlay with backdrop blur
- ✅ Smooth animations (slideIn, fadeIn, slideUp)
- ✅ Form field focus states
- ✅ Responsive design (mobile-friendly)
- ✅ Success/Error alert animations
- ✅ Button hover effects
- ✅ Clean, modern UI

## Future Enhancements

Possible additions:
- Patient search before creating new
- Duplicate patient check
- Barcode/QR code for token
- SMS notification to patient
- Doctor assignment automation
- Queue position updates in real-time
- Patient history view before consultation

---

**Status**: ✅ Fully Functional  
**Date**: January 19, 2026  
**Role Required**: Nurse (for Add Patient button)  
**All Users**: Can use Start/Complete buttons
