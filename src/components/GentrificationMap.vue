<script setup>
import { ref, onMounted } from "vue";
import L from "leaflet";
import ZoningLayer from "./ZoningLayer.vue";
import BuildingsWithPricesLayer from "./BuildingsWithPricesLayer.vue";
import GentrificationTractsLayer from "./GentrificationTractsLayer.vue";
import Legend from "./Legend.vue";

// Reference to the map container DOM element
const mapContainer = ref(null);
const map = ref(null);
const showZoning = ref(true);
const showPriceBuildings = ref(true);
const showGentrificationTracts = ref(true);

// Initialize the Leaflet map on component mount
onMounted(async () => {
  // Initialize Leaflet map centered on Highland Park, LA
  map.value = L.map(mapContainer.value, {
    center: [34.115, -118.188],
    zoom: 14,
    minZoom: 13,
    maxZoom: 18,
    zoomControl: true,
  });

  // Add base map tile layer - CartoDB Positron (clean, minimal style)
  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 20,
  }).addTo(map.value);

  try {
    // Load Highland Park boundary only
    const baseUrl = import.meta.env.BASE_URL;
    const response = await fetch(`${baseUrl}highland_park_only.geojson`);
    const highlandParkData = await response.json();

    // Get the bounds from Highland Park (using temporary layer for bounds calculation)
    const tempBoundaryLayer = L.geoJSON(highlandParkData);
    const bounds = tempBoundaryLayer.getBounds();

    // Set max bounds to lock the map to Highland Park only
    map.value.setMaxBounds(bounds.pad(0.1));
    map.value.options.maxBoundsViscosity = 1.0;

    // Fit the map perfectly to Highland Park
    map.value.fitBounds(bounds, { padding: [20, 20] });
  } catch (error) {
    console.error("Error loading Highland Park:", error);
    alert(
      "Error loading Highland Park boundary. Please check that highland_park_only.geojson is in the public folder."
    );
  }
});

</script>

<template>
  <div class="map-wrapper">
    <div ref="mapContainer" class="map-container"></div>

    <!-- Zoning Layer (Joann's existing layer) -->
    <ZoningLayer v-if="map" :map="map" :visible="showZoning" />

    <!-- Gentrification Tracts Layer (outlines from UDP map) -->
    <GentrificationTractsLayer
      v-if="map"
      :map="map"
      :visible="showGentrificationTracts"
    />

    <!-- Commercial Buildings WITH Price Data -->
    <BuildingsWithPricesLayer
      v-if="map"
      :map="map"
      :visible="showPriceBuildings"
    />

    <!-- Combined Legend (replaces separate legends) -->
    <Legend
      :show-zoning="showZoning"
      :show-price="showPriceBuildings"
      :show-gentrification="showGentrificationTracts"
    />

    <!-- Layer Controls -->
    <div class="layer-controls">
      <h4>Map Layers</h4>
      <label class="layer-toggle">
        <input type="checkbox" v-model="showZoning" />
        <span>Show Zoning</span>
      </label>
      <label class="layer-toggle">
        <input type="checkbox" v-model="showGentrificationTracts" />
        <span>Gentrification Tracts</span>
      </label>
      <label class="layer-toggle">
        <input type="checkbox" v-model="showPriceBuildings" />
        <span>Commercial Buildings</span>
      </label>
    </div>

    <!-- Info Badge -->
    <div class="map-info">
      <p>📍 Highland Park</p>
      <p class="map-info-sub">Los Angeles, CA</p>
    </div>
  </div>
</template>

<style scoped>
.map-wrapper {
  flex: 1;
  position: relative;
  width: 100%;
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
}

.layer-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  min-width: 200px;
}

.layer-controls h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #2c3e50;
  font-weight: 600;
}

.layer-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  font-size: 14px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.layer-toggle:last-child {
  margin-bottom: 0;
}

.layer-toggle input[type="checkbox"] {
  cursor: pointer;
  width: 16px;
  height: 16px;
}

.map-info {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.95);
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  z-index: 1000;
  pointer-events: none;
}

.map-info p {
  margin: 0;
}

.map-info-sub {
  font-size: 12px;
  font-weight: 400;
  color: #5a6c7d;
  margin-top: 4px !important;
}

:deep(.leaflet-control-container) {
  z-index: 1000;
}
</style>
