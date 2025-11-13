<template>
  <div class="temporal-map-container">
    <!-- Map Container -->
    <div ref="mapContainer" class="map-container"></div>

    <!-- Temporal Controls -->
    <div class="controls-panel">
      <div class="year-display">
        <h3>Year: {{ currentYear }}</h3>
      </div>

      <div class="slider-container">
        <label for="year-slider">Timeline (2015-2022)</label>
        <input
          id="year-slider"
          v-model.number="currentYear"
          type="range"
          min="2015"
          max="2022"
          step="1"
          class="year-slider"
        />
        <div class="year-labels">
          <span>2015</span>
          <span>2022</span>
        </div>
      </div>

      <div class="playback-controls">
        <button @click="togglePlayback" class="play-button">
          {{ isPlaying ? '⏸ Pause' : '▶ Play' }}
        </button>
        <button @click="resetYear" class="reset-button">
          ↺ Reset
        </button>
      </div>

      <!-- NEW: Selection Info -->
      <div v-if="selectedZipCode" class="selection-info">
        <span class="selected-zip">ZIP {{ selectedZipCode }} selected</span>
        <button @click="clearSelection" class="clear-button">✕ Clear</button>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend-panel">
      <div class="legend-section">
        <h4>Housing Costs</h4>
        <div class="color-scale">
          <div class="scale-gradient housing-gradient"></div>
          <div class="scale-labels">
            <span>Affordable</span>
            <span>Expensive</span>
          </div>
        </div>
      </div>

      <div class="legend-section">
        <h4>Business Density</h4>
        <div class="pattern-examples">
          <div class="pattern-item">
            <svg width="40" height="40">
              <defs>
                <pattern id="legend-low" patternUnits="userSpaceOnUse" width="20" height="20">
                  <path d="M 0 10 L 20 10" stroke="#000" stroke-width="1.5" opacity="0.4"/>
                </pattern>
              </defs>
              <rect width="40" height="40" fill="url(#legend-low)"/>
            </svg>
            <span>Low (0-50)</span>
          </div>
          <div class="pattern-item">
            <svg width="40" height="40">
              <defs>
                <pattern id="legend-med" patternUnits="userSpaceOnUse" width="12" height="12">
                  <path d="M 0 6 L 12 6" stroke="#000" stroke-width="1.5" opacity="0.5"/>
                </pattern>
              </defs>
              <rect width="40" height="40" fill="url(#legend-med)"/>
            </svg>
            <span>Medium (50-150)</span>
          </div>
          <div class="pattern-item">
            <svg width="40" height="40">
              <defs>
                <pattern id="legend-high" patternUnits="userSpaceOnUse" width="8" height="8">
                  <path d="M 0 4 L 8 4" stroke="#000" stroke-width="1.5" opacity="0.7"/>
                  <path d="M 4 0 L 4 8" stroke="#000" stroke-width="1.5" opacity="0.7"/>
                </pattern>
              </defs>
              <rect width="40" height="40" fill="url(#legend-high)"/>
            </svg>
            <span>High (150+)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading data...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import mapboxgl from 'mapbox-gl'
import * as d3 from 'd3'
import 'mapbox-gl/dist/mapbox-gl.css'

