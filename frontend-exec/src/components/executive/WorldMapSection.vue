<template>
  <div class="world-map-section">
    <!-- Header Section -->
    <div class="section-header">
      <h2><i class="fas fa-globe-americas"></i> World Distribution Map</h2>
      <p class="section-description">
        Interactive visualization of global content distribution across countries
      </p>
    </div>

    <!-- Map Controls -->
    <div class="map-controls">
      <div class="map-filters">
        <!-- Search Country -->
        <div class="filter-group">
          <label>
            <i class="fas fa-search"></i>
            Search Country:
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Enter country name..."
              @input="onSearchInput"
            >
          </label>
        </div>

        <!-- Country Select -->
        <div class="filter-group">
          <label>
            <i class="fas fa-flag"></i>
            Select Country:
            <select v-model="selectedCountryCode" @change="onCountrySelect">
              <option value="">All Countries</option>
              <option v-for="country in countryList" :key="country.code || country" :value="country.code || country">
                {{ country.name || country }} ({{ country.shows || 0 }})
              </option>
            </select>
          </label>
        </div>

        <div class="filter-actions">
          <button class="btn-refresh" @click="loadMapData" :disabled="loading">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i> Refresh
          </button>
          <button class="btn-reset" @click="resetFilters">
            <i class="fas fa-redo"></i> Reset
          </button>
          <button class="btn-demo" @click="useDemoData" :disabled="loading">
            <i class="fas fa-desktop"></i> Demo Data
          </button>
        </div>
      </div>
    </div>

    <!-- Map Container -->
    <div class="chart-container">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading world map data...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ error }}</p>
        <div class="error-actions">
          <button @click="loadMapData" class="btn-retry">
            <i class="fas fa-redo"></i> Retry
          </button>
          <button @click="useDemoData" class="btn-demo">
            <i class="fas fa-desktop"></i> Use Demo Data
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!mapData || mapData.length === 0" class="empty-state">
        <i class="fas fa-globe"></i>
        <p>No map data available</p>
        <button @click="useDemoData" class="btn-demo">
          <i class="fas fa-desktop"></i> Load Demo Data
        </button>
      </div>

      <!-- World Map -->
      <div v-else ref="mapContainer" class="map-wrapper">
        <!-- Map akan dirender oleh D3 di sini -->
      </div>
    </div>

    <!-- Map Stats -->
    <div v-if="mapStats && !loading" class="map-stats-panel">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-globe"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ mapStats.total_countries || mapData.length || 0 }}</div>
          <div class="stat-label">Countries</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-film"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ (mapStats.total_shows || totalShows).toLocaleString() }}</div>
          <div class="stat-label">Total Shows</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-chart-line"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ (mapStats.avg_shows || averageShows).toFixed(0) }}</div>
          <div class="stat-label">Avg Shows/Country</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="fas fa-crown"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ mapStats.top_country?.name || topCountry?.country || 'N/A' }}</div>
          <div class="stat-label">Top Country</div>
        </div>
      </div>
    </div>

    <!-- Country Details Panel -->
    <div v-if="selectedCountryData" class="country-details-panel">
      <div class="panel-header">
        <h3>
          <i class="fas fa-flag"></i>
          {{ selectedCountryData.country || selectedCountryData.name }}
          <span class="country-code">({{ getCountryCode(selectedCountryData.country || selectedCountryData.name) }})</span>
        </h3>
        <button @click="selectedCountryData = null" class="close-btn">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="panel-content">
        <div class="country-stats">
          <div class="stat-item">
            <span class="stat-label">Total Shows:</span>
            <span class="stat-value">{{ (selectedCountryData.total_shows || selectedCountryData.value || 0).toLocaleString() }}</span>
          </div>
          
          <!-- Parsed Genres -->
          <div v-if="selectedCountryData.genres?.parsed?.length > 0 || selectedCountryData.topGenres" class="stat-item">
            <span class="stat-label">Top Genres:</span>
            <div class="genre-list">
              <template v-if="selectedCountryData.genres?.parsed?.length > 0">
                <span v-for="genre in selectedCountryData.genres.parsed.slice(0, 3)" 
                      :key="genre.rank" 
                      class="genre-tag">
                  {{ genre.rank }}. {{ genre.name }} ({{ genre.shows }})
                </span>
              </template>
              <template v-else-if="selectedCountryData.topGenres">
                <span class="genre-tag">
                  {{ selectedCountryData.topGenres }}
                </span>
              </template>
            </div>
          </div>
          
          <!-- Parsed Production Companies -->
          <div v-if="selectedCountryData.production_companies?.parsed?.length > 0 || selectedCountryData.topCompanies" 
               class="stat-item">
            <span class="stat-label">Top Companies:</span>
            <div class="company-list">
              <template v-if="selectedCountryData.production_companies?.parsed?.length > 0">
                <span v-for="company in selectedCountryData.production_companies.parsed.slice(0, 3)" 
                      :key="company.rank" 
                      class="company-tag">
                  {{ company.rank }}. {{ company.company }} ({{ company.shows }})
                </span>
              </template>
              <template v-else-if="selectedCountryData.topCompanies">
                <span class="company-tag">
                  {{ selectedCountryData.topCompanies }}
                </span>
              </template>
            </div>
          </div>
        </div>

        <div class="country-actions">
          <button class="btn-action" @click="viewCountryRawData">
            <i class="fas fa-code"></i> View Raw Data
          </button>
        </div>
      </div>
    </div>

    <!-- Demo Mode Indicator -->
    <div v-if="isDemoMode" class="demo-indicator">
      <i class="fas fa-info-circle"></i>
      <span>Demo Mode - Using Sample Data</span>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import * as topojson from 'topojson-client'

