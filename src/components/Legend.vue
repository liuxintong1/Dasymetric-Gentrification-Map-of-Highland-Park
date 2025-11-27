<script setup>
const props = defineProps({
  showZoning: {
    type: Boolean,
    default: true,
  },
  showPrice: {
    type: Boolean,
    default: true,
  },
});

// Zoning legend items
const zoningItems = [
  { name: "Single Family Residential", color: "#4A90E2" },
  { name: "Multifamily Residential", color: "#9B59B6" },
];

// Price legend items
const priceItems = [
  { level: 1, price: "$", color: "#4CAF50", label: "Inexpensive" },
  { level: 2, price: "$$", color: "#FFEB3B", label: "Moderate" },
  { level: 3, price: "$$$", color: "#F57C00", label: "Expensive" },
  { level: 4, price: "$$$$", color: "#F44336", label: "Very Expensive" },
  { level: null, price: "N/A", color: "#cccccc", label: "No price data" },
];
</script>

<template>
  <div v-if="showZoning || showPrice" class="combined-legend">
    <!-- Zoning Section -->
    <div v-if="showZoning" class="legend-section">
      <h4>Zoning</h4>
      <div class="legend-items">
        <div v-for="item in zoningItems" :key="item.name" class="legend-item">
          <div
            class="legend-color"
            :style="{ backgroundColor: item.color }"
          ></div>
          <span class="legend-label">{{ item.name }}</span>
        </div>
      </div>
    </div>

    <!-- Divider -->
    <hr v-if="showZoning && showPrice" class="legend-divider" />

    <!-- Price Section -->
    <div v-if="showPrice" class="legend-section">
      <h4>Commercial Buildings</h4>
      <div class="legend-items">
        <div v-for="item in priceItems" :key="item.level" class="legend-item">
          <div
            class="legend-color"
            :style="{ backgroundColor: item.color }"
          ></div>
          <div class="legend-text">
            <span class="price-symbols">{{ item.price }}</span>
            <span class="price-label">{{ item.label }}</span>
          </div>
        </div>
      </div>
      <div class="legend-note">
        <small>Data from Yelp Fusion API</small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.combined-legend {
  position: absolute;
  bottom: 80px;
  left: 20px;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  min-width: 220px;
  max-width: 280px;
}

.legend-section {
  margin-bottom: 0;
}

.legend-section:last-child {
  margin-bottom: 0;
}

.legend-section h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #2c3e50;
  font-weight: 600;
}

.legend-divider {
  margin: 16px 0;
  border: none;
  border-top: 1px solid #ddd;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-color {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 1px solid #666;
  flex-shrink: 0;
}

.legend-label {
  font-size: 13px;
  color: #2c3e50;
}

.legend-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.price-symbols {
  font-size: 13px;
  font-weight: bold;
  color: #2c3e50;
}

.price-label {
  font-size: 11px;
  color: #666;
}

.legend-note {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid #eee;
  text-align: center;
}

.legend-note small {
  font-size: 10px;
  color: #999;
}
</style>