// ==================== Props & Emits ====================
const props = defineProps({
  // Optional prop to sync year from parent component
  currentYear: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['year-change', 'zip-selected'])

// ==================== Configuration ====================
const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN
mapboxgl.accessToken = MAPBOX_TOKEN

const LA_CENTER = [-118.2437, 34.0522]
const INITIAL_ZOOM = 9

// ==================== State Management ====================
const mapContainer = ref(null)
const map = ref(null)
// Initialize with prop value if provided, otherwise default to 2015
const currentYear = ref(props.currentYear || 2015)
const isLoading = ref(true)
const isPlaying = ref(false)
const processedMapData = ref({})
const geoJsonData = ref(null)
const selectedZipCode = ref(null)

let playbackInterval = null
let overlayCanvas = null
let overlayContext = null

// ==================== Data Loading Functions ====================

async function loadGeoJSON() {
  try {
    const response = await fetch('/data/la_zip_codes.json')
    const data = await response.json()
    console.log('Loaded GeoJSON features:', data.features.length)
    return data
  } catch (error) {
    console.error('Error loading GeoJSON:', error)
    return { type: 'FeatureCollection', features: [] }
  }
}

async function loadProcessedData() {
  try {
    console.log('Loading pre-processed temporal data...')
    const response = await fetch('/data/processed_temporal_data.json')
    const data = await response.json()
    console.log('✓ Loaded processed data for', Object.keys(data).length, 'ZIP codes')
    return data
  } catch (error) {
    console.error('Error loading processed data:', error)
    console.warn('Falling back to on-demand processing...')
    return null
  }
}

// ==================== Data Processing ====================

// Data is now pre-processed. See scripts/processData.js for processing logic.

// ==================== Map Initialization ====================

function initializeMap() {
  if (!mapContainer.value) return

  map.value = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: LA_CENTER,
    zoom: INITIAL_ZOOM,
    pitch: 0,
    bearing: 0
  })

  map.value.on('load', () => {
    console.log('Map loaded successfully')
    setupMapLayers()
    createOverlayCanvas()
  })

  // Add navigation controls
  map.value.addControl(new mapboxgl.NavigationControl(), 'top-right')
}

function setupMapLayers() {
  if (!map.value || !geoJsonData.value) return

  // Add feature IDs if they don't exist
  const geoJsonWithIds = {
    ...geoJsonData.value,
    features: geoJsonData.value.features.map((feature, index) => ({
      ...feature,
      id: feature.id || index  // Use existing id or create from index
    }))
  }

  // Add ZIP code boundaries source
  map.value.addSource('zip-codes', {
    type: 'geojson',
    data: geoJsonWithIds,  // Use the version with IDs
    generateId: true  // Tell Mapbox to generate IDs if missing
  })

  // Add housing cost choropleth layer
  map.value.addLayer({
    id: 'housing-choropleth',
    type: 'fill',
    source: 'zip-codes',
    paint: {
      'fill-color': '#3182bd',
      'fill-opacity': 0.7
    }
  })

  // Add ZIP code boundaries
  map.value.addLayer({
    id: 'zip-boundaries',
    type: 'line',
    source: 'zip-codes',
    paint: {
      'line-color': '#ffffff',
      'line-width': 1.5,
      'line-opacity': 0.8
    }
  })

  // Add hover interactions
  setupMapInteractions()

  // Initial render
  updateMap(currentYear.value)
}

function setupMapInteractions() {
  let hoveredZipId = null
  let popup = null

  map.value.on('mousemove', 'housing-choropleth', (e) => {
    if (e.features.length > 0) {
      if (hoveredZipId !== null) {
        map.value.setFeatureState(
          { source: 'zip-codes', id: hoveredZipId },
          { hover: false }
        )
      }

      hoveredZipId = e.features[0].id
      map.value.setFeatureState(
        { source: 'zip-codes', id: hoveredZipId },
        { hover: true }
      )

      // Show tooltip
      const zipCode = e.features[0].properties.ZIPCODE
      const data = processedMapData.value[zipCode]?.[currentYear.value.toString()]

      if (data) {
        if (popup) popup.remove()

        popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false
        })
          .setLngLat(e.lngLat)
          .setHTML(`
            <div style="padding: 8px;">
              <strong>ZIP: ${zipCode}</strong><br/>
              <strong>Year: ${currentYear.value}</strong><br/>
              Housing Cost: $${Math.round(data.housingCost).toLocaleString()}<br/>
              Businesses: ${data.businessDensity || 0}
            </div>
          `)
          .addTo(map.value)

        map.value.getCanvas().style.cursor = 'pointer'
      }
    }
  })

  map.value.on('mouseleave', 'housing-choropleth', () => {
    if (hoveredZipId !== null) {
      map.value.setFeatureState(
        { source: 'zip-codes', id: hoveredZipId },
        { hover: false }
      )
    }
    hoveredZipId = null
    map.value.getCanvas().style.cursor = ''

    if (popup) {
      popup.remove()
      popup = null
    }
  })

  // NEW: Add click handler for ZIP selection
  map.value.on('click', 'housing-choropleth', (e) => {
    if (e.features && e.features.length > 0) {
      const zipCode = e.features[0].properties.ZIPCODE
      
      // Toggle selection: if clicking same ZIP, deselect it
      if (selectedZipCode.value === zipCode) {
        selectedZipCode.value = null
        emit('zip-selected', null)
      } else {
        selectedZipCode.value = zipCode
        emit('zip-selected', zipCode)
      }
      
      // Update visual highlight
      updateZipHighlight()
    }
  })
}

