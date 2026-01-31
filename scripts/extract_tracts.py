#!/usr/bin/env python3
"""
Extract gentrification tract data from highland-park_udp.html and convert to GeoJSON
"""
import json
import re
from pathlib import Path

def extract_tract_data():
    """Extract tract polygons from the HTML file"""
    html_file = Path(__file__).parent.parent / "highland-park" / "highland-park_udp.html"
    
    # Read the HTML file
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
    layer_name = args[2] if len(args) > 2 and args[2] else None  # Layer name is at index 2
    style_info = args[3] if len(args) > 3 and isinstance(args[3], dict) else {}  # Style info at index 3
    popups = args[4] if len(args) > 4 and isinstance(args[4], list) else []  # Popups at index 4
    labels = args[5] if len(args) > 5 and isinstance(args[5], list) else []  # Labels at index 5
    
    # Extract colors
    colors = style_info.get('color', [])
    fill_colors = style_info.get('fillColor', colors)
    
    # Convert to GeoJSON format
    features = []
    
    for i, poly_group in enumerate(polygon_coords):
        # Each poly_group is an array of polygons (can have multiple rings)
        # We'll take the first polygon in each group
        if poly_group and len(poly_group) > 0:
            first_poly = poly_group[0]
            
            # Convert from {lng: [...], lat: [...]} format to [[lng, lat], ...]
            if isinstance(first_poly, dict) and 'lng' in first_poly and 'lat' in first_poly:
                coords = [[lng, lat] for lng, lat in zip(first_poly['lng'], first_poly['lat'])]
                # Close the polygon
                if coords[0] != coords[-1]:
                    coords.append(coords[0])
            else:
                # Handle nested structure
                coords = []
                for coord_obj in first_poly:
                    if isinstance(coord_obj, dict) and 'lng' in coord_obj and 'lat' in coord_obj:
                        coords = [[lng, lat] for lng, lat in zip(coord_obj['lng'], coord_obj['lat'])]
                        break
                if coords and coords[0] != coords[-1]:
                    coords.append(coords[0])
            
            if not coords:
                continue
            
            # Extract tract ID and typology
            tract_id = None
            typology = None
            
            if i < len(popups):
                popup = popups[i]
                # Try to extract tract ID from popup HTML
                tract_match = re.search(r'Tract:\s*(\d+)', popup)
                if tract_match:
                    tract_id = tract_match.group(1)
                
                # Extract typology from popup - it's in the format: "<b>Tract: ...<br>Typology Name</b>"
                typology_match = re.search(r'<b>Tract:[^<]*<br>([^<]+)</b>', popup)
                if typology_match:
                    typology = typology_match.group(1).strip()
            
            # Fallback to labels array if available
            if not typology and i < len(labels):
                typology = labels[i]
            
            # Get color for this tract
            color = colors[i] if i < len(colors) else colors[0] if colors else "#333333"
            
            feature = {
                "type": "Feature",
                "properties": {
                    "tract_id": tract_id,
                    "typology": typology,
                    "color": color,
                    "popup": popups[i] if i < len(popups) else None
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                }
            }
            features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson

if __name__ == "__main__":
    try:
        geojson_data = extract_tract_data()
        
        # Save to public folder
        output_file = Path(__file__).parent.parent / "public" / "highland_park_gentrification_tracts.geojson"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, indent=2)
        
        print(f"✅ Successfully extracted {len(geojson_data['features'])} tracts")
        print(f"📁 Saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

