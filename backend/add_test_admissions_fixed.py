"""
Add test admissions data for disease-based demand prediction - FIXED VERSION
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.authentication.models import Patient, Department, Bed, Admission
from django.utils import timezone

print("Adding test admissions for disease-based predictions...")

# Get or create departments (using actual MySQL schema)
depts_data = [
    (101, 'General Medicine', 1),
    (102, 'Cardiology', 1),
    (103, 'Pulmonology', 1),
    (104, 'Emergency', 1)
]
departments = {}
for dept_id, dept_name, hospital_id in depts_data:
    try:
        dept, created = Department.objects.get_or_create(
            department_id=dept_id,
            defaults={
                'department_name': dept_name,
                'hospital_id': hospital_id,
                'total_beds': 10,
                'available_beds': 5,
            }
        )
        departments[dept_name] = dept
        if created:
            print(f"Created department: {dept_name} (ID: {dept_id})")
    except Exception as e:
        print(f"Error with department {dept_name}: {e}")

# Get next bed ID
max_bed = Bed.objects.order_by('-bed_id').first()
bed_id_start = max_bed.bed_id + 1 if max_bed else 1

# Create some beds
for dept_name, dept in departments.items():
    for i in range(1, 4):
        try:
            bed, created = Bed.objects.get_or_create(
                bed_id=bed_id_start,
                defaults={
                    'department_id': dept.department_id,
                    'hospital_id': dept.hospital_id,
                    'bed_type': 'Normal',
                    'status': 'Available' if i > 2 else 'Occupied',
                }
            )
            if created:
                print(f"Created bed: {dept_name[:3].upper()}-{i:02d} (ID: {bed_id_start})")
                bed_id_start += 1
        except Exception as e:
            print(f"Error creating bed: {e}")

# Get patients or create more if needed
patients = list(Patient.objects.all())
print(f"Found {len(patients)} existing patients")

if len(patients) < 12:
    # Create more patients if needed
    max_patient = Patient.objects.order_by('-patient_id').first()
    patient_id = max_patient.patient_id + 1 if max_patient else 1
    
    for i in range(len(patients) + 1, 13):
        try:
            p = Patient.objects.create(
                patient_id=patient_id,
                first_name=f'Patient{i}',
                last_name=f'Admitted{i}',
                date_of_birth='1985-05-15',
                gender='M' if i % 2 else 'F',
                contact_number=f'98765432{i:02d}',
                address='Hospital Address',
                email=f'patient{i}@hospital.com',
                registration_date=timezone.now().date(),
            )
            patients.append(p)
            patient_id += 1
            print(f"Created patient: {p.first_name} (ID: {p.patient_id})")
        except Exception as e:
            print(f"Error creating patient: {e}")

# Create admissions with different diagnoses
diagnoses = [
    'Respiratory Infection',
    'Respiratory Infection', 
    'Respiratory Infection',
    'Fever/Viral',
    'Fever/Viral',
    'Diabetes',
    'Diabetes',
    'Hypertension',
    'Cardiac',
    'Infection/Bacterial',
    'Pain/Injury',
    'Allergy',
]

# Get available beds
available_beds = list(Bed.objects.filter(status='Available')[:len(diagnoses)])

# Get next admission ID
max_admission = Admission.objects.order_by('-admission_id').first()
admission_id = max_admission.admission_id + 1 if max_admission else 1

for i, (patient, diagnosis) in enumerate(zip(patients[:len(diagnoses)], diagnoses)):
    try:
        # Check if admission already exists for this patient with Active status
        existing = Admission.objects.filter(
            patient_id=patient.patient_id,
            status='Active'
        ).first()
        
        if not existing:
            admission = Admission.objects.create(
                admission_id=admission_id,
                patient_id=patient.patient_id,
                bed_id=available_beds[i].bed_id if i < len(available_beds) else None,
                admission_time=timezone.now(),
                condition_level='High' if i < 5 else 'Medium',
                status='Active',
            )
            admission_id += 1
            print(f"Created admission: {patient.first_name} - {diagnosis} (ID: {admission.admission_id})")
        else:
            print(f"Admission already exists for {patient.first_name}")
    except Exception as e:
        print(f"Error creating admission for {patient.first_name}: {e}")

print("\n=== Admissions Summary ===")
print(f"Total active admissions: {Admission.objects.filter(status='Active').count()}")
print(f"Total beds: {Bed.objects.count()}")
print(f"Available beds: {Bed.objects.filter(status='Available').count()}")

print("\nDone! Now try the demand forecast.")
