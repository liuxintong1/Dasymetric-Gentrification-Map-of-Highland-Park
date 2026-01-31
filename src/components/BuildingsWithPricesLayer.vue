<script setup>
import { ref, onMounted, watch } from "vue";
import L from "leaflet";

const props = defineProps({
  map: {
    type: Object,
    required: true,
  },
  visible: {
    type: Boolean,
    default: true,
  },
});

let buildingsLayer = null;

// Price level colors - green to red gradient
const priceColors = {
  1: "#4CAF50", // $ - Green (cheap)
  2: "#FFEB3B", // $$ - Bright Yellow (moderate) - lighter
  3: "#F57C00", // $$$ - Dark Orange (expensive) - darker
  4: "#F44336", // $$$$ - Red (very expensive)
  null: "#cccccc", // No price data - gray
};

// Style function for building footprints with price variation
function buildingStyle(feature) {
  const priceLevel = feature.properties.price_level;
  const fillColor = priceColors[priceLevel] || priceColors[null];

  return {
    fillColor: fillColor,
    fillOpacity: 0.75,
    color: "#333333", // Dark gray border (works with all colors)
    weight: 1.5, // Slightly thicker to stand out over base layer
    opacity: 1,
  };
}

// Create popup content for each building
function createPopupContent(properties) {
  const height = properties.HEIGHT
    ? `${properties.HEIGHT.toFixed(2)} ft`
    : "N/A";
  const area = properties.AREA
    ? `${properties.AREA.toLocaleString()} sq ft`
    : "N/A";
  const buildingId = properties.BLD_ID || properties.OBJECTID || "Unknown";

  // Price information
  const price = properties.price || "Not available";
  const businessName = properties.business_name || "Unknown";
  const hasYelpData = properties.yelp_data_found;

  let popupHtml = `
    <div style="font-family: Arial, sans-serif; min-width: 240px;">
      <strong style="font-size: 14px; color: #2c3e50;">Commercial Building</strong>
      <span style="float: right; background: #4CAF50; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">PRICE DATA</span>
      <hr style="margin: 8px 0; border: none; border-top: 1px solid #ddd;">
  `;

  // Add business info
  if (hasYelpData) {
    popupHtml += `
      <div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin-bottom: 8px;">
        <strong style="font-size: 12px; color: #2c3e50;">💼 Business:</strong><br>
        <span style="font-size: 11px;">${businessName}</span><br>
        <strong style="font-size: 12px; color: #2c3e50; margin-top: 4px; display: inline-block;">Price Range:</strong>
        <span style="font-size: 16px; font-weight: bold; float: right; color: #2c3e50;">${price}</span>
      </div>
    `;
  } else {
    popupHtml += `
      <div style="background: #fff3cd; padding: 8px; border-radius: 4px; margin-bottom: 8px;">
        <span style="font-size: 11px; color: #856404;">⚠️ No business found at this location</span>
      </div>
    `;
  }

  popupHtml += `
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Building ID:</strong><br>
        <span style="font-size: 11px;">${buildingId}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Height:</strong>
        <span style="font-size: 11px; float: right;">${height}</span>
      </div>
      
      <div style="margin: 4px 0;">
        <strong style="font-size: 12px; color: #666;">Area:</strong>
        <span style="font-size: 11px; float: right;">${area}</span>
      </div>
    </div>
  `;

  return popupHtml;
}

// Add hover effects and popup
function onEachFeature(feature, layer) {
  layer.bindPopup(createPopupContent(feature.properties));

  layer.on({
    mouseover: function (e) {
      const layer = e.target;
      layer.setStyle({
        weight: 3,
        opacity: 1,
        fillOpacity: 0.95,
      });
      layer.bringToFront();
    },
    mouseout: function (e) {
      buildingsLayer.resetStyle(e.target);
    },
  });
}

async function loadBuildingData() {
  try {
    console.log("💰 Loading commercial buildings WITH PRICE DATA...");

    const response = await fetch(
      "/highland_park_commercial_buildings_with_prices.geojson"
    );

    if (!response.ok) {
      throw new Error(
        `Failed to load: ${response.status} ${response.statusText}`
      );
    }

    const buildingData = await response.json();

    // Create the Leaflet GeoJSON layer
    buildingsLayer = L.geoJSON(buildingData, {
      style: buildingStyle,
      onEachFeature: onEachFeature,
    });

    // Add to map if visible
    if (props.visible) {
      buildingsLayer.addTo(props.map);
    }

    // Summary stats
    const totalBuildings = buildingData.features.length;
    let buildingsWithPrice = 0;
    let priceDistribution = { 1: 0, 2: 0, 3: 0, 4: 0, null: 0 };

    buildingData.features.forEach((feature) => {
      const priceLevel = feature.properties.price_level;
      if (priceLevel) {
        buildingsWithPrice++;
        priceDistribution[priceLevel]++;
      } else {
        priceDistribution[null]++;
      }
    });

    console.log(`✅ Loaded ${totalBuildings} buildings WITH price data`);
    console.log(`   💰 Price data: ${buildingsWithPrice} buildings`);
    console.log(
      `   Distribution: $ (${priceDistribution[1]}), $$ (${
        priceDistribution[2]
      }), $$$ (${priceDistribution[3]}), $$$$ (${
        priceDistribution[4]
      }), No data (${priceDistribution[null]})`
    );
  } catch (error) {
    console.error("❌ Error loading buildings with price data:", error);
    console.log(
      "   ℹ️  Make sure you've run the Yelp data fetcher and the file exists in public/"
    );
  }
}

// Watch visibility prop to show/hide layer
watch(
  () => props.visible,
  (visible) => {
    if (buildingsLayer) {
      if (visible) {
        buildingsLayer.addTo(props.map);
      } else {
        props.map.removeLayer(buildingsLayer);
      }
    }
  }
);

onMounted(() => {
  loadBuildingData();
});

// Expose methods for parent component
defineExpose({
  refresh: loadBuildingData,
  layer: buildingsLayer,
});
</script>

<template>
  <div style="display: none"></div>
</template>
