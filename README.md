# Dasymetric Disaggregation of Gentrification Map (Highland Park, CA)

Interactive map visualization showing gentrification typology, residential zoning, and business price level indicators for Highland Park, Los Angeles.

[Live Demo]([https://liuxintong1.github.io/project-team13-Xintong/](https://liuxintong1.github.io/project-team13-Xintong/)) | [Video](https://www.youtube.com/watch?v=x0_6Q_OOnRM)

## Overview

Conventional gentrification maps rely on census tract-level typologies, which obscure within-neighborhood variation and limit analysis of how displacement pressures differ across land-use contexts. To address this, we redistribute tract-level classifications onto parcel-level zoning geometries and integrate commercial building data in a multi-layer visualization.

## Key Features

- **Dasymetric disaggregation at parcel zoning scale** — Tract-level gentrification typologies are redistributed onto residential zoning polygons (maximum-overlap assignment from tract–zoning intersection), so patterns that are washed out in choropleth maps appear at a finer spatial grain within Highland Park.
- **Unified multi-layer map** — A single Leaflet view combines (1) residential zoning colored by merged typology, (2) census tract outlines for context, and (3) commercial building footprints with a price-level indicator, so housing-related signals and business price level can be read together.
- **Interactive exploration** — Toggle layers on or off, use popups and hover styling for parcels and buildings, and consult split legends that encode zoning gradients, tract categories, and commercial price bins.

## Tech stack

- **Vue 3** — Frontend framework
- **Vite** — Build tool and dev server
- **Bootstrap 5.3** — UI styling and responsive layout
- **Leaflet** — Interactive basemap and layer rendering
- **Turf.js** — Client-side geospatial operations (e.g., intersections and spatial joins)

## How to run

First, clone this repository and move into the project folder (use your fork’s URL if applicable):

```bash
git clone https://github.com/liuxintong1/Dasymetric-Gentrification-Map-of-Highland-Park.git
cd Dasymetric-Gentrification-Map-of-Highland-Park
```

**Install dependencies**

```bash
npm install
```

**Development** (runs at `http://localhost:3000`)

```bash
npm run dev
```

**Production build** 

```bash
npm run build
```

**Preview production build locally**

```bash
npm run preview
```

## Project structure

The **Vue** app lives under `src/`: `main.js` bootstraps the app, `App.vue` wraps the layout, and `GentrificationMap.vue` owns the Leaflet instance, max-bounds to Highland Park, and the layer checkboxes. Each major map concern is a child component (`ZoningLayer`, `GentrificationTractsLayer`, `BuildingsWithPricesLayer`, `Legend`). Global map styling is in `src/assets/map.css`.

`**public/`** holds GeoJSON (and any other static files) loaded at runtime via `fetch` and `import.meta.env.BASE_URL`—for example the neighborhood mask, zoning-derived features, tract outlines, and commercial buildings with price attributes. These files are copied as-is into the production build.

`**scripts/**` contains Python utilities used to prepare or enrich data (e.g., clipping tracts, Yelp-related helpers); they are not executed by the web app itself.

`**highland-park/**` stores reference materials from the Urban Displacement Project–style workflow (e.g., standalone HTML exports) and extra GeoJSON copies; the interactive app primarily relies on the curated files under `public/`.

```
Dasymetric-Gentrification-Map-of-Highland-Park/
├── index.html                    # Vite entry HTML
├── vite.config.js                # Base path, dev server (port 3000), build output
├── package.json
├── src/
│   ├── main.js                   # App bootstrap
│   ├── App.vue                   # Root shell (imports global CSS)
│   ├── assets/
│   │   └── map.css               # Shared Leaflet / layout styles
│   └── components/
│       ├── GentrificationMap.vue # Leaflet map, bounds, layer toggles, UI chrome
│       ├── ZoningLayer.vue       # Residential zones + gentrification-linked symbology
│       ├── GentrificationTractsLayer.vue  # Tract boundaries / typology context
│       ├── BuildingsWithPricesLayer.vue   # Commercial footprints + price styling & popups
│       └── Legend.vue            # Legends for zoning, tracts, and commercial layers
├── public/                       # Served at site root; paths use BASE_URL for GitHub Pages
│   ├── highland_park_only.geojson
│   ├── highland_park_gentrification_tracts.geojson
│   ├── highland_park_commercial_buildings_footprint.geojson
│   └── highland_park_commercial_buildings_with_prices.geojson
├── scripts/                      # Offline Python data prep (not run by npm)
│   ├── clip_tract_to_boundary.py
│   ├── extract_tracts.py
│   ├── fetch_yelp_prices.py
│   ├── restore_tract_geometry.py
│   └── test_yelp_api.py
├── highland-park/                # Reference UDP HTML bundle + auxiliary GeoJSON
└── .github/workflows/            # Optional GitHub Pages deploy workflows
```

## Datasets used


| Name                                                                                                                                                                                                      | Description                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **[Urban Displacement Project, 2021](https://www.urbandisplacement.org/maps/los-angeles-gentrification-and-displacement/)**                                                                               | Census tract–level displacement typology for Los Angeles County.                                                                                                               |
| **[Residential zoning](https://geohub.lacity.org/datasets/f2b84d74972a4084aac79fbe504d9b11_15/explore?location=34.084007%2C-118.186365%2C15)**                                                            | Parcel-level zoning used to separate single-family vs. multifamily residential areas.                                                                                          |
| **[Building footprints](https://geohub.lacity.org/datasets/813fcefde1f64b209103107b26a8909f_0/explore?location=34.018387%2C-118.410168%2C10) and business price level** (LA City GeoHub; Yelp Fusion API) | Commercial building geometries from the city; each building linked to a price-level indicator derived from Yelp Fusion to approximate how expensive associated businesses are. |
| **[Neighborhood boundary](https://geohub.lacity.org/datasets/d6c55385a0e749519f238b77135eafac_0/explore?location=34.020728%2C-118.410084%2C10/)**                                                         | Highland Park polygon from LA Times neighborhood boundaries.                                                                                                                   |


## Citation

If you use this work in your research, please cite:

> *(Add your preferred citation: course report, Zenodo DOI, or proceedings entry when available.)*

## Authors

Omar Nava, Xintong (Tracy) Liu, Chi-Fang (Joann) Cheng, and YuanYuan Xue
University of Southern California