// IMPORT API FUNCTIONS dari file api.js yang sudah ada
import { 
  getWorldMapData,
  getCountryMapDetails,
  getCountryList,
  getMapStatistics,
  getColorForValue,
  getCountryName,
  getCountryCode,
  parseTopItems,
  formatMapTooltip
} from '../../utils/api'

// Demo data untuk fallback
const DEMO_DATA = {
  data: [
    {
      country: 'United States',
      total_shows: 12500,
      genres: { text: '1. Drama (4500), 2. Comedy (3200), 3. Action (1800)' },
      production_companies: { text: '1. Netflix (2500), 2. Warner Bros (1800), 3. Disney (1500)' }
    },
    {
      country: 'United Kingdom',
      total_shows: 8500,
      genres: { text: '1. Drama (3200), 2. Comedy (2100), 3. Mystery (1500)' },
      production_companies: { text: '1. BBC (2000), 2. Netflix (1800), 3. ITV (1200)' }
    },
    {
      country: 'Japan',
      total_shows: 7200,
      genres: { text: '1. Anime (3500), 2. Drama (1800), 3. Romance (1200)' },
      production_companies: { text: '1. Toei Animation (1500), 2. Studio Ghibli (1200), 3. TV Tokyo (1000)' }
    },
    {
      country: 'South Korea',
      total_shows: 6800,
      genres: { text: '1. Drama (2800), 2. Romance (1800), 3. Comedy (1500)' },
      production_companies: { text: '1. CJ ENM (2000), 2. Netflix (1500), 3. SBS (1200)' }
    },
    {
      country: 'India',
      total_shows: 9500,
      genres: { text: '1. Drama (4000), 2. Romance (2500), 3. Comedy (1800)' },
      production_companies: { text: '1. Yash Raj Films (2000), 2. Dharma Productions (1500), 3. Red Chillies (1200)' }
    },
    {
      country: 'Brazil',
      total_shows: 4200,
      genres: { text: '1. Telenovela (2000), 2. Drama (1200), 3. Comedy (800)' },
      production_companies: { text: '1. Globo (1800), 2. RecordTV (800), 3. SBT (600)' }
    },
    {
      country: 'France',
      total_shows: 3800,
      genres: { text: '1. Drama (1500), 2. Comedy (1200), 3. Romance (800)' },
      production_companies: { text: '1. Canal+ (1200), 2. TF1 (1000), 3. Gaumont (800)' }
    },
    {
      country: 'Germany',
      total_shows: 3500,
      genres: { text: '1. Crime (1400), 2. Drama (1200), 3. Comedy (600)' },
      production_companies: { text: '1. ZDF (1200), 2. ARD (1000), 3. Netflix (800)' }
    },
    {
      country: 'Australia',
      total_shows: 2800,
      genres: { text: '1. Drama (1200), 2. Comedy (800), 3. Reality (600)' },
      production_companies: { text: '1. ABC (1000), 2. Seven Network (800), 3. Netflix (600)' }
    },
    {
      country: 'Canada',
      total_shows: 3200,
      genres: { text: '1. Drama (1400), 2. Comedy (1000), 3. Documentary (600)' },
      production_companies: { text: '1. CBC (1200), 2. Netflix (800), 3. Bell Media (600)' }
    }
  ],
  summary: {
    total_countries: 10,
    total_shows: 65200,
    avg_shows: 6520,
    top_country: { name: 'United States', shows: 12500 }
  }
}

// Fungsi untuk mendapatkan warna dari gradasi ungu ke pink
function getPurpleToPinkColor(value, maxValue) {
  if (!value || value === 0) return '#2a2a4a' // Warna dasar gelap
  
  const intensity = Math.min(value / maxValue, 1) // Normalize to 0-1 scale
  
  // Gradient dari ungu gelap ke pink terang
  // Warna-warna dalam format HEX:
  // #2a2a4a (ungu gelap) -> #4a2a7a -> #7B1FA2 -> #BA68C8 -> #FF6B9D (pink)
  
  if (intensity < 0.2) return '#2a2a4a'        // Ungu sangat gelap
  if (intensity < 0.4) return '#4a2a7a'        // Ungu gelap
  if (intensity < 0.6) return '#7B1FA2'        // Ungu medium
  if (intensity < 0.8) return '#BA68C8'        // Ungu muda/lavender
  return '#FF6B9D'                            // Pink cerah
}