// ==================== Overlay Canvas for Patterns ====================

function createOverlayCanvas() {
  if (!map.value) return

  const canvas = document.createElement('canvas')
  const container = map.value.getCanvasContainer()

  canvas.style.position = 'absolute'
  canvas.style.top = '0'
  canvas.style.left = '0'
  canvas.style.pointerEvents = 'none'

  container.appendChild(canvas)

  overlayCanvas = canvas
  overlayContext = canvas.getContext('2d')

  let updateTimeout = null
  let isUpdating = false

  const debouncedUpdate = () => {
    if (updateTimeout) clearTimeout(updateTimeout)
    updateTimeout = setTimeout(() => {
      if (!isUpdating) {
        isUpdating = true
        requestAnimationFrame(() => {
          updateOverlayPatterns()
          isUpdating = false
        })
      }
    }, 150) // Wait 150ms after movement stops
  }

  // Resize canvas to match map
  const resize = () => {
    const mapCanvas = map.value.getCanvas()
    canvas.width = mapCanvas.width
    canvas.height = mapCanvas.height
    updateOverlayPatterns()
  }

  map.value.on('resize', resize)
  map.value.on('move', debouncedUpdate)
  map.value.on('zoom', () => {
    // Clear patterns immediately when zooming
    overlayContext.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height)
    debouncedUpdate()
  })
  map.value.on('moveend', updateOverlayPatterns)
  map.value.on('zoomend', updateOverlayPatterns)

  resize()
}

function updateOverlayPatterns() {
  const startTime = performance.now()

  if (!overlayCanvas || !overlayContext || !geoJsonData.value || !map.value) return

  // Check if map is loaded and has valid bounds
  if (!map.value.isStyleLoaded() || !map.value.getCanvas()) {
    // Defer until map is ready
    setTimeout(() => updateOverlayPatterns(), 100)
    return
  }

  overlayContext.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height)

  // Get current map bounds to only draw visible features
  let bounds
  try {
    bounds = map.value.getBounds()
    // Validate bounds
    if (!bounds || isNaN(bounds.getNorth()) || isNaN(bounds.getSouth()) ||
        isNaN(bounds.getEast()) || isNaN(bounds.getWest())) {
      console.warn('Invalid map bounds:', bounds)
      return
    }
  } catch (error) {
    console.error('Error getting map bounds:', error)
    return
  }

  let drawnCount = 0
  const maxFeaturesToDraw = 100 // Limit features drawn at once

  geoJsonData.value.features.forEach(feature => {
    if (drawnCount >= maxFeaturesToDraw) return

    const zipCode = feature.properties.ZIPCODE
    const data = processedMapData.value[zipCode]?.[currentYear.value.toString()]

    if (!data || !data.businessDensity) return

    // Get geometry coordinates based on type
    let coords
    if (feature.geometry.type === 'Polygon') {
      coords = feature.geometry.coordinates[0]
    } else if (feature.geometry.type === 'MultiPolygon') {
      coords = feature.geometry.coordinates[0][0]
    }

    if (!coords || coords.length === 0) return

    // Check if any part of the feature is in viewport by testing multiple points
    const isVisible = coords.some(coord => {
      try {
        return bounds.contains([coord[0], coord[1]])
      } catch {
        return false
      }
    })

    if (!isVisible) return

    // Draw hatched pattern based on business density
    drawHatchPattern(feature.geometry, data.businessDensity)
    drawnCount++
  })

  const endTime = performance.now()
  if (drawnCount > 0 || geoJsonData.value.features.length > 0) {
    console.log(`Drew patterns for ${drawnCount} visible ZIP codes (from ${geoJsonData.value.features.length} total), rendering took ${Math.round(endTime - startTime)}ms`)
  }
}

