import os
import sys
import django
import requests
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import StaffUser

print("\n" + "="*60)
print("API ENDPOINT TEST")
print("="*60)

# Get admin user for authentication
admin_user = StaffUser.objects.filter(role='Admin').first()

if not admin_user:
    print("❌ No admin user found!")
    sys.exit(1)

print(f"\n✓ Found admin user: {admin_user.first_name} {admin_user.last_name}")

# Test API endpoint
base_url = "http://localhost:8000"
endpoint = "/api/opd/queue/"

print(f"\n📡 Testing endpoint: {base_url}{endpoint}")

# Test WITHOUT authentication
print("\n1. Request WITHOUT authentication:")
response = requests.get(f"{base_url}{endpoint}")
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Response: {response.text[:200]}")

# Test WITH authentication (get token first)
print("\n2. Requesting auth token...")
auth_response = requests.post(
    f"{base_url}/api/auth/login/",
    json={
        "email": admin_user.email,
        "password_or_phone": "admin123"
    }
)

if auth_response.status_code == 200:
    token = auth_response.json().get('access')
    print(f"   ✓ Got token: {token[:20]}...")
    
    # Test WITH authentication
    print(f"\n3. Request WITH authentication:")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}{endpoint}", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Got response!")
        
        # Check if paginated
        if isinstance(data, dict) and 'results' in data:
            print(f"   Paginated response:")
            print(f"     - Count: {data.get('count', 'N/A')}")
            print(f"     - Next: {data.get('next', 'None')}")
            print(f"     - Results length: {len(data['results'])}")
            if data['results']:
                print(f"     - First result token: #{data['results'][0].get('token_number')}")
        elif isinstance(data, list):
            print(f"   Array response:")
            print(f"     - Length: {len(data)}")
            if data:
                print(f"     - First item token: #{data[0].get('token_number')}")
        else:
            print(f"   Response type: {type(data)}")
            print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    else:
        print(f"   ❌ Error response:")
        print(f"   {response.text[:300]}")
else:
    print(f"   ❌ Could not get token!")
    print(f"   Response: {auth_response.text[:200]}")

print("\n" + "="*60)
