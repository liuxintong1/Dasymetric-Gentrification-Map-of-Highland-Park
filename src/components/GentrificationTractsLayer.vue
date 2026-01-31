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

let tractsLayer = null;

// Green-to-red gradient colors for gentrification tract outlines
const tractOutlineColors = {
  "Low-Income/Susceptible to Displacement": "#2E7D32", // Dark Green
  "Early/Ongoing Gentrification": "#689F38", // Light Green
  "Advanced Gentrification": "#FBC02D", // Amber Yellow
  "Stable Moderate/Mixed Income": "#F57C00", // Orange
  "Becoming Exclusive": "#C62828", // Dark Red
};

// Style function for tracts - outlines only
function tractStyle(feature) {
  const typology = feature.properties.typology || "";
  // Use the typology-based color, or fallback to the original color property
  const color = tractOutlineColors[typology] || feature.properties.color || "#333333";
  return {
    fillColor: color,
    fillOpacity: 0, // No fill, just outlines
    color: color,
    weight: 3, // Line width for outlines (thicker)
    opacity: 0.8,
  };
}

// Popup content for each tract
function createPopupContent(properties) {
  const typology = properties.typology || "Unknown";
  const tractId = properties.tract_id || "";

  let popupHtml = `
    <div style="font-family: Arial, sans-serif; min-width: 200px;">
      <strong style="font-size: 14px; color: #2c3e50;">Typology:</strong><br>
      <span style="font-size: 13px;">${typology}</span>
  `;

  if (tractId) {
    popupHtml += `
      <br><br>
      <strong style="font-size: 12px; color: #666;">Tract ID:</strong><br>
      <span style="font-size: 11px; color: #666;">${tractId}</span>
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
        weight: 5, // Even thicker on hover
        opacity: 1,
      });
      layer.bringToFront();
    },
    mouseout: function (e) {
      tractsLayer.resetStyle(e.target);
    },
  });
}

async function loadTractData() {
  try {
    const baseUrl = import.meta.env.BASE_URL;
    const response = await fetch(`${baseUrl}highland_park_gentrification_tracts.geojson`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const tractData = await response.json();

    if (!tractData.features || tractData.features.length === 0) {
      throw new Error("No features found in tract data");
    }

    // Tracts to exclude
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

    // Filter out excluded tracts
    const originalCount = tractData.features.length;
    tractData.features = tractData.features.filter((feature) => {
      const tractId = feature.properties.tract_id || "";
      return !excludedTracts.includes(tractId);
    });

    const filteredCount = originalCount - tractData.features.length;
    if (filteredCount > 0) {
      console.log(
        `🚫 Filtered out ${filteredCount} tract(s): ${excludedTracts.join(", ")}`
      );
    }

    console.log(`✅ Loaded ${tractData.features.length} gentrification tracts`);

    // Create the Leaflet GeoJSON layer
    tractsLayer = L.geoJSON(tractData, {
      style: tractStyle,
      onEachFeature: onEachFeature,
    });

    if (props.visible) {
      tractsLayer.addTo(props.map);
    }

    console.log(
      `📊 Loaded ${tractData.features.length} gentrification tract outlines`
    );
  } catch (error) {
    console.error("Error loading gentrification tract data:", error);
    alert(
      "Could not load gentrification tract data. Make sure highland_park_gentrification_tracts.geojson is in the public folder."
    );
  }
}

watch(
  () => props.visible,
  (visible) => {
    if (tractsLayer) {
      if (visible) {
        tractsLayer.addTo(props.map);
      } else {
        props.map.removeLayer(tractsLayer);
      }
    }
  }
);

onMounted(() => {
  loadTractData();
});

defineExpose({
  refresh: loadTractData,
  layer: tractsLayer,
});
</script>

<template>
  <div style="display: none"></div>
</template>

