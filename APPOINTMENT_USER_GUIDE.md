# Appointment Booking & Management - Quick Start Guide

## For Patients (Landing Page)

### How to Book an Appointment

1. **Visit the Home Page**
   - Navigate to the landing page (/)
   - Scroll to the "Book an Appointment" section

2. **Fill in Your Information**
   - **Full Name**: Enter your complete name
   - **Phone Number**: Your contact number (required)
   - **Email Address**: Your email (required)
   - **Department**: Select the medical department (required)
   - **Preferred Date**: Select your preferred appointment date (optional - today if not specified)
   - **Preferred Time**: Select your preferred time (optional - 10:00 AM if not specified)
   - **Message**: Describe your symptoms or concerns (optional)

3. **Submit the Form**
   - Click "Request Appointment" button
   - Wait for confirmation message
   - A success message will appear if booking is successful
   - You're all set! Our team will contact you shortly.

### What Happens After Booking
- Your appointment is recorded in the system
- A patient profile is automatically created
- Admin/Nurse staff can view and manage your appointment

---

## For Admin & Nurse Staff

### How to Access Appointments

1. **Login to Dashboard**
   - Use your staff credentials to login
   - Navigate to the main dashboard

2. **Open Appointments Tab**
   - Look at the left sidebar menu
   - Click on "Appointments" (with 📅 icon)
   - You'll see all appointments in the system

### Managing Appointments

#### Filter Appointments
- **All**: View all appointments in system
- **Scheduled**: View only appointments waiting to happen
- **Completed**: View appointments that have been completed
- **Cancelled**: View cancelled appointments

#### Update Appointment Status
For **Scheduled** appointments, you can:
- Click **✓** button to mark as **Completed**
- Click **✕** button to **Cancel** the appointment

#### View Appointment Details
Table columns show:
- **Appointment ID**: Unique identifier (#)
- **Patient Name**: Full name of the patient
- **Date**: Appointment date
- **Time**: Appointment time
- **Reason for Visit**: Why the patient is coming (department + notes)
- **Status**: Current status (Scheduled/Completed/Cancelled)

### Features
- **Real-time Updates**: Page automatically refreshes every 30 seconds
- **Quick Status Changes**: Update appointments without page reload
- **Filtering**: Organize appointments by status
- **Responsive Design**: Works on desktop, tablet, and mobile

### Data Privacy
- Only Admin and Nurse users can access this page
- Patient information is protected and used only for appointment management
- All operations are logged for audit purposes

---

## API Reference (For Developers)

### Create Appointment
```
POST /api/receptionist/appointments/
Content-Type: application/json

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

### Get All Appointments
```
GET /api/receptionist/appointments/
Authorization: Bearer {access_token}
```

### Get Scheduled Appointments
```
GET /api/receptionist/appointments/scheduled/
Authorization: Bearer {access_token}
```

### Update Appointment Status
```
PATCH /api/receptionist/appointments/{appointment_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "Completed"
}
```

---

## Troubleshooting

### "Unauthorized: Only Admin and Nurse can view appointments"
- Your user role doesn't have permission to view appointments
- Contact your system administrator
- Only Admin and Nurse roles can access this feature

### "Failed to fetch appointments"
- Check your internet connection
- Ensure backend server is running
- Try refreshing the page
- Check browser console for detailed error

### Appointment booking form shows error
- Verify all required fields are filled (Name, Phone, Email, Department)
- Check your internet connection
- Ensure backend API is running at http://localhost:8000
- Check browser console for specific error message

### Appointments not showing after booking
- Refresh the page
- Wait a few seconds for the backend to process
- Check that you're logged in as Admin or Nurse to view appointments

---

## System Requirements

### Frontend
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- React 17+

### Backend
- Django 3.2+
- Django REST Framework
- MySQL database with appointments table
- Python 3.8+

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review browser console for error messages
3. Contact your system administrator
4. Check application logs

---

## Feature Highlights

✅ **Easy Booking**: Simple form with minimal required fields
✅ **Automatic Patient Creation**: Patient records created on first appointment
✅ **Role-Based Access**: Only authorized staff can view appointments
✅ **Real-time Management**: Update appointment status instantly
✅ **Mobile Friendly**: Works on all screen sizes
✅ **Auto-refresh**: Data updates every 30 seconds
✅ **Status Tracking**: Clear visual indicators for appointment status
✅ **Filtering**: Organize appointments by status

---

*Last Updated: January 20, 2026*
*Version: 1.0*
