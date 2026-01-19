-- Test Data for Hospital Management System
-- All staff users have password: "admin"
-- Password hash generated using Django's make_password function
-- Run this after creating the schema

USE hospital_management;

-- Clear existing data (if any)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE audit_log;
TRUNCATE TABLE financial_transactions;
TRUNCATE TABLE inventory_usage;
TRUNCATE TABLE inventory_items;
TRUNCATE TABLE billing;
TRUNCATE TABLE treatments;
TRUNCATE TABLE appointments;
TRUNCATE TABLE visits;
TRUNCATE TABLE admissions;
TRUNCATE TABLE beds;
TRUNCATE TABLE doctors;
TRUNCATE TABLE staff_users;
TRUNCATE TABLE patients;
TRUNCATE TABLE departments;
TRUNCATE TABLE hospitals;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- HOSPITALS
-- =====================================================
INSERT INTO hospitals (hospital_id, hospital_name, region, facility_size_beds, admin_id) VALUES
(1, 'City General Hospital', 'Urban', 500, 1),
(2, 'Riverside Medical Center', 'Urban', 350, 1),
(3, 'Green Valley Hospital', 'Rural', 150, 1),
(4, 'Metro Health Institute', 'Urban', 600, 1);

-- =====================================================
-- DEPARTMENTS
-- =====================================================
INSERT INTO departments (department_id, hospital_id, department_name, total_beds, available_beds, emergency_beds, admin_id) VALUES
-- Hospital 1 departments
(1, 1, 'Emergency', 50, 12, 20, 1),
(2, 1, 'Cardiology', 40, 8, 5, 1),
(3, 1, 'Orthopedics', 35, 10, 3, 1),
(4, 1, 'Pediatrics', 45, 15, 8, 1),
(5, 1, 'ICU', 30, 5, 10, 1),
-- Hospital 2 departments
(6, 2, 'Emergency', 35, 8, 15, 2),
(7, 2, 'Neurology', 25, 6, 3, 2),
(8, 2, 'Oncology', 30, 7, 2, 2),
-- Hospital 3 departments
(9, 3, 'General Medicine', 40, 18, 10, 3),
(10, 3, 'Surgery', 25, 8, 5, 3),
-- Hospital 4 departments
(11, 4, 'Emergency', 60, 15, 25, 4),
(12, 4, 'Cardiology', 50, 12, 8, 4);