// Fungsi interpolasi warna untuk gradient yang lebih smooth
function interpolatePurpleToPink(t) {
  // Color stops untuk gradient dari ungu ke pink
  const colorStops = [
    { pos: 0.0, color: '#2a2a4a' },   // Ungu sangat gelap
    { pos: 0.2, color: '#3a2a5a' },   // Ungu gelap
    { pos: 0.4, color: '#5a2a7a' },   // Ungu medium gelap
    { pos: 0.6, color: '#7B1FA2' },   // Ungu medium
    { pos: 0.7, color: '#9C27B0' },   // Ungu
    { pos: 0.8, color: '#BA68C8' },   // Ungu muda/lavender
    { pos: 0.9, color: '#E91E63' },   // Pink medium
    { pos: 1.0, color: '#FF6B9D' }    // Pink cerah
  ]
  
  // Cari dua warna yang mengapit nilai t
  for (let i = 1; i < colorStops.length; i++) {
    if (t <= colorStops[i].pos) {
      const prev = colorStops[i - 1]
      const next = colorStops[i]
      const ratio = (t - prev.pos) / (next.pos - prev.pos)
      
      // Interpolasi warna
      const r = Math.round(parseInt(prev.color.slice(1, 3), 16) * (1 - ratio) + parseInt(next.color.slice(1, 3), 16) * ratio)
      const g = Math.round(parseInt(prev.color.slice(3, 5), 16) * (1 - ratio) + parseInt(next.color.slice(3, 5), 16) * ratio)
      const b = Math.round(parseInt(prev.color.slice(5, 7), 16) * (1 - ratio) + parseInt(next.color.slice(5, 7), 16) * ratio)
      
      return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
    }
  }
  
  return colorStops[colorStops.length - 1].color
}

