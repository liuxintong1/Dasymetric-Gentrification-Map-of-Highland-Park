<script setup>
import { ref, onMounted, watch } from "vue";
import L from "leaflet";
import * as turf from "@turf/turf";

const props = defineProps({
  map: {
    type: Object,
    required: true,
  },
  visible: {
    type: Boolean,
    default: true,
  },
});

// Blue gradient colors for Single Family Residential based on gentrification typology
// Reordered: light to dark gradient
const typologyColors = {
  "Low-Income/Susceptible to Displacement": "#E3F2FD", // Very light blue (lightest)
  "Early/Ongoing Gentrification": "#90CAF9", // Light blue
  "Advanced Gentrification": "#42A5F5", // Medium-light blue
  "Stable Moderate/Mixed Income": "#1E88E5", // Medium blue
  "Becoming Exclusive": "#0D47A1", // Very dark blue (darkest)
};

// Purple gradient colors for Multifamily Residential based on gentrification typology
// Reordered: light to dark gradient
const multifamilyTypologyColors = {
  "Low-Income/Susceptible to Displacement": "#F3E5F5", // Very light purple (lightest)
  "Early/Ongoing Gentrification": "#CE93D8", // Light purple
  "Advanced Gentrification": "#AB47BC", // Medium-light purple
  "Stable Moderate/Mixed Income": "#7B1FA2", // Medium-dark purple
  "Becoming Exclusive": "#4A148C", // Very dark purple (darkest)
};

// Mapping for display names
const categoryDisplayNames = {
  "Single Family Residential": "Single Family Residential",
  "Multiple Family Residential": "Multifamily Residential",
  "Residential Multiple Family": "Multifamily Residential",
};

let zoningLayer = null;
let gentrificationTracts = null;
let zoningTypologyMap = new Map(); // Maps zone feature IDs to typology

// Function to get display name for category
function getDisplayName(properties) {
  const category =
    properties.CATEGORY ||
    properties.category ||
    properties.ZONE_CLASS ||
    properties.zone_class ||
    "Unknown";

  return categoryDisplayNames[category] || category;
}

// Function to get the gentrification typology for a zoning feature
function getTypologyForZone(zoneFeature) {
  if (zoningTypologyMap.has(zoneFeature.properties)) {
    return zoningTypologyMap.get(zoneFeature.properties);
  }
  return null;
}

// Function to find the gentrification tract that a zone intersects with
function findIntersectingTract(zoneFeature) {
  if (!gentrificationTracts || gentrificationTracts.features.length === 0) {
    return null;
  }

  let bestMatch = null;
  let maxIntersectionArea = 0;

  for (const tract of gentrificationTracts.features) {
    try {
      // First, try to get the intersection polygon
      const intersection = turf.intersect(zoneFeature, tract);
      if (intersection) {
        const intersectionArea = turf.area(intersection);
        if (intersectionArea > maxIntersectionArea) {
          maxIntersectionArea = intersectionArea;
          bestMatch = tract;
        }
      }
    } catch (e) {
      // If intersection fails, try using the centroid of the zone to see if it's inside the tract
      try {
        const zoneCentroid = turf.centroid(zoneFeature);
        if (turf.booleanPointInPolygon(zoneCentroid, tract)) {
          const zoneArea = turf.area(zoneFeature);
          if (zoneArea > maxIntersectionArea) {
            maxIntersectionArea = zoneArea;
            bestMatch = tract;
          }
        }
      } catch (e2) {
        // Skip this tract if we can't check it
        continue;
      }
    }
  }

  return bestMatch;
}

// Style function for the zoning layer
function zoningStyle(feature) {
  const category =
    feature.properties.CATEGORY ||
    feature.properties.category ||
    feature.properties.ZONE_CLASS ||
    feature.properties.zone_class ||
    "";

  let fillColor;

  if (category === "Single Family Residential") {
    // Get typology for this zone
    const typology = getTypologyForZone(feature);
    fillColor = typology && typologyColors[typology]
      ? typologyColors[typology]
      : "#E3F2FD"; // Default to lightest blue if no typology found
  } else if (
    category === "Multiple Family Residential" ||
    category === "Residential Multiple Family"
  ) {
    // Get typology for this zone
    const typology = getTypologyForZone(feature);
    fillColor = typology && multifamilyTypologyColors[typology]
      ? multifamilyTypologyColors[typology]
      : "#F3E5F5"; // Default to lightest purple if no typology found
  } else {
    fillColor = null;
  }

  return {
    fillColor: fillColor,
    fillOpacity: 0.9, // Higher opacity for more saturation/visibility
    color: "#333",
    weight: 0.5,
    opacity: 0.8,
  };
}

// Popup content for each zone
function createPopupContent(properties) {
  const displayName = getDisplayName(properties);
  const zoneCode =
    properties.ZONE_CMPLT || properties.zone_code || properties.OBJECTID || "";

  let popupHtml = `
    <div style="font-family: Arial, sans-serif; min-width: 200px;">
      <strong style="font-size: 14px; color: #2c3e50;">Category:</strong><br>
      <span style="font-size: 13px;">${displayName}</span>
  `;

  if (zoneCode) {
    popupHtml += `
      <br><br>
      <strong style="font-size: 12px; color: #666;">Zone Code:</strong><br>
      <span style="font-size: 11px; color: #666;">${zoneCode}</span>
    `;
  }

  // Add gentrification typology if available
  const typology = properties._gentrificationTypology;
  if (typology) {
    popupHtml += `
      <br><br>
      <strong style="font-size: 12px; color: #666;">Gentrification Typology:</strong><br>
      <span style="font-size: 11px; color: #666;">${typology}</span>
    `;
  }

  popupHtml += `</div>`;

  return popupHtml;
}