-- =====================================================
-- STAFF USERS (15+ users, all with password "admin")
-- Password hash for "admin": pbkdf2_sha256$600000$saltvalue$hashedpassword
-- Using Django's default password hasher
-- =====================================================
INSERT INTO staff_users (staff_id, hospital_id, department_id, first_name, last_name, role, phone_number, email, password_hash, is_active, admin_id) VALUES
(1, 1, 1, 'Admin', 'Master', 'Admin', '1234567890', 'admin@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(2, 1, 2, 'John', 'Smith', 'Doctor', '1234567891', 'john.smith@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(3, 1, 2, 'Sarah', 'Johnson', 'Nurse', '1234567892', 'sarah.johnson@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(4, 1, 1, 'Emily', 'Davis', 'Receptionist', '1234567893', 'emily.davis@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(5, 1, 3, 'Michael', 'Brown', 'Doctor', '1234567894', 'michael.brown@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(6, 1, 4, 'Lisa', 'Wilson', 'Doctor', '1234567895', 'lisa.wilson@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(7, 1, 4, 'Robert', 'Taylor', 'Nurse', '1234567896', 'robert.taylor@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(8, 1, 5, 'Jennifer', 'Anderson', 'Doctor', '1234567897', 'jennifer.anderson@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(9, 2, 6, 'David', 'Martinez', 'Admin', '1234567898', 'david.martinez@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 2),
(10, 2, 7, 'Jessica', 'Garcia', 'Doctor', '1234567899', 'jessica.garcia@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 2),
(11, 2, 8, 'Daniel', 'Rodriguez', 'Doctor', '1234567800', 'daniel.rodriguez@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 2),
(12, 2, 6, 'Amanda', 'Lee', 'Nurse', '1234567801', 'amanda.lee@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 2),
(13, 3, 9, 'Christopher', 'White', 'Admin', '1234567802', 'christopher.white@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 3),
(14, 3, 10, 'Ashley', 'Harris', 'Doctor', '1234567803', 'ashley.harris@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 3),
(15, 3, 9, 'Matthew', 'Clark', 'Nurse', '1234567804', 'matthew.clark@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 3),
(16, 4, 11, 'Samantha', 'Lewis', 'Admin', '1234567805', 'samantha.lewis@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 4),
(17, 4, 12, 'James', 'Walker', 'Doctor', '1234567806', 'james.walker@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 4),
(18, 1, 3, 'Rachel', 'Young', 'Pharmacist', '1234567807', 'rachel.young@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 1),
(19, 2, 7, 'Kevin', 'Hall', 'Nurse', '1234567808', 'kevin.hall@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 2),
(20, 4, 11, 'Nicole', 'Allen', 'Receptionist', '1234567809', 'nicole.allen@hospital.com', 'pbkdf2_sha256$600000$YGFiYzEyMzQ1Njc4OQ$jGm2jM8L3lL9KZq5g8K7qH6P5N4M3L2K1J0I9H8G7F6E5D4C3B2A1Z', 1, 4);

-- =====================================================
-- DOCTORS (subset of staff_users with role='Doctor')
-- =====================================================
INSERT INTO doctors (doctor_id, specialization, years_experience, admin_id) VALUES
(2, 'Cardiology', 15, 1),
(5, 'Orthopedics', 10, 1),
(6, 'Pediatrics', 8, 1),
(8, 'Critical Care', 12, 1),
(10, 'Neurology', 18, 2),
(11, 'Oncology', 14, 2),
(14, 'General Surgery', 9, 3),
(17, 'Cardiology', 20, 4);

-- =====================================================
-- PATIENTS
-- =====================================================
INSERT INTO patients (patient_id, first_name, last_name, gender, date_of_birth, contact_number, address, registration_date, insurance_provider, insurance_number, email, admin_id) VALUES
(1, 'Alice', 'Cooper', 'F', '1985-03-15', '9876543210', '123 Main St, City', '2025-01-01', 'HealthFirst', 'HF001234', 'alice.cooper@email.com', 1),
(2, 'Bob', 'Dylan', 'M', '1990-07-22', '9876543211', '456 Oak Ave, City', '2025-01-02', 'MediCare Plus', 'MP005678', 'bob.dylan@email.com', 1),
(3, 'Carol', 'King', 'F', '1978-11-30', '9876543212', '789 Pine Rd, City', '2025-01-03', 'HealthFirst', 'HF009012', 'carol.king@email.com', 1),
(4, 'David', 'Bowie', 'M', '1995-05-18', '9876543213', '321 Elm St, Town', '2025-01-04', 'United Health', 'UH003456', 'david.bowie@email.com', 2),
(5, 'Emma', 'Stone', 'F', '1988-09-10', '9876543214', '654 Maple Dr, City', '2025-01-05', NULL, NULL, 'emma.stone@email.com', 1),
(6, 'Frank', 'Sinatra', 'M', '1982-12-25', '9876543215', '987 Cedar Ln, Village', '2025-01-06', 'MediCare Plus', 'MP007890', 'frank.sinatra@email.com', 3),
(7, 'Grace', 'Kelly', 'F', '1992-02-14', '9876543216', '147 Birch Ave, City', '2025-01-07', 'HealthFirst', 'HF012345', 'grace.kelly@email.com', 1),
(8, 'Henry', 'Ford', 'M', '1975-08-08', '9876543217', '258 Spruce St, Town', '2025-01-08', 'United Health', 'UH006789', 'henry.ford@email.com', 2),
(9, 'Iris', 'West', 'F', '1998-04-04', '9876543218', '369 Willow Rd, City', '2025-01-09', 'HealthFirst', 'HF015678', 'iris.west@email.com', 1),
(10, 'Jack', 'Nicholson', 'M', '1980-06-20', '9876543219', '741 Aspen Dr, Village', '2025-01-10', NULL, NULL, 'jack.nicholson@email.com', 3),
(11, 'Kate', 'Winslet', 'F', '1987-10-12', '9876543220', '852 Poplar Ln, City', '2025-01-11', 'MediCare Plus', 'MP009012', 'kate.winslet@email.com', 1),
(12, 'Leo', 'DiCaprio', 'M', '1993-01-28', '9876543221', '963 Hickory Ave, Town', '2025-01-12', 'United Health', 'UH008901', 'leo.dicaprio@email.com', 2),
(13, 'Mary', 'Poppins', 'F', '1970-07-07', '9876543222', '159 Sycamore St, City', '2025-01-13', 'HealthFirst', 'HF018901', 'mary.poppins@email.com', 1),
(14, 'Nathan', 'Drake', 'M', '1996-03-03', '9876543223', '357 Redwood Rd, Village', '2025-01-14', 'MediCare Plus', 'MP012345', 'nathan.drake@email.com', 3),
(15, 'Olivia', 'Newton', 'F', '1984-11-11', '9876543224', '486 Magnolia Dr, City', '2025-01-15', NULL, NULL, 'olivia.newton@email.com', 1),
(16, 'Peter', 'Parker', 'M', '1999-08-27', '9876543225', '597 Dogwood Ln, Town', '2025-01-16', 'United Health', 'UH011234', 'peter.parker@email.com', 2),
(17, 'Quinn', 'Fabray', 'F', '1991-05-05', '9876543226', '608 Cherry Ave, City', '2025-01-17', 'HealthFirst', 'HF021234', 'quinn.fabray@email.com', 1),
(18, 'Ryan', 'Reynolds', 'M', '1986-09-15', '9876543227', '719 Walnut St, Village', '2025-01-18', 'MediCare Plus', 'MP015678', 'ryan.reynolds@email.com', 3),
(19, 'Sophia', 'Loren', 'F', '1977-12-20', '9876543228', '820 Chestnut Rd, City', '2025-01-19', 'United Health', 'UH014567', 'sophia.loren@email.com', 1),
(20, 'Tom', 'Hanks', 'M', '1989-02-02', '9876543229', '931 Fir Dr, Town', '2025-01-20', NULL, NULL, 'tom.hanks@email.com', 2);

-- =====================================================
-- BEDS
-- =====================================================
INSERT INTO beds (bed_id, hospital_id, department_id, bed_type, status, admin_id) VALUES
-- Hospital 1, Emergency Department
(1, 1, 1, 'Emergency', 'Available', 1),
(2, 1, 1, 'Emergency', 'Occupied', 1),
(3, 1, 1, 'Normal', 'Available', 1),
(4, 1, 1, 'ICU', 'Occupied', 1),
-- Hospital 1, Cardiology
(5, 1, 2, 'Normal', 'Available', 1),
(6, 1, 2, 'ICU', 'Occupied', 1),
(7, 1, 2, 'Normal', 'Available', 1),
(8, 1, 2, 'Ventilator', 'Maintenance', 1),
-- Hospital 1, Orthopedics
(9, 1, 3, 'Normal', 'Available', 1),
(10, 1, 3, 'Normal', 'Occupied', 1),
(11, 1, 3, 'Normal', 'Available', 1),
-- Hospital 1, Pediatrics
(12, 1, 4, 'Normal', 'Available', 1),
(13, 1, 4, 'Normal', 'Occupied', 1),
(14, 1, 4, 'Emergency', 'Available', 1),
-- Hospital 1, ICU
(15, 1, 5, 'ICU', 'Occupied', 1),
(16, 1, 5, 'Ventilator', 'Occupied', 1),
(17, 1, 5, 'ICU', 'Available', 1),
-- Hospital 2
(18, 2, 6, 'Emergency', 'Available', 2),
(19, 2, 6, 'Emergency', 'Occupied', 2),
(20, 2, 7, 'Normal', 'Available', 2),
(21, 2, 7, 'ICU', 'Occupied', 2),
(22, 2, 8, 'Normal', 'Available', 2),
(23, 2, 8, 'Normal', 'Occupied', 2),
-- Hospital 3
(24, 3, 9, 'Normal', 'Available', 3),
(25, 3, 9, 'Normal', 'Occupied', 3),
(26, 3, 10, 'Normal', 'Available', 3),
(27, 3, 10, 'Emergency', 'Occupied', 3),
-- Hospital 4
(28, 4, 11, 'Emergency', 'Available', 4),
(29, 4, 11, 'Emergency', 'Occupied', 4),
(30, 4, 12, 'ICU', 'Occupied', 4),
(31, 4, 12, 'Normal', 'Available', 4);

-- =====================================================
-- ADMISSIONS
-- =====================================================
INSERT INTO admissions (admission_id, patient_id, bed_id, doctor_id, admission_time, discharge_time, condition_level, status, admin_id) VALUES
(1, 1, 2, 2, '2026-01-15 08:30:00', NULL, 'High', 'Active', 1),
(2, 3, 4, 8, '2026-01-16 14:20:00', NULL, 'Critical', 'Active', 1),
(3, 5, 6, 2, '2026-01-17 10:15:00', NULL, 'Medium', 'Active', 1),
(4, 7, 10, 5, '2026-01-14 16:45:00', '2026-01-18 12:00:00', 'Low', 'Discharged', 1),
(5, 9, 13, 6, '2026-01-13 09:00:00', NULL, 'Medium', 'Active', 1),
(6, 11, 15, 8, '2026-01-12 22:30:00', NULL, 'Critical', 'Active', 1),
(7, 13, 16, 8, '2026-01-11 18:45:00', NULL, 'Critical', 'Active', 1),
(8, 4, 19, 10, '2026-01-16 11:20:00', NULL, 'High', 'Active', 2),
(9, 8, 21, 10, '2026-01-15 07:30:00', NULL, 'Critical', 'Active', 2),
(10, 12, 23, 11, '2026-01-14 13:15:00', NULL, 'Medium', 'Active', 2),
(11, 6, 25, 14, '2026-01-17 15:00:00', NULL, 'Low', 'Active', 3),
(12, 10, 27, 14, '2026-01-16 20:10:00', NULL, 'High', 'Active', 3),
(13, 16, 29, 17, '2026-01-15 06:45:00', NULL, 'High', 'Active', 4),
(14, 19, 30, 17, '2026-01-14 19:30:00', NULL, 'Critical', 'Active', 4);

-- =====================================================
-- VISITS
-- =====================================================
INSERT INTO visits (visit_id, patient_id, hospital_id, department_id, visit_datetime, day_of_week, season, time_of_day, urgency_level, nurse_patient_ratio, specialist_availability, time_to_registration_min, time_to_triage_min, time_to_medical_professional_min, total_wait_time_min, patient_outcome, patient_satisfaction, admin_id) VALUES
(1, 1, 1, 1, '2026-01-15 08:30:00', 'Wednesday', 'Winter', 'Morning', 'High', 0.15, 1, 5, 10, 25, 40, 'Admitted', 8, 1),
(2, 2, 1, 2, '2026-01-15 10:15:00', 'Wednesday', 'Winter', 'Morning', 'Medium', 0.20, 1, 3, 8, 20, 31, 'Discharged', 9, 1),
(3, 3, 1, 1, '2026-01-16 14:20:00', 'Thursday', 'Winter', 'Afternoon', 'Critical', 0.12, 1, 2, 5, 8, 15, 'Admitted', 7, 1),
(4, 5, 1, 2, '2026-01-17 10:15:00', 'Friday', 'Winter', 'Morning', 'Medium', 0.18, 1, 7, 12, 30, 49, 'Admitted', 6, 1),
(5, 7, 1, 3, '2026-01-14 16:45:00', 'Tuesday', 'Winter', 'Afternoon', 'Low', 0.25, 1, 10, 15, 35, 60, 'Admitted', 5, 1),
(6, 9, 1, 4, '2026-01-13 09:00:00', 'Monday', 'Winter', 'Morning', 'Medium', 0.22, 1, 4, 9, 22, 35, 'Admitted', 8, 1),
(7, 11, 1, 5, '2026-01-12 22:30:00', 'Sunday', 'Winter', 'Night', 'Critical', 0.10, 1, 1, 3, 6, 10, 'Admitted', 9, 1),
(8, 13, 1, 5, '2026-01-11 18:45:00', 'Saturday', 'Winter', 'Evening', 'Critical', 0.11, 1, 2, 4, 7, 13, 'Admitted', 8, 1),
(9, 15, 1, 2, '2026-01-18 11:00:00', 'Saturday', 'Winter', 'Morning', 'Low', 0.23, 1, 12, 18, 40, 70, 'Discharged', 7, 1),
(10, 17, 1, 4, '2026-01-19 14:30:00', 'Sunday', 'Winter', 'Afternoon', 'Medium', 0.20, 1, 6, 11, 28, 45, 'Discharged', 8, 1),
(11, 4, 2, 6, '2026-01-16 11:20:00', 'Thursday', 'Winter', 'Morning', 'High', 0.17, 1, 4, 8, 18, 30, 'Admitted', 9, 2),
(12, 8, 2, 7, '2026-01-15 07:30:00', 'Wednesday', 'Winter', 'Morning', 'Critical', 0.13, 1, 3, 5, 10, 18, 'Admitted', 8, 2),
(13, 12, 2, 8, '2026-01-14 13:15:00', 'Tuesday', 'Winter', 'Afternoon', 'Medium', 0.19, 1, 8, 14, 32, 54, 'Admitted', 7, 2),
(14, 6, 3, 9, '2026-01-17 15:00:00', 'Friday', 'Winter', 'Afternoon', 'Low', 0.28, 1, 15, 20, 45, 80, 'Admitted', 6, 3),
(15, 10, 3, 10, '2026-01-16 20:10:00', 'Thursday', 'Winter', 'Night', 'High', 0.16, 1, 5, 9, 20, 34, 'Admitted', 7, 3),
(16, 14, 3, 9, '2026-01-18 09:45:00', 'Saturday', 'Winter', 'Morning', 'Medium', 0.24, 0, 10, 25, 50, 85, 'Discharged', 5, 3),
(17, 16, 4, 11, '2026-01-15 06:45:00', 'Wednesday', 'Winter', 'Morning', 'High', 0.14, 1, 3, 7, 15, 25, 'Admitted', 9, 4),
(18, 18, 3, 9, '2026-01-17 12:20:00', 'Friday', 'Winter', 'Afternoon', 'Low', 0.26, 1, 20, 30, 55, 105, 'Discharged', 4, 3),
(19, 19, 4, 12, '2026-01-14 19:30:00', 'Tuesday', 'Winter', 'Evening', 'Critical', 0.12, 1, 2, 4, 8, 14, 'Admitted', 8, 4),
(20, 20, 2, 6, '2026-01-19 08:15:00', 'Sunday', 'Winter', 'Morning', 'Medium', 0.21, 1, 7, 13, 30, 50, 'Discharged', 7, 2);

-- =====================================================
-- APPOINTMENTS
-- =====================================================
INSERT INTO appointments (appointment_id, patient_id, doctor_id, visit_id, appointment_date, appointment_time, reason_for_visit, status, admin_id) VALUES
(1, 1, 2, 1, '2026-01-15', '08:30:00', 'Chest pain and shortness of breath', 'Completed', 1),
(2, 2, 2, 2, '2026-01-15', '10:15:00', 'Routine cardiac checkup', 'Completed', 1),
(3, 3, 8, 3, '2026-01-16', '14:20:00', 'Severe respiratory distress', 'Completed', 1),
(4, 5, 2, 4, '2026-01-17', '10:15:00', 'Follow-up heart monitoring', 'Completed', 1),
(5, 7, 5, 5, '2026-01-14', '16:45:00', 'Knee injury from fall', 'Completed', 1),
(6, 9, 6, 6, '2026-01-13', '09:00:00', 'Child fever and cough', 'Completed', 1),
(7, 11, 8, 7, '2026-01-12', '22:30:00', 'Severe trauma emergency', 'Completed', 1),
(8, 13, 8, 8, '2026-01-11', '18:45:00', 'Multi-organ failure', 'Completed', 1),
(9, 4, 10, 11, '2026-01-16', '11:20:00', 'Severe headache and dizziness', 'Completed', 2),
(10, 8, 10, 12, '2026-01-15', '07:30:00', 'Stroke symptoms', 'Completed', 2),
(11, 12, 11, 13, '2026-01-14', '13:15:00', 'Cancer treatment follow-up', 'Completed', 2),
(12, 6, 14, 14, '2026-01-17', '15:00:00', 'Routine health checkup', 'Completed', 3),
(13, 10, 14, 15, '2026-01-16', '20:10:00', 'Post-surgery complications', 'Completed', 3),
(14, 16, 17, 17, '2026-01-15', '06:45:00', 'Cardiac emergency', 'Completed', 4),
(15, 19, 17, 19, '2026-01-14', '19:30:00', 'Heart attack', 'Completed', 4),
-- Scheduled future appointments
(16, 15, 2, NULL, '2026-01-25', '10:00:00', 'Cardiac screening', 'Scheduled', 1),
(17, 17, 6, NULL, '2026-01-26', '14:30:00', 'Child vaccination', 'Scheduled', 1),
(18, 18, 14, NULL, '2026-01-27', '09:15:00', 'General checkup', 'Scheduled', 3),
(19, 20, 10, NULL, '2026-01-28', '11:45:00', 'Neurological assessment', 'Scheduled', 2),
(20, 2, 5, NULL, '2026-01-29', '15:00:00', 'Orthopedic consultation', 'Scheduled', 1);

-- =====================================================
-- TREATMENTS
-- =====================================================
INSERT INTO treatments (treatment_id, appointment_id, treatment_type, description, cost, treatment_date, admin_id) VALUES
(1, 1, 'Emergency Care', 'ECG, oxygen therapy, cardiac monitoring', 5500.00, '2026-01-15', 1),
(2, 2, 'Consultation', 'Routine cardiac examination and blood tests', 1200.00, '2026-01-15', 1),
(3, 3, 'Critical Care', 'Ventilator support, intensive monitoring', 25000.00, '2026-01-16', 1),
(4, 4, 'Follow-up', 'Cardiac monitoring and medication adjustment', 1500.00, '2026-01-17', 1),
(5, 5, 'Orthopedic Surgery', 'Knee arthroscopy and repair', 45000.00, '2026-01-14', 1),
(6, 6, 'Pediatric Care', 'Medication and observation', 2500.00, '2026-01-13', 1),
(7, 7, 'Trauma Care', 'Emergency stabilization and surgery', 75000.00, '2026-01-12', 1),
(8, 8, 'Critical Care', 'Multi-organ support, dialysis', 150000.00, '2026-01-11', 1),
(9, 9, 'Neurology', 'MRI scan and neurological assessment', 8500.00, '2026-01-16', 2),
(10, 10, 'Stroke Treatment', 'Thrombolysis and intensive care', 95000.00, '2026-01-15', 2),
(11, 11, 'Chemotherapy', 'Cancer treatment session', 125000.00, '2026-01-14', 2),
(12, 12, 'General Medicine', 'Complete health checkup', 3500.00, '2026-01-17', 3),
(13, 13, 'Post-Surgical Care', 'Wound care and medication', 8500.00, '2026-01-16', 3),
(14, 14, 'Cardiac Emergency', 'Emergency angioplasty', 185000.00, '2026-01-15', 4),
(15, 15, 'Cardiac Surgery', 'Emergency bypass surgery', 350000.00, '2026-01-14', 4);

-- =====================================================
-- BILLING
-- =====================================================
INSERT INTO billing (bill_id, patient_id, treatment_id, bill_date, amount, payment_method, payment_status, admin_id) VALUES
(1, 1, 1, '2026-01-15', 5500.00, 'Insurance', 'Paid', 1),
(2, 2, 2, '2026-01-15', 1200.00, 'Cash', 'Paid', 1),
(3, 3, 3, '2026-01-16', 25000.00, 'Insurance', 'Pending', 1),
(4, 5, 4, '2026-01-17', 1500.00, 'Card', 'Paid', 1),
(5, 7, 5, '2026-01-14', 45000.00, 'Insurance', 'Paid', 1),
(6, 9, 6, '2026-01-13', 2500.00, 'Cash', 'Paid', 1),
(7, 11, 7, '2026-01-12', 75000.00, 'Insurance', 'Pending', 1),
(8, 13, 8, '2026-01-11', 150000.00, 'Insurance', 'Pending', 1),
(9, 4, 9, '2026-01-16', 8500.00, 'Insurance', 'Paid', 2),
(10, 8, 10, '2026-01-15', 95000.00, 'Insurance', 'Pending', 2),
(11, 12, 11, '2026-01-14', 125000.00, 'Insurance', 'Paid', 2),
(12, 6, 12, '2026-01-17', 3500.00, 'Cash', 'Paid', 3),
(13, 10, 13, '2026-01-16', 8500.00, 'Card', 'Paid', 3),
(14, 16, 14, '2026-01-15', 185000.00, 'Insurance', 'Pending', 4),
(15, 19, 15, '2026-01-14', 350000.00, 'Insurance', 'Pending', 4);

-- =====================================================
-- INVENTORY ITEMS
-- =====================================================
INSERT INTO inventory_items (item_id, item_name, category, quantity_available, reorder_level, supplier, admin_id) VALUES
(1, 'Paracetamol 500mg', 'Medicine', 5000, 1000, 'PharmaCorp India', 1),
(2, 'Amoxicillin 250mg', 'Medicine', 3500, 800, 'MediSupply Ltd', 1),
(3, 'Insulin Glargine', 'Medicine', 800, 200, 'BioPharm Solutions', 1),
(4, 'Surgical Gloves (Box)', 'Consumable', 2500, 500, 'MedEquip Supplies', 1),
(5, 'Syringes 5ml (Pack)', 'Consumable', 4000, 800, 'DisposaMed Inc', 1),
(6, 'N95 Masks (Box)', 'Consumable', 1500, 300, 'SafetyFirst Medical', 1),
(7, 'IV Fluid 500ml', 'Consumable', 3000, 600, 'Fluid Solutions Ltd', 1),
(8, 'Bandages (Roll)', 'Consumable', 2000, 400, 'WoundCare Supplies', 1),
(9, 'ECG Machine', 'Equipment', 8, 2, 'CardioTech Systems', 1),
(10, 'Ventilator', 'Equipment', 12, 3, 'RespiraTech Inc', 1),
(11, 'X-Ray Machine', 'Equipment', 4, 1, 'ImagingPro Medical', 1),
(12, 'Blood Pressure Monitor', 'Equipment', 35, 10, 'VitalCheck Devices', 1),
(13, 'Oxygen Cylinder', 'Equipment', 150, 30, 'OxygenSystems Ltd', 1),
(14, 'Aspirin 75mg', 'Medicine', 4500, 900, 'PharmaCorp India', 2),
(15, 'Cotton Swabs (Pack)', 'Consumable', 3500, 700, 'MedicalCare Supplies', 2),
(16, 'Thermometer Digital', 'Equipment', 50, 15, 'TempCheck Medical', 3),
(17, 'Wheelchair', 'Equipment', 25, 5, 'MobilityAid Solutions', 4),
(18, 'Stethoscope', 'Equipment', 60, 15, 'DiagnosticTools Inc', 1),
(19, 'Gauze Pads (Box)', 'Consumable', 2800, 600, 'WoundCare Supplies', 1),
(20, 'Antibacterial Soap (L)', 'Consumable', 500, 100, 'HygienePro Products', 1);

-- =====================================================
-- INVENTORY USAGE
-- =====================================================
INSERT INTO inventory_usage (usage_id, item_id, patient_id, quantity_used, usage_date, department, admin_id) VALUES
(1, 1, 1, 10, '2026-01-15 09:00:00', 'Emergency', 1),
(2, 7, 1, 2, '2026-01-15 09:15:00', 'Emergency', 1),
(3, 5, 1, 3, '2026-01-15 09:30:00', 'Emergency', 1),
(4, 2, 2, 15, '2026-01-15 10:30:00', 'Cardiology', 1),
(5, 4, 3, 20, '2026-01-16 14:30:00', 'Emergency', 1),
(6, 5, 3, 10, '2026-01-16 14:45:00', 'Emergency', 1),
(7, 7, 3, 5, '2026-01-16 15:00:00', 'Emergency', 1),
(8, 1, 5, 8, '2026-01-17 10:30:00', 'Cardiology', 1),
(9, 8, 7, 25, '2026-01-14 17:00:00', 'Orthopedics', 1),
(10, 4, 7, 30, '2026-01-14 17:15:00', 'Orthopedics', 1),
(11, 1, 9, 12, '2026-01-13 09:30:00', 'Pediatrics', 1),
(12, 5, 9, 2, '2026-01-13 09:45:00', 'Pediatrics', 1),
(13, 7, 11, 10, '2026-01-12 23:00:00', 'ICU', 1),
(14, 4, 11, 50, '2026-01-12 23:15:00', 'ICU', 1),
(15, 6, 13, 15, '2026-01-11 19:00:00', 'ICU', 1),
(16, 7, 13, 8, '2026-01-11 19:15:00', 'ICU', 1),
(17, 14, 4, 7, '2026-01-16 12:00:00', 'Neurology', 2),
(18, 5, 8, 5, '2026-01-15 08:00:00', 'Neurology', 2),
(19, 15, 12, 20, '2026-01-14 14:00:00', 'Oncology', 2),
(20, 4, 12, 25, '2026-01-14 14:15:00', 'Oncology', 2),
(21, 1, 6, 6, '2026-01-17 15:30:00', 'General Medicine', 3),
(22, 8, 10, 15, '2026-01-16 20:30:00', 'Surgery', 3),
(23, 4, 10, 40, '2026-01-16 20:45:00', 'Surgery', 3),
(24, 5, 16, 8, '2026-01-15 07:15:00', 'Emergency', 4),
(25, 7, 16, 3, '2026-01-15 07:30:00', 'Emergency', 4),
(26, 1, 19, 20, '2026-01-14 20:00:00', 'Cardiology', 4),
(27, 4, 19, 60, '2026-01-14 20:15:00', 'Cardiology', 4),
(28, 5, 19, 15, '2026-01-14 20:30:00', 'Cardiology', 4),
(29, 7, 19, 12, '2026-01-14 20:45:00', 'Cardiology', 4),
(30, 8, 19, 30, '2026-01-14 21:00:00', 'Cardiology', 4);

-- =====================================================
-- FINANCIAL TRANSACTIONS
-- =====================================================
INSERT INTO financial_transactions (transaction_id, hospital_id, reference_type, reference_id, transaction_type, amount, payment_method, description, transaction_date, admin_id) VALUES
(1, 1, 'Billing', 1, 'INCOME', 5500.00, 'Insurance', 'Patient billing - Emergency care', '2026-01-15 10:00:00', 1),
(2, 1, 'Billing', 2, 'INCOME', 1200.00, 'Cash', 'Patient billing - Cardiac checkup', '2026-01-15 11:30:00', 1),
(3, 1, 'Billing', 4, 'INCOME', 1500.00, 'Card', 'Patient billing - Follow-up', '2026-01-17 12:00:00', 1),
(4, 1, 'Billing', 5, 'INCOME', 45000.00, 'Insurance', 'Patient billing - Orthopedic surgery', '2026-01-14 18:00:00', 1),
(5, 1, 'Billing', 6, 'INCOME', 2500.00, 'Cash', 'Patient billing - Pediatric care', '2026-01-13 10:30:00', 1),
(6, 1, 'Inventory', 1, 'EXPENSE', 12500.00, 'Bank', 'Medicine procurement - Paracetamol', '2026-01-10 14:00:00', 1),
(7, 1, 'Inventory', 4, 'EXPENSE', 8900.00, 'Bank', 'Consumables purchase - Surgical gloves', '2026-01-11 15:30:00', 1),
(8, 1, 'Inventory', 9, 'EXPENSE', 450000.00, 'Bank', 'Equipment purchase - ECG machine', '2026-01-05 10:00:00', 1),
(9, 1, 'Salary', 2, 'EXPENSE', 85000.00, 'Bank', 'Monthly salary - Dr. John Smith', '2026-01-01 09:00:00', 1),
(10, 1, 'Salary', 3, 'EXPENSE', 45000.00, 'Bank', 'Monthly salary - Sarah Johnson', '2026-01-01 09:00:00', 1),
(11, 1, 'Maintenance', NULL, 'EXPENSE', 35000.00, 'Cash', 'Equipment maintenance - Ventilators', '2026-01-12 11:00:00', 1),
(12, 2, 'Billing', 9, 'INCOME', 8500.00, 'Insurance', 'Patient billing - Neurology', '2026-01-16 13:00:00', 2),
(13, 2, 'Billing', 11, 'INCOME', 125000.00, 'Insurance', 'Patient billing - Chemotherapy', '2026-01-14 15:00:00', 2),
(14, 2, 'Inventory', 14, 'EXPENSE', 9500.00, 'Bank', 'Medicine procurement - Aspirin', '2026-01-09 14:00:00', 2),
(15, 2, 'Salary', 10, 'EXPENSE', 95000.00, 'Bank', 'Monthly salary - Dr. Jessica Garcia', '2026-01-01 09:00:00', 2),
(16, 3, 'Billing', 12, 'INCOME', 3500.00, 'Cash', 'Patient billing - Health checkup', '2026-01-17 16:00:00', 3),
(17, 3, 'Billing', 13, 'INCOME', 8500.00, 'Card', 'Patient billing - Post-surgical care', '2026-01-16 21:00:00', 3),
(18, 3, 'Salary', 14, 'EXPENSE', 78000.00, 'Bank', 'Monthly salary - Dr. Ashley Harris', '2026-01-01 09:00:00', 3),
(19, 4, 'Billing', 14, 'INCOME', 185000.00, 'Insurance', 'Patient billing - Cardiac emergency', '2026-01-15 08:00:00', 4),
(20, 4, 'Billing', 15, 'INCOME', 350000.00, 'Insurance', 'Patient billing - Bypass surgery', '2026-01-14 21:00:00', 4),
(21, 4, 'Inventory', 17, 'EXPENSE', 125000.00, 'Bank', 'Equipment purchase - Wheelchairs', '2026-01-08 12:00:00', 4),
(22, 4, 'Salary', 17, 'EXPENSE', 110000.00, 'Bank', 'Monthly salary - Dr. James Walker', '2026-01-01 09:00:00', 4),
(23, 1, 'Other', NULL, 'EXPENSE', 45000.00, 'Bank', 'Utility bills - Electricity', '2026-01-15 16:00:00', 1),
(24, 2, 'Other', NULL, 'EXPENSE', 32000.00, 'Bank', 'Utility bills - Water and electricity', '2026-01-15 16:00:00', 2),
(25, 3, 'Other', NULL, 'EXPENSE', 18000.00, 'Cash', 'Building maintenance', '2026-01-13 10:00:00', 3),
(26, 4, 'Other', NULL, 'EXPENSE', 55000.00, 'Bank', 'Equipment maintenance and utilities', '2026-01-14 14:00:00', 4);

-- =====================================================
-- AUDIT LOG
-- =====================================================
INSERT INTO audit_log (table_name, record_id, operation_type, admin_id, admin_name, admin_role, old_values, new_values, changed_fields, ip_address, user_agent, timestamp) VALUES
('patients', 1, 'INSERT', 1, 'Admin Master', 'Admin', NULL, '{"patient_id": 1, "first_name": "Alice", "last_name": "Cooper"}', 'All fields', '192.168.1.100', 'Mozilla/5.0', '2025-01-01 10:30:00'),
('patients', 1, 'UPDATE', 1, 'Admin Master', 'Admin', '{"email": null}', '{"email": "alice.cooper@email.com"}', 'email', '192.168.1.100', 'Mozilla/5.0', '2025-01-02 14:20:00'),
('staff_users', 2, 'INSERT', 1, 'Admin Master', 'Admin', NULL, '{"staff_id": 2, "first_name": "John", "last_name": "Smith", "role": "Doctor"}', 'All fields', '192.168.1.100', 'Mozilla/5.0', '2025-01-01 09:15:00'),
('beds', 2, 'UPDATE', 1, 'Admin Master', 'Admin', '{"status": "Available"}', '{"status": "Occupied"}', 'status', '192.168.1.101', 'Mozilla/5.0', '2026-01-15 08:30:00'),
('beds', 4, 'UPDATE', 1, 'Admin Master', 'Admin', '{"status": "Available"}', '{"status": "Occupied"}', 'status', '192.168.1.101', 'Mozilla/5.0', '2026-01-16 14:20:00'),
('admissions', 1, 'INSERT', 1, 'Admin Master', 'Admin', NULL, '{"admission_id": 1, "patient_id": 1, "bed_id": 2}', 'All fields', '192.168.1.102', 'Mozilla/5.0', '2026-01-15 08:30:00'),
('inventory_items', 1, 'UPDATE', 1, 'Admin Master', 'Admin', '{"quantity_available": 5010}', '{"quantity_available": 5000}', 'quantity_available', '192.168.1.103', 'Mozilla/5.0', '2026-01-15 09:00:00'),
('billing', 1, 'INSERT', 1, 'Admin Master', 'Admin', NULL, '{"bill_id": 1, "patient_id": 1, "amount": 5500.00}', 'All fields', '192.168.1.104', 'Mozilla/5.0', '2026-01-15 10:00:00'),
('billing', 1, 'UPDATE', 1, 'Admin Master', 'Admin', '{"payment_status": "Pending"}', '{"payment_status": "Paid"}', 'payment_status', '192.168.1.104', 'Mozilla/5.0', '2026-01-15 10:05:00'),
('admissions', 4, 'UPDATE', 1, 'Admin Master', 'Admin', '{"status": "Active", "discharge_time": null}', '{"status": "Discharged", "discharge_time": "2026-01-18 12:00:00"}', 'status, discharge_time', '192.168.1.102', 'Mozilla/5.0', '2026-01-18 12:00:00');

-- =====================================================
-- Summary Statistics
-- =====================================================
SELECT 'Data Import Complete!' as Status;
SELECT 
    'Hospitals' as Table_Name, COUNT(*) as Record_Count FROM hospitals
UNION ALL SELECT 'Departments', COUNT(*) FROM departments
UNION ALL SELECT 'Staff Users', COUNT(*) FROM staff_users
UNION ALL SELECT 'Doctors', COUNT(*) FROM doctors
UNION ALL SELECT 'Patients', COUNT(*) FROM patients
UNION ALL SELECT 'Beds', COUNT(*) FROM beds
UNION ALL SELECT 'Admissions', COUNT(*) FROM admissions
UNION ALL SELECT 'Visits', COUNT(*) FROM visits
UNION ALL SELECT 'Appointments', COUNT(*) FROM appointments
UNION ALL SELECT 'Treatments', COUNT(*) FROM treatments
UNION ALL SELECT 'Billing', COUNT(*) FROM billing
UNION ALL SELECT 'Inventory Items', COUNT(*) FROM inventory_items
UNION ALL SELECT 'Inventory Usage', COUNT(*) FROM inventory_usage
UNION ALL SELECT 'Financial Transactions', COUNT(*) FROM financial_transactions
UNION ALL SELECT 'Audit Log', COUNT(*) FROM audit_log;

-- Important Note:
-- The password hash used above is a PLACEHOLDER. 
-- After importing this data, you MUST run the Python script to set proper password hashes:
-- python backend/create_staff_users.py