function drawHatchPattern(geometry, density) {
  if (!map.value) return

  // Handle both Polygon and MultiPolygon
  if (geometry.type === 'Polygon') {
    drawPolygonPattern(geometry.coordinates[0], density)
  } else if (geometry.type === 'MultiPolygon') {
    geometry.coordinates.forEach(polygon => {
      drawPolygonPattern(polygon[0], density)
    })
  }
}

function drawPolygonPattern(coordinates, density) {
  if (!coordinates || coordinates.length === 0) return

  const maxDensity = getMaxBusinessDensity()
  if (maxDensity === 0 || density === 0) return

  const normalizedDensity = Math.min(density / maxDensity, 1)

  // Only draw patterns for significant density (optimization)
  if (normalizedDensity < 0.1) return

  // Simpler spacing: fewer lines = better performance
  const spacing = Math.max(8, 40 - (normalizedDensity * 32)) // 8-40 pixels

  // Convert geographic coordinates to pixel coordinates
  const pixelCoords = coordinates.map(coord => {
    try {
      const projected = map.value.project(coord)
      // Validate projected coordinates
      if (isNaN(projected.x) || isNaN(projected.y)) {
        return null
      }
      return projected
    } catch {
      return null
    }
  }).filter(coord => coord !== null)

  if (pixelCoords.length === 0) return

  // Bounding box
  const minX = Math.min(...pixelCoords.map(p => p.x))
  const maxX = Math.max(...pixelCoords.map(p => p.x))
  const minY = Math.min(...pixelCoords.map(p => p.y))
  const maxY = Math.max(...pixelCoords.map(p => p.y))

  // Validate bounding box
  if (isNaN(minX) || isNaN(maxX) || isNaN(minY) || isNaN(maxY)) return

  // Skip very small areas (not visible anyway)
  const width = maxX - minX
  const height = maxY - minY
  if (width < 3 || height < 3) return

  overlayContext.save()

  // Create clipping path
  overlayContext.beginPath()
  pixelCoords.forEach((coord, i) => {
    if (i === 0) {
      overlayContext.moveTo(coord.x, coord.y)
    } else {
      overlayContext.lineTo(coord.x, coord.y)
    }
  })
  overlayContext.closePath()
  overlayContext.clip()

  // Style based on density
  const opacity = 0.3 + (normalizedDensity * 0.5) // 0.3 to 0.8
  overlayContext.strokeStyle = `rgba(0, 0, 0, ${opacity})`
  overlayContext.lineWidth = 1.5

  // Draw diagonal lines (single direction for performance)
  for (let i = minX - height; i < maxX + height; i += spacing) {
    overlayContext.beginPath()
    overlayContext.moveTo(i, minY)
    overlayContext.lineTo(i + height, maxY)
    overlayContext.stroke()
  }

  // Add cross-hatching ONLY for very high density
  if (normalizedDensity > 0.75) {
    overlayContext.strokeStyle = `rgba(0, 0, 0, ${opacity * 0.7})`
    for (let i = minX; i < maxX + height; i += spacing * 1.5) {
      overlayContext.beginPath()
      overlayContext.moveTo(i, minY)
      overlayContext.lineTo(i - height, maxY)
      overlayContext.stroke()
    }
  }

  overlayContext.restore()
}

