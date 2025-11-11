<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Main Map Area -->
      <div class="col-lg-9 p-0">
        <div class="map-container">
          <div ref="migrationMap" class="w-100 h-100"></div>
          
          <!-- Map Controls (overlay) -->
          <div class="map-controls">
            <h6 class="mb-2">Migration Flow Controls</h6>
            <div class="form-check">
              <input 
                class="form-check-input" 
                type="checkbox" 
                id="showInflow"
                v-model="showInflow"
                @change="updateFlowLayers"
              >
              <label class="form-check-label" for="showInflow">
                Show Inflow (to LA)
              </label>
            </div>
            <div class="form-check">
              <input 
                class="form-check-input" 
                type="checkbox" 
                id="showOutflow"
                v-model="showOutflow"
                @change="updateFlowLayers"
              >
              <label class="form-check-label" for="showOutflow">
                Show Outflow (from LA)
              </label>
            </div>
            <hr class="my-2">
            <label class="form-label small mb-1">Flow Intensity</label>
            <input 
              type="range" 
              class="form-range" 
              min="1" 
              max="100"
              v-model.number="flowIntensity"
              @input="updateFlowIntensity"
            >
          </div>
        </div>
      </div>

      <!-- Right Sidebar: Statistics -->
      <div class="col-lg-3 p-4 bg-light overflow-auto" style="max-height: 100vh;">
        <h4 class="mb-4">Migration Statistics</h4>
        
        <!-- Time Period Display -->
        <div class="card mb-3">
          <div class="card-body">
            <h6 class="card-title">Time Period</h6>
            <p class="card-text">{{ currentQuarter }}</p>
          </div>
        </div>

        <!-- Top Source Cities -->
        <div class="card mb-3">
          <div class="card-body">
            <h6 class="card-title">Top Inflow Cities</h6>
            <ol class="mb-0 ps-3">
              <li v-for="city in topInflowCities" :key="city.name" class="mb-2">
                <strong>{{ city.name }}</strong>
                <br>
                <small class="text-muted">{{ city.count }} migrants</small>
              </li>
            </ol>
          </div>
        </div>

        <!-- Top Destination Neighborhoods -->
        <div class="card mb-3">
          <div class="card-body">
            <h6 class="card-title">Top Destination Neighborhoods</h6>
            <ol class="mb-0 ps-3">
              <li v-for="hood in topDestinations" :key="hood.name" class="mb-2">
                <strong>{{ hood.name }}</strong>
                <br>
                <small class="text-muted">{{ hood.count }} arrivals</small>
              </li>
            </ol>
          </div>
        </div>

        <!-- Migration Patterns -->
        <div class="card">
          <div class="card-body">
            <h6 class="card-title">Key Insights</h6>
            <ul class="mb-0 small">
              <li class="mb-2">
                Most migrants from <strong>Bay Area</strong> (35%)
              </li>
              <li class="mb-2">
                <strong>Arts District</strong> seeing highest growth
              </li>
              <li>
                Peak migration in <strong>Q2-Q3</strong> annually
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import mapboxgl from 'mapbox-gl';
// import { ArcLayer } from '@deck.gl/layers';
// import { MapboxOverlay } from '@deck.gl/mapbox';

