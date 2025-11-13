<template>
  <div class="container-fluid p-0">
    <div class="row g-0 vh-100">
      <!-- Left Side: Joann's Mapbox Map (60% width) -->
      <div class="col-lg-7 map-column">
        <TemporalMap 
          :current-year="currentYear"
          @year-change="onYearChange"
          @zip-selected="onZipSelected"
        />
      </div>

      <!-- Right Side: Your Analysis Charts (40% width) -->
      <div class="col-lg-5 analysis-column">
        <div class="analysis-container">
          <GentrificationAnalysis 
            :current-time="currentTimeIndex"
            :selected-neighborhood="selectedNeighborhood"
            :selected-zip-code="selectedZipCode"
            @neighborhood-change="onNeighborhoodChange"
            @time-change="onTimeChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GentrificationAnalysis from '../components/GentrificationAnalysis.vue';
import TemporalMap from '../components/TemporalMap.vue';

export default {
  name: 'NeighborhoodAnalysis',
  
  components: {
    GentrificationAnalysis,
    TemporalMap
  },
  
  data() {
    return {
      // Current year for the map (2015-2022)
      currentYear: 2015,
      
      // Selected neighborhood from charts
      selectedNeighborhood: 'business-led',
      
      // Time index for quarterly data (0-43 for 2015 Q1 to 2025 Q4)
      currentTimeIndex: 0,
      
      // NEW: Selected ZIP code from map
      selectedZipCode: null
    };
  },
  
  methods: {
    /**
     * Handle year changes from the map's timeline slider
     * Convert year to quarterly index for the charts
     */
    onYearChange(year) {
      this.currentYear = year;
      
      // Convert year to quarterly index (each year has 4 quarters)
      // Year 2015 → index 0-3
      // Year 2016 → index 4-7, etc.
      const baseYear = 2015;
      const yearOffset = year - baseYear;
      const quarterlyIndex = yearOffset * 4; // Start of that year (Q1)
      
      this.currentTimeIndex = quarterlyIndex;
      
      console.log(`Map year changed to ${year} → Chart index ${quarterlyIndex}`);
    },
    
    /**
     * Handle time changes from the chart's global slider
     * Convert quarterly index to year for the map
     */
    onTimeChange(timeIndex) {
      this.currentTimeIndex = timeIndex;
      
      // Convert quarterly index to year
      const baseYear = 2015;
      const year = baseYear + Math.floor(timeIndex / 4);
      
      // Only update map if year changed (to avoid excessive updates)
      if (year !== this.currentYear && year >= 2015 && year <= 2022) {
        this.currentYear = year;
        console.log(`Chart index ${timeIndex} → Map year ${year}`);
      }
    },
    
    /**
     * Handle neighborhood selection changes from the charts
     */
    onNeighborhoodChange(neighborhoodId) {
      this.selectedNeighborhood = neighborhoodId;
      console.log('Selected neighborhood:', neighborhoodId);
      
      // TODO: In future, you could highlight this neighborhood on the map
      // by passing the selection to TemporalMap via props
    },
    
    /**
     * Handle ZIP code selection from the map
     */
    onZipSelected(zipCode) {
      this.selectedZipCode = zipCode;
      console.log('Selected ZIP:', zipCode);
      
      // When a ZIP is selected, the charts will automatically update
      // through the prop binding
    }
  }
};
</script>

<style scoped>
/* Remove all padding/margins for full-screen split layout */
.container-fluid {
  padding: 0 !important;
  margin: 0 !important;
}

.row {
  margin: 0 !important;
}

/* Map column takes up left side */
.map-column {
  padding: 0 !important;
  height: 100vh;
  overflow: hidden;
}

/* Analysis column takes up right side */
.analysis-column {
  padding: 0 !important;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  background: #f8f9fa;
}

.analysis-container {
  height: 100%;
  padding: 0;
}

/* Ensure no gaps between columns */
.col-lg-7, .col-lg-5 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}

/* Hide scrollbar for analysis column but keep functionality */
.analysis-column::-webkit-scrollbar {
  width: 8px;
}

.analysis-column::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.analysis-column::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.analysis-column::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>