function getMaxBusinessDensity() {
  let max = 0
  Object.values(processedMapData.value).forEach(zipData => {
    Object.values(zipData).forEach(yearData => {
      if (yearData.businessDensity > max) {
        max = yearData.businessDensity
      }
    })
  })
  return max || 1
}

// ==================== Map Update Functions ====================

function updateMap(year) {
  if (!map.value || !map.value.getSource('zip-codes')) return

  const yearStr = year.toString()

  // Calculate color scale for housing costs
  const housingCosts = []
  Object.entries(processedMapData.value).forEach(([, data]) => {
    const cost = data[yearStr]?.housingCost
    if (cost && cost > 0) {
      housingCosts.push(cost)
    }
  })

  if (housingCosts.length === 0) {
    console.warn('No housing cost data for year:', year)
    return
  }

  const minCost = d3.min(housingCosts)
  const maxCost = d3.max(housingCosts)

  // Use quantile scale for better distribution
  housingCosts.sort((a, b) => a - b)
  const q25 = housingCosts[Math.floor(housingCosts.length * 0.25)]
  const q75 = housingCosts[Math.floor(housingCosts.length * 0.75)]

  console.log(`Year ${year}: range $${Math.round(minCost)} - $${Math.round(maxCost)}, IQR: $${Math.round(q25)} - $${Math.round(q75)}`)

  // Better color scale with more contrast
  const colorScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([q25, q75])  // Use interquartile range for better contrast

  // Create expression for fill-color
  const expression = ['match', ['get', 'ZIPCODE']]

  let matchCount = 0
  Object.entries(processedMapData.value).forEach(([zipCode, data]) => {
    const cost = data[yearStr]?.housingCost
    if (cost && cost > 0) {
      expression.push(zipCode)
      // Clamp values to show more contrast
      const clampedCost = Math.max(q25, Math.min(q75, cost))
      expression.push(colorScale(clampedCost))
      matchCount++
    }
  })

  expression.push('#e0e0e0') // Light gray fallback

  console.log(`Created color expression with ${matchCount} ZIP codes`)

  // Update the map
  map.value.setPaintProperty('housing-choropleth', 'fill-color', expression)
  map.value.setPaintProperty('housing-choropleth', 'fill-opacity', 0.75) // Slightly more opaque

  // Update overlay patterns
  updateOverlayPatterns()
}

// NEW: Function to highlight selected ZIP
function updateZipHighlight() {
  if (!map.value) return
  
  if (selectedZipCode.value) {
    // Highlight selected ZIP with different style
    map.value.setPaintProperty('zip-boundaries', 'line-color', [
      'case',
      ['==', ['get', 'ZIPCODE'], selectedZipCode.value],
      '#ff6b35', // Orange for selected
      '#ffffff'  // White for others
    ])
    
    map.value.setPaintProperty('zip-boundaries', 'line-width', [
      'case',
      ['==', ['get', 'ZIPCODE'], selectedZipCode.value],
      4, // Thicker for selected
      1.5
    ])
  } else {
    // Reset to default
    map.value.setPaintProperty('zip-boundaries', 'line-color', '#ffffff')
    map.value.setPaintProperty('zip-boundaries', 'line-width', 1.5)
  }
}

// NEW: Function to clear selection
function clearSelection() {
  selectedZipCode.value = null
  emit('zip-selected', null)
  updateZipHighlight()
}

// ==================== Playback Controls ====================

function togglePlayback() {
  if (isPlaying.value) {
    stopPlayback()
  } else {
    startPlayback()
  }
}

function startPlayback() {
  isPlaying.value = true
  playbackInterval = setInterval(() => {
    if (currentYear.value >= 2022) {
      currentYear.value = 2015
    } else {
      currentYear.value++
    }
  }, 1000)
}

