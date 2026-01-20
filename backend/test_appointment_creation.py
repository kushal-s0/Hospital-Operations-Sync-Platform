#!/usr/bin/env python
"""
Test script to verify appointment creation works
"""
import os
import sys
import django
from datetime import date

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import Patient, Appointment
from django.db import connection

def test_appointment_creation():
    """Test creating an appointment with automatic patient creation"""
    
    print("=" * 60)
    print("TESTING APPOINTMENT CREATION")
    print("=" * 60)
    
    try:
        # Get next patient ID
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(patient_id) FROM patients")
        max_id = cursor.fetchone()[0]
        next_patient_id = (max_id or 0) + 1
        print(f"\nNext patient ID will be: {next_patient_id}")
        
        # Create patient
        patient = Patient.objects.create(
            patient_id=next_patient_id,
            first_name="Sagar",
            last_name="Shetty",
            contact_number="09820517950",
            email="sagar.shetty1@somaiya.edu",
            gender="M",
            date_of_birth=date(2000, 1, 1),
            address="Test Address",
            registration_date=date.today()
        )
        print(f"✓ Created patient: {patient.full_name} (ID: {patient.patient_id})")
        
        # Get next appointment ID
        cursor.execute("SELECT MAX(appointment_id) FROM appointments")
        max_app_id = cursor.fetchone()[0]
        next_app_id = (max_app_id or 0) + 1
        print(f"Next appointment ID will be: {next_app_id}")
        
        # Create appointment
        appointment = Appointment.objects.create(
            appointment_id=next_app_id,
            patient=patient,
            appointment_date=date(2026, 1, 20),
            appointment_time="19:55:00",
            reason_for_visit="Department: Dermatology",
            status="Scheduled"
        )
        print(f"✓ Created appointment ID: {appointment.appointment_id}")
        print(f"  Patient: {appointment.patient.full_name}")
        print(f"  Date: {appointment.appointment_date}")
        print(f"  Time: {appointment.appointment_time}")
        print(f"  Status: {appointment.status}")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Appointment created successfully")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    test_appointment_creation()
