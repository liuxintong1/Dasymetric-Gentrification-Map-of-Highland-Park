#!/usr/bin/env python3
"""
Script to clip tract 6037183222 to align with the Highland Park boundary.
This will make the tract "hug" the outline of the Highland Park boundary.
"""

import json
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union

def load_geojson(file_path):
    """Load a GeoJSON file and return the data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_geojson(data, file_path):
    """Save data to a GeoJSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def clip_tract_to_boundary(tract_geojson_path, boundary_geojson_path, output_path, tract_ids):
    """
    Clip specified tracts to the Highland Park boundary.
    
    Args:
        tract_geojson_path: Path to the gentrification tracts GeoJSON file
        boundary_geojson_path: Path to the Highland Park boundary GeoJSON file
        output_path: Path to save the modified GeoJSON file
        tract_ids: List of tract IDs to clip (e.g., ["6037183222", "6037186203"])
    """
    # Load the tract data
    tract_data = load_geojson(tract_geojson_path)
    
    # Load the boundary data
    boundary_data = load_geojson(boundary_geojson_path)
    
    # Find the Highland Park boundary polygon
    hp_boundary_feature = boundary_data['features'][0]
    hp_boundary_geom = shape(hp_boundary_feature['geometry'])
    
    # Process each specified tract
    modified_tracts = []
    for tract_id in tract_ids:
        found = False
        for feature in tract_data['features']:
            if feature['properties'].get('tract_id') == tract_id:
                print(f"Found tract {tract_id}")
                found = True
                
                # Get the tract polygon
                tract_geom = shape(feature['geometry'])
                
                # Clip the tract to the Highland Park boundary using intersection
                # This will create a polygon that only includes the parts inside Highland Park
                clipped_geom = tract_geom.intersection(hp_boundary_geom)
                
                # Convert back to GeoJSON format
                if clipped_geom.is_empty:
                    print(f"Warning: Intersection is empty for tract {tract_id}")
                    continue
                
                # Handle different geometry types (Polygon, MultiPolygon, etc.)
                if clipped_geom.geom_type == 'Polygon':
                    # Single polygon
                    coords = [list(clipped_geom.exterior.coords)]
                    # Add holes if any
                    for interior in clipped_geom.interiors:
                        coords.append(list(interior.coords))
                    
                    feature['geometry'] = {
                        'type': 'Polygon',
                        'coordinates': coords
                    }
                elif clipped_geom.geom_type == 'MultiPolygon':
                    # Multiple polygons - take the largest one
                    polygons = list(clipped_geom.geoms)
                    largest = max(polygons, key=lambda p: p.area)
                    coords = [list(largest.exterior.coords)]
                    for interior in largest.interiors:
                        coords.append(list(interior.coords))
                    
                    feature['geometry'] = {
                        'type': 'Polygon',
                        'coordinates': coords
                    }
                else:
                    print(f"Warning: Unexpected geometry type: {clipped_geom.geom_type}")
                    continue
                
                print(f"Successfully clipped tract {tract_id} to Highland Park boundary")
                modified_tracts.append(tract_id)
                break
        
        if not found:
            print(f"Error: Tract {tract_id} not found in the GeoJSON file")
    
    if not modified_tracts:
        print("Error: No tracts were modified")
        return False
    
    # Save the modified data
    save_geojson(tract_data, output_path)
    print(f"Saved modified GeoJSON to {output_path}")
    print(f"Successfully clipped {len(modified_tracts)} tract(s): {', '.join(modified_tracts)}")
    return True

if __name__ == "__main__":
    import sys
    
    tract_file = "public/highland_park_gentrification_tracts.geojson"
    boundary_file = "public/highland_park_only.geojson"
    output_file = "public/highland_park_gentrification_tracts.geojson"
    
    # List of tract IDs to clip
    tract_ids_to_clip = ["6037183222", "6037186203", "6037183402", "6037185100", "6037199400"]
    
    success = clip_tract_to_boundary(
        tract_file,
        boundary_file,
        output_file,
        tract_ids=tract_ids_to_clip
    )
    
    if success:
        print(f"✅ Successfully clipped {len(tract_ids_to_clip)} tract(s) to Highland Park boundary")
    else:
        print("❌ Failed to clip tracts")
        sys.exit(1)