function stopPlayback() {
  isPlaying.value = false
  if (playbackInterval) {
    clearInterval(playbackInterval)
    playbackInterval = null
  }
}

function resetYear() {
  stopPlayback()
  currentYear.value = 2015
}

// ==================== Watchers ====================

// Watch for internal year changes (from slider/playback) and emit to parent
watch(currentYear, (newYear, oldYear) => {
  if (newYear !== oldYear) {
    updateMap(newYear)
    emit('year-change', newYear)
  }
})

// Watch for prop changes from parent (when charts update the year)
watch(() => props.currentYear, (newYear) => {
  if (newYear !== null && newYear !== currentYear.value) {
    // Parent wants to change the year, update our local state
    // Make sure it's within valid range (2015-2022)
    if (newYear >= 2015 && newYear <= 2022) {
      currentYear.value = newYear
    }
  }
})

// ==================== Lifecycle Hooks ====================

onMounted(async () => {
  console.log('TemporalMap component mounted')

  try {
    // Load GeoJSON and pre-processed data in parallel
    const [geojson, processedData] = await Promise.all([
      loadGeoJSON(),
      loadProcessedData()
    ])

    if (!processedData) {
      console.error('Could not load processed data and no fallback available')
      isLoading.value = false
      return
    }

    console.log('Data loaded:', {
      geojsonFeatures: geojson.features.length,
      processedZips: Object.keys(processedData).length
    })

    geoJsonData.value = geojson
    processedMapData.value = processedData

    // Initialize map
    initializeMap()

    isLoading.value = false
  } catch (error) {
    console.error('Error initializing map:', error)
    isLoading.value = false
  }
})

onBeforeUnmount(() => {
  stopPlayback()
  if (map.value) {
    map.value.remove()
  }
})
</script>

<style scoped>
.temporal-map-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #f5f5f5;
}

.map-container {
  width: 100%;
  height: 100%;
}

.controls-panel {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 400px;
}

.year-display {
  text-align: center;
  margin-bottom: 15px;
}

.year-display h3 {
  margin: 0;
  font-size: 24px;
  color: #2c3e50;
  font-weight: 600;
}

.slider-container {
  margin-bottom: 15px;
}

.slider-container label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
  font-size: 14px;
}

.year-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;  /* Add this standard property */
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.year-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.year-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2c3e50;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.year-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 5px;
  font-size: 12px;
  color: #777;
}

.playback-controls {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.play-button,
.reset-button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.play-button {
  background: #3182bd;
  color: white;
}

.play-button:hover {
  background: #2171a6;
}

.reset-button {
  background: #f0f0f0;
  color: #333;
}

.reset-button:hover {
  background: #e0e0e0;
}

.legend-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 200px;
}

.legend-section {
  margin-bottom: 20px;
}

.legend-section:last-child {
  margin-bottom: 0;
}

.legend-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #2c3e50;
  font-weight: 600;
}

.color-scale {
  margin-top: 8px;
}

.scale-gradient {
  height: 20px;
  border-radius: 4px;
  margin-bottom: 5px;
}

.housing-gradient {
  background: linear-gradient(to right, #deebf7, #3182bd);
}

.scale-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #666;
}

.pattern-examples {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pattern-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #666;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3182bd;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-overlay p {
  margin-top: 20px;
  font-size: 16px;
  color: #555;
}

/* NEW: Selection info styles */
.selection-info {
  margin-top: 15px;
  padding: 10px;
  background: #fff3cd;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ffc107;
}

.selected-zip {
  font-weight: 600;
  color: #856404;
  font-size: 14px;
}

.clear-button {
  padding: 4px 12px;
  background: #fff;
  border: 1px solid #ffc107;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  color: #856404;
  transition: all 0.2s;
}

.clear-button:hover {
  background: #ffc107;
  color: #fff;
}
</style>