import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Patient, Appointment, StaffUser, Department
from django.db import models

print("Testing Patient model...")
try:
    # Test getting max patient_id
    max_patient_id = Patient.objects.aggregate(models.Max('patient_id'))['patient_id__max']
    print(f"Max patient_id: {max_patient_id}")
    
    # Test getting max appointment_id
    max_appt_id = Appointment.objects.aggregate(models.Max('appointment_id'))['appointment_id__max']
    print(f"Max appointment_id: {max_appt_id}")
    
    # Test getting departments
    departments = Department.objects.all()
    print(f"Departments count: {departments.count()}")
    
    # Test getting doctors
    doctors = StaffUser.objects.filter(role='Doctor', is_active=True)
    print(f"Active doctors count: {doctors.count()}")
    
    print("\n✅ All database queries successful!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
