"""
Highland Park Commercial Buildings - Yelp Price Data Fetcher

This script fetches business price level data from Yelp Fusion API and adds it
to the commercial building footprints GeoJSON file.

USAGE:
    1. Place this script in the 'scripts/' folder
    2. Add your Yelp API key on line 33
    3. Run from anywhere in the project:
       python scripts/fetch_yelp_prices.py
       
       Or from the scripts folder:
       cd scripts
       python fetch_yelp_prices.py

REQUIREMENTS:
    pip install requests

OUTPUT:
    - Creates: public/highland_park_commercial_buildings_with_prices.geojson
    - Progress tracking: scripts/yelp_progress.json

RATE LIMITS:
    - Check your Yelp API dashboard for current limits
    - Script will continue until all buildings are processed or rate limit is hit
    - If rate limited, wait and re-run the script (progress is saved)
"""

import json
import requests
import time
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent

# ==============================
# CONFIGURATION
# ==============================
YELP_API_KEY = "API_KEY"

# File paths (using absolute paths based on script location)
INPUT_FILE = PROJECT_ROOT / "public" / "highland_park_commercial_buildings_footprint.geojson"
OUTPUT_FILE = PROJECT_ROOT / "public" / "highland_park_commercial_buildings_with_prices.geojson"
PROGRESS_FILE = SCRIPT_DIR / "yelp_progress.json"  # Keep progress in scripts folder

# API endpoint
YELP_API_URL = "https://api.yelp.com/v3/businesses/search"

# Note: Check your Yelp API limits on your dashboard
# Free tier typically has monthly limits (check Yelp for current limits)

# ==============================
# HELPER FUNCTIONS
# ==============================

def get_building_centroid(geometry):
    """Calculate the centroid of a polygon geometry"""
    if geometry['type'] == 'Polygon':
        coords = geometry['coordinates'][0]
    else:
        # Handle MultiPolygon or other types
        coords = geometry['coordinates'][0][0]
    
    # Calculate centroid
    lon_sum = sum(coord[0] for coord in coords)
    lat_sum = sum(coord[1] for coord in coords)
    count = len(coords)
    
    return {
        'longitude': lon_sum / count,
        'latitude': lat_sum / count
    }

def search_yelp_business(latitude, longitude, api_key):
    """
    Search for businesses at a given location using Yelp API
    Returns the price level if found, otherwise None
    """
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': 30,   # Search within 30 meters - close enough for same building, not neighbors
        'limit': 1      # Get the closest business
        # Removed categories filter - accept any business type
    }
    
    try:
        response = requests.get(YELP_API_URL, headers=headers, params=params)
        
        # Check for rate limit error
        if response.status_code == 429:
            print(f"   ⚠️  Rate limit hit! Save progress and try again later.")
            return None
            
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('businesses') and len(data['businesses']) > 0:
            business = data['businesses'][0]
            price = business.get('price', None)  # Returns "$", "$$", "$$$", or "$$$$"
            name = business.get('name', 'Unknown')
            
            # Convert price to numeric level for easier styling
            price_level = None
            if price:
                price_level = len(price)  # "$" = 1, "$$" = 2, etc.
            
            return {
                'price': price,
                'price_level': price_level,
                'business_name': name,
                'yelp_data_found': True
            }
        else:
            return {
                'price': None,
                'price_level': None,
                'business_name': None,
                'yelp_data_found': False
            }
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ API Error: {e}")
        return None

def load_progress():
    """Load progress from previous runs"""
    if PROGRESS_FILE.exists():
        with open(str(PROGRESS_FILE), 'r') as f:
            return json.load(f)
    return {'processed_ids': []}

def save_progress(progress):
    """Save progress to resume later"""
    with open(str(PROGRESS_FILE), 'w') as f:
        json.dump(progress, f)

def save_results(geojson_data, output_file):
    """Save the updated GeoJSON with price data"""
    with open(str(output_file), 'w') as f:
        json.dump(geojson_data, f, indent=2)
    print(f"\n💾 Saved results to: {output_file}")