export default {
  name: 'WorldMapSection',
  
  data() {
    return {
      loading: false,
      error: null,
      mapData: [],
      mapStats: null,
      countryList: [],
      selectedCountryData: null,
      searchQuery: '',
      selectedCountryCode: '',
      isDemoMode: false,
      
      // D3 variables
      svg: null,
      width: 800,
      height: 450,
      tooltip: null,
      zoom: null,
      projection: null,
      path: null,
      g: null,
      currentScale: 1,
      initialScale: 110,
      countries: [],
      dataMap: new Map()
    }
  },

  computed: {
    totalShows() {
      if (!this.mapData || this.mapData.length === 0) return 0
      return this.mapData.reduce((sum, item) => sum + (item.total_shows || item.value || 0), 0)
    },
    
    averageShows() {
      if (!this.mapData || this.mapData.length === 0) return 0
      return Math.round(this.totalShows / this.mapData.length)
    },
    
    topCountry() {
      if (!this.mapData || this.mapData.length === 0) return null
      return this.mapData.reduce((max, item) => 
        (item.total_shows || item.value || 0) > (max.total_shows || max.value || 0) ? item : max
      )
    }
  },

  async mounted() {
    await this.loadCountryList()
    await this.loadMapData()
    
    // Initialize map after data is loaded
    this.$nextTick(() => {
      if (this.mapData && this.mapData.length > 0) {
        this.initMap()
      }
    })
  },

  beforeUnmount() {
    this.cleanupMap()
  },

  watch: {
    searchQuery(newSearch) {
      this.highlightCountry(newSearch)
    },
    
    mapData(newData) {
      if (newData && newData.length > 0) {
        this.updateDataMap()
        this.$nextTick(() => {
          if (!this.svg) {
            this.initMap()
          } else {
            this.renderMap()
          }
        })
      }
    }
  },

  methods: {
    async loadCountryList() {
      try {
        this.loading = true
        const response = await getCountryList()
        
        if (response && response.success) {
          this.countryList = response.countries || []
          // Jika response berupa array string, ubah ke format objek
          if (Array.isArray(this.countryList) && typeof this.countryList[0] === 'string') {
            this.countryList = this.countryList.map(countryCode => ({
              code: countryCode,
              name: getCountryName(countryCode),
              shows: 0
            }))
          }
        } else {
          console.warn('Failed to load country list from API, using demo data')
          this.countryList = DEMO_DATA.data.map(item => ({
            code: getCountryCode(item.country),
            name: item.country,
            shows: item.total_shows
          }))
        }
      } catch (err) {
        console.error('Error loading country list:', err)
        this.countryList = DEMO_DATA.data.map(item => ({
          code: getCountryCode(item.country),
          name: item.country,
          shows: item.total_shows
        }))
      } finally {
        this.loading = false
      }
    },

    async loadMapData() {
      try {
        this.loading = true
        this.error = null
        this.isDemoMode = false
        
        console.log('Loading map data from API...')
        
        // Coba load dari API menggunakan fungsi dari api.js
        const mapResponse = await getWorldMapData()
        
        if (mapResponse && mapResponse.success) {
          this.mapData = mapResponse.data || []
          this.mapStats = mapResponse.summary || {}
          
          console.log('Loaded map data from API:', this.mapData.length, 'countries')
          
          // Format country list berdasarkan data yang diterima
          this.updateCountryListFromData()
        } else {
          throw new Error('Failed to load data from API')
        }
        
      } catch (err) {
        console.error('Error loading map data:', err)
        this.error = 'Unable to connect to server. Please try again or use demo data.'
        this.mapData = []
        this.mapStats = null
      } finally {
        this.loading = false
      }
    },

    updateCountryListFromData() {
      if (!this.mapData || this.mapData.length === 0) return
      
      this.countryList = this.mapData.map(item => ({
        code: getCountryCode(item.country),
        name: item.country,
        shows: item.total_shows || 0
      })).sort((a, b) => b.shows - a.shows) // Sort by shows descending
    },

    useDemoData() {
      this.loading = true
      this.error = null
      this.isDemoMode = true
      
      console.log('Loading demo data...')
      
      setTimeout(() => {
        this.mapData = DEMO_DATA.data
        this.mapStats = DEMO_DATA.summary
        
        // Update country list dari demo data
        this.countryList = DEMO_DATA.data.map(item => ({
          code: getCountryCode(item.country),
          name: item.country,
          shows: item.total_shows
        })).sort((a, b) => b.shows - a.shows)
        
        console.log('Demo data loaded:', this.mapData.length, 'countries')
        this.loading = false
        
        // Update data map
        this.updateDataMap()
        
        // Initialize or update map
        this.$nextTick(() => {
          if (!this.svg) {
            this.initMap()
          } else {
            this.renderMap()
          }
        })
      }, 500)
    },

    initMap() {
      this.cleanupMap()
      
      const container = this.$refs.mapContainer
      if (!container) {
        console.warn('Map container not found, retrying...')
        setTimeout(() => {
          if (this.$refs.mapContainer) {
            this.initMap()
          }
        }, 100)
        return
      }
      
      // Clear container
      container.innerHTML = ''
      
      // Create SVG
      this.svg = d3.select(container)
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', [0, 0, this.width, this.height])
        .style('background', 'transparent')
        .style('border-radius', '10px')
        .style('overflow', 'hidden')

      this.g = this.svg.append('g')
      
      // Setup projection
      this.projection = d3.geoMercator()
        .scale(this.initialScale)
        .translate([this.width / 2, this.height / 1.5])
        .center([0, 20])
      
      this.path = d3.geoPath().projection(this.projection)
      
      // Setup zoom
      this.zoom = d3.zoom()
        .scaleExtent([0.5, 8])
        .on('zoom', (event) => {
          this.g.attr('transform', event.transform)
          this.currentScale = event.transform.k
        })
      
      this.svg.call(this.zoom)
      
      // Create tooltip
      this.createTooltip()
      
      // Load world map
      this.loadWorldMap()
    },

    cleanupMap() {
      if (this.tooltip) {
        this.tooltip.remove()
        this.tooltip = null
      }
      
      if (this.svg) {
        this.svg.remove()
        this.svg = null
      }
    },

    createTooltip() {
      d3.select('body').selectAll('.world-map-tooltip').remove()
      
      this.tooltip = d3.select('body')
        .append('div')
        .attr('class', 'world-map-tooltip')
        .style('position', 'absolute')
        .style('background', 'rgba(40, 35, 30, 0.95)')
        .style('color', 'white')
        .style('padding', '10px 14px')
        .style('border-radius', '8px')
        .style('font-size', '12px')
        .style('font-weight', '600')
        .style('pointer-events', 'none')
        .style('z-index', '99999')
        .style('opacity', 0)
        .style('border', '1px solid rgba(255, 107, 157, 0.3)')
        .style('box-shadow', '0 4px 12px rgba(0, 0, 0, 0.3)')
        .style('min-width', '140px')
        .style('backdrop-filter', 'blur(5px)')
    },

    async loadWorldMap() {
      try {
        const world = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
        this.countries = topojson.feature(world, world.objects.countries).features
        
        console.log('Loaded world countries:', this.countries.length)
        
        // Draw base map
        this.g.selectAll('.country')
          .data(this.countries)
          .enter()
          .append('path')
          .attr('class', 'country')
          .attr('d', this.path)
          .attr('fill', '#2a2a4a') // Warna dasar ungu gelap
          .attr('stroke', 'rgba(255, 255, 255, 0.15)')
          .attr('stroke-width', '0.5')
          .style('cursor', 'pointer')
          .on('mouseover', this.handleMouseOver.bind(this))
          .on('mouseout', this.handleMouseOut.bind(this))
          .on('click', this.handleCountryClick.bind(this))
        
        // Add zoom controls
        this.addZoomControls()
        
        // Add legend dengan nilai default
        this.addLegend(12500)
        
        // Render map jika ada data
        if (this.dataMap.size > 0) {
          this.renderMap()
        }
        
      } catch (error) {
        console.error('Error loading world map:', error)
        this.showErrorMessage('Failed to load world map')
      }
    },

    updateDataMap() {
      this.dataMap.clear()
      
      this.mapData.forEach(item => {
        if (item && item.country) {
          const countryCode = getCountryCode(item.country)
          const formattedData = {
            ...item,
            name: item.country,
            code: countryCode,
            value: item.total_shows || 0,
            topGenres: item.genres?.text || item.top_genres || '',
            topCompanies: item.production_companies?.text || item.top_companies || ''
          }
          
          // Store by country name and code
          this.dataMap.set(item.country.toLowerCase().trim(), formattedData)
          this.dataMap.set(countryCode.toLowerCase().trim(), formattedData)
        }
      })
      
      console.log('DataMap updated, size:', this.dataMap.size)
    },

    renderMap() {
      if (!this.g || this.dataMap.size === 0) {
        console.warn('Cannot render map: g element or data not available')
        return
      }
      
      // Calculate max value for color scale
      const values = Array.from(this.dataMap.values())
        .map(d => d.value || 0)
        .filter(v => !isNaN(v))
      
      if (values.length === 0) {
        console.warn('No valid values for color scale')
        this.clearMapColors()
        return
      }
      
      const maxValue = Math.max(...values, 1)
      
      // Create color scale dengan gradient ungu ke pink
      const colorScale = d3.scaleSequential()
        .domain([0, maxValue])
        .interpolator(t => interpolatePurpleToPink(t))
      
      // Update country colors
      this.g.selectAll('.country')
        .attr('fill', d => {
          const countryName = d.properties?.name || ''
          if (!countryName) return '#2a2a4a'
          
          const countryCode = getCountryCode(countryName)
          
          // Try to find data by code first
          const dataByCode = countryCode ? this.dataMap.get(countryCode.toLowerCase()) : null
          const dataByName = this.dataMap.get(countryName.toLowerCase())
          
          const data = dataByCode || dataByName
          
          if (data) {
            const value = data.value || 0
            return colorScale(value)
          }
          
          return '#2a2a4a'
        })
      
      // Update legend dengan warna yang sesuai
      this.updateLegend(maxValue)
    },

    updateLegend(maxValue) {
      const legend = d3.select(this.$refs.mapContainer).select('.map-legend')
      if (legend.empty()) {
        this.addLegend(maxValue)
        return
      }
      
      // Update gradient di legend
      legend.select('.legend-gradient')
        .style('background', 'linear-gradient(to top, #2a2a4a 0%, #4a2a7a 25%, #7B1FA2 50%, #BA68C8 75%, #FF6B9D 100%)')
      
      legend.select('.max-value').text(this.formatLegendValue(maxValue))
    },

    clearMapColors() {
      if (this.g) {
        this.g.selectAll('.country')
          .attr('fill', '#2a2a4a')
      }
    },

    highlightCountry(searchTerm) {
      if (!this.g || !searchTerm) return
      
      const searchLower = searchTerm.toLowerCase().trim()
      
      this.g.selectAll('.country')
        .attr('stroke', (d) => {
          const countryName = d.properties?.name || ''
          const countryCode = getCountryCode(countryName)
          
          const nameMatch = countryName.toLowerCase().includes(searchLower)
          const codeMatch = countryCode.toLowerCase().includes(searchLower)
          
          return (nameMatch || codeMatch) ? '#FF6B9D' : 'rgba(255, 255, 255, 0.15)'
        })
        .attr('stroke-width', (d) => {
          const countryName = d.properties?.name || ''
          const countryCode = getCountryCode(countryName)
          
          const nameMatch = countryName.toLowerCase().includes(searchLower)
          const codeMatch = countryCode.toLowerCase().includes(searchLower)
          
          return (nameMatch || codeMatch) ? '2.5' : '0.5'
        })
        .style('filter', (d) => {
          const countryName = d.properties?.name || ''
          const countryCode = getCountryCode(countryName)
          
          const nameMatch = countryName.toLowerCase().includes(searchLower)
          const codeMatch = countryCode.toLowerCase().includes(searchLower)
          
          return (nameMatch || codeMatch) ? 'drop-shadow(0 0 6px rgba(255, 107, 157, 0.5))' : 'none'
        })
    },

    handleMouseOver(event, d) {
      const countryName = d.properties?.name || 'Unknown'
      const countryCode = getCountryCode(countryName)
      
      // Highlight country
      d3.select(event.currentTarget)
        .attr('stroke', '#FF6B9D')
        .attr('stroke-width', '1.5')
        .style('filter', 'drop-shadow(0 0 8px rgba(255, 107, 157, 0.4))')
      
      // Find matching data
      let countryData = null
      
      if (countryCode) {
        countryData = this.dataMap.get(countryCode.toLowerCase())
      }
      
      if (!countryData) {
        countryData = this.dataMap.get(countryName.toLowerCase())
      }
      
      // Show tooltip
      if (this.tooltip) {
        if (countryData) {
          const tooltipHTML = formatMapTooltip({
            name: countryData.name || countryName,
            code: countryCode,
            value: countryData.value || 0,
            topGenres: countryData.topGenres || '',
            topCompanies: countryData.topCompanies || ''
          })
          this.tooltip
            .html(tooltipHTML)
            .style('opacity', 1)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 100) + 'px')
        } else {
          this.tooltip
            .html(`
              <div style="font-weight: bold; margin-bottom: 5px; color: #FFD1DC;">${countryName}</div>
              <div style="font-size: 10px; color: #FFB6C1;">No data available</div>
            `)
            .style('opacity', 1)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 100) + 'px')
        }
      }
    },

    handleMouseOut(event) {
      d3.select(event.currentTarget)
        .attr('stroke', 'rgba(255, 255, 255, 0.15)')
        .attr('stroke-width', '0.5')
        .style('filter', 'none')
      
      if (this.tooltip) {
        this.tooltip.style('opacity', 0)
      }
      
      // Reapply search highlight if active
      if (this.searchQuery) {
        this.highlightCountry(this.searchQuery)
      }
    },

    async handleCountryClick(event, d) {
      const countryName = d.properties?.name || 'Unknown'
      const countryCode = getCountryCode(countryName)
      
      // Find matching data
      let countryData = null
      
      if (countryCode) {
        countryData = this.dataMap.get(countryCode.toLowerCase())
      }
      
      if (!countryData) {
        countryData = this.dataMap.get(countryName.toLowerCase())
      }
      
      if (countryData) {
        try {
          // Coba load detail country dari API
          const countryNameForAPI = getCountryName(countryCode) || countryName
          const response = await getCountryMapDetails(countryNameForAPI)
          
          if (response?.success) {
            this.selectedCountryData = {
              country: response.country || countryName,
              total_shows: response.total_shows || countryData.value || 0,
              genres: response.genres || {
                text: countryData.topGenres || '',
                parsed: parseTopItems(countryData.topGenres)
              },
              production_companies: response.production_companies || {
                text: countryData.topCompanies || '',
                parsed: parseTopItems(countryData.topCompanies)
              }
            }
          } else {
            // Fallback ke data yang ada
            this.selectedCountryData = {
              country: countryData.name || countryName,
              total_shows: countryData.value || 0,
              genres: {
                text: countryData.topGenres || '',
                parsed: parseTopItems(countryData.topGenres)
              },
              production_companies: {
                text: countryData.topCompanies || '',
                parsed: parseTopItems(countryData.topCompanies)
              }
            }
          }
        } catch (error) {
          console.error('Error loading country details:', error)
          // Fallback ke data yang ada
          this.selectedCountryData = {
            country: countryData.name || countryName,
            total_shows: countryData.value || 0,
            genres: {
              text: countryData.topGenres || '',
              parsed: parseTopItems(countryData.topGenres)
            },
            production_companies: {
              text: countryData.topCompanies || '',
              parsed: parseTopItems(countryData.topCompanies)
            }
          }
        }
      } else {
        // Jika tidak ada data, buat objek minimal
        this.selectedCountryData = {
          country: countryName,
          total_shows: 0,
          genres: { text: 'No data', parsed: [] },
          production_companies: { text: 'No data', parsed: [] }
        }
      }
      
      this.selectedCountryCode = countryCode
    },

    addZoomControls() {
      const controls = d3.select(this.$refs.mapContainer)
        .append('div')
        .attr('class', 'zoom-controls')
        .style('position', 'absolute')
        .style('top', '10px')
        .style('left', '10px')
        .style('z-index', '10')
        .style('background', 'rgba(40, 35, 30, 0.8)')
        .style('padding', '8px')
        .style('border-radius', '6px')
        .style('border', '1px solid rgba(255, 107, 157, 0.2)')
        .style('backdrop-filter', 'blur(5px)')

      controls.append('button')
        .attr('class', 'zoom-btn')
        .style('width', '24px')
        .style('height', '24px')
        .style('background', 'rgba(255, 107, 157, 0.1)')
        .style('border', '1px solid rgba(255, 107, 157, 0.3)')
        .style('border-radius', '4px')
        .style('color', '#FF6B9D')
        .style('cursor', 'pointer')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('+')
        .on('click', () => {
          this.svg.transition()
            .duration(250)
            .call(this.zoom.scaleBy, 1.5)
        })

      controls.append('button')
        .attr('class', 'zoom-btn')
        .style('width', '24px')
        .style('height', '24px')
        .style('background', 'rgba(255, 107, 157, 0.1)')
        .style('border', '1px solid rgba(255, 107, 157, 0.3)')
        .style('border-radius', '4px')
        .style('color', '#FF6B9D')
        .style('cursor', 'pointer')
        .style('font-size', '14px')
        .style('font-weight', 'bold')
        .text('-')
        .on('click', () => {
          this.svg.transition()
            .duration(250)
            .call(this.zoom.scaleBy, 0.67)
        })

      controls.append('button')
        .attr('class', 'zoom-btn')
        .style('width', '24px')
        .style('height', '24px')
        .style('background', 'rgba(255, 107, 157, 0.2)')
        .style('border', '1px solid #FF6B9D')
        .style('border-radius', '4px')
        .style('color', '#FF6B9D')
        .style('cursor', 'pointer')
        .style('font-size', '12px')
        .text('↺')
        .on('click', () => {
          this.svg.transition()
            .duration(350)
            .call(this.zoom.transform, d3.zoomIdentity)
          this.currentScale = 1
        })
    },

    addLegend(maxValue) {
      d3.select(this.$refs.mapContainer).selectAll('.map-legend').remove()
      
      const legend = d3.select(this.$refs.mapContainer)
        .append('div')
        .attr('class', 'map-legend')
        .style('position', 'absolute')
        .style('top', '10px')
        .style('right', '10px')
        .style('z-index', '10')
        .style('background', 'rgba(40, 35, 30, 0.8)')
        .style('padding', '8px 10px')
        .style('border-radius', '6px')
        .style('border', '1px solid rgba(255, 107, 157, 0.2)')
        .style('backdrop-filter', 'blur(5px)')

      legend.append('div')
        .attr('class', 'legend-title')
        .style('font-size', '9px')
        .style('color', '#FFD1DC')
        .style('font-weight', '800')
        .text('SHOWS COUNT')

      const wrapper = legend.append('div')
        .style('display', 'flex')
        .style('align-items', 'center')
        .style('gap', '10px')

      wrapper.append('div')
        .attr('class', 'legend-gradient')
        .style('width', '12px')
        .style('height', '70px')
        .style('background', 'linear-gradient(to top, #2a2a4a 0%, #4a2a7a 25%, #7B1FA2 50%, #BA68C8 75%, #FF6B9D 100%)')
        .style('border-radius', '2px')
        .style('border', '1px solid rgba(255, 107, 157, 0.3)')

      const labels = wrapper.append('div')
        .style('display', 'flex')
        .style('flex-direction', 'column')
        .style('justify-content', 'space-between')
        .style('height', '70px')

      labels.append('div')
        .style('font-size', '9px')
        .style('color', '#FFB6C1')
        .style('font-weight', '600')
        .text('0')

      labels.append('div')
        .attr('class', 'max-value')
        .style('font-size', '9px')
        .style('color', '#FFB6C1')
        .style('font-weight', '600')
        .text(this.formatLegendValue(maxValue))
    },

    formatLegendValue(value) {
      if (value >= 1000000) return (value / 1000000).toFixed(1) + 'M'
      if (value >= 1000) return (value / 1000).toFixed(1) + 'K'
      return Math.round(value).toString()
    },

    showErrorMessage(message) {
      const container = this.$refs.mapContainer
      if (!container) return
      
      container.innerHTML = `
        <div style="
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #FF6B9D;
          text-align: center;
          padding: 20px;
        ">
          <div style="font-size: 32px; margin-bottom: 12px;">🗺️</div>
          <div style="font-size: 14px; font-weight: 600;">
            ${message}
          </div>
        </div>
      `
    },

    onSearchInput() {
      // Handled by watcher
    },

    async onCountrySelect() {
      if (this.selectedCountryCode) {
        try {
          const countryName = getCountryName(this.selectedCountryCode)
          const response = await getCountryMapDetails(countryName)
          
          if (response?.success) {
            this.selectedCountryData = {
              country: response.country || countryName,
              total_shows: response.total_shows || 0,
              genres: response.genres || { text: 'No data', parsed: [] },
              production_companies: response.production_companies || { text: 'No data', parsed: [] }
            }
          } else {
            // Fallback to local data
            const localData = this.mapData.find(item => 
              getCountryCode(item.country) === this.selectedCountryCode
            )
            if (localData) {
              this.selectedCountryData = {
                country: localData.country,
                total_shows: localData.total_shows || 0,
                genres: localData.genres || { text: 'No data', parsed: [] },
                production_companies: localData.production_companies || { text: 'No data', parsed: [] }
              }
            }
          }
        } catch (err) {
          console.error('Error loading country details:', err)
          // Fallback to local data
          const localData = this.mapData.find(item => 
            getCountryCode(item.country) === this.selectedCountryCode
          )
          if (localData) {
            this.selectedCountryData = {
              country: localData.country,
              total_shows: localData.total_shows || 0,
              genres: localData.genres || { text: 'No data', parsed: [] },
              production_companies: localData.production_companies || { text: 'No data', parsed: [] }
            }
          }
        }
      } else {
        this.selectedCountryData = null
      }
    },

    resetFilters() {
      this.searchQuery = ''
      this.selectedCountryCode = ''
      this.selectedCountryData = null
      this.isDemoMode = false
      this.loadMapData()
    },

    viewCountryRawData() {
      if (this.selectedCountryData) {
        console.log('Country raw data:', this.selectedCountryData)
        alert(JSON.stringify(this.selectedCountryData, null, 2))
      }
    }
  }
}
</script>