export default {
  name: 'MigrationFlow',
  
  props: {
    currentTime: {
      type: Number,
      default: 42
    }
  },
  
  data() {
    return {
      map: null,
      deckOverlay: null,
      showInflow: true,
      showOutflow: false,
      flowIntensity: 50,
      
      // Sample data (replace with real data)
      topInflowCities: [
        { name: 'San Francisco, CA', count: 2450 },
        { name: 'New York, NY', count: 1820 },
        { name: 'Seattle, WA', count: 1630 },
        { name: 'Austin, TX', count: 1420 },
        { name: 'Chicago, IL', count: 1180 }
      ],
      
      topDestinations: [
        { name: 'Arts District', count: 1850 },
        { name: 'Silver Lake', count: 1620 },
        { name: 'Downtown LA', count: 1450 },
        { name: 'Echo Park', count: 980 },
        { name: 'Venice', count: 750 }
      ]
    };
  },
  
  computed: {
    currentQuarter() {
      const year = 2015 + Math.floor(this.currentTime / 4);
      const quarter = (this.currentTime % 4) + 1;
      return `${year} Q${quarter}`;
    }
  },
  
  mounted() {
    this.initializeMigrationMap();
  },
  
  watch: {
    currentTime(newTime) {
      this.updateMigrationData(newTime);
    }
  },
  
  methods: {
    initializeMigrationMap() {
      // TODO: Initialize Mapbox with DeckGL overlay
      
      /*
      mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
      
      this.map = new mapboxgl.Map({
        container: this.$refs.migrationMap,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [-118.2437, 34.0522], // LA center
        zoom: 5, // Zoom out to show surrounding states
        pitch: 45,
        bearing: 0
      });
      
      this.map.on('load', () => {
        this.addDeckGLOverlay();
      });
      */
      
      // Placeholder
      const container = this.$refs.migrationMap;
      container.innerHTML = `
        <div class="d-flex align-items-center justify-content-center h-100 bg-dark text-white">
          <div class="text-center">
            <h3>Migration Flow Map</h3>
            <p class="text-muted">
              Mapbox + DeckGL ArcLayer showing migration flows<br/>
              from other US cities to LA neighborhoods
            </p>
            <div class="mt-4">
              <p class="small">Expected Visualization:</p>
              <ul class="list-unstyled small text-white-50">
                <li>• ArcLayer: Curved lines showing migration routes</li>
                <li>• Color: Gradient based on flow volume</li>
                <li>• Width: Thickness represents migration count</li>
                <li>• Animation: Flows animate over time with slider</li>
                <li>• Interactive: Hover for origin/destination details</li>
              </ul>
            </div>
          </div>
        </div>
      `;
    },
    
    addDeckGLOverlay() {
      // TODO: Add DeckGL ArcLayer for migration flows
      
      /*
      // Sample flow data structure
      const flowData = [
        {
          source: [-122.4194, 37.7749], // San Francisco
          target: [-118.2437, 34.0522], // LA
          count: 2450
        },
        {
          source: [-74.0060, 40.7128], // New York
          target: [-118.2437, 34.0522], // LA
          count: 1820
        },
        // ... more flows
      ];
      
      const arcLayer = new ArcLayer({
        id: 'migration-arcs',
        data: flowData,
        getSourcePosition: d => d.source,
        getTargetPosition: d => d.target,
        getSourceColor: [255, 140, 0], // Orange for source
        getTargetColor: [0, 128, 255], // Blue for destination
        getWidth: d => Math.sqrt(d.count) / 2,
        getHeight: 0.5,
        pickable: true,
        autoHighlight: true,
        onHover: info => this.showFlowTooltip(info)
      });
      
      this.deckOverlay = new MapboxOverlay({
        layers: [arcLayer]
      });
      
      this.map.addControl(this.deckOverlay);
      */
    },
    
    updateFlowLayers() {
      // TODO: Update which layers are visible
      console.log('Inflow:', this.showInflow, 'Outflow:', this.showOutflow);
      
      /*
      const layers = [];
      
      if (this.showInflow) {
        layers.push(this.createInflowLayer());
      }
      
      if (this.showOutflow) {
        layers.push(this.createOutflowLayer());
      }
      
      this.deckOverlay.setProps({ layers });
      */
    },
    
    updateFlowIntensity() {
      // TODO: Update arc width based on intensity slider
      console.log('Flow intensity:', this.flowIntensity);
      
      /*
      const scale = this.flowIntensity / 50; // Normalize to 0-2 range
      
      this.deckOverlay.setProps({
        layers: [
          new ArcLayer({
            ...previousLayerProps,
            getWidth: d => (Math.sqrt(d.count) / 2) * scale
          })
        ]
      });
      */
    },
    
    updateMigrationData(timeIndex) {
      // TODO: Filter data by time period and update visualization
      console.log('Update migration data for time:', timeIndex);
      
      /*
      const quarter = this.getQuarterFromIndex(timeIndex);
      const filteredData = this.allFlowData.filter(
        flow => flow.quarter === quarter
      );
      
      // Update arc layer with new data
      this.deckOverlay.setProps({
        layers: [
          new ArcLayer({
            id: 'migration-arcs',
            data: filteredData,
            // ... other props
          })
        ]
      });
      
      // Update statistics
      this.updateStatistics(filteredData);
      */
    },
    
    showFlowTooltip(info) {
      if (info.object) {
        // TODO: Show tooltip with flow details
        const { source, target, count } = info.object;
        console.log(`Flow: ${count} people from ${source} to ${target}`);
      }
    },
    
    getQuarterFromIndex(index) {
      const year = 2015 + Math.floor(index / 4);
      const quarter = (index % 4) + 1;
      return `${year}-Q${quarter}`;
    }
  },
  
  beforeUnmount() {
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
  background: #1a1a2e;
}

.map-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  z-index: 1;
  min-width: 200px;
}

.map-controls h6 {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

.card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.overflow-auto {
  overflow-y: auto;
}
</style>
