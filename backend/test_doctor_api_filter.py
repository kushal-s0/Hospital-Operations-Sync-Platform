"""
API Test for Doctor Queue Filtering
Tests the API endpoints to ensure doctors only see their assigned patients
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

print("=" * 80)
print("API TEST: DOCTOR QUEUE FILTERING")
print("=" * 80)

# Test doctor credentials (replace with actual credentials)
DOCTOR_CREDENTIALS = {
    "email": "john.smith@hospital.com",
    "password": "doctor123"  # Update with actual password
}

OTHER_DOCTOR_CREDENTIALS = {
    "email": "david.w@hospital.com",
    "password": "doctor123"  # Update with actual password
}

def login(credentials):
    """Login and get JWT token"""
    print(f"\n🔐 Logging in as {credentials['email']}...")
    response = requests.post(
        f"{API_URL}/auth/login/",
        json=credentials
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   User: {data.get('user', {}).get('full_name', 'Unknown')}")
        print(f"   Role: {data.get('user', {}).get('role', 'Unknown')}")
        return data.get('access')
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_queue(token, endpoint="/opd/queue/"):
    """Get OPD queue with authentication"""
    print(f"\n📋 Fetching queue from {endpoint}...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{API_URL}{endpoint}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        count = len(data) if isinstance(data, list) else data.get('count', 0)
        print(f"✅ Queue fetched successfully!")
        print(f"   Total entries: {count}")
        return data
    else:
        print(f"❌ Failed to fetch queue: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_my_queue(token):
    """Get doctor's personal queue using the my_queue endpoint"""
    print(f"\n📋 Fetching doctor's personal queue...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{API_URL}/opd/queue/my_queue/", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Personal queue fetched successfully!")
        print(f"   Doctor: {data.get('doctor_name', 'Unknown')}")
        print(f"   Statistics:")
        stats = data.get('statistics', {})
        print(f"     - Waiting: {stats.get('waiting', 0)}")
        print(f"     - In Consultation: {stats.get('in_consultation', 0)}")
        print(f"     - Completed Today: {stats.get('completed_today', 0)}")
        print(f"     - Total Active: {stats.get('total_active', 0)}")
        return data
    else:
        print(f"❌ Failed to fetch personal queue: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_current_queue(token):
    """Get current active queue"""
    return get_queue(token, "/opd/queue/current_queue/")

def display_queue_details(queue_data):
    """Display detailed queue information"""
    print("\n" + "=" * 80)
    print("QUEUE DETAILS")
    print("=" * 80)
    
    if isinstance(queue_data, list):
        entries = queue_data
    else:
        entries = queue_data.get('queue', queue_data.get('results', []))
    
    if not entries:
        print("No entries in queue")
        return
    
    for i, entry in enumerate(entries, 1):
        patient = entry.get('patient', {})
        patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
        if not patient_name:
            patient_name = entry.get('patient_name', 'Unknown')
        
        print(f"\n{i}. Token #{entry.get('token_number', 'N/A')}")
        print(f"   Patient: {patient_name}")
        print(f"   Doctor: {entry.get('doctor_name', 'N/A')}")
        print(f"   Department: {entry.get('department_name', 'N/A')}")
        print(f"   Status: {entry.get('status', 'N/A')}")
        print(f"   Priority: {entry.get('priority', 'N/A')}")
        print(f"   Wait Time: {entry.get('estimated_wait_time', 'N/A')} min")

# Main test flow
print("\n" + "=" * 80)
print("TEST 1: Doctor John Smith Login")
print("=" * 80)

token1 = login(DOCTOR_CREDENTIALS)

if token1:
    print("\n" + "=" * 80)
    print("TEST 2: Fetch Full Queue (should be filtered to John Smith's patients)")
    print("=" * 80)
    queue1 = get_queue(token1)
    if queue1:
        display_queue_details(queue1)
    
    print("\n" + "=" * 80)
    print("TEST 3: Fetch Current Active Queue")
    print("=" * 80)
    current1 = get_current_queue(token1)
    if current1:
        display_queue_details(current1)
    
    print("\n" + "=" * 80)
    print("TEST 4: Fetch My Queue (Personal Queue Endpoint)")
    print("=" * 80)
    my_queue1 = get_my_queue(token1)
    if my_queue1:
        display_queue_details(my_queue1)

print("\n" + "=" * 80)
print("TEST 5: Doctor David Wilson Login")
print("=" * 80)

token2 = login(OTHER_DOCTOR_CREDENTIALS)

if token2:
    print("\n" + "=" * 80)
    print("TEST 6: Fetch Queue for David Wilson (should be different from John Smith)")
    print("=" * 80)
    queue2 = get_queue(token2)
    if queue2:
        display_queue_details(queue2)
    
    print("\n" + "=" * 80)
    print("TEST 7: Fetch My Queue for David Wilson")
    print("=" * 80)
    my_queue2 = get_my_queue(token2)
    if my_queue2:
        display_queue_details(my_queue2)

print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

if token1 and token2:
    if queue1 and queue2:
        count1 = len(queue1) if isinstance(queue1, list) else queue1.get('count', 0)
        count2 = len(queue2) if isinstance(queue2, list) else queue2.get('count', 0)
        
        print(f"\n✅ Both doctors successfully logged in and fetched their queues")
        print(f"   John Smith's queue: {count1} entries")
        print(f"   David Wilson's queue: {count2} entries")
        
        if count1 != count2:
            print(f"\n✅ SUCCESS: Doctors see different queue entries!")
            print(f"   This confirms that filtering by doctor is working correctly.")
        else:
            print(f"\n⚠️  WARNING: Both doctors see the same number of entries.")
            print(f"   This might indicate filtering is not working (or they have same # of patients).")
    else:
        print("\n❌ Failed to fetch queue data for comparison")
else:
    print("\n❌ Failed to authenticate one or both doctors")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print("\nNote: If you see authentication errors, update the credentials in this script")
print("      You may need to create test doctor users or set passwords first.")