<style scoped>
.world-map-section {
  width: 100%;
  min-height: 600px;
  background: linear-gradient(145deg, 
    rgba(40, 35, 30, 0.95) 0%, 
    rgba(30, 25, 20, 0.95) 100%);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid rgba(216, 160, 165, 0.2);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  position: relative;
}

.section-header {
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 22px;
  font-weight: 700;
  color: #FFD1DC;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header h2 i {
  color: #FF6B9D;
}

.section-description {
  color: #FFB6C1;
  font-size: 13px;
  opacity: 0.8;
  line-height: 1.4;
}

.map-controls {
  margin-bottom: 20px;
  padding: 14px;
  background: rgba(50, 42, 36, 0.6);
  border-radius: 10px;
  border: 1px solid rgba(255, 107, 157, 0.15);
}

.map-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 180px;
}

.filter-group label {
  color: #FFD1DC;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-group label i {
  color: #FF6B9D;
  font-size: 12px;
}

.filter-group select,
.filter-group input {
  background: rgba(38, 32, 26, 0.9);
  border: 1px solid rgba(255, 107, 157, 0.25);
  border-radius: 5px;
  padding: 8px 10px;
  color: #FFD1DC;
  font-size: 13px;
  width: 100%;
  transition: all 0.2s ease;
}

