<template>
  <div class="container-fluid py-4">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <h1 class="mb-2">
          {{ selectedZipCode ? `ZIP ${selectedZipCode}` : 'LA Neighborhood' }} Gentrification: Lead/Lag Analysis
        </h1>
        <p class="text-muted">
          {{ selectedZipCode ? 'Real data from LA County records (2015-2022)' : 'Analyzing which comes first: business changes or housing cost increases' }}
        </p>
      </div>
    </div>

    <!-- Neighborhood Selector & Time Slider -->
    <div class="row mb-4">
      <div v-if="!selectedZipCode" class="col-md-6">
        <div class="card">
          <div class="card-body">
            <label class="form-label fw-bold">Select Neighborhood:</label>
            <select 
              :value="selectedNeighborhood" 
              class="form-select"
              @change="onNeighborhoodChange($event.target.value)"
            >
              <option 
                v-for="(info, key) in neighborhoods" 
                :key="key" 
                :value="key"
              >
                {{ info.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <div v-else class="col-md-6">
        <div class="card bg-light">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-info-circle me-2 text-primary" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                <path d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
              </svg>
              <div>
                <strong>Showing real data for ZIP {{ selectedZipCode }}</strong>
                <div class="small text-muted">Click "Clear" on the map to return to synthetic examples</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <label class="form-label fw-bold">
              Component Time Range: {{ formatQuarter(timeRange[0]) }} - {{ formatQuarter(timeRange[1]) }}
            </label>
            <input 
              type="range" 
              class="form-range" 
              :min="0" 
              :max="maxTimeIndex"
              v-model.number="timeRange[1]"
              @input="onTimeRangeChange"
            >
            <div class="d-flex justify-content-between small text-muted">
              <span>2015 Q1</span>
              <span>2025 Q3</span>
            </div>
            <div class="small text-info mt-2">
              <i class="bi bi-info-circle"></i> This slider is synced with the global slider above
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Summary Card -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card border-primary">
          <div class="card-body">
            <h5 class="card-title">{{ neighborhoods[selectedNeighborhood].name }} - Analysis Summary</h5>
            <div class="row text-center">
              <div class="col-md-4">
                <div class="small text-muted mb-1">Pattern</div>
                <div class="h5 mb-0" :style="{ color: neighborhoods[selectedNeighborhood].color }">
                  {{ analysisResult.interpretation }}
                </div>
              </div>
              <div class="col-md-4">
                <div class="small text-muted mb-1">Lead Time</div>
                <div class="h5 mb-0">
                  {{ analysisResult.leadTime }} {{ analysisResult.leadTime === 1 ? 'quarter' : 'quarters' }}
                </div>
              </div>
              <div class="col-md-4">
                <div class="small text-muted mb-1">Confidence</div>
                <div class="h5 mb-0">
                  {{ analysisResult.confidence }} (r={{ analysisResult.peakCorrelation }})
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Visualization Charts -->
    <div class="row mb-4">
      <!-- Chart 1: Normalized Trends (Vega) -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">1. Normalized Trends (0-100 Scale)</h5>
            <p class="text-muted small">
              Both metrics scaled to 0-100 for direct visual comparison. The line that rises first indicates the leading factor.
            </p>
            <div ref="vegaChart" class="w-100" style="min-height: 350px;"></div>
            <div class="alert alert-warning mt-3 mb-0 small">
              <strong>Interpretation:</strong> The line that rises first indicates the leading factor. 
              Compare slopes to see which metric accelerates faster.
            </div>
          </div>
        </div>
      </div>

      <!-- Chart 2: Rate of Change (D3) -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">2. Quarter-over-Quarter Rate of Change</h5>
            <p class="text-muted small">
              Percentage change from previous quarter. Spikes indicate acceleration points.
            </p>
            <div ref="rateChart" style="min-height: 400px;"></div>
            <div class="alert alert-info mt-3 mb-0 small">
              <strong>Interpretation:</strong> First spike indicates when rapid change began. 
              Compare which metric spikes first to identify the leading indicator.
            </div>
          </div>
        </div>
      </div>

      <!-- Chart 3: Cross-Correlation (D3) -->
      <div class="col-12 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">3. Cross-Correlation Analysis</h5>
            <p class="text-muted small">
              Statistical measure of how well the two time series correlate at different time lags.
            </p>
            <div ref="correlationChart" style="min-height: 400px;"></div>
            <div class="alert alert-success mt-3 mb-0 small">
              <strong>Interpretation:</strong> Peak at lag = <strong>{{ analysisResult.peakLag }}</strong> quarters. 
              {{ analysisResult.lagInterpretation }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- How to Use Panel -->
    <div class="row">
      <div class="col-12">
        <div class="card border-start border-5 border-primary">
          <div class="card-body">
            <h5 class="card-title">Integration Notes for Your Dashboard</h5>
            <ol class="mb-0">
              <li class="mb-2">
                <strong>Page 1 (Map + Analysis):</strong> When user selects a neighborhood on the Mapbox map, 
                update <code>selectedNeighborhood</code> to show these analytics.
              </li>
              <li class="mb-2">
                <strong>Time Slider Synchronization:</strong> ✅ The global time slider now controls all visualizations! 
                Both sliders are synced - change either one and both update.
              </li>
              <li class="mb-2">
                <strong>Color Coding:</strong> Use the same color scheme on the map - red for business-led, 
                blue for housing-led, purple for simultaneous.
              </li>
              <li class="mb-0">
                <strong>Risk Assessment (Future):</strong> Neighborhoods with high business growth + lag time 
                can be flagged as "at risk" for displacement.
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import embed from 'vega-embed';

export default {
  name: 'GentrificationAnalysis',
  
  props: {
    currentTime: {
      type: Number,
      default: 42
    },
    selectedNeighborhood: {
      type: String,
      default: 'business-led'
    },
    selectedZipCode: {
      type: [String, Number],
      default: null
    }
  },
  
  data() {
    return {
      // Use prop as initial value
      timeRange: [0, this.currentTime],
      maxTimeIndex: 42,
      
      neighborhoods: {
        'business-led': { 
          name: 'Silver Lake', 
          color: '#ef4444',
          pattern: 'business-led'
        },
        'housing-led': { 
          name: 'Arts District', 
          color: '#3b82f6',
          pattern: 'housing-led'
        },
        'simultaneous': { 
          name: 'Downtown LA', 
          color: '#8b5cf6',
          pattern: 'simultaneous'
        },
        'stable': { 
          name: 'Echo Park', 
          color: '#6b7280',
          pattern: 'stable'
        }
      },
      
      // Will hold the full dataset
      fullData: [],
      
      // Filtered data based on time range
      filteredData: [],
      
      // NEW: Real ZIP code data
      realZipData: null,
      isLoadingZipData: false,
      
      // Analysis results
      analysisResult: {
        interpretation: '',
        leadTime: 0,
        confidence: '',
        peakCorrelation: 0,
        peakLag: 0,
        lagInterpretation: ''
      }
    };
  },
  
  watch: {
    // Watch for changes to the global time slider
    currentTime(newTime) {
      console.log('Global time changed, updating component to:', newTime);
      this.timeRange[1] = newTime;
      this.filterDataByTimeRange();
      this.updateVisualizations();
    },
    
    // Watch for changes to selected neighborhood from parent
    selectedNeighborhood(newNeighborhood) {
      console.log('Neighborhood changed from parent:', newNeighborhood);
      this.generateSampleData();
      this.updateVisualizations();
    },
    
    // NEW: Watch for ZIP code changes
    selectedZipCode: {
      handler(newZipCode) {
        console.log('ZIP code changed:', newZipCode);
        this.loadRealZipData(newZipCode);
      },
      immediate: true
    }
  },
  
  mounted() {
    // Generate sample data
    this.generateSampleData();
    
    // Initial render
    this.updateVisualizations();
  },
  
  methods: {
    // Generate realistic sample data for LA neighborhoods
    generateSampleData() {
      const quarters = [];
      const startYear = 2015;
      const startQuarter = 1;
      
      // Generate 43 quarters (2015 Q1 to 2025 Q3)
      for (let i = 0; i < 43; i++) {
        const year = startYear + Math.floor((startQuarter - 1 + i) / 4);
        const quarter = ((startQuarter - 1 + i) % 4) + 1;
        quarters.push({ year, quarter, index: i, label: `${year} Q${quarter}` });
      }
      
      // Use the prop for selected neighborhood
      const pattern = this.neighborhoods[this.selectedNeighborhood].pattern;
      
      this.fullData = quarters.map((q, i) => {
        return {
          ...q,
          ...this.generatePatternData(i, 43, pattern)
        };
      });
      
      this.filterDataByTimeRange();
    },
    
    generatePatternData(index, total, pattern) {
      const i = index;
      
      if (pattern === 'business-led') {
        // Business changes 2-3 quarters before housing
        return {
          expensiveBusiness: Math.max(0, Math.min(100, 10 + i * 1.8 + (i > 8 ? (i - 8) * 1 : 0))),
          housingCost: Math.max(0, Math.min(100, 5 + (i > 10 ? (i - 10) * 2.2 : i * 0.6)))
        };
      } else if (pattern === 'housing-led') {
        // Housing rises first, business follows
        return {
          expensiveBusiness: Math.max(0, Math.min(100, 8 + (i > 12 ? (i - 12) * 2 : i * 0.5))),
          housingCost: Math.max(0, Math.min(100, 12 + i * 1.8 + (i > 8 ? (i - 8) * 0.8 : 0)))
        };
      } else if (pattern === 'simultaneous') {
        // Both rise together
        return {
          expensiveBusiness: Math.max(0, Math.min(100, 15 + i * 1.6 + Math.random() * 2)),
          housingCost: Math.max(0, Math.min(100, 18 + i * 1.5 + Math.random() * 2))
        };
      } else {
        // Stable, no clear gentrification
        return {
          expensiveBusiness: Math.max(0, Math.min(100, 20 + Math.random() * 3)),
          housingCost: Math.max(0, Math.min(100, 25 + i * 0.5 + Math.random() * 2))
        };
      }
    },
    
    filterDataByTimeRange() {
      this.filteredData = this.fullData.slice(this.timeRange[0], this.timeRange[1] + 1);
    },
    
    formatQuarter(index) {
      const q = this.fullData[index];
      return q ? q.label : '';
    },
    
    onNeighborhoodChange(value) {
      // Emit event to parent
      this.$emit('neighborhood-change', value);
      // Parent will update the prop, which will trigger regeneration
    },
    
    onTimeRangeChange() {
      // Emit event to parent to sync global slider
      this.$emit('time-change', this.timeRange[1]);
      this.filterDataByTimeRange();
      this.updateVisualizations();
    },
    
    updateVisualizations() {
      this.calculateAnalysis();
      this.renderVegaChart();
      this.renderRateChart();
      this.renderCorrelationChart();
    },
    
    calculateAnalysis() {
      const data = this.filteredData;
      
      if (data.length < 2) {
        this.analysisResult = {
          interpretation: 'Insufficient data',
          leadTime: 0,
          confidence: 'N/A',
          peakCorrelation: 0,
          peakLag: 0,
          lagInterpretation: ''
        };
        return;
      }
      
      // Calculate cross-correlation
      const result = this.calculateCrossCorrelation(data);
      const peak = result.peak;
      const leadTime = Math.abs(peak.lag);
      
      let interpretation = '';
      let lagInterpretation = '';
      
      if (peak.lag > 0) {
        interpretation = `Business leads housing by ${leadTime} ${leadTime === 1 ? 'quarter' : 'quarters'}`;
        lagInterpretation = 'Positive lag means business changes predict future housing changes.';
      } else if (peak.lag < 0) {
        interpretation = `Housing leads business by ${leadTime} ${leadTime === 1 ? 'quarter' : 'quarters'}`;
        lagInterpretation = 'Negative lag means housing changes predict future business changes.';
      } else {
        interpretation = 'Simultaneous change (no clear leader)';
        lagInterpretation = 'Zero lag means both change simultaneously.';
      }
      
      const confidenceLevel = Math.abs(peak.correlation);
      let confidence = 'Low';
      if (confidenceLevel > 0.7) confidence = 'High';
      else if (confidenceLevel > 0.4) confidence = 'Medium';
      
      this.analysisResult = {
        interpretation,
        leadTime,
        confidence,
        peakCorrelation: peak.correlation.toFixed(2),
        peakLag: peak.lag,
        lagInterpretation
      };
    },
    
    calculateCrossCorrelation(data) {
      const business = data.map(d => d.expensiveBusiness);
      const housing = data.map(d => d.housingCost);
      
      // Normalize
      const businessMean = business.reduce((a, b) => a + b, 0) / business.length;
      const housingMean = housing.reduce((a, b) => a + b, 0) / housing.length;
      const businessStd = Math.sqrt(business.reduce((a, b) => a + Math.pow(b - businessMean, 2), 0) / business.length);
      const housingStd = Math.sqrt(housing.reduce((a, b) => a + Math.pow(b - housingMean, 2), 0) / housing.length);
      
      const businessNorm = business.map(v => (v - businessMean) / businessStd);
      const housingNorm = housing.map(v => (v - housingMean) / housingStd);
      
      // Calculate correlation at different lags
      const maxLag = Math.min(8, Math.floor(data.length / 3));
      const correlations = [];
      
      for (let lag = -maxLag; lag <= maxLag; lag++) {
        let sum = 0;
        let count = 0;
        
        for (let i = 0; i < business.length; i++) {
          const j = i + lag;
          if (j >= 0 && j < housing.length) {
            sum += businessNorm[i] * housingNorm[j];
            count++;
          }
        }
        
        correlations.push({
          lag: lag,
          correlation: count > 0 ? sum / count : 0
        });
      }
      
      // Find peak
      const peak = correlations.reduce((max, curr) => {
        return Math.abs(curr.correlation) > Math.abs(max.correlation) ? curr : max;
      });
      
      return { correlations, peak };
    },
    
    // Render Vega chart (Normalized Trends)
    renderVegaChart() {
      const vegaSpec = {
        $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
        width: 'container',
        height: 300,
        data: {
          values: this.filteredData
        },
        layer: [
          {
            mark: { type: 'area', opacity: 0.3, color: '#ef4444' },
            encoding: {
              x: { 
                field: 'label', 
                type: 'ordinal', 
                title: 'Quarter',
                axis: { labelAngle: -45 }
              },
              y: { 
                field: 'expensiveBusiness', 
                type: 'quantitative', 
                title: 'Normalized Index (0-100)',
                scale: { domain: [0, 100] }
              }
            }
          },
          {
            mark: { type: 'line', color: '#ef4444', strokeWidth: 2 },
            encoding: {
              x: { field: 'label', type: 'ordinal' },
              y: { field: 'expensiveBusiness', type: 'quantitative' }
            }
          },
          {
            mark: { type: 'area', opacity: 0.3, color: '#3b82f6' },
            encoding: {
              x: { field: 'label', type: 'ordinal' },
              y: { field: 'housingCost', type: 'quantitative' }
            }
          },
          {
            mark: { type: 'line', color: '#3b82f6', strokeWidth: 2 },
            encoding: {
              x: { field: 'label', type: 'ordinal' },
              y: { field: 'housingCost', type: 'quantitative' }
            }
          }
        ],
        resolve: { scale: { y: 'shared' } }
      };
      
      embed(this.$refs.vegaChart, vegaSpec, { actions: false });
    },
    
    // Render D3 Rate of Change chart
    renderRateChart() {
      // Clear previous
      d3.select(this.$refs.rateChart).selectAll('*').remove();
      
      // Calculate rate of change
      const rateData = this.filteredData.map((d, i) => {
        if (i === 0) {
          return { 
            label: d.label, 
            businessChange: 0, 
            housingChange: 0 
          };
        }
        const prev = this.filteredData[i - 1];
        return {
          label: d.label,
          businessChange: prev.expensiveBusiness > 0 
            ? ((d.expensiveBusiness - prev.expensiveBusiness) / prev.expensiveBusiness) * 100 
            : 0,
          housingChange: prev.housingCost > 0 
            ? ((d.housingCost - prev.housingCost) / prev.housingCost) * 100 
            : 0
        };
      });
      
      // Set up dimensions
      const container = this.$refs.rateChart;
      const width = container.clientWidth;
      const height = 400;
      const margin = { top: 20, right: 120, bottom: 60, left: 60 };
      
      const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
      
      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
      
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;
      
      // Scales
      const xScale = d3.scaleBand()
        .domain(rateData.map(d => d.label))
        .range([0, innerWidth])
        .padding(0.1);
      
      const yScale = d3.scaleLinear()
        .domain([
          Math.min(-5, d3.min(rateData, d => Math.min(d.businessChange, d.housingChange))),
          Math.max(20, d3.max(rateData, d => Math.max(d.businessChange, d.housingChange)))
        ])
        .range([innerHeight, 0]);
      
      // Axes
      g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(xScale))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end');
      
      g.append('g')
        .call(d3.axisLeft(yScale));
      
      // Y-axis label
      g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -innerHeight / 2)
        .attr('y', -45)
        .attr('text-anchor', 'middle')
        .text('% Change from Previous Quarter');
      
      // Lines
      const businessLine = d3.line()
        .x(d => xScale(d.label) + xScale.bandwidth() / 2)
        .y(d => yScale(d.businessChange));
      
      const housingLine = d3.line()
        .x(d => xScale(d.label) + xScale.bandwidth() / 2)
        .y(d => yScale(d.housingChange));
      
      g.append('path')
        .datum(rateData)
        .attr('fill', 'none')
        .attr('stroke', '#ef4444')
        .attr('stroke-width', 2)
        .attr('d', businessLine);
      
      g.append('path')
        .datum(rateData)
        .attr('fill', 'none')
        .attr('stroke', '#3b82f6')
        .attr('stroke-width', 2)
        .attr('d', housingLine);
      
      // Legend
      const legend = g.append('g')
        .attr('transform', `translate(${innerWidth + 10}, 0)`);
      
      legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 10)
        .attr('y2', 10)
        .attr('stroke', '#ef4444')
        .attr('stroke-width', 2);
      
      legend.append('text')
        .attr('x', 25)
        .attr('y', 14)
        .style('font-size', '12px')
        .text('Business');
      
      legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 30)
        .attr('y2', 30)
        .attr('stroke', '#3b82f6')
        .attr('stroke-width', 2);
      
      legend.append('text')
        .attr('x', 25)
        .attr('y', 34)
        .style('font-size', '12px')
        .text('Housing');
    },
    
    // Render D3 Cross-Correlation chart
    renderCorrelationChart() {
      // Clear previous
      d3.select(this.$refs.correlationChart).selectAll('*').remove();
      
      const result = this.calculateCrossCorrelation(this.filteredData);
      const correlations = result.correlations;
      
      // Set up dimensions
      const container = this.$refs.correlationChart;
      const width = container.clientWidth;
      const height = 400;
      const margin = { top: 20, right: 20, bottom: 60, left: 60 };
      
      const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
      
      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
      
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;
      
      // Scales
      const xScale = d3.scaleBand()
        .domain(correlations.map(d => d.lag))
        .range([0, innerWidth])
        .padding(0.1);
      
      const yScale = d3.scaleLinear()
        .domain([-1, 1])
        .range([innerHeight, 0]);
      
      // Axes
      g.append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(xScale));
      
      g.append('g')
        .call(d3.axisLeft(yScale));
      
      // Axis labels
      g.append('text')
        .attr('x', innerWidth / 2)
        .attr('y', innerHeight + 45)
        .attr('text-anchor', 'middle')
        .text('Lag (quarters)');
      
      g.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -innerHeight / 2)
        .attr('y', -45)
        .attr('text-anchor', 'middle')
        .text('Correlation Coefficient');
      
      // Bars
      g.selectAll('rect')
        .data(correlations)
        .enter()
        .append('rect')
        .attr('x', d => xScale(d.lag))
        .attr('y', d => d.correlation >= 0 ? yScale(d.correlation) : yScale(0))
        .attr('width', xScale.bandwidth())
        .attr('height', d => Math.abs(yScale(d.correlation) - yScale(0)))
        .attr('fill', d => d.lag === result.peak.lag ? '#10b981' : '#94a3b8');
      
      // Zero line
      g.append('line')
        .attr('x1', 0)
        .attr('x2', innerWidth)
        .attr('y1', yScale(0))
        .attr('y2', yScale(0))
        .attr('stroke', '#666')
        .attr('stroke-dasharray', '3,3');
    },
    
    // NEW: Load real ZIP code data
    async loadRealZipData(zipCode) {
      if (!zipCode) {
        this.realZipData = null;
        // When ZIP is cleared, regenerate synthetic data
        this.generateSampleData();
        this.updateVisualizations();
        return;
      }
      
      this.isLoadingZipData = true;
      
      try {
        // Load processed temporal data
        const response = await fetch('/data/processed_temporal_data.json');
        const allData = await response.json();
        
        // Get data for this specific ZIP
        const zipData = allData[zipCode];
        
        if (!zipData) {
          console.warn(`No data found for ZIP ${zipCode}`);
          this.realZipData = null;
          this.isLoadingZipData = false;
          return;
        }
        
        // Convert yearly data (2015-2022) to quarterly format for compatibility
        const quarterlyData = this.convertYearlyToQuarterly(zipData, zipCode);
        this.realZipData = quarterlyData;
        
        // Update the fullData with real ZIP data
        this.fullData = quarterlyData;
        this.filterDataByTimeRange();
        this.updateVisualizations();
        
        console.log(`Loaded real data for ZIP ${zipCode}:`, quarterlyData.length, 'quarters');
      } catch (error) {
        console.error('Error loading ZIP data:', error);
        this.realZipData = null;
      }
      
      this.isLoadingZipData = false;
    },
    
    // NEW: Convert yearly data to quarterly format
    convertYearlyToQuarterly(yearlyData, zipCode) {
      // Create quarterly data from 2015-2022 (8 years × 4 quarters = 32 quarters)
      const quarters = [];
      const years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'];
      
      years.forEach((year, yearIndex) => {
        const yearData = yearlyData[year];
        
        if (!yearData) return;
        
        // Create 4 quarters for this year with same values
        // (Linear interpolation could be added for smoothness)
        for (let q = 0; q < 4; q++) {
          const quarterIndex = yearIndex * 4 + q;
          const quarter = q + 1;
          
          quarters.push({
            quarter: quarterIndex,
            year: parseInt(year),
            quarterLabel: quarter,
            label: `${year} Q${quarter}`,
            housingCost: yearData.housingCost || 0,
            expensiveBusiness: yearData.businessDensity || 0,
            businessCount: yearData.businessCount || 0
          });
        }
      });
      
      return quarters;
    }
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.form-range {
  cursor: pointer;
}

.alert {
  border-left: 4px solid;
}

.alert-warning {
  border-left-color: #f59e0b;
}

.alert-info {
  border-left-color: #3b82f6;
}

.alert-success {
  border-left-color: #10b981;
}
</style>