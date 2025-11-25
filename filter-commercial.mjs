// filter-commercial.mjs
// Extracts only Commercial category from highland_park_zoning.json
// Run with: node filter-commercial.mjs

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// ES module equivalent of __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// File paths
const inputFile = path.join(__dirname, 'public', 'highland_park_zoning.json');
const outputFile = path.join(__dirname, 'public', 'highland_commercial.geojson');

console.log('🔍 Reading Highland Park zoning data...');

try {
  // Read and parse the zoning data
  const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  
  console.log(`📊 Total features in file: ${data.features.length}`);
  
  // Filter for Commercial category only
  const commercialFeatures = data.features.filter(
    feature => {
      const category = feature.properties.CATEGORY || 
                      feature.properties.category ||
                      '';
      return category === 'Commercial';
    }
  );
  
  if (commercialFeatures.length === 0) {
    console.error('❌ No Commercial features found!');
    console.log('\nAvailable categories:');
    const categories = [...new Set(data.features.map(f => 
      f.properties.CATEGORY || f.properties.category
    ))].sort();
    categories.forEach(cat => console.log(`  - ${cat}`));
    process.exit(1);
  }
  
  // Create new GeoJSON with only Commercial features
  const commercialOnly = {
    type: "FeatureCollection",
    features: commercialFeatures
  };
  
  // Write to new file
  fs.writeFileSync(
    outputFile, 
    JSON.stringify(commercialOnly, null, 2),
    'utf8'
  );
  
  console.log('\n✅ Success!');
  console.log(`📄 Created: ${outputFile}`);
  console.log(`📊 Commercial features: ${commercialFeatures.length}`);
  
  // Show file sizes
  const originalSize = fs.statSync(inputFile).size;
  const newSize = fs.statSync(outputFile).size;
  
  console.log(`\n📁 File sizes:`);
  console.log(`   Original: ${(originalSize / 1024).toFixed(2)} KB`);
  console.log(`   Commercial only: ${(newSize / 1024).toFixed(2)} KB`);
  console.log(`   Reduction: ${((1 - newSize/originalSize) * 100).toFixed(1)}%`);
  
  console.log('\n🎯 File ready to use in your map!');
  
} catch (error) {
  console.error('❌ Error:', error.message);
  
  if (error.code === 'ENOENT') {
    console.log('\n💡 Make sure highland_park_zoning.json is in the public/ folder');
    console.log(`   Looking for: ${inputFile}`);
  }
  
  process.exit(1);
}
