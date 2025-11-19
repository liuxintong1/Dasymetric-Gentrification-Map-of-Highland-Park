<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'

const props = defineProps({
  map: {
    type: Object,
    required: true
  },
  visible: {
    type: Boolean,
    default: true
  }
})

// Zoning color scheme - using CATEGORY field
const categoryColors = {
  // Primary categories
  'Single Family Residential': '#FFFFE0',
  'Multiple Family Residential': '#FFD700',
  'Residential Multiple Family': '#FFD700',
  'Residential-Mixed': '#8B4513',
  'Commercial': '#FF6B6B',
  'Commercial-Mixed': '#C71585',
  'Manufacturing': '#87CEEB',
  'Industrial': '#4682B4',
  'Industrial-Mixed': '#800020',
  'Hybrid Industrial': '#8B008B',
  'Public Facilities': '#7CFC00',
  'Public': '#32CD32',
  'Suburban': '#E0FFE0',
  'Open Space': '#98FB98',
  'Parking': '#D3D3D3',
  'Agricultural': '#90EE90',
  'Freeway': '#B0B0B0',
  
  // Default for unknown types
  'default': '#CCCCCC'
}

let zoningLayer = null

// Function to get color based on category
function getCategoryColor(properties) {
  // Use CATEGORY field from the data
  const category = properties.CATEGORY || 
                   properties.category ||
                   properties.ZONE_CLASS || 
                   properties.zone_class ||
                   'Unknown'
  
  return categoryColors[category] || categoryColors['default']
}

// Style function for the zoning layer
function zoningStyle(feature) {
  return {
    fillColor: getCategoryColor(feature.properties),
    fillOpacity: 0.65,
    color: '#333',
    weight: 0.5,
    opacity: 0.8
  }
}

// Popup content for each zone
function createPopupContent(properties) {
  const category = properties.CATEGORY || 
                   properties.category ||
                   'Unknown'
  
  // Get any additional useful information
  const zoneCode = properties.ZONE_CMPLT || 
                   properties.zone_code ||
                   properties.OBJECTID ||
                   ''
  
  let popupHtml = `
    <div style="font-family: Arial, sans-serif; min-width: 200px;">
      <strong style="font-size: 14px; color: #2c3e50;">Category:</strong><br>
      <span style="font-size: 13px;">${category}</span>
  `
  
  if (zoneCode) {
    popupHtml += `
      <br><br>
      <strong style="font-size: 12px; color: #666;">Zone Code:</strong><br>
      <span style="font-size: 11px; color: #666;">${zoneCode}</span>
    `
  }
  
  popupHtml += `</div>`
  
  return popupHtml
}

// Add hover effect
function onEachFeature(feature, layer) {
  // Popup on click
  layer.bindPopup(createPopupContent(feature.properties))
  
  // Hover effect
  layer.on({
    mouseover: function(e) {
      const layer = e.target
      layer.setStyle({
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
      })
      layer.bringToFront()
    },
    mouseout: function(e) {
      zoningLayer.resetStyle(e.target)
    }
  })
}

async function loadZoningData() {
  try {
    // Try multiple possible filenames
    let response
    const possibleFiles = [
      '/highland_park_zoning.geojson',
      '/highland_park_zoning.json',
      '/la_zoning_highland_park.geojson',
      '/zoning.geojson'
    ]
    
    let zoningData = null
    for (const file of possibleFiles) {
      try {
        response = await fetch(file)
        if (response.ok) {
          zoningData = await response.json()
          console.log(`✅ Loaded zoning data from: ${file}`)
          break
        }
      } catch (e) {
        // Continue to next file
      }
    }
    
    if (!zoningData) {
      throw new Error('Could not find zoning data file. Tried: ' + possibleFiles.join(', '))
    }
    
    // Log first feature to see available fields
    if (zoningData.features && zoningData.features.length > 0) {
      console.log('Sample zoning feature properties:', zoningData.features[0].properties)
    }
    
    // Create the Leaflet GeoJSON layer
    zoningLayer = L.geoJSON(zoningData, {
      style: zoningStyle,
      onEachFeature: onEachFeature
    })
    
    // Add to map if visible
    if (props.visible) {
      zoningLayer.addTo(props.map)
    }
    
    console.log(`📊 Loaded ${zoningData.features.length} zoning features`)
    
  } catch (error) {
    console.error('Error loading zoning data:', error)
    alert('Could not load zoning data. Make sure highland_park_zoning.geojson (or .json) is in the public folder.')
  }
}

// Watch visibility prop to show/hide layer
watch(() => props.visible, (visible) => {
  if (zoningLayer) {
    if (visible) {
      zoningLayer.addTo(props.map)
    } else {
      props.map.removeLayer(zoningLayer)
    }
  }
})

onMounted(() => {
  loadZoningData()
})

// Expose methods for parent component
defineExpose({
  refresh: loadZoningData,
  layer: zoningLayer
})
</script>

<template>
  <!-- This component has no visual template - it only adds layers to the map -->
  <div style="display: none;"></div>
</template>