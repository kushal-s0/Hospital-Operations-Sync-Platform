# Appointment Booking & Management Implementation

## Overview
This implementation adds functional appointment booking from the home page landing form and creates an appointments management tab visible to Admin and Nurse roles only.

## Changes Made

### 1. Backend - Appointment API Endpoints

**File: `backend/apps/receptionist/serializers.py`**
- Added `AppointmentSerializer` with patient name and doctor name fields
- Includes all appointment fields: appointment_id, patient, doctor, visit, appointment_date, appointment_time, reason_for_visit, status

**File: `backend/apps/receptionist/views.py`**
- Added `AppointmentViewSet` with:
  - `create()`: Creates new appointments from booking form, automatically creates patient records if needed
  - `scheduled()`: Retrieves all scheduled appointments
  - `upcoming()`: Retrieves upcoming appointments from today onwards
  - Automatic patient creation from booking form data (first_name, last_name, contact_number, email, address)

**File: `backend/apps/receptionist/urls.py`**
- Registered `AppointmentViewSet` with route `/api/receptionist/appointments/`

### 2. Frontend - Appointment Booking Form

**File: `frontend/src/pages/Landing/Landing.js`**
- Converted static form to functional component with state management
- Added form fields:
  - Name, Phone, Email, Department (existing)
  - Appointment Date (optional)
  - Appointment Time (optional)
- Implemented `handleFormSubmit()` that:
  - Sends appointment data to `/api/receptionist/appointments/`
  - Automatically creates patient record in database
  - Shows success/error messages
  - Clears form on successful submission
- Added loading state to prevent duplicate submissions
- Mobile-responsive form with better UX

### 3. Frontend - Appointments Management Page

**File: `frontend/src/pages/Appointments/Appointments.js`** (NEW)
- Created dedicated page for viewing and managing appointments
- Features:
  - Role-based access control (Admin & Nurse only)
  - Real-time appointment list fetching from API
  - Filter buttons: All, Scheduled, Completed, Cancelled
  - Status badges for visual identification
  - Action buttons to update appointment status (Mark Complete, Cancel)
  - Auto-refresh every 30 seconds
  - Responsive table design

**File: `frontend/src/pages/Appointments/Appointments.css`** (NEW)
- Comprehensive styling for appointments page
- Color-coded status badges
- Interactive filter and action buttons
- Mobile-responsive layout

### 4. Frontend - Integration

**File: `frontend/src/App.js`**
- Imported `Appointments` component
- Added route `/appointments` with role-based access (Admin & Nurse)
- Route wrapped in Layout component for consistent UI

**File: `frontend/src/components/Sidebar/Sidebar.js`**
- Added "Appointments" menu item with 📅 icon
- Added to baseMenuItems with roles: ['Admin', 'Nurse']
- Menu item navigates to `/appointments`

## API Endpoints Created

### POST `/api/receptionist/appointments/`
**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "contact_number": "9876543210",
  "email": "john@example.com",
  "address": "123 Main St",
  "appointment_date": "2026-01-25",
  "appointment_time": "10:00:00",
  "reason_for_visit": "Department: Cardiology",
  "status": "Scheduled"
}
```

**Response:** Created appointment with auto-generated patient record

### GET `/api/receptionist/appointments/`
Returns list of all appointments

### GET `/api/receptionist/appointments/scheduled/`
Returns all scheduled appointments

### GET `/api/receptionist/appointments/upcoming/`
Returns upcoming appointments from today onwards

### PATCH `/api/receptionist/appointments/{id}/`
Updates appointment status (Scheduled → Completed/Cancelled)

## Data Flow

### Patient Books Appointment
1. Patient fills form on Landing page (name, phone, email, department, optional date/time)
2. Form submission triggers `handleFormSubmit()`
3. Data sent to `/api/receptionist/appointments/`
4. Backend automatically creates Patient record
5. Backend creates Appointment record with patient reference
6. Success message displayed to patient

### Admin/Nurse Views Appointments
1. Click "Appointments" in left sidebar
2. Page loads all appointments from `/api/receptionist/appointments/`
3. Filters and status management available
4. Can mark appointments as Completed or Cancelled
5. Page auto-refreshes every 30 seconds

## Database Tables Used

- `patients`: Stores patient information created from booking form
- `appointments`: Stores appointment records with reference to patients

## Security

- Appointment viewing restricted to Admin and Nurse roles via `RoleBasedRoute`
- Authorization header with Bearer token required for PATCH operations
- Form validation on both frontend and backend

## Future Enhancements

1. Doctor assignment to appointments
2. Appointment cancellation notifications
3. Email/SMS confirmation to patients
4. Calendar view of appointments
5. Integration with doctor availability
6. Appointment reminders
7. Patient self-service cancellation portal

## Testing Checklist

- [ ] Patient can book appointment from landing page
- [ ] Appointment data saved to database
- [ ] Patient record created automatically
- [ ] Admin/Nurse can access appointments page
- [ ] Filter buttons work correctly
- [ ] Status updates work (Complete/Cancel)
- [ ] Unauthorized users cannot access appointments page
- [ ] Auto-refresh works every 30 seconds
- [ ] Error handling and validation work
- [ ] Mobile responsive on all screen sizes