// Add hover effect
function onEachFeature(feature, layer) {
  layer.bindPopup(createPopupContent(feature.properties));

  layer.on({
    mouseover: function (e) {
      const layer = e.target;
      layer.setStyle({
        color: "#000000", // Black outline on hover
        weight: 3, // Thicker outline
        opacity: 1,
        fillOpacity: 0.9, // Keep the same fill opacity as default
      });
      layer.bringToFront();
    },
    mouseout: function (e) {
      zoningLayer.resetStyle(e.target);
    },
  });
}

// Load gentrification tract data
async function loadGentrificationTracts() {
  try {
    const baseUrl = import.meta.env.BASE_URL;
    const response = await fetch(`${baseUrl}highland_park_gentrification_tracts.geojson`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    gentrificationTracts = await response.json();

    // Filter out excluded tracts (same as in GentrificationTractsLayer)
    const excludedTracts = [
      "6037185202",
      "6037183702",
      "6037181600",
      "6037480600",
      "6037463800",
      "6037199300",
      "6037181500",
      "6037199000",
      "6037186201",
    ];

    gentrificationTracts.features = gentrificationTracts.features.filter(
      (feature) => {
        const tractId = feature.properties.tract_id || "";
        return !excludedTracts.includes(tractId);
      }
    );

    console.log(
      `✅ Loaded ${gentrificationTracts.features.length} gentrification tracts for zoning overlay`
    );
    return true;
  } catch (error) {
    console.error("Error loading gentrification tracts:", error);
    return false;
  }
}

// Map zoning features to gentrification typologies
function mapZoningToGentrification(zoningData) {
  zoningTypologyMap.clear();

  if (!gentrificationTracts || gentrificationTracts.features.length === 0) {
    console.warn("No gentrification tracts available for mapping");
    return;
  }

  let mappedCount = 0;

  for (const zoneFeature of zoningData.features) {
    const category =
      zoneFeature.properties.CATEGORY ||
      zoneFeature.properties.category ||
      "";

    if (
      category === "Single Family Residential" ||
      category === "Multiple Family Residential" ||
      category === "Residential Multiple Family"
    ) {
      const intersectingTract = findIntersectingTract(zoneFeature);
      if (intersectingTract && intersectingTract.properties.typology) {
        const typology = intersectingTract.properties.typology;
        zoningTypologyMap.set(zoneFeature.properties, typology);
        zoneFeature.properties._gentrificationTypology = typology;
        mappedCount++;
      }
    }
  }

  console.log(
    `🗺️  Mapped ${mappedCount} residential zones (Single Family & Multifamily) to gentrification typologies`
  );
}

async function loadZoningData() {
  try {
    // First, load gentrification tracts
    await loadGentrificationTracts();

    let response;
    const baseUrl = import.meta.env.BASE_URL;
    const possibleFiles = [
      `${baseUrl}highland_park_zoning.geojson`,
      `${baseUrl}highland_park_zoning.json`,
      `${baseUrl}la_zoning_highland_park.geojson`,
      `${baseUrl}zoning.geojson`,
    ];

    let zoningData = null;
    for (const file of possibleFiles) {
      try {
        response = await fetch(file);
        if (response.ok) {
          zoningData = await response.json();
          console.log(`✅ Loaded zoning data from: ${file}`);
          break;
        }
      } catch (e) {
        // Continue to next file
      }
    }

    if (!zoningData) {
      throw new Error(
        "Could not find zoning data file. Tried: " + possibleFiles.join(", ")
      );
    }

    // Filter to only show our 2 residential categories
    const originalCount = zoningData.features.length;
    zoningData.features = zoningData.features.filter((feature) => {
      const category =
        feature.properties.CATEGORY || feature.properties.category || "";
      // Only keep Single Family and Multifamily Residential
      return (
        category === "Single Family Residential" ||
        category === "Multiple Family Residential" ||
        category === "Residential Multiple Family"
      );
    });

    const filtered = originalCount - zoningData.features.length;
    console.log(`   Filtered out ${filtered} zones (showing only residential)`);

    // Map Single Family Residential zones to gentrification typologies
    mapZoningToGentrification(zoningData);

    if (zoningData.features && zoningData.features.length > 0) {
      console.log(
        "Sample zoning feature properties:",
        zoningData.features[0].properties
      );
    }

    // Create the Leaflet GeoJSON layer
    zoningLayer = L.geoJSON(zoningData, {
      style: zoningStyle,
      onEachFeature: onEachFeature,
    });

    if (props.visible) {
      zoningLayer.addTo(props.map);
    }

    console.log(
      `📊 Loaded ${zoningData.features.length} zoning features (2 residential categories)`
    );
  } catch (error) {
    console.error("Error loading zoning data:", error);
    alert(
      "Could not load zoning data. Make sure highland_park_zoning.geojson (or .json) is in the public folder."
    );
  }
}

watch(
  () => props.visible,
  (visible) => {
    if (zoningLayer && props.map) {
      if (visible) {
        // Check if layer is already on the map before adding
        if (!props.map.hasLayer(zoningLayer)) {
          zoningLayer.addTo(props.map);
        }
      } else {
        // Check if layer is on the map before removing
        if (props.map.hasLayer(zoningLayer)) {
          props.map.removeLayer(zoningLayer);
        }
      }
    }
  },
  { immediate: false }
);

onMounted(() => {
  loadZoningData();
});

defineExpose({
  refresh: loadZoningData,
  layer: zoningLayer,
});
</script>

<template>
  <div style="display: none"></div>
</template>
