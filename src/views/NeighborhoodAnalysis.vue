<template>
  <div class="container-fluid">
    <div class="row vh-100">
      <!-- Left Side: Mapbox Map (60% width) -->
      <div class="col-lg-7 p-0 position-relative">
        <div class="map-container">
          <!-- Mapbox map will go here -->
          <div ref="mapContainer" class="w-100 h-100"></div>
          
          <!-- Map Legend (overlay on map) -->
          <div class="map-legend">
            <h6 class="mb-2">Gentrification Pattern</h6>
            <div class="legend-item">
              <span class="legend-color" style="background: #ef4444;"></span>
              Business-Led
            </div>
            <div class="legend-item">
              <span class="legend-color" style="background: #3b82f6;"></span>
              Housing-Led
            </div>
            <div class="legend-item">
              <span class="legend-color" style="background: #8b5cf6;"></span>
              Simultaneous
            </div>
            <div class="legend-item">
              <span class="legend-color" style="background: #6b7280;"></span>
              Stable
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Analysis Panel (40% width) -->
      <div class="col-lg-5 p-0 overflow-auto" style="max-height: 100vh;">
        <GentrificationAnalysis 
          :current-time="currentTime"
          :selected-neighborhood="localNeighborhood"
          @neighborhood-change="onNeighborhoodChange"
          @time-change="onTimeChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import GentrificationAnalysis from '../components/GentrificationAnalysis.vue';
// import mapboxgl from 'mapbox-gl'; // Uncomment when ready to add Mapbox

