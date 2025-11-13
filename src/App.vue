<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">LA Gentrification Dashboard</a>
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Neighborhood Analysis</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/migration" class="nav-link">Migration Flow</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Global Time Slider (controls all views) -->
    <div class="container-fluid py-3 bg-light border-bottom">
      <div class="row">
        <div class="col-12">
          <label class="form-label fw-bold">
            Global Time Control: {{ formatQuarter(currentTime) }}
          </label>
          <input 
            type="range" 
            class="form-range" 
            min="0" 
            max="42"
            v-model.number="currentTime"
            @input="onGlobalTimeChange"
          >
          <div class="d-flex justify-content-between small text-muted">
            <span>2015 Q1</span>
            <span>2025 Q3</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Page Content -->
    <router-view 
      :current-time="currentTime"
      :selected-neighborhood="selectedNeighborhood"
      @neighborhood-change="onNeighborhoodChange"
      @time-change="onTimeChange"
    />
  </div>
</template>

<script>
export default {
  name: 'App',
  
  data() {
    return {
      currentTime: 42, // 2025 Q3 (end index)
      selectedNeighborhood: 'business-led',
      timeLabels: this.generateTimeLabels()
    };
  },
  
  methods: {
    generateTimeLabels() {
      const labels = [];
      for (let i = 0; i < 43; i++) {
        const year = 2015 + Math.floor(i / 4);
        const quarter = (i % 4) + 1;
        labels.push(`${year} Q${quarter}`);
      }
      return labels;
    },
    
    formatQuarter(index) {
      return this.timeLabels[index] || '';
    },
    
    onGlobalTimeChange() {
      // This will propagate to all child components through props
      console.log('Global time changed to:', this.formatQuarter(this.currentTime));
    },
    
    onNeighborhoodChange(neighborhoodId) {
      this.selectedNeighborhood = neighborhoodId;
      console.log('Selected neighborhood:', neighborhoodId);
    },
    
    onTimeChange(newTime) {
      // Update global time when child component changes it
      this.currentTime = newTime;
    }
  }
};
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.router-link-active {
  font-weight: bold;
}

.form-range {
  cursor: pointer;
}
</style>