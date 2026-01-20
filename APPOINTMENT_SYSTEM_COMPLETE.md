# Appointment Booking and Management System

## Overview
A complete appointment booking system that allows patients to book appointments from the landing page and enables Admin/Nurse staff to manage, approve, and process appointments.

## Features Implemented

### 1. **Patient Appointment Booking (Landing Page)**
- **Public Access**: Anyone can book an appointment without logging in
- **Form Fields**:
  - Personal Information: Name, Email, Phone, DOB, Gender, Address
  - Appointment Details: Department, Doctor (optional), Date, Time, Reason
- **Smart Features**:
  - Auto-populates departments from database
  - Filters doctors by selected department
  - Prevents booking dates in the past
  - Creates/updates patient records automatically
  - Shows success confirmation

### 2. **Appointments Management Dashboard**
**Access**: Admin, Nurse, Receptionist

#### Statistics Cards:
- 📊 **Pending Approval**: Count of appointments awaiting approval
- 📆 **Today's Appointments**: Appointments scheduled for today
- 📅 **Upcoming (7 days)**: Appointments in the next week

#### Tabs:
1. **Pending**: Appointments awaiting approval (Status: Scheduled)
2. **Today**: All appointments for current date
3. **Upcoming**: Future scheduled appointments
4. **All Appointments**: Complete appointment history

#### Appointment Card Display:
Each appointment shows:
- Patient name, contact number, email
- Appointment date and time
- Assigned doctor and department
- Reason for visit
- Current status (Scheduled/Completed/Cancelled)
- Action buttons

### 3. **Appointment Workflow**

```
Patient Books → Scheduled (Pending) → Admin/Nurse Approves → OPD Queue
                                    ↓
                                 Cancelled
```

#### Step-by-Step:
1. **Patient Books Appointment**: Status = "Scheduled" (pending approval)
2. **Admin/Nurse Reviews**: Can see all pending appointments
3. **Approve Action**:
   - If appointment is for today: Automatically adds to OPD Queue with token number
   - If appointment is for future date: Marked as approved, will be queued on that date
4. **Cancel Action**: Can cancel appointments if needed

### 4. **Integration with OPD Queue**

When an appointment is approved for today:
- ✅ Patient automatically added to OPD Queue
- 🎫 Token number assigned
- 👨‍⚕️ Assigned to selected doctor
- 📝 Notes include appointment reason
- ⏱️ Status set to "waiting"

## API Endpoints

### Public Endpoints (No Auth Required):
- `POST /api/appointments/book/` - Book a new appointment
- `GET /api/appointments/departments/` - Get list of departments
- `GET /api/appointments/doctors/?department_id=X` - Get doctors by department

### Protected Endpoints (Auth Required):
- `GET /api/appointments/appointments/` - List all appointments
  - Query params: `?status=`, `?date=`, `?doctor_id=`, `?all=true`
- `GET /api/appointments/appointments/pending/` - Get pending appointments
- `GET /api/appointments/appointments/stats/` - Get statistics
- `POST /api/appointments/appointments/{id}/approve/` - Approve appointment
- `POST /api/appointments/appointments/{id}/cancel/` - Cancel appointment

## Database Schema

### Appointments Table (Existing)
Already exists in MySQL with fields:
- appointment_id (Primary Key)
- patient_id (Foreign Key to patients)
- doctor_id (Foreign Key to staff_users)
- visit_id (Foreign Key - optional)
- appointment_date
- appointment_time
- reason_for_visit
- status (Scheduled/Completed/Cancelled)
- created_at, updated_at

### Patients Table (Existing)
Patient records are created/updated automatically:
- patient_id
- first_name, last_name
- email, contact_number
- date_of_birth, gender
- address
- registration_date
- insurance details

## Frontend Components

### 1. AppointmentBookingForm Component
**Location**: `frontend/src/components/AppointmentBookingForm/`
- Modal dialog with professional design
- Two-step form (Personal Info → Appointment Details)
- Real-time department and doctor loading
- Form validation
- Success/Error messages
- Responsive design

### 2. AppointmentsManagement Page
**Location**: `frontend/src/pages/Appointments/`
- Dashboard with statistics
- Tabbed interface for filtering
- Card-based appointment display
- Approve/Cancel actions
- Real-time updates
- Loading states

