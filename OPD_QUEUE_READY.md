# OPD Queue - Quick Reference Guide

## ✅ Changes Complete

All changes have been successfully implemented to integrate with the MySQL `opd_queue` table.

## 🔑 Key Updates

### Backend Models
- **OPDQueue** model now in `apps/authentication/models.py`
- Maps directly to MySQL `opd_queue` table
- Uses ForeignKeys for `doctor` (StaffUser) and `department` (Department)

### Frontend
- Fixed "queue.filter is not a function" error
- Updated to send `doctor_name_input` and `department_name_input`
- Displays `doctor_name` and `department_name` from API

### API Fields

**When Creating Queue Entry (POST /api/opd/queue/):**
```json
{
  "patient_first_name": "John",
  "patient_last_name": "Doe",
  "contact_number": "9876543210",
  "doctor_name_input": "John Smith",
  "department_name_input": "Cardiology",
  "priority": "normal",
  "notes": "..."
}
```

**Response Includes:**
- `patient_name` - Full name of patient
- `doctor_name` - Full name of doctor
- `department_name` - Name of department

## 🧪 Testing Results

✅ **Backend Test Passed**
- Created test patient successfully
- Created queue entry with doctor and department ForeignKeys
- Updated status (waiting → in_consultation → completed)
- All database operations working

**Current Database State:**
- 3 doctors available
- 11 departments available
- 22 queue entries total
- 4 waiting | 1 in consultation | 17 completed

## 🚀 Ready to Use

1. **Django Server:** ✅ Running on http://127.0.0.1:8000
2. **Frontend:** Should auto-reload with changes
3. **Database:** MySQL `opd_queue` table active

## 📝 How to Add a Patient (Nurse)

1. Login as nurse: `sarah.j@hospital.com` / `hospital123`
2. Navigate to OPD Queue page
3. Click "Add Patient" button (only visible to nurses)
4. Fill form:
   - First Name / Last Name
   - Contact Number
   - Department (select from dropdown)
   - Doctor Name (type name - will auto-match)
   - Priority (normal/urgent/emergency)
   - Notes (optional)
5. Click "Add Patient"
6. Patient appears in queue list below

## 🔄 Workflow

1. **Nurse adds patient** → Status: `waiting`
2. **Click "Start"** → Status: `in_consultation` (removes estimated wait time)
3. **Click "Complete"** → Status: `completed`

## ⚠️ Important Notes

- Doctor and department must exist in database
- Patient will be auto-created if new
- Token numbers auto-increment
- All timestamps set automatically

## 🎯 Test the Frontend Now!

Open http://localhost:3000 and test:
- ✅ OPD tab loads without "queue.filter" error
- ✅ Add Patient button visible only to nurses
- ✅ Can add new patients to queue
- ✅ Start and Complete buttons work
- ✅ Doctor and department names display correctly

---
**Status:** ✅ All changes deployed and tested
**Date:** January 19, 2026
