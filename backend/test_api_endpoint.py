"""
Test backend API endpoint accessibility
"""
import requests
import json

print("=" * 60)
print("TESTING BACKEND API ENDPOINT")
print("=" * 60)

backend_url = "http://localhost:8000/api/auth/login/"

print(f"\nTesting: {backend_url}")
print("\nSending login request...")

try:
    response = requests.post(
        backend_url,
        json={
            "username": "admin",
            "password": "admin123"
        },
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ SUCCESS! Login endpoint works!")
        data = response.json()
        print("\nResponse data:")
        print(f"  - Access Token: {data.get('access', 'N/A')[:50]}...")
        print(f"  - Refresh Token: {data.get('refresh', 'N/A')[:50]}...")
        print(f"  - User: {data.get('user', {}).get('username', 'N/A')}")
    else:
        print("✗ FAILED! Login endpoint returned error")
        print(f"\nResponse: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Cannot connect to backend!")
    print("  Make sure backend is running on http://localhost:8000")
    print("  Run: python manage.py runserver")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TESTING CORS AND PREFLIGHT")
print("=" * 60)

try:
    # Test OPTIONS request (CORS preflight)
    options_response = requests.options(
        backend_url,
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    print(f"\nCORS Preflight Status: {options_response.status_code}")
    print(f"Access-Control-Allow-Origin: {options_response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    print(f"Access-Control-Allow-Methods: {options_response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    
except Exception as e:
    print(f"CORS test error: {e}")

print("\n" + "=" * 60)
