"""
Add test data to OPD queue for testing predictions - FIXED VERSION
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.authentication.models import Patient
from apps.opd.models import OPDQueue
from django.utils import timezone

print("Adding test data to OPD queue...")

# Get next patient ID
max_patient = Patient.objects.order_by('-patient_id').first()
patient_id_start = max_patient.patient_id + 1 if max_patient else 1

# Create test patients with correct field names
created_patients = []
for i in range(1, 8):
    try:
        p, created = Patient.objects.get_or_create(
            patient_id=patient_id_start + i - 1,
            defaults={
                'first_name': f'Test{i}',
                'last_name': f'Patient{i}',
                'date_of_birth': '1990-01-01',
                'gender': 'M',
                'contact_number': f'123456789{i}',  # Correct field name
                'address': 'Test Address',
                'email': f'test{i}@patient.com',
                'registration_date': timezone.now().date(),
            }
        )
        if created:
            created_patients.append(p)
            print(f"Created patient: {p.first_name} {p.last_name} (ID: {p.patient_id})")
        else:
            created_patients.append(p)
            print(f"Patient already exists: {p.first_name} {p.last_name} (ID: {p.patient_id})")
    except Exception as e:
        print(f"Error creating patient {i}: {e}")

# Add patients to OPD queue
if created_patients:
    patients = created_patients
else:
    patients = list(Patient.objects.all()[:7])

statuses = ['waiting', 'waiting', 'waiting', 'waiting', 'waiting', 'in_consultation', 'in_consultation']
priorities = ['normal', 'normal', 'urgent', 'normal', 'emergency', 'normal', 'urgent']

# Get next token number
max_token = OPDQueue.objects.order_by('-token_number').first()
token_start = max_token.token_number + 1 if max_token else 100

for i, patient in enumerate(patients[:len(statuses)]):
    try:
        queue_entry, created = OPDQueue.objects.get_or_create(
            patient=patient,
            token_number=token_start + i,
            defaults={
                'department': 'General Medicine',
                'doctor_name': 'Dr. Smith',
                'status': statuses[i],
                'priority': priorities[i],
            }
        )
        if created:
            print(f"Added to queue: Token #{token_start+i} - {patient.first_name} ({statuses[i]}, {priorities[i]})")
    except Exception as e:
        print(f"Error adding patient to queue: {e}")

print("\n=== OPD Queue Summary ===")
print(f"Total in queue: {OPDQueue.objects.count()}")
print(f"Waiting: {OPDQueue.objects.filter(status='waiting').count()}")
print(f"In consultation: {OPDQueue.objects.filter(status='in_consultation').count()}")
print("\nDone! Now try the predictions again.")
