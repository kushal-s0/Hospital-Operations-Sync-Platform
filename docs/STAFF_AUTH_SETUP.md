# Staff User Authentication Setup

## Overview
The authentication system now uses the `staff_users` table from your hospital schema instead of Django's default `auth_user` table.

## Login Options
Staff can login using any of the following:
- **Email** (e.g., `admin@hospital.com`)
- **Phone Number** (e.g., `9876543210`)
- **Staff ID** (e.g., `1`)

## Setup Instructions

### 1. Import the Schema
```bash
mysql -u root -p hospital_ops_db < hospital_schema.sql
```

### 2. Insert Dummy Data
```bash
mysql -u root -p hospital_ops_db < backend/insert_dummy_data.sql
```

### 3. Create Staff Users with Hashed Passwords
```bash
cd backend
python create_staff_users.py
```

This script will update all staff users with properly hashed passwords.

### 4. Test Authentication
```bash
cd backend
python test_staff_login.py
```

## Test Credentials

| Name | Email | Phone | Password | Role |
|------|-------|-------|----------|------|
| Admin User | admin@hospital.com | 9876543210 | admin123 | Admin |
| John Smith | john.smith@hospital.com | 9876543211 | doctor123 | Doctor |
| Sarah Johnson | sarah.j@hospital.com | 9876543212 | nurse123 | Nurse |
| Emily Davis | emily.d@hospital.com | 9876543213 | reception123 | Receptionist |
| Michael Brown | michael.b@hospital.com | 9876543214 | pharma123 | Pharmacist |
| David Wilson | david.w@hospital.com | 9876543215 | doctor123 | Doctor |
| Lisa Anderson | lisa.a@hospital.com | 9876543216 | doctor123 | Doctor |
| Robert Taylor | robert.t@hospital.com | 9876543217 | nurse123 | Nurse |

## Login Examples

### Using Email:
```json
{
  "username": "admin@hospital.com",
  "password": "admin123"
}
```

### Using Phone:
```json
{
  "username": "9876543210",
  "password": "admin123"
}
```

### Using Staff ID:
```json
{
  "username": "1",
  "password": "admin123"
}
```

## Response Format
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@hospital.com",
    "phone_number": "9876543210",
    "first_name": "Admin",
    "last_name": "User",
    "full_name": "Admin User",
    "role": "Admin",
    "hospital_id": 1,
    "department_id": 1,
    "is_active": true
  }
}
```

## Database Tables Populated

The dummy data includes:
- **3 Hospitals** (City General, Rural Health Center, Metro Medical)
- **7 Departments** (Emergency, Cardiology, ICU, etc.)
- **8 Staff Users** (Admins, Doctors, Nurses, etc.)
- **3 Doctors** (with specializations)
- **5 Patients**
- **10 Beds** (Various types and statuses)
- **5 Visits**
- **6 Appointments**
- **3 Active Admissions**
- **5 Treatments**
- **5 Billing Records**
- **8 Inventory Items**
- **5 Inventory Usage Records**
- **5 Financial Transactions**

## Verify Data
After running the SQL scripts, verify with:
```sql
SELECT 'hospitals' as table_name, COUNT(*) as count FROM hospitals
UNION ALL SELECT 'staff_users', COUNT(*) FROM staff_users
UNION ALL SELECT 'patients', COUNT(*) FROM patients;
```

## API Endpoints

### Login
```
POST /api/auth/login/
```

### Get Profile
```
GET /api/auth/profile/
Headers: Authorization: Bearer <access_token>
```

### Logout
```
POST /api/auth/logout/
Headers: Authorization: Bearer <access_token>
Body: { "refresh": "<refresh_token>" }
```

## Notes
- All passwords are hashed using Django's PBKDF2 algorithm
- JWT tokens contain staff_id, email, and role
- `last_login` is automatically updated on successful login
- Only active users (`is_active=1`) can login
