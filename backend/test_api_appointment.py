#!/usr/bin/env python
"""
Test the appointment API endpoint
"""
import requests
import json

API_URL = "http://127.0.0.1:8000/api/receptionist/appointments/"

appointment_data = {
    "first_name": "John",
    "last_name": "Doe",
    "contact_number": "1234567890",
    "email": "john@example.com",
    "address": "123 Main Street",
    "appointment_date": "2026-01-25",
    "appointment_time": "10:30:00",
    "reason_for_visit": "Department: Cardiology - Regular checkup",
    "status": "Scheduled"
}

print("=" * 60)
print("TESTING APPOINTMENT API ENDPOINT")
print("=" * 60)
print(f"\nAPI URL: {API_URL}")
print(f"\nPayload:")
print(json.dumps(appointment_data, indent=2))

try:
    response = requests.post(
        API_URL,
        json=appointment_data,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"\n{'=' * 60}")
    print(f"Response Status Code: {response.status_code}")
    print(f"{'=' * 60}")
    print(f"\nResponse Content:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        print("\n✓ SUCCESS! Appointment created successfully")
    else:
        print(f"\n✗ Error: Status code {response.status_code}")
        
except Exception as e:
    print(f"\n✗ Error making request: {e}")
    import traceback
    traceback.print_exc()
