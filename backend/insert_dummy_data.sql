-- ============================================
-- HOSPITAL MANAGEMENT SYSTEM - DUMMY DATA
-- ============================================

-- 1. HOSPITALS
INSERT INTO hospitals (hospital_id, hospital_name, region, facility_size_beds) VALUES
(1, 'City General Hospital', 'Urban', 500),
(2, 'Rural Health Center', 'Rural', 150),
(3, 'Metro Medical Center', 'Urban', 350);

-- 2. DEPARTMENTS
INSERT INTO departments (department_id, hospital_id, department_name, total_beds, available_beds, emergency_beds) VALUES
(1, 1, 'Emergency', 50, 10, 20),
(2, 1, 'Cardiology', 40, 15, 5),
(3, 1, 'Orthopedics', 35, 12, 3),
(4, 1, 'Pediatrics', 45, 18, 8),
(5, 2, 'General Medicine', 60, 25, 10),
(6, 3, 'ICU', 30, 5, 15),
(7, 3, 'Surgery', 40, 10, 5);

-- 3. STAFF USERS (Passwords are hashed using Django's make_password with 'password123')
-- Note: You'll need to run a Python script to generate proper Django password hashes
-- For now, these are placeholder hashes - use the create_staff_users.py script
INSERT INTO staff_users (staff_id, hospital_id, department_id, first_name, last_name, role, phone_number, email, password_hash, is_active) VALUES
(1, 1, 1, 'Admin', 'User', 'Admin', '9876543210', 'admin@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(2, 1, 2, 'John', 'Smith', 'Doctor', '9876543211', 'john.smith@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(3, 1, 2, 'Sarah', 'Johnson', 'Nurse', '9876543212', 'sarah.j@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(4, 1, 1, 'Emily', 'Davis', 'Receptionist', '9876543213', 'emily.d@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(5, 1, 3, 'Michael', 'Brown', 'Pharmacist', '9876543214', 'michael.b@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(6, 2, 5, 'David', 'Wilson', 'Doctor', '9876543215', 'david.w@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(7, 3, 6, 'Lisa', 'Anderson', 'Doctor', '9876543216', 'lisa.a@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1),
(8, 3, 6, 'Robert', 'Taylor', 'Nurse', '9876543217', 'robert.t@hospital.com', 'pbkdf2_sha256$600000$placeholder$hash', 1);

-- 4. DOCTORS (extends staff_users)
INSERT INTO doctors (doctor_id, specialization, years_experience) VALUES
(2, 'Cardiology', 10),
(6, 'General Practitioner', 5),
(7, 'Critical Care', 8);

-- 5. PATIENTS
INSERT INTO patients (patient_id, first_name, last_name, gender, date_of_birth, contact_number, address, registration_date, insurance_provider, insurance_number, email) VALUES
(1, 'James', 'Miller', 'M', '1985-03-15', '8765432101', '123 Main St, City', '2024-01-10', 'Health Plus', 'HP12345', 'james.m@email.com'),
(2, 'Maria', 'Garcia', 'F', '1990-07-22', '8765432102', '456 Oak Ave, Town', '2024-02-05', 'Care First', 'CF67890', 'maria.g@email.com'),
(3, 'William', 'Martinez', 'M', '1978-11-30', '8765432103', '789 Pine Rd, Village', '2024-03-12', 'Med Insurance', 'MI54321', 'william.m@email.com'),
(4, 'Emma', 'Rodriguez', 'F', '2010-05-18', '8765432104', '321 Elm St, City', '2024-04-20', 'Health Plus', 'HP98765', 'emma.r@email.com'),
(5, 'Oliver', 'Hernandez', 'M', '1995-09-08', '8765432105', '654 Maple Dr, Town', '2024-05-15', NULL, NULL, 'oliver.h@email.com');

-- 6. BEDS
INSERT INTO beds (bed_id, hospital_id, department_id, bed_type, status) VALUES
(1, 1, 1, 'Emergency', 'Available'),
(2, 1, 1, 'Emergency', 'Occupied'),
(3, 1, 2, 'Normal', 'Available'),
(4, 1, 2, 'ICU', 'Occupied'),
(5, 1, 3, 'Normal', 'Available'),
(6, 2, 5, 'Normal', 'Available'),
(7, 3, 6, 'ICU', 'Occupied'),
(8, 3, 6, 'Ventilator', 'Available'),
(9, 1, 4, 'Normal', 'Available'),
(10, 1, 1, 'Emergency', 'Maintenance');

-- 7. VISITS
INSERT INTO visits (visit_id, patient_id, hospital_id, department_id, visit_datetime, day_of_week, season, time_of_day, urgency_level, nurse_patient_ratio, specialist_availability, time_to_registration_min, time_to_triage_min, time_to_medical_professional_min, total_wait_time_min, patient_outcome, patient_satisfaction) VALUES
(1, 1, 1, 2, '2024-06-15 09:30:00', 'Saturday', 'Summer', 'Morning', 'Medium', 0.25, 3, 10, 15, 25, 50, 'Admitted', 8),
(2, 2, 1, 1, '2024-06-16 14:20:00', 'Sunday', 'Summer', 'Afternoon', 'High', 0.30, 5, 5, 10, 15, 30, 'Discharged', 9),
(3, 3, 2, 5, '2024-06-17 11:00:00', 'Monday', 'Summer', 'Morning', 'Low', 0.20, 2, 20, 30, 40, 90, 'Discharged', 6),
(4, 4, 1, 4, '2024-06-18 16:45:00', 'Tuesday', 'Summer', 'Evening', 'Critical', 0.35, 4, 3, 5, 8, 16, 'Admitted', 10),
(5, 5, 3, 6, '2024-06-19 08:15:00', 'Wednesday', 'Summer', 'Morning', 'Critical', 0.40, 6, 2, 3, 5, 10, 'Admitted', 9);

-- 8. APPOINTMENTS
INSERT INTO appointments (appointment_id, patient_id, doctor_id, visit_id, appointment_date, appointment_time, reason_for_visit, status) VALUES
(1, 1, 2, 1, '2024-06-15', '09:30:00', 'Chest pain', 'Completed'),
(2, 2, 2, 2, '2024-06-16', '14:20:00', 'Heart checkup', 'Completed'),
(3, 3, 6, 3, '2024-06-17', '11:00:00', 'Fever and cough', 'Completed'),
(4, 4, 2, 4, '2024-06-18', '16:45:00', 'Vaccination', 'Completed'),
(5, 5, 7, 5, '2024-06-19', '08:15:00', 'Accident injury', 'Completed'),
(6, 1, 2, NULL, '2024-07-01', '10:00:00', 'Follow-up checkup', 'Scheduled');

-- 9. ADMISSIONS
INSERT INTO admissions (admission_id, patient_id, bed_id, doctor_id, admission_time, discharge_time, condition_level, status) VALUES
(1, 1, 4, 2, '2024-06-15 10:00:00', NULL, 'High', 'Active'),
(2, 4, 2, 2, '2024-06-18 17:00:00', NULL, 'Critical', 'Active'),
(3, 5, 7, 7, '2024-06-19 09:00:00', NULL, 'Critical', 'Active');

-- 10. TREATMENTS
INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date) VALUES
(1, 1, 'ECG Test', 'Electrocardiogram to check heart rhythm', 1500.00, '2024-06-15'),
(2, 2, 'Blood Test', 'Complete blood count and lipid profile', 800.00, '2024-06-16'),
(3, 3, 'Consultation', 'General physician consultation', 500.00, '2024-06-17'),
(4, 4, 'Vaccination', 'DTaP booster shot', 300.00, '2024-06-18'),
(5, 5, 'X-Ray', 'Chest X-ray for injury assessment', 1200.00, '2024-06-19');

-- 11. BILLING
INSERT INTO billing (bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status) VALUES
(1, 1, 1, '2024-06-15', 1500.00, 'Card', 'Paid'),
(2, 2, 2, '2024-06-16', 800.00, 'Insurance', 'Paid'),
(3, 3, 3, '2024-06-17', 500.00, 'Cash', 'Paid'),
(4, 4, 4, '2024-06-18', 300.00, 'Card', 'Paid'),
(5, 5, 5, '2024-06-19', 1200.00, 'Insurance', 'Pending');

-- 12. INVENTORY ITEMS
INSERT INTO inventory_items (item_id, item_name, category, quantity_available, reorder_level, supplier) VALUES
(1, 'Paracetamol 500mg', 'Medicine', 5000, 1000, 'PharmaCorp Ltd'),
(2, 'Surgical Gloves', 'Consumable', 2000, 500, 'MedSupply Inc'),
(3, 'Syringes 5ml', 'Consumable', 3000, 800, 'MedSupply Inc'),
(4, 'Blood Pressure Monitor', 'Equipment', 50, 10, 'MedEquip Solutions'),
(5, 'Amoxicillin 250mg', 'Medicine', 3000, 600, 'PharmaCorp Ltd'),
(6, 'Bandages', 'Consumable', 1500, 300, 'MedSupply Inc'),
(7, 'Oxygen Cylinder', 'Equipment', 100, 20, 'OxyMed Systems'),
(8, 'Insulin Injection', 'Medicine', 800, 200, 'PharmaCorp Ltd');

-- 13. INVENTORY USAGE
INSERT INTO inventory_usage (usage_id, item_id, patient_id, quantity_used, usage_date, department) VALUES
(1, 1, 1, 10, '2024-06-15 10:30:00', 'Cardiology'),
(2, 2, 2, 5, '2024-06-16 14:30:00', 'Emergency'),
(3, 3, 3, 2, '2024-06-17 11:30:00', 'General Medicine'),
(4, 5, 4, 7, '2024-06-18 17:00:00', 'Pediatrics'),
(5, 7, 5, 1, '2024-06-19 09:15:00', 'ICU');

-- 14. FINANCIAL TRANSACTIONS
INSERT INTO financial_transactions (transaction_id, hospital_id, reference_type, reference_id, transaction_type, amount, payment_method, description, transaction_date) VALUES
(1, 1, 'Billing', 1, 'INCOME', 1500.00, 'Card', 'Patient billing payment', '2024-06-15 11:00:00'),
(2, 1, 'Billing', 2, 'INCOME', 800.00, 'Insurance', 'Insurance claim settled', '2024-06-16 15:00:00'),
(3, 2, 'Inventory', 1, 'EXPENSE', 50000.00, 'Bank', 'Medicine stock purchase', '2024-06-17 10:00:00'),
(4, 1, 'Salary', NULL, 'EXPENSE', 150000.00, 'Bank', 'Monthly staff salary', '2024-06-01 09:00:00'),
(5, 3, 'Maintenance', NULL, 'EXPENSE', 25000.00, 'Bank', 'Equipment maintenance', '2024-06-20 14:00:00');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check total records in each table
SELECT 'hospitals' as table_name, COUNT(*) as count FROM hospitals
UNION ALL SELECT 'departments', COUNT(*) FROM departments
UNION ALL SELECT 'staff_users', COUNT(*) FROM staff_users
UNION ALL SELECT 'doctors', COUNT(*) FROM doctors
UNION ALL SELECT 'patients', COUNT(*) FROM patients
UNION ALL SELECT 'beds', COUNT(*) FROM beds
UNION ALL SELECT 'visits', COUNT(*) FROM visits
UNION ALL SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL SELECT 'admissions', COUNT(*) FROM admissions
UNION ALL SELECT 'treatments', COUNT(*) FROM treatments
UNION ALL SELECT 'billing', COUNT(*) FROM billing
UNION ALL SELECT 'inventory_items', COUNT(*) FROM inventory_items
UNION ALL SELECT 'inventory_usage', COUNT(*) FROM inventory_usage
UNION ALL SELECT 'financial_transactions', COUNT(*) FROM financial_transactions;
