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

let buildingsLayer = null;

// Style function for building footprints
function buildingStyle(feature) {
  return {
    fillColor: "#FF6B6B", // Red/coral color for commercial buildings
    fillOpacity: 0.6,
    color: "#d63031", // Darker red border
    weight: 1,
    opacity: 0.9,
  };
}

// Create popup content for each building
function createPopupContent(properties) {
  const height = properties.HEIGHT
    ? `${properties.HEIGHT.toFixed(2)} ft`
    : "N/A";
  const area = properties.AREA
    ? `${properties.AREA.toLocaleString()} sq ft`
    : "N/A";
  const buildingId = properties.BLD_ID || properties.OBJECTID || "Unknown";
  const status = properties.STATUS || "N/A";
  const year = properties.LARIAC_DATE || "N/A";

  return `
    <div style="font-family: Arial, sans-serif; min-width: 220px;">
      <strong style="font-size: 14px; color: #2c3e50;">Commercial Building</strong>
      <hr style="margin: 8px 0; border: none; border-top: 1px solid #ddd;">
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Building ID:</strong><br>
        <span style="font-size: 11px;">${buildingId}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Height:</strong>
        <span style="font-size: 11px; float: right;">${height}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Area:</strong>
        <span style="font-size: 11px; float: right;">${area}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Status:</strong>
        <span style="font-size: 11px; float: right;">${status}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Data Year:</strong>
        <span style="font-size: 11px; float: right;">${year}</span>
      </div>
    </div>
  `;
}

// Add hover effects and popup
function onEachFeature(feature, layer) {
  // Popup on click
  layer.bindPopup(createPopupContent(feature.properties));

  // Hover effect
  layer.on({
    mouseover: function (e) {
      const layer = e.target;
      layer.setStyle({
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85,
        fillColor: "#e74c3c", // Brighter red on hover
      });
      layer.bringToFront();
    },
    mouseout: function (e) {
      buildingsLayer.resetStyle(e.target);
    },
  });
}

async function loadBuildingData() {
  try {
    console.log("🏢 Loading commercial building footprints...");

    const response = await fetch(
      "/highland_park_commercial_buildings_footprint.geojson"
    );

    if (!response.ok) {
      throw new Error(
        `Failed to load: ${response.status} ${response.statusText}`
      );
    }

    const buildingData = await response.json();

    // Log first feature to see available fields
    if (buildingData.features && buildingData.features.length > 0) {
      console.log(
        "Sample building feature properties:",
        buildingData.features[0].properties
      );
    }

    // Create the Leaflet GeoJSON layer
    buildingsLayer = L.geoJSON(buildingData, {
      style: buildingStyle,
      onEachFeature: onEachFeature,
    });

    // Add to map if visible
    if (props.visible) {
      buildingsLayer.addTo(props.map);
    }

    console.log(
      `✅ Loaded ${buildingData.features.length} commercial building footprints`
    );
  } catch (error) {
    console.error("❌ Error loading commercial building data:", error);
    alert(
      "Could not load commercial building footprints. Make sure highland_park_commercial_buildings_footprint.geojson is in the public folder."
    );
  }
}

// Watch visibility prop to show/hide layer
watch(
  () => props.visible,
  (visible) => {
    if (buildingsLayer) {
      if (visible) {
        buildingsLayer.addTo(props.map);
      } else {
        props.map.removeLayer(buildingsLayer);
      }
    }
  }
);

onMounted(() => {
  loadBuildingData();
});

// Expose methods for parent component
defineExpose({
  refresh: loadBuildingData,
  layer: buildingsLayer,
});
</script>

<template>
  <!-- This component has no visual template - it only adds layers to the map -->
  <div style="display: none"></div>
</template>