.filter-group select:focus,
.filter-group input:focus {
  outline: none;
  border-color: #FF6B9D;
  box-shadow: 0 0 0 2px rgba(255, 107, 157, 0.15);
}

.filter-group input::placeholder {
  color: #FFB6C1;
  opacity: 0.6;
}

.filter-actions {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  margin-top: 10px;
}

.btn-refresh, .btn-reset, .btn-retry, .btn-demo {
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-refresh {
  background: linear-gradient(135deg, #FF6B9D, #BA68C8);
  color: white;
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reset {
  background: rgba(255, 107, 157, 0.1);
  color: #FF6B9D;
  border: 1px solid rgba(255, 107, 157, 0.25);
}

.btn-demo {
  background: linear-gradient(135deg, #7B1FA2, #4A148C);
  color: white;
}

.btn-retry {
  background: linear-gradient(135deg, #BA68C8, #7B1FA2);
  color: white;
}

.btn-refresh:hover:not(:disabled), 
.btn-reset:hover, 
.btn-retry:hover,
.btn-demo:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(255, 107, 157, 0.25);
}

.chart-container {
  position: relative;
  width: 100%;
  height: 450px;
  background: rgba(50, 42, 36, 0.6);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(216, 160, 165, 0.1);
}

.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.loading-state, .error-state, .empty-state {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(50, 42, 36, 0.9);
  border-radius: 12px;
  z-index: 10;
}

.loading-state p, .error-state p, .empty-state p {
  color: #FFD1DC;
  font-size: 14px;
  margin-top: 12px;
}

.error-state i, .empty-state i {
  font-size: 40px;
  color: #FF6B9D;
  margin-bottom: 12px;
}

.error-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 107, 157, 0.25);
  border-top: 3px solid #FF6B9D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.map-stats-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 20px;
  padding: 14px;
  background: rgba(50, 42, 36, 0.6);
  border-radius: 10px;
  border: 1px solid rgba(255, 107, 157, 0.15);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(38, 32, 26, 0.7);
  border-radius: 8px;
  border: 1px solid rgba(216, 160, 165, 0.1);
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-1px);
  border-color: rgba(255, 107, 157, 0.25);
  box-shadow: 0 3px 10px rgba(255, 107, 157, 0.15);
}

.stat-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.15), rgba(186, 104, 200, 0.1));
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FF6B9D;
  font-size: 16px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #FFD1DC;
  line-height: 1;
}

