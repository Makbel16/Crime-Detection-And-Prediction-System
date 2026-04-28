"""
Test the generate-sample endpoint
"""

import requests

print("Testing Generate Sample Data endpoint...")
print("=" * 70)

try:
    response = requests.post("http://localhost:8000/api/crimes/generate-sample")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✓ SUCCESS! Sample data generated.")
        
        # Verify data exists
        crimes_response = requests.get("http://localhost:8000/api/crimes/?skip=0&limit=5")
        data = crimes_response.json()
        print(f"✓ Database now has {data['total']} records")
    else:
        print(f"\n✗ FAILED! Error: {response.json().get('detail')}")
        
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")

print("=" * 70)
