#!/usr/bin/env python3
"""
Restore the original geometry for tract 6037183222 from the HTML file.
"""

import json
import re

def find_tract_index(popups, tract_id):
    """Find the index of a tract in the popup list."""
    for i, popup in enumerate(popups):
        if f"Tract: {tract_id}" in popup:
            return i
    return None

def restore_tract_geometry():
    """Restore tract 6037183222 to its original geometry."""
    # Read the HTML file
    html_file = "highland-park/highland-park_udp.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract the JSON data from the script tag
    match = re.search(r'<script type="application/json".*?>({.*?})</script>', html_content, re.DOTALL)
    if not match:
        raise ValueError("Could not find JSON data in HTML file")
    
    data = json.loads(match.group(1))
    
    # Find the addPolygons call
    polygons_call = None
    for call in data['x']['calls']:
        if call.get('method') == 'addPolygons':
            polygons_call = call
            break
    
    if not polygons_call:
        raise ValueError("Could not find addPolygons call in data")
    
    args = polygons_call['args']
    polygon_coords = args[0]  # Array of polygon coordinates
    popups = args[4] if len(args) > 4 and isinstance(args[4], list) else []
    
    # Find tract 6037183222
    tract_index = find_tract_index(popups, "6037183222")
    if tract_index is None:
        raise ValueError("Could not find tract 6037183222 in original data")
    
    print(f"Found tract 6037183222 at index {tract_index}")
    
    # Get original polygon coordinates
    # Structure: polygon_coords[i] is a list, first element is a list of rings
    # Each ring is a dict with 'lng' and 'lat' arrays
    poly_group = polygon_coords[tract_index]
    if not poly_group or len(poly_group) == 0:
        raise ValueError("No polygon data found for tract 6037183222")
    
    # Get the first ring (exterior ring)
    first_ring = poly_group[0]
    if not first_ring or len(first_ring) == 0:
        raise ValueError("No ring data found for tract 6037183222")
    
    coord_dict = first_ring[0]
    if not isinstance(coord_dict, dict) or 'lng' not in coord_dict or 'lat' not in coord_dict:
        raise ValueError("Invalid coordinate format")
    
    # Extract coordinates from lng and lat arrays
    lngs = coord_dict['lng']
    lats = coord_dict['lat']
    
    if len(lngs) != len(lats):
        raise ValueError("Mismatched lng and lat array lengths")
    
    coords = [[lng, lat] for lng, lat in zip(lngs, lats)]
    
    if not coords:
        raise ValueError("Could not extract coordinates from polygon data")
    
    # Close the polygon if needed
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    
    print(f"Extracted {len(coords)} coordinate points")
    
    # Now load the current GeoJSON file
    geojson_file = "public/highland_park_gentrification_tracts.geojson"
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Find and update the tract
    found = False
    for feature in geojson_data['features']:
        if feature['properties'].get('tract_id') == '6037183222':
            # Restore original coordinates
            feature['geometry']['coordinates'] = [coords]
            print(f"✅ Restored original geometry for tract 6037183222")
            found = True
            break
    
    if not found:
        raise ValueError("Could not find tract 6037183222 in GeoJSON file")
    
    # Save the updated GeoJSON
    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2)
    
    print(f"📁 Saved updated GeoJSON to: {geojson_file}")

if __name__ == "__main__":
    try:
        restore_tract_geometry()
        print("✅ Successfully restored tract 6037183222 to original geometry")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

