<script setup>
import { ref, onMounted, watch } from "vue";
import L from "leaflet";

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

// Simplified zoning color scheme - 2 categories only
const categoryColors = {
  "Single Family Residential": "#4A90E2", // Blue
  "Multiple Family Residential": "#9B59B6", // Purple
  "Residential Multiple Family": "#9B59B6", // Purple (alternate name)
  default: null, // Will be filtered out
};

// Mapping for display names
const categoryDisplayNames = {
  "Single Family Residential": "Single Family Residential",
  "Multiple Family Residential": "Multifamily Residential",
  "Residential Multiple Family": "Multifamily Residential",
};

let zoningLayer = null;

// Function to get color based on category
function getCategoryColor(properties) {
  const category =
    properties.CATEGORY ||
    properties.category ||
    properties.ZONE_CLASS ||
    properties.zone_class ||
    "";

  return categoryColors[category] || categoryColors["default"];
}

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

// Style function for the zoning layer
function zoningStyle(feature) {
  return {
    fillColor: getCategoryColor(feature.properties),
    fillOpacity: 0.65,
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
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85,
      });
      layer.bringToFront();
    },
    mouseout: function (e) {
      zoningLayer.resetStyle(e.target);
    },
  });
}

async function loadZoningData() {
  try {
    let response;
    const possibleFiles = [
      "/highland_park_zoning.geojson",
      "/highland_park_zoning.json",
      "/la_zoning_highland_park.geojson",
      "/zoning.geojson",
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
    if (zoningLayer) {
      if (visible) {
        zoningLayer.addTo(props.map);
      } else {
        props.map.removeLayer(zoningLayer);
      }
    }
  }
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
