# Implementation Steps: Highland Park Gentrification Map Visualization

## Overview
This document outlines all the steps involved in building the interactive map visualization that displays gentrification data, zoning information, and commercial building prices for Highland Park, Los Angeles.

---

## Phase 1: Project Setup & Infrastructure

### 1.1 Vue.js Application Setup
- ✅ Created Vue 3 application with Vite as the build tool
- ✅ Set up project structure with component-based architecture
- ✅ Installed core dependencies:
  - `vue` (^3.4.21) - Frontend framework
  - `leaflet` (^1.9.4) - Map library
  - `d3` (^7.9.0) - Data visualization and SVG manipulation
  - `@turf/turf` (^7.3.1) - Spatial analysis library

### 1.2 Map Container Setup
- ✅ Created main map component (`GentrificationMap.vue`)
- ✅ Initialized Leaflet map centered on Highland Park coordinates [34.115, -118.188]
- ✅ Configured map bounds (minZoom: 13, maxZoom: 18)
- ✅ Added CartoDB Positron base map for clean, minimal aesthetic

---

## Phase 2: Highland Park Boundary & Masking

### 2.1 Boundary Data
- ✅ Obtained Highland Park boundary GeoJSON data (`highland_park_only.geojson`)
- ✅ Loaded boundary data on map initialization
- ✅ Set map bounds to lock view to Highland Park area