export default {
  name: 'NeighborhoodAnalysis',
  
  components: {
    GentrificationAnalysis
  },
  
  props: {
    currentTime: {
      type: Number,
      default: 42
    },
    selectedNeighborhood: {
      type: String,
      default: 'business-led'
    }
  },
  
  data() {
    return {
      localNeighborhood: this.selectedNeighborhood,
      map: null
    };
  },
  
  mounted() {
    this.initializeMap();
  },
  
  watch: {
    currentTime(newTime) {
      // Update map layers based on time
      this.updateMapForTime(newTime);
    },
    
    selectedNeighborhood(newNeighborhood) {
      this.localNeighborhood = newNeighborhood;
      // Highlight neighborhood on map
      this.highlightNeighborhood(newNeighborhood);
    }
  },
  
  methods: {
    initializeMap() {
      // TODO: Initialize Mapbox map
      // This is a placeholder - add your Mapbox initialization here
      
      /*
      mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
      
      this.map = new mapboxgl.Map({
        container: this.$refs.mapContainer,
        style: 'mapbox://styles/mapbox/light-v11',
        center: [-118.2437, 34.0522], // LA center
        zoom: 10
      });
      
      this.map.on('load', () => {
        this.addNeighborhoodLayers();
        this.setupMapInteractions();
      });
      */
      
      // For now, show placeholder
      const container = this.$refs.mapContainer;
      container.innerHTML = `
        <div class="d-flex align-items-center justify-content-center h-100 bg-light">
          <div class="text-center">
            <h3 class="text-muted">Mapbox Map Goes Here</h3>
            <p class="text-muted">
              Initialize your Mapbox map in the initializeMap() method<br/>
              Add dual-layer choropleth with housing costs + business density
            </p>
            <div class="mt-4">
              <p class="small text-muted">Expected Layers:</p>
              <ul class="list-unstyled small text-muted">
                <li>• Choropleth: Housing cost (color intensity)</li>
                <li>• Overlay: Business density (hatched patterns)</li>
                <li>• Interactive: Click to select neighborhood</li>
                <li>• Temporal: Updates with time slider</li>
              </ul>
            </div>
          </div>
        </div>
      `;
    },
    
    addNeighborhoodLayers() {
      // TODO: Add your neighborhood GeoJSON layers
      
      /*
      // Example structure:
      this.map.addSource('neighborhoods', {
        type: 'geojson',
        data: '/data/la-neighborhoods.geojson'
      });
      
      // Housing cost choropleth layer
      this.map.addLayer({
        id: 'housing-choropleth',
        type: 'fill',
        source: 'neighborhoods',
        paint: {
          'fill-color': [
            'interpolate',
            ['linear'],
            ['get', 'housingCost'],
            0, '#f0f9ff',
            50, '#0ea5e9',
            100, '#1e40af'
          ],
          'fill-opacity': 0.7
        }
      });
      
      // Business density overlay (using patterns)
      this.map.addLayer({
        id: 'business-overlay',
        type: 'fill',
        source: 'neighborhoods',
        paint: {
          'fill-pattern': [
            'step',
            ['get', 'businessDensity'],
            'pattern-low',
            33, 'pattern-medium',
            66, 'pattern-high'
          ],
          'fill-opacity': 0.5
        }
      });
      */
    },
    
    setupMapInteractions() {
      // TODO: Setup click handlers for neighborhood selection
      
      /*
      this.map.on('click', 'housing-choropleth', (e) => {
        if (e.features.length > 0) {
          const neighborhoodId = e.features[0].properties.id;
          this.onNeighborhoodChange(neighborhoodId);
        }
      });
      
      // Change cursor on hover
      this.map.on('mouseenter', 'housing-choropleth', () => {
        this.map.getCanvas().style.cursor = 'pointer';
      });
      
      this.map.on('mouseleave', 'housing-choropleth', () => {
        this.map.getCanvas().style.cursor = '';
      });
      */
    },
    
    updateMapForTime(timeIndex) {
      // TODO: Update map layers to show data for the selected time period
      
      /*
      // Example: Update the filter on your layers
      const quarter = this.getQuarterFromIndex(timeIndex);
      
      this.map.setFilter('housing-choropleth', [
        '==',
        ['get', 'quarter'],
        quarter
      ]);
      
      this.map.setFilter('business-overlay', [
        '==',
        ['get', 'quarter'],
        quarter
      ]);
      */
      
      console.log('Update map for time index:', timeIndex);
    },
    
    highlightNeighborhood(neighborhoodId) {
      // TODO: Highlight selected neighborhood on map
      
      /*
      // Remove previous highlight
      if (this.map.getLayer('neighborhood-highlight')) {
        this.map.removeLayer('neighborhood-highlight');
      }
      
      // Add new highlight
      this.map.addLayer({
        id: 'neighborhood-highlight',
        type: 'line',
        source: 'neighborhoods',
        paint: {
          'line-color': '#ff0000',
          'line-width': 3
        },
        filter: ['==', ['get', 'id'], neighborhoodId]
      });
      
      // Fly to neighborhood
      const feature = this.getNeighborhoodFeature(neighborhoodId);
      if (feature) {
        const bbox = turf.bbox(feature);
        this.map.fitBounds(bbox, { padding: 50 });
      }
      */
      
      console.log('Highlight neighborhood:', neighborhoodId);
    },
    
    onNeighborhoodChange(neighborhoodId) {
      this.localNeighborhood = neighborhoodId;
      this.$emit('neighborhood-change', neighborhoodId);
    },
    
    onTimeChange(newTime) {
      // Bubble up the time change event to App.vue
      this.$emit('time-change', newTime);
    },
    
    getQuarterFromIndex(index) {
      const year = 2015 + Math.floor(index / 4);
      const quarter = (index % 4) + 1;
      return `${year}-Q${quarter}`;
    }
  },
  
  beforeUnmount() {
    // Clean up map
    if (this.map) {
      this.map.remove();
    }
  }
};
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #f8f9fa;
}

.map-legend {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 1;
}

.map-legend h6 {
  font-size: 14px;
  font-weight: bold;
  margin: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 13px;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  margin-right: 8px;
  border: 1px solid #ccc;
}

.overflow-auto {
  overflow-y: auto;
  overflow-x: hidden;
}
</style>