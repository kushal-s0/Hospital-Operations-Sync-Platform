# Public Appointment Booking Implementation

## Overview
Implemented a complete public appointment booking system that allows patients to book appointments through the landing page without authentication. These appointments will appear in the staff appointments list for review and can be added to the OPD queue.

## Changes Made

### 1. Backend Changes

#### Added Public API Endpoints:

**File: `backend/apps/authentication/views.py`**
- Added `public_doctors_list()` endpoint
  - Route: `GET /api/auth/public/doctors/`
  - No authentication required
  - Returns list of all active doctors with their details

**File: `backend/apps/opd/views.py`**
- Added `public_book_appointment()` endpoint
  - Route: `POST /api/opd/public/book-appointment/`
  - No authentication required
  - Creates new patient record automatically
  - Creates appointment with status 'Scheduled'
  - Returns appointment details

**File: `backend/apps/authentication/urls.py`**
- Added route: `path('public/doctors/', views.public_doctors_list, name='public_doctors_list')`

**File: `backend/apps/opd/urls.py`**
- Added route: `path('public/book-appointment/', public_book_appointment, name='public-book-appointment')`

#### Updated Imports:
- Added necessary imports for Patient, Doctor, Appointment models in OPD views
- Added IsAuthenticated permission class for proper authentication handling

### 2. Frontend Changes

#### New Component:
**File: `frontend/src/components/PublicAppointmentForm.js`**
- Created a new component based on AppointmentForm
- Works without authentication
- Uses public API endpoints
- Features:
  - Fetches doctors list from public endpoint
  - Auto-generates time slots (30-minute duration)
  - Validates all required fields
  - Shows success/error messages
  - Resets form after successful booking
  - Min date validation (cannot book in the past)

#### Updated Landing Page:
**File: `frontend/src/pages/Landing/Landing.js`**
- Replaced the old contact form with PublicAppointmentForm
- Added state management for success messages
- Imported and integrated the new component
- Updated section heading to "Schedule Your Visit"

**File: `frontend/src/pages/Landing/Landing.css`**
- Added styles for `.appointment-form-wrapper`
- Styled the appointment form to match landing page design
- Ensured proper layout in the contact section grid

## How It Works

### Patient Flow:
1. Patient visits landing page
2. Scrolls to "Book Appointment" section (#contact)
3. Fills out form:
   - First Name, Last Name (required)
   - Age (required)
   - Contact Number (required)
   - Select Doctor from dropdown (required)
   - Choose preferred date and time (required)
   - Time slot auto-generates
   - Optional reason for visit
4. Submits form
5. Backend creates new patient record
6. Backend creates appointment with status 'Scheduled'
7. Patient sees success message

### Staff Flow:
1. Nurse logs into system
2. Navigates to Appointments page
3. Views all appointments including public bookings
4. Can filter by status, date, doctor, etc.
5. Reviews appointment details
6. Clicks "Add to Queue" when patient arrives
7. Patient is added to OPD queue for consultation

## API Endpoints

### Public Endpoints (No Authentication Required):

```
GET /api/auth/public/doctors/
Response: [
  {
    "staff_id": 1,
    "first_name": "John",
    "last_name": "Smith",
    "full_name": "John Smith",
    "department_id": 1
  },
  ...
]
```

```
POST /api/opd/public/book-appointment/
Body: {
  "patient_first_name": "Jane",
  "patient_last_name": "Doe",
  "contact_number": "1234567890",
  "age": 30,
  "doctor_id": 1,
  "appointment_date": "2026-01-25",
  "appointment_time": "10:00:00",
  "time_slot": "10:00-10:30",
  "reason_for_visit": "Regular checkup"
}

Response: {
  "message": "Appointment booked successfully!",
  "appointment": {
    "appointment_id": 123,
    "patient_name": "Jane Doe",
    "doctor_name": "Dr. John Smith",
    "appointment_date": "2026-01-25",
    "appointment_time": "10:00:00",
    "status": "Scheduled",
    ...
  }
}
```

## Testing Instructions

### 1. Start Backend Server:
```bash
cd backend
python manage.py runserver
```

### 2. Start Frontend Server:
```bash
cd frontend
npm start
```

### 3. Test Public Booking:
1. Open browser to `http://localhost:3000`
2. Click "Book Appointment" in navigation or scroll to bottom
3. Fill out the appointment form
4. Verify doctors appear in dropdown
5. Submit form
6. Verify success message appears

### 4. Test Staff View:
1. Navigate to `http://localhost:3000/login`
2. Login as nurse/admin
3. Go to Appointments page
4. Verify the newly created appointment appears in the list
5. Test "Add to Queue" functionality

## Features Implemented

✅ Public appointment booking without authentication
✅ Doctor dropdown populated from database
✅ Auto-generated time slots (30-minute intervals)
✅ Form validation for all required fields
✅ Patient record auto-creation
✅ Appointments visible to staff in appointments list
✅ Integration with existing "Add to Queue" workflow
✅ Responsive design matching landing page aesthetic
✅ Success/error message handling
✅ Form reset after successful submission

## Database Impact

### New Records Created:
- **patients table**: New patient record for each booking
- **appointments table**: New appointment record with status 'Scheduled'

### No Changes to Existing:
- All existing appointments remain unchanged
- No modifications to queue system
- No changes to staff authentication

## Security Considerations

- Public endpoints do not expose sensitive staff information
- Only active doctors are shown in public list
- Patient data is validated before insertion
- No authentication tokens exposed to public
- CORS configuration should be reviewed for production deployment

## Next Steps for Production

1. Add email/SMS confirmation for booked appointments
2. Implement appointment availability checking
3. Add captcha to prevent spam bookings
4. Rate limiting on public endpoints
5. Enhanced validation (e.g., phone number format)
6. Patient portal for viewing/managing their appointments
7. Calendar integration for doctors
8. Automated reminders for appointments

## Compatibility

✅ Works with existing authentication system
✅ Compatible with current appointments list
✅ Integrates with OPD queue system
✅ No breaking changes to existing functionality
✅ All staff features remain intact