# ==============================
# MAIN SCRIPT
# ==============================

def main():
    
    print("=" * 60)
    print("🏢 Highland Park Commercial Buildings - Yelp Price Fetcher")
    print("=" * 60)
    
    # Validate API key
    if YELP_API_KEY == "YOUR_API_KEY_HERE":
        print("\n❌ ERROR: Please replace 'YOUR_API_KEY_HERE' with your actual Yelp API key!")
        print("Get your key from: https://www.yelp.com/developers/v3/manage_app")
        return
    
    # Load data
    print("\n📂 Loading commercial buildings data...")
    print(f"   Looking for: {INPUT_FILE}")
    with open(str(INPUT_FILE), 'r') as f:
        geojson_data = json.load(f)
    
    buildings = geojson_data['features']
    total_buildings = len(buildings)
    print(f"   ✅ Loaded {total_buildings} buildings")
    
    # Load progress
    progress = load_progress()
    processed_ids = set(progress.get('processed_ids', []))
    
    if processed_ids:
        print(f"   📋 Resuming: {len(processed_ids)} buildings already processed")
    
    # Process buildings
    print(f"\n🔍 Fetching Yelp price data...")
    print(f"   ⚠️  Check your Yelp dashboard for current API limits")
    
    buildings_processed = 0
    buildings_with_data = 0
    buildings_without_data = 0
    api_calls_made = 0
    
    for idx, building in enumerate(buildings, 1):
        # Get building ID
        building_id = building['properties'].get('OBJECTID', building['properties'].get('BLD_ID', str(idx)))
        
        # Skip if already processed
        if str(building_id) in processed_ids:
            continue
        
        # Get building location
        centroid = get_building_centroid(building['geometry'])
        
        print(f"\n[{idx}/{total_buildings}] Building {building_id}")
        print(f"   📍 Location: {centroid['latitude']:.6f}, {centroid['longitude']:.6f}")
        
        # Call Yelp API
        yelp_data = search_yelp_business(
            centroid['latitude'], 
            centroid['longitude'], 
            YELP_API_KEY
        )
        
        if yelp_data:
            api_calls_made += 1
            
            # Add price data to building properties
            building['properties']['price'] = yelp_data['price']
            building['properties']['price_level'] = yelp_data['price_level']
            building['properties']['business_name'] = yelp_data['business_name']
            building['properties']['yelp_data_found'] = yelp_data['yelp_data_found']
            
            if yelp_data['yelp_data_found']:
                buildings_with_data += 1
                print(f"   ✅ Found: {yelp_data['business_name']} - {yelp_data['price'] or 'No price'}")
            else:
                buildings_without_data += 1
                print(f"   ⚪ No business found at this location")
            
            # Mark as processed
            processed_ids.add(str(building_id))
            buildings_processed += 1
            
            # Save progress every 10 buildings
            if buildings_processed % 10 == 0:
                progress['processed_ids'] = list(processed_ids)
                save_progress(progress)
                save_results(geojson_data, OUTPUT_FILE)
                print(f"   💾 Progress saved")
            
            # Rate limiting: delay between requests to avoid hitting limits
            time.sleep(0.5)
        else:
            print(f"   ⚠️  API call failed, skipping...")
    
    # Final save
    progress['processed_ids'] = list(processed_ids)
    save_progress(progress)
    save_results(geojson_data, OUTPUT_FILE)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"   Buildings processed this session: {buildings_processed}")
    print(f"   Buildings with price data: {buildings_with_data}")
    print(f"   Buildings without data: {buildings_without_data}")
    print(f"   Total processed so far: {len(processed_ids)}/{total_buildings}")
    print(f"   API calls made this session: {api_calls_made}")
    
    remaining = total_buildings - len(processed_ids)
    if remaining > 0:
        print(f"\n   ⚠️  {remaining} buildings remaining")
        print(f"   💡 Run this script again to continue!")
    else:
        print(f"\n   🎉 All buildings processed!")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()