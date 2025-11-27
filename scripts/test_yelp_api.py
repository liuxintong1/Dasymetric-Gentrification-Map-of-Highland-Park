import requests
import json

# REPLACE THIS WITH YOUR ACTUAL API KEY
YELP_API_KEY = "9IspzF3VuW0yDv_JCdtSRqMfz9MUGag7PO6X1YMG3DniWhqQFURtBwNjPAmuCj9nxDr-GD7_GHP8xvm5V6KPTzkBAXIydERrgSKKxbed2D086KjQf2EdHkykXHwnaXYx"

# Test with a known location (Highland Park, LA)
test_latitude = 34.115
test_longitude = -118.188

print("🧪 Testing Yelp API Connection...")
print(f"API Key: {YELP_API_KEY[:10]}..." if len(YELP_API_KEY) > 10 else "KEY TOO SHORT!")
print(f"Location: {test_latitude}, {test_longitude}")
print()

# Test 1: Simple search without categories
print("Test 1: Simple business search...")
headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
params = {
    'latitude': test_latitude,
    'longitude': test_longitude,
    'limit': 1
}

try:
    response = requests.get('https://api.yelp.com/v3/businesses/search', 
                          headers=headers, 
                          params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! API key works!")
        data = response.json()
        if data.get('businesses'):
            biz = data['businesses'][0]
            print(f"   Found business: {biz.get('name')}")
            print(f"   Price: {biz.get('price', 'N/A')}")
        else:
            print("   No businesses found at this location")
    elif response.status_code == 401:
        print("❌ AUTHENTICATION ERROR - Your API key is invalid!")
        print("   Get your key from: https://www.yelp.com/developers/v3/manage_app")
    elif response.status_code == 400:
        print("❌ BAD REQUEST")
        print("   Response:", response.text)
    else:
        print(f"❌ Error: {response.status_code}")
        print("   Response:", response.text)
        
except Exception as e:
    print(f"❌ Connection Error: {e}")

print()
print("Test 2: With categories (like main script)...")
params2 = {
    'latitude': test_latitude,
    'longitude': test_longitude,
    'radius': 50,
    'limit': 1,
    'categories': 'restaurants,food,shopping,services'
}

try:
    response2 = requests.get('https://api.yelp.com/v3/businesses/search',
                            headers=headers,
                            params=params2)
    print(f"Status Code: {response2.status_code}")
    
    if response2.status_code == 200:
        print("✅ SUCCESS!")
        data = response2.json()
        print(f"   Found {len(data.get('businesses', []))} businesses")
    elif response2.status_code == 400:
        print("❌ BAD REQUEST - Issue with parameters")
        print("   Response:", response2.text)
    else:
        print(f"❌ Error: {response2.status_code}")
        print("   Response:", response2.text)
        
except Exception as e:
    print(f"❌ Connection Error: {e}")