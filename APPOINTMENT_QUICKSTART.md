# Quick Start Guide - Appointment System

## 🚀 Start the System

### 1. Start Backend Server
```powershell
cd backend
python manage.py runserver
```

### 2. Start Frontend Server (New Terminal)
```powershell
cd frontend
npm start
```

## 📝 Test the Appointment Booking Flow

### Step 1: Book an Appointment (Public User)
1. Open browser: http://localhost:3000
2. Click **"Book Appointment"** button (either in navbar or hero section)
3. Fill in the form:
   ```
   First Name: John
   Last Name: Doe
   Email: john.doe@test.com
   Contact: 1234567890
   Date of Birth: 1990-01-01
   Gender: Male
   Address: 123 Test Street
   
   Department: Select any (e.g., Cardiology)
   Doctor: Select any or leave as "Any Available"
   Appointment Date: Tomorrow's date
   Time: 10:00 AM
   Reason: Routine checkup
   ```
4. Click **"Book Appointment"**
5. See success message ✓

### Step 2: Manage Appointments (Admin/Nurse)
1. Login as Admin/Nurse/Receptionist
   - Email: admin@hospital.com / nurse@hospital.com
   - Password: admin123 / nurse123
2. Click **"Appointments"** in sidebar (📅 icon)
3. See the new appointment in "Pending" tab
4. Click **"Approve & Add to Queue"** button
5. Confirm the action
6. If appointment is for today, it will be added to OPD Queue

### Step 3: Verify in OPD Queue
1. Click **"OPD Queue"** in sidebar
2. See the approved appointment (if it was for today)
3. Patient will have a token number and "waiting" status

## 🎯 Key Features to Test

### Appointment Booking Form:
- ✅ All fields validation
- ✅ Department loading from database
- ✅ Doctor filtering by department
- ✅ Date validation (no past dates)
- ✅ Success/error messages
- ✅ Responsive design

### Appointments Dashboard:
- ✅ Statistics cards (Pending, Today, Upcoming)
- ✅ Tab filtering (Pending, Today, Upcoming, All)
- ✅ Appointment cards with full details
- ✅ Approve button (adds to OPD queue)
- ✅ Cancel button
- ✅ Status badges
- ✅ Real-time updates

### Integration:
- ✅ Patient record creation/update
- ✅ Automatic OPD queue entry
- ✅ Token number generation
- ✅ Doctor assignment

## 🔍 API Endpoints to Test

### Public Endpoints (No Auth):
```powershell
# Get Departments
curl http://localhost:8000/api/appointments/departments/

# Get Doctors by Department
curl http://localhost:8000/api/appointments/doctors/?department_id=1

# Book Appointment
curl -X POST http://localhost:8000/api/appointments/book/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com",
    "contact_number": "1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "appointment_date": "2026-01-22",
    "appointment_time": "10:00",
    "department_id": 1,
    "reason_for_visit": "Routine checkup"
  }'
```

### Protected Endpoints (Auth Required):
```powershell
# Get All Appointments
curl http://localhost:8000/api/appointments/appointments/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Pending Appointments
curl http://localhost:8000/api/appointments/appointments/?status=Scheduled \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Statistics
curl http://localhost:8000/api/appointments/appointments/stats/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Approve Appointment
curl -X POST http://localhost:8000/api/appointments/appointments/1/approve/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Cancel Appointment
curl -X POST http://localhost:8000/api/appointments/appointments/1/cancel/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🎨 UI Components

### Landing Page:
- **Book Appointment Button**: Top navbar and hero section
- **Modal Form**: Slides up with smooth animation
- **Two Sections**: Personal Info + Appointment Details
- **Success Screen**: Green checkmark with confirmation

### Appointments Management:
- **Header**: Title + description
- **Stats Row**: 3 colorful cards with counts
- **Tabs**: Pending, Today, Upcoming, All
- **Grid Layout**: Responsive appointment cards
- **Action Buttons**: Approve (green) + Cancel (red)

## 🐛 Troubleshooting

### Backend Issues:
```powershell
# If appointments app not recognized
cd backend
python manage.py migrate

# Check if URLs are loaded
python manage.py show_urls | grep appointments
```

### Frontend Issues:
```powershell
# If component not found
cd frontend
npm install

# Clear cache
npm start -- --reset-cache
```

### Database Issues:
```powershell
# Check if appointments table exists
cd backend
python manage.py dbshell
SHOW TABLES LIKE 'appointments';
```

## 📊 Expected Data Flow

```
1. Patient fills form on landing page
   ↓
2. POST /api/appointments/book/
   ↓
3. Creates/updates patient record
   ↓
4. Creates appointment (status: Scheduled)
   ↓
5. Admin/Nurse sees in dashboard
   ↓
6. Clicks "Approve & Add to Queue"
   ↓
7. POST /api/appointments/{id}/approve/
   ↓
8. If today: Creates OPD queue entry
   ↓
9. Patient gets token number
   ↓
10. Appears in OPD Queue page
```

## ✅ Success Checklist

- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Can access landing page
- [ ] Book appointment button works
- [ ] Form loads departments
- [ ] Can submit appointment
- [ ] Login as admin/nurse works
- [ ] Appointments menu visible in sidebar
- [ ] Can see appointments dashboard
- [ ] Statistics show correct counts
- [ ] Can approve appointment
- [ ] Appointment appears in OPD queue (if today)

## 🎉 You're All Set!

The appointment system is now fully operational and integrated with your hospital management system. Patients can book appointments online, and staff can efficiently manage and process them.

### Next Steps:
1. Test all features thoroughly
2. Customize styling if needed
3. Add email/SMS notifications (optional)
4. Deploy to production

---

**Need Help?** Check the main documentation: `APPOINTMENT_SYSTEM_COMPLETE.md`
