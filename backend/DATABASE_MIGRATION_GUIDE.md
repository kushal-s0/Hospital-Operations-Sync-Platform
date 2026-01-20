# Database Setup for Appointment System

## Prerequisites
- MySQL database `hospital_ops` should be running
- Backend virtual environment activated
- Django project configured with correct database credentials in `.env`

## Step-by-Step Database Changes

### Step 1: Add Columns to `appointments` Table
Run this script to add `age` and `time_slot` columns:

```bash
cd backend
.\venv\Scripts\Activate.ps1
python add_appointment_columns.py
```

**What it does:**
- Adds `age INT NULL` column to store patient age at appointment time
- Adds `time_slot VARCHAR(50) NULL` column to store time slot (e.g., "09:00-09:30")

---

### Step 2: Make `appointment_id` AUTO_INCREMENT
Run this script to enable auto-increment for appointment IDs:

```bash
python fix_appointment_id.py
```

**What it does:**
- Modifies `appointment_id` column to be `AUTO_INCREMENT`
- Ensures new appointments get automatic ID assignment

---

### Step 3: Make `patient_id` AUTO_INCREMENT
Run this script to enable auto-increment for patient IDs:

```bash
python fix_patient_id.py
```

**What it does:**
- Modifies `patient_id` column to be `AUTO_INCREMENT`
- Ensures new patients get automatic ID assignment

---

## Verification

After running all scripts, verify the changes:

```bash
python -c "import os, sys, django; sys.path.append('.'); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings'); django.setup(); from django.db import connection; cursor = connection.cursor(); cursor.execute('DESCRIBE appointments'); print('\n'.join([str(c) for c in cursor.fetchall()]))"
```

You should see:
- `age: int(11) NULL`
- `time_slot: varchar(50) NULL`
- `appointment_id: int(11) NOT NULL auto_increment`

---

## Manual SQL Alternative

If you prefer running SQL directly in MySQL Workbench or command line:

```sql
USE hospital_ops;

-- Add columns
ALTER TABLE appointments ADD COLUMN age INT NULL COMMENT 'Patient age at time of appointment';
ALTER TABLE appointments ADD COLUMN time_slot VARCHAR(50) NULL COMMENT 'Time slot (e.g., 09:00-09:30)';

-- Make appointment_id auto-increment
ALTER TABLE appointments MODIFY COLUMN appointment_id INT(11) NOT NULL AUTO_INCREMENT;

-- Make patient_id auto-increment
ALTER TABLE patients MODIFY COLUMN patient_id INT(11) NOT NULL AUTO_INCREMENT;

-- Verify
DESCRIBE appointments;
DESCRIBE patients;
```

---

## Files Included

The following Python scripts are provided in the `backend/` directory:
- `add_appointment_columns.py` - Adds age and time_slot columns
- `fix_appointment_id.py` - Makes appointment_id auto-increment
- `fix_patient_id.py` - Makes patient_id auto-increment
- `check_doctor_relationship.py` - Utility to verify doctor-staff relationships

---

## Notes

1. **All scripts are safe to run multiple times** - They check if changes already exist
2. **Backup recommended** - Always backup your database before schema changes
3. **No data loss** - These are additive changes only (no columns removed)
4. **Order matters** - Run scripts in the order listed above

---

## Troubleshooting

**Error: "Access denied"**
- Check MySQL credentials in `.env` file
- Ensure virtual environment is activated

**Error: "Foreign key constraint"**
- This is handled automatically by the scripts
- If manual SQL fails, the scripts handle constraints properly

**Error: "Column already exists"**
- Safe to ignore - scripts detect existing columns
- You can proceed to next step