### 2.2 Visual Masking Implementation
- ✅ Created D3.js SVG overlay to mask everything outside Highland Park
- ✅ Implemented dynamic mask update on zoom/pan events
- ✅ Used gray overlay (#8a8a8a at 97% opacity) to hide areas outside boundary
- ✅ Added responsive mask that updates with map movement

---

## Phase 3: Gentrification Tract Data Extraction & Processing

### 3.1 Data Extraction from HTML Widget
- ✅ Created Python script (`scripts/extract_tracts.py`) to extract GeoJSON from embedded HTML
- ✅ Parsed complex JSON structure in `highland-park_udp.html`
- ✅ Extracted:
  - Polygon coordinates (converted from lng/lat objects to GeoJSON format)
  - Typology labels (e.g., "Advanced Gentrification", "Stable Moderate/Mixed Income")
  - Color codes for each tract
  - Popup HTML content with demographic data
- ✅ Generated `highland_park_gentrification_tracts.geojson` file

### 3.2 Tract Filtering & Customization
- ✅ Created `GentrificationTractsLayer.vue` component to display tracts
- ✅ Implemented filtering mechanism to exclude specific tracts:
  - Removed tracts: 6037185202, 6037183702, 6037181600, 6037480600, 6037463800, 6037199300, 6037181500, 6037199000
- ✅ Styled tracts as outlines only (no fill, weight: 2)
- ✅ Added popup information showing typology and tract ID

### 3.3 Geometric Adjustments
- ✅ Created `scripts/clip_tract_to_boundary.py` to clip tracts to Highland Park boundary
- ✅ Used Shapely library for geometric intersection operations
- ✅ Clipped specific tracts to "hug" the boundary outline:
  - 6037183222, 6037186203, 6037183402, 6037185100, 6037199400
- ✅ Created restoration script for undoing changes when needed

---

## Phase 4: Zoning Layer Integration

### 4.1 Zoning Data Preparation
- ✅ Loaded Highland Park zoning data (`highland_park_zoning.json`)
- ✅ Filtered to show only residential zones:
  - Single Family Residential
  - Multiple Family Residential / Multifamily Residential

### 4.2 Spatial Analysis & Typology Mapping
- ✅ Loaded gentrification tract data in `ZoningLayer.vue`
- ✅ Implemented spatial intersection using Turf.js:
  - Used `turf.intersect()` for polygon intersection
  - Used `turf.booleanPointInPolygon()` with centroid as fallback
- ✅ Mapped each residential zone to its intersecting gentrification typology
- ✅ Stored typology mapping in feature properties for popup display

### 4.3 Color Gradient Implementation
- ✅ Created blue gradient for Single Family Residential:
  - Stable Moderate/Mixed Income: #E3F2FD (very light blue)
  - Low-Income/Susceptible to Displacement: #90CAF9 (light blue)
  - Early/Ongoing Gentrification: #42A5F5 (medium-light blue)
  - Advanced Gentrification: #1E88E5 (medium blue)
  - Becoming Exclusive: #0D47A1 (very dark blue)
- ✅ Created purple gradient for Multifamily Residential:
  - Stable Moderate/Mixed Income: #F3E5F5 (very light purple)
  - Low-Income/Susceptible to Displacement: #CE93D8 (light purple)
  - Early/Ongoing Gentrification: #AB47BC (medium-light purple)
  - Advanced Gentrification: #7B1FA2 (medium-dark purple)
  - Becoming Exclusive: #4A148C (very dark purple)
- ✅ Applied colors dynamically based on intersecting typology

### 4.4 Visual Enhancements
- ✅ Increased fill opacity to 0.9 for better color saturation and visibility
- ✅ Implemented hover effects:
  - Black outline (weight: 3) on hover
  - Maintains fill opacity for consistent color visibility
- ✅ Added interactive popups showing:
  - Zoning category
  - Zone code
  - Associated gentrification typology

---

## Phase 5: Commercial Buildings Layer

### 5.1 Building Footprint Data
- ✅ Integrated building footprint GeoJSON data
- ✅ Loaded commercial buildings with price data (`highland_park_commercial_buildings_with_prices.geojson`)
- ✅ Created `BuildingsWithPricesLayer.vue` component

### 5.2 Price Categorization
- ✅ Implemented color coding based on Yelp price levels:
  - $ (Inexpensive): Green (#4CAF50)
  - $$ (Moderate): Yellow (#FFEB3B)
  - $$$ (Expensive): Orange (#F57C00)
  - $$$$ (Very Expensive): Red (#F44336)
  - N/A: Gray (#cccccc)
- ✅ Added popup information for each building

---

## Phase 6: Layer Controls & Interactivity

### 6.1 Custom Layer Toggle Controls
- ✅ Created checkbox-based layer controls in top-right corner
- ✅ Implemented toggle functionality for:
  - Show Zoning
  - Gentrification Tracts
  - Commercial Buildings
- ✅ Used Vue reactive refs to manage layer visibility state

### 6.2 Layer Visibility Management
- ✅ Implemented `watch` functions to handle layer add/remove
- ✅ Ensured proper cleanup when toggling layers off
- ✅ Prevented duplicate layers on re-activation

---

## Phase 7: Legend Implementation

### 7.1 Split Legend Design
- ✅ Created split legend layout:
  - **Right side**: Zoning typology gradients (blue and purple)
  - **Left side**: Gentrification typology outlines + Commercial building price categories
- ✅ Positioned legends with proper spacing:
  - Zoning legend: `bottom: 100px, right: 20px`
  - Other legends: `bottom: 80px, left: 20px`

### 7.2 Legend Content
- ✅ Zoning legend shows both gradient scales:
  - Single Family Residential (Blue gradient) - 5 typology levels
  - Multifamily Residential (Purple gradient) - 5 typology levels
- ✅ Gentrification legend shows outline colors for 5 typology categories
- ✅ Price legend shows 4 price levels + N/A

---

## Phase 8: UI/UX Enhancements

### 8.1 Base Map Selection
- ✅ Changed from OpenStreetMap to CartoDB Positron for cleaner appearance
- ✅ Minimal style reduces visual clutter

### 8.2 Color Saturation Improvements
- ✅ Increased zoning color saturation from 0.65 to 0.9 fill opacity
- ✅ Colors remain visible at all times (not just on hover)
- ✅ Hover shows black outline instead of changing fill

### 8.3 Visual Polish
- ✅ Added Highland Park location info box (bottom-right)
- ✅ Styled all controls with consistent design:
  - White background
  - Rounded corners
  - Box shadows
  - Proper z-index layering

---

## Phase 9: Data Processing Scripts

### 9.1 Python Scripts Created
1. **`extract_tracts.py`**
   - Extracts GeoJSON from HTML widget
   - Parses complex nested JSON structure
   - Generates clean GeoJSON output

2. **`clip_tract_to_boundary.py`**
   - Clips tracts to Highland Park boundary using Shapely
   - Handles MultiPolygon results
   - Preserves tract properties

3. **`restore_tract_geometry.py`**
   - Restores original tract geometry from HTML source
   - Useful for undoing clipping operations

---

## Technical Architecture

### Component Structure
```
GentrificationMap.vue (Main container)
├── ZoningLayer.vue (Residential zones with gradient colors)
├── GentrificationTractsLayer.vue (Tract outlines)
├── BuildingsWithPricesLayer.vue (Commercial buildings)
└── Legend.vue (Split legend components)
```

### Key Technologies
- **Vue 3 Composition API**: Reactive state management
- **Leaflet**: Map rendering and interaction
- **D3.js**: SVG masking and projections
- **Turf.js**: Spatial analysis (intersection, point-in-polygon)
- **Shapely (Python)**: Geometric operations for data preprocessing

### Data Flow
1. GeoJSON files loaded from `/public` directory
2. Gentrification tracts loaded and filtered
3. Spatial analysis performed to map zones to typologies
4. Colors assigned based on typology mapping
5. Layers rendered with interactive features
6. User interactions trigger layer visibility changes

---

## Key Features Implemented

✅ **Interactive Map Layers**
- Toggleable zoning layer with gentrification-based coloring
- Toggleable gentrification tract outlines
- Toggleable commercial building footprints with price colors

✅ **Spatial Analysis**
- Automatic mapping of zones to gentrification typologies
- Boundary clipping for specific tracts
- Centroid-based fallback for intersection failures

✅ **Color Encoding**
- Blue gradient for Single Family Residential
- Purple gradient for Multifamily Residential
- 5-level typology scale for each residential type
- Price-based colors for commercial buildings

✅ **User Interface**
- Custom checkbox controls for layer toggling
- Split legend layout (zoning right, others left)
- Interactive popups with detailed information
- Hover effects with black outline highlighting
- Highland Park boundary masking

✅ **Data Processing**
- Python scripts for data extraction and manipulation
- Filtered tract display (excluded 8 specific tracts)
- Custom geometric adjustments

---

## File Structure

```
project-team13/
├── src/
│   ├── components/
│   │   ├── GentrificationMap.vue      # Main map container
│   │   ├── ZoningLayer.vue            # Residential zones with gradients
│   │   ├── GentrificationTractsLayer.vue  # Tract outlines
│   │   ├── BuildingsWithPricesLayer.vue   # Commercial buildings
│   │   └── Legend.vue                 # Split legend components
│   └── App.vue                        # Root component
├── public/
│   ├── highland_park_only.geojson     # Boundary data
│   ├── highland_park_zoning.json      # Zoning data
│   ├── highland_park_gentrification_tracts.geojson  # Tract data
│   └── highland_park_commercial_buildings_with_prices.geojson
├── scripts/
│   ├── extract_tracts.py              # Extract data from HTML
│   ├── clip_tract_to_boundary.py      # Clip tracts to boundary
│   └── restore_tract_geometry.py      # Restore original geometry
└── package.json                       # Dependencies
```

---

## Summary

The implementation involved multiple phases:
1. **Setup**: Vue.js application with mapping libraries
2. **Data Processing**: Extracting and preparing GeoJSON data
3. **Spatial Analysis**: Mapping zones to gentrification typologies
4. **Visualization**: Color gradients, layers, and interactivity
5. **UI/UX**: Legends, controls, and visual enhancements

The result is a comprehensive, interactive map visualization that effectively communicates the relationship between zoning, gentrification, and commercial development in Highland Park, Los Angeles.

