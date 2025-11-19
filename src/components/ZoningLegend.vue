<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: true
  }
})

const collapsed = ref(false)

// Updated to match the actual CATEGORY field values
const categoryItems = [
  { color: '#FFFFE0', label: 'Single Family Residential' },
  { color: '#FFD700', label: 'Multiple Family Residential' },
  { color: '#8B4513', label: 'Residential-Mixed' },
  { color: '#FF6B6B', label: 'Commercial' },
  { color: '#C71585', label: 'Commercial-Mixed' },
  { color: '#87CEEB', label: 'Manufacturing' },
  { color: '#4682B4', label: 'Industrial' },
  { color: '#800020', label: 'Industrial-Mixed' },
  { color: '#8B008B', label: 'Hybrid Industrial' },
  { color: '#7CFC00', label: 'Public Facilities' },
  { color: '#32CD32', label: 'Public' },
  { color: '#E0FFE0', label: 'Suburban' },
  { color: '#98FB98', label: 'Open Space' },
  { color: '#D3D3D3', label: 'Parking' },
  { color: '#90EE90', label: 'Agricultural' },
  { color: '#B0B0B0', label: 'Freeway' }
]
</script>

<template>
  <div v-if="visible" class="zoning-legend" :class="{ collapsed }">
    <div class="legend-header" @click="collapsed = !collapsed">
      <h3>Zoning Category</h3>
      <button class="toggle-btn">{{ collapsed ? '▼' : '▲' }}</button>
    </div>
    
    <div v-show="!collapsed" class="legend-content">
      <div 
        v-for="item in categoryItems" 
        :key="item.label"
        class="legend-item"
      >
        <div 
          class="color-box" 
          :style="{ backgroundColor: item.color }"
        ></div>
        <span class="label">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.zoning-legend {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-width: 250px;
  z-index: 1000;
  font-family: Arial, sans-serif;
}

.legend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin-bottom: 10px;
}

.legend-header h3 {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
  font-weight: 600;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 12px;
  cursor: pointer;
  padding: 4px;
  color: #666;
}

.toggle-btn:hover {
  color: #2c3e50;
}

.legend-content {
  max-height: 500px;
  overflow-y: auto;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 10px;
}

.color-box {
  width: 24px;
  height: 16px;
  border: 1px solid #333;
  border-radius: 3px;
  flex-shrink: 0;
}

.label {
  font-size: 13px;
  color: #333;
  line-height: 1.3;
}

.collapsed .legend-content {
  display: none;
}

/* Scrollbar styling for legend content */
.legend-content::-webkit-scrollbar {
  width: 6px;
}

.legend-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.legend-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.legend-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>