.stat-label {
  font-size: 11px;
  color: #FFB6C1;
  opacity: 0.8;
  margin-top: 3px;
}

.country-details-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 450px;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.98) 0%, 
    rgba(38, 32, 26, 0.98) 100%);
  border-radius: 16px;
  padding: 20px;
  border: 2px solid rgba(255, 107, 157, 0.25);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4),
              0 0 30px rgba(255, 107, 157, 0.15);
  z-index: 1000;
  backdrop-filter: blur(15px);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 107, 157, 0.2);
}

.panel-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #FFD1DC;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-header h3 i {
  color: #FF6B9D;
}

.country-code {
  font-size: 14px;
  color: #FF6B9D;
  font-weight: 600;
}

.close-btn {
  width: 32px;
  height: 32px;
  background: rgba(255, 107, 157, 0.1);
  border: 1px solid rgba(255, 107, 157, 0.25);
  border-radius: 6px;
  color: #FF6B9D;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 107, 157, 0.2);
  transform: rotate(90deg);
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.country-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px;
  background: rgba(38, 32, 26, 0.7);
  border-radius: 6px;
  border: 1px solid rgba(216, 160, 165, 0.1);
}

.stat-label {
  font-size: 11px;
  color: #FFB6C1;
  opacity: 0.8;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #FF6B9D;
}

