import fs from 'fs'
import path from 'path'

const DATA_DIR = './public/data'
const OUTPUT_FILE = path.join(DATA_DIR, 'processed_temporal_data.json')

async function loadData() {
  console.log('Loading raw data files...')

  const loadJSON = (filePath) => {
    try {
      const data = fs.readFileSync(path.join(DATA_DIR, filePath), 'utf-8')
      return JSON.parse(data)
    } catch (error) {
      console.warn(`Could not load ${filePath}:`, error.message)
      return null
    }
  }

  // Special handling for business data due to NaN values
  const loadBusinessData = () => {
    try {
      let data = fs.readFileSync(path.join(DATA_DIR, 'business_la_county_by_zip.json'), 'utf-8')
      // Replace NaN with null
      data = data.replace(/NaN/g, 'null')
      return JSON.parse(data)
    } catch (error) {
      console.warn('Could not load business data:', error.message)
      return {}
    }
  }

  return {
    housing: loadJSON('zillow_housing_by_zip.json') || {},
    reviews: loadJSON('la_county_zip_review_records.json') || [],
    business: loadBusinessData(),
    geojson: loadJSON('la_zip_codes.json') || { type: 'FeatureCollection', features: [] }
  }
}

function processRawData(housingData, reviewRecords, businessData = {}) {
  console.log('Processing data...')
  const processed = {}

  // Process housing data
  Object.entries(housingData).forEach(([zipCode, zipData]) => {
    if (!processed[zipCode]) {
      processed[zipCode] = {}
    }

    const timeSeries = zipData.time_series || {}

    // Aggregate monthly data into yearly averages
    for (let year = 2010; year <= 2025; year++) {
      const yearStr = year.toString()
      const monthlyValues = []

      Object.entries(timeSeries).forEach(([dateStr, value]) => {
        const date = new Date(dateStr)
        if (date.getFullYear() === year && value !== null && !isNaN(value)) {
          monthlyValues.push(value)
        }
      })

      if (!processed[zipCode][yearStr]) {
        processed[zipCode][yearStr] = {}
      }

      // Calculate annual average or use first available value
      if (monthlyValues.length > 0) {
        processed[zipCode][yearStr].housingCost =
          monthlyValues.reduce((a, b) => a + b, 0) / monthlyValues.length
      } else {
        // Use previous year's value or first available value
        const prevYear = (year - 1).toString()
        if (processed[zipCode][prevYear]?.housingCost) {
          processed[zipCode][yearStr].housingCost = processed[zipCode][prevYear].housingCost
        } else {
          // Find first available value in time series
          const firstValue = Object.values(timeSeries).find(v => v !== null && !isNaN(v))
          processed[zipCode][yearStr].housingCost = firstValue || 0
        }
      }
    }
  })

  // Process business density from business registry (if available)
  if (businessData && Object.keys(businessData).length > 0) {
    console.log('Processing business registry data...')
    let totalBusinesses = 0

    Object.entries(businessData).forEach(([zipCode, businesses]) => {
      if (!Array.isArray(businesses)) return

      if (!processed[zipCode]) {
        processed[zipCode] = {}
      }

      // Count businesses by year based on their start/end dates
      for (let year = 2010; year <= 2025; year++) {
        const yearStr = year.toString()

        if (!processed[zipCode][yearStr]) {
          processed[zipCode][yearStr] = {}
        }

        // Count active businesses in this year
        const activeBusinesses = businesses.filter(business => {
          if (!business.LOCATION_START_DATE) return false

          const startDate = new Date(business.LOCATION_START_DATE)
          const endDate = business.LOCATION_END_DATE === 'NaT' ||
                         business.LOCATION_END_DATE === null ||
                         !business.LOCATION_END_DATE
            ? new Date('2025-12-31')
            : new Date(business.LOCATION_END_DATE)

          const yearStart = new Date(`${year}-01-01`)
          const yearEnd = new Date(`${year}-12-31`)

          // Business is active if it started before year end and ended after year start
          return startDate <= yearEnd && endDate >= yearStart
        })

        processed[zipCode][yearStr].businessDensity = activeBusinesses.length
        processed[zipCode][yearStr].businessCount = activeBusinesses.length
        totalBusinesses += activeBusinesses.length
      }
    })

    console.log(`✓ Processed ${totalBusinesses} total business records`)
  } else {
    console.log('No business registry data, using review records only')
  }

  // Process business density from review records
  reviewRecords.forEach(record => {
    const zipCode = record.postal_code.toString()
    const year = record.year.toString()

    if (!processed[zipCode]) {
      processed[zipCode] = {}
    }

    if (!processed[zipCode][year]) {
      processed[zipCode][year] = {}
    }

    // Add review metrics
    processed[zipCode][year].avgRating = record.avg_rating || 0
    processed[zipCode][year].reviewCount = record.review_count || 0

    // Only use review count if we don't have business registry data
    if (!processed[zipCode][year].businessDensity) {
      // Multiply by 50 to make patterns visible
      processed[zipCode][year].businessDensity = (record.business_count || 0) * 50
      processed[zipCode][year].businessCount = record.business_count || 0
    }
  })

  // Fill in missing business density values with 0
  Object.keys(processed).forEach(zipCode => {
    for (let year = 2010; year <= 2025; year++) {
      const yearStr = year.toString()
      if (processed[zipCode][yearStr] && processed[zipCode][yearStr].businessDensity === undefined) {
        processed[zipCode][yearStr].businessDensity = 0
      }
    }
  })

  console.log('Processed data sample:', {
    totalZips: Object.keys(processed).length,
    sampleZip: Object.keys(processed)[0],
    sampleData: processed[Object.keys(processed)[0]]
  })

  return processed
}

async function main() {
  try {
    const data = await loadData()

    console.log('Data loaded:')
    console.log(`  - Housing ZIPs: ${Object.keys(data.housing).length}`)
    console.log(`  - Review records: ${data.reviews.length}`)
    console.log(`  - Business ZIPs: ${Object.keys(data.business).length}`)
    console.log(`  - GeoJSON features: ${data.geojson.features.length}`)

    // Get valid ZIP codes from GeoJSON
    const validZips = new Set(data.geojson.features.map(f => f.properties.ZIPCODE.toString()))
    console.log(`\nFiltering to ${validZips.size} ZIPs in GeoJSON...`)

    // Filter input data to only include ZIPs in GeoJSON
    const filteredHousing = {}
    Object.entries(data.housing).forEach(([zip, value]) => {
      if (validZips.has(zip)) {
        filteredHousing[zip] = value
      }
    })

    const filteredReviews = data.reviews.filter(r => validZips.has(r.postal_code.toString()))

    const filteredBusiness = {}
    Object.entries(data.business).forEach(([zip, value]) => {
      if (validZips.has(zip)) {
        filteredBusiness[zip] = value
      }
    })

    console.log('Filtered data:')
    console.log(`  - Housing ZIPs: ${Object.keys(filteredHousing).length}`)
    console.log(`  - Review records: ${filteredReviews.length}`)
    console.log(`  - Business ZIPs: ${Object.keys(filteredBusiness).length}`)

    const processed = processRawData(filteredHousing, filteredReviews, filteredBusiness)

    console.log(`\nSaving processed data to ${OUTPUT_FILE}...`)
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(processed, null, 2))

    console.log('✓ Data processing complete!')
    console.log(`✓ File size: ${(fs.statSync(OUTPUT_FILE).size / 1024 / 1024).toFixed(2)} MB`)
  } catch (error) {
    console.error('Error processing data:', error)
    // eslint-disable-next-line no-undef
    process.exit(1)
  }
}

main()
