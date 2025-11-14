<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import * as d3 from 'd3'

// Reference to the map container DOM element
const mapContainer = ref(null)

// Initialize the Leaflet map on component mount
onMounted(async () => {
  // Initialize Leaflet map centered on Highland Park, LA
  const map = L.map(mapContainer.value, {
    center: [34.115, -118.188],
    zoom: 14,
    minZoom: 13,
    maxZoom: 18,
    zoomControl: true
  })

  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map)

  try {
    // Load the full LA neighborhoods GeoJSON
    const response = await fetch('/highland.geojson')
    const allNeighborhoods = await response.json()

    // Filter to get ONLY Highland Park
    const highlandParkFeature = allNeighborhoods.features.find(
      feature => feature.properties.name === "Highland Park"
    )

    if (!highlandParkFeature) {
      throw new Error('Highland Park not found in GeoJSON.')
    }

    // Create a new GeoJSON with only Highland Park
    const highlandParkOnly = {
      type: "FeatureCollection",
      features: [highlandParkFeature]
    }

    // Create a Leaflet GeoJSON layer for Highland Park boundary only
    const boundaryLayer = L.geoJSON(highlandParkOnly, {
      style: {
        color: '#2c3e50',
        weight: 3,
        fillOpacity: 0,
        dashArray: '5, 5'
      }
    }).addTo(map)

    // Get the bounds from Highland Park only
    const bounds = boundaryLayer.getBounds()
    
    // Set max bounds to lock the map to Highland Park only
    map.setMaxBounds(bounds.pad(0.1))
    map.options.maxBoundsViscosity = 1.0

    // Fit the map perfectly to Highland Park
    map.fitBounds(bounds, { padding: [20, 20] })

    // Create SVG overlay for masking everything outside Highland Park
    const svg = d3.select(map.getPanes().overlayPane)
      .append('svg')
      .attr('class', 'highland-park-mask')
      .style('position', 'absolute')
      .style('top', 0)
      .style('left', 0)
      .style('pointer-events', 'none')

    const g = svg.append('g')
      .attr('class', 'leaflet-zoom-hide')

    // Function to update the mask on zoom/pan
    function updateMask() {
      const mapBounds = map.getBounds()
      const topLeft = map.latLngToLayerPoint(mapBounds.getNorthWest())
      const bottomRight = map.latLngToLayerPoint(mapBounds.getSouthEast())

      svg
        .attr('width', bottomRight.x - topLeft.x)
        .attr('height', bottomRight.y - topLeft.y)
        .style('left', topLeft.x + 'px')
        .style('top', topLeft.y + 'px')

      g.attr('transform', `translate(${-topLeft.x},${-topLeft.y})`)

      // Create the path projection
      const geoPath = d3.geoPath().projection(
        d3.geoTransform({
          point: function(lng, lat) {
            const point = map.latLngToLayerPoint(new L.LatLng(lat, lng))
            this.stream.point(point.x, point.y)
          }
        })
      )

      // Clear existing paths
      g.selectAll('path').remove()

      // Get map pixel bounds for creating outer rectangle
      const pixelBounds = map.getPixelBounds()
      const padding = 5000

      // Create coordinates for outer world rectangle
      const outerCoords = [
        [pixelBounds.min.x - padding, pixelBounds.min.y - padding],
        [pixelBounds.max.x + padding, pixelBounds.min.y - padding],
        [pixelBounds.max.x + padding, pixelBounds.max.y + padding],
        [pixelBounds.min.x - padding, pixelBounds.max.y + padding]
      ].map(p => {
        const latlng = map.layerPointToLatLng(L.point(p[0], p[1]))
        return [latlng.lng, latlng.lat]
      })

      // Draw outer rectangle covering everything
      g.append('path')
        .datum({
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [outerCoords]
          }
        })
        .attr('d', geoPath)
        .attr('fill', 'white')
        .attr('fill-opacity', 0.88)
        .attr('class', 'outer-mask')

      // Draw Highland Park boundary
      g.append('path')
        .datum(highlandParkOnly)
        .attr('d', geoPath)
        .attr('fill', 'transparent')
        .attr('stroke', '#2c3e50')
        .attr('stroke-width', 3)
        .attr('stroke-dasharray', '8, 4')
        .attr('class', 'boundary-line')
    }

    // Update mask on map move/zoom
    map.on('moveend zoom', updateMask)
    updateMask()

    // Add popup to boundary
    boundaryLayer.bindPopup('<b>Highland Park</b><br>Los Angeles, CA<br><small>Neighborhood boundary</small>')

  } catch (error) {
    console.error('Error loading Highland Park:', error)
    alert('Error loading Highland Park boundary. Please check that highland.geojson is in the public folder.')
  }

  // TODO: Add D3 data visualization layers here
  // D3 is available and ready for use with the variable 'd3'

  // TODO: Implement cleanup on component unmount
  // onUnmounted(() => {
  //   if (map) {
  //     map.remove()
  //   }
  // })
})
</script>

<template>
  <div class="map-wrapper">
    <div ref="mapContainer" class="map-container"></div>
    <div class="map-info">
      <p>📍 Highland Park Only</p>
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

:deep(.highland-park-mask) {
  z-index: 400;
}

:deep(.leaflet-control-container) {
  z-index: 1000;
}
</style>