.genre-list, .company-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 6px;
}

.genre-tag, .company-tag {
  background: rgba(255, 107, 157, 0.1);
  border: 1px solid rgba(255, 107, 157, 0.2);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 11px;
  color: #FFD1DC;
  margin-right: 4px;
  margin-bottom: 4px;
  display: inline-block;
}

.genre-tag:hover, .company-tag:hover {
  background: rgba(255, 107, 157, 0.2);
  border-color: rgba(255, 107, 157, 0.4);
}

.country-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-action {
  flex: 1;
  padding: 10px;
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.1), rgba(186, 104, 200, 0.05));
  border: 1px solid rgba(255, 107, 157, 0.25);
  border-radius: 6px;
  color: #FF6B9D;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-action:hover {
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.2), rgba(186, 104, 200, 0.1));
  border-color: #FF6B9D;
  transform: translateY(-1px);
}

.demo-indicator {
  position: absolute;
  top: 20px;
  right: 20px;
  background: linear-gradient(135deg, rgba(123, 31, 162, 0.9), rgba(74, 20, 140, 0.9));
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 100;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.demo-indicator i {
  font-size: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .map-filters {
    flex-direction: column;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .chart-container {
    height: 400px;
  }
  
  .map-stats-panel {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .country-stats {
    grid-template-columns: 1fr;
  }
  
  .country-actions {
    flex-direction: column;
  }
  
  .filter-actions {
    flex-wrap: wrap;
  }
  
  .demo-indicator {
    top: 10px;
    right: 10px;
    font-size: 10px;
    padding: 4px 8px;
  }
}

/* D3 Map Styles */
:deep(.world-map-tooltip) {
  font-family: 'Inter', system-ui, sans-serif !important;
  pointer-events: none !important;
}

:deep(.country) {
  transition: fill 0.3s ease, stroke 0.3s ease;
}

:deep(.country:hover) {
  fill-opacity: 0.9;
}

/* Custom legend gradient untuk ungu ke pink */
:deep(.legend-gradient) {
  background: linear-gradient(to top, #2a2a4a 0%, #4a2a7a 25%, #7B1FA2 50%, #BA68C8 75%, #FF6B9D 100%) !important;
}
</style>