## Sidebar Navigation

### Updated Menu Items:
- **Admin**: See "Appointments" menu item (3rd position)
- **Nurse**: See "Appointments" menu item
- **Receptionist**: See "Appointments" menu item
- **Icon**: 📅 Calendar icon with dots

## User Experience Flow

### For Patients:
1. Visit landing page
2. Click "Book Appointment" button (navbar or hero section)
3. Fill in the booking form
4. Receive confirmation message
5. Wait for approval notification

### For Admin/Nurse:
1. Login to system
2. Click "Appointments" in sidebar
3. See pending appointments dashboard
4. Review appointment details
5. Click "Approve & Add to Queue" or "Cancel"
6. Patient appears in OPD Queue (if today's appointment)

## Styling & Design

### Design System:
- **Colors**: 
  - Primary: Purple gradient (#667eea to #764ba2)
  - Success: Green (#10b981)
  - Warning: Amber (#f59e0b)
  - Danger: Red (#dc2626)
- **Cards**: Clean white cards with subtle shadows
- **Animations**: Smooth transitions and hover effects
- **Icons**: Professional SVG icons
- **Responsive**: Mobile-first design

### Status Badges:
- **Scheduled**: Yellow/Amber (pending approval)
- **Completed**: Green (finished)
- **Cancelled**: Red (cancelled)
- **Approved**: Blue (approved but not yet in queue)

## Installation & Setup

### Backend Setup:
1. App already added to `INSTALLED_APPS` in settings.py
2. URLs registered in main urls.py
3. No migrations needed (using existing tables)

### Frontend Setup:
1. Component created and imported
2. Route added to App.js
3. Sidebar updated with new menu item

## Testing the Feature

### Test Appointment Booking:
1. Navigate to http://localhost:3000
2. Click "Book Appointment"
3. Fill form with test data:
   - Name: John Doe
   - Email: john@test.com
   - Phone: 1234567890
   - DOB: 1990-01-01
   - Select Department and Doctor
   - Choose future date and time
   - Add reason
4. Submit and verify success message

### Test Appointment Management:
1. Login as Admin/Nurse
2. Go to Appointments page
3. See the pending appointment
4. Click "Approve & Add to Queue"
5. Check OPD Queue to see new entry (if today's appointment)

## Future Enhancements (Optional)

- Email notifications on booking/approval
- SMS reminders for appointments
- Calendar view for appointments
- Recurring appointments
- Online payment integration
- Patient appointment history portal
- Doctor availability checking
- Appointment rescheduling
- Waitlist management

## Files Created/Modified

### Backend:
- ✅ `backend/apps/appointments/__init__.py`
- ✅ `backend/apps/appointments/models.py`
- ✅ `backend/apps/appointments/serializers.py`
- ✅ `backend/apps/appointments/views.py`
- ✅ `backend/apps/appointments/urls.py`
- ✅ `backend/apps/appointments/admin.py`
- ✅ `backend/hospital_ops/settings.py` (updated)
- ✅ `backend/hospital_ops/urls.py` (updated)

### Frontend:
- ✅ `frontend/src/components/AppointmentBookingForm/AppointmentBookingForm.js`
- ✅ `frontend/src/components/AppointmentBookingForm/AppointmentBookingForm.css`
- ✅ `frontend/src/pages/Appointments/AppointmentsManagement.js`
- ✅ `frontend/src/pages/Appointments/AppointmentsManagement.css`
- ✅ `frontend/src/pages/Landing/Landing.js` (updated)
- ✅ `frontend/src/App.js` (updated)
- ✅ `frontend/src/components/Sidebar/Sidebar.js` (updated)

## Summary

The appointment system is now fully functional with:
- ✅ Public appointment booking from landing page
- ✅ Patient record management
- ✅ Admin/Nurse appointment management dashboard
- ✅ Approval workflow
- ✅ Automatic OPD queue integration
- ✅ Statistics and filtering
- ✅ Professional UI/UX design
- ✅ Mobile responsive
- ✅ Real-time updates

The system seamlessly connects the public-facing appointment booking with the internal hospital management system, ensuring smooth patient flow from appointment to consultation.
