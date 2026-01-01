<template>
  <div class="chart-container">
    <div ref="mapContainer" class="world-map"></div>
    
    <!-- Zoom Controls -->
    <div class="zoom-controls">
      <div class="zoom-info">
        <div class="zoom-level-display">
          Zoom: {{ currentScale.toFixed(1) }}x
        </div>
        <div class="zoom-instruction">
          Scroll / Drag to navigate
        </div>
      </div>
      <div class="zoom-buttons">
        <button @click="zoomIn" class="zoom-btn" title="Zoom In">
          <span>+</span>
        </button>
        <button @click="zoomOut" class="zoom-btn" title="Zoom Out">
          <span>-</span>
        </button>
        <button @click="resetZoom" class="zoom-btn reset-btn" title="Reset Zoom">
          <span>↺</span>
        </button>
      </div>
    </div>
    
    <!-- Legend -->
    <div class="category-legend" v-if="legendData">
      <div class="legend-title">MAP LEGEND</div>
      <div class="legend-subtitle">
        Color shows total movies per country
      </div>
      <div class="legend-wrapper">
        <div class="legend-bar-wrapper">
          <div class="legend-bar">
            <div class="legend-gradient"></div>
          </div>
          <div class="legend-label bottom-label">
            <span class="label-text">0</span>
          </div>
          <div class="legend-label top-label">
            <span class="label-text">{{ formatLegendMax(legendData.maxValue) }}</span>
          </div>
        </div>
        <div class="legend-info">
          <div class="info-item">
            <div class="info-dot" style="background: #2a2a4a;"></div>
            <span>Few movies</span>
          </div>
          <div class="info-item">
            <div class="info-dot" style="background: #FF6B9D;"></div>
            <span>Many movies</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Debug Info (temporary) -->
    <div class="debug-info" v-if="debugMode">
      <div>Countries Loaded: {{ loadedCountries }}</div>
      <div>Category Type: {{ categoryType }}</div>
      <div>Sample Data: {{ sampleCountryData }}</div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import * as topojson from 'topojson-client'

export default {
  name: 'CountryCategoryMap',
  
  props: {
    chartData: {
      type: Array,
      default: () => []
    },
    categoryType: {
      type: String,
      default: 'genre'
    }
  },

  data() {
    return {
      svg: null,
      width: 800,
      height: 450,
      tooltip: null,
      countryDataMap: new Map(),
      zoom: null,
      projection: null,
      path: null,
      zoomTransform: d3.zoomIdentity,
      currentScale: 1,
      initialScale: 115,
      countriesData: null,
      legendData: null,
      g: null,
      debugMode: false, // Set to false in production
      loadedCountries: 0,
      sampleCountryData: null
    }
  },

  mounted() {
    console.log('🗺️ CountryCategoryMap Mounted')
    console.log('📊 Props received:', {
      chartData: this.chartData,
      categoryType: this.categoryType,
      dataLength: this.chartData?.length || 0
    })
    
    if (this.chartData && this.chartData.length > 0) {
      console.log('📊 First country sample:', this.chartData[0])
      this.sampleCountryData = JSON.stringify(this.chartData[0], null, 2)
      this.loadedCountries = this.chartData.length
    }
    
    this.$nextTick(() => {
      this.createTooltip()
      this.renderWorldMap()
    })
  },

  watch: {
    chartData: {
      handler(newData) {
        console.log('🔄 chartData updated:', {
          length: newData?.length || 0,
          sample: newData?.[0]
        })
        
        this.loadedCountries = newData?.length || 0
        if (newData && newData.length > 0) {
          this.sampleCountryData = JSON.stringify(newData[0], null, 2)
        }
        
        this.clearMap()
        if (newData && newData.length > 0) {
          this.renderWorldMap()
        } else {
          this.showMessage('No country data available', 'info')
        }
      },
      deep: true,
      immediate: true
    },
    categoryType() {
      console.log('🔄 categoryType changed to:', this.categoryType)
      this.renderWorldMap()
    }
  },

  methods: {
    formatLegendMax(value) {
      if (!value && value !== 0) return '0'
      if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + 'M'
      }
      if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'k'
      }
      return value.toString()
    },

    createTooltip() {
      d3.select("body").selectAll(".world-map-tooltip").remove()
      
      this.tooltip = d3.select("body")
        .append("div")
        .attr("class", "world-map-tooltip category-map-tooltip")
        .style("position", "absolute")
        .style("background", "rgba(50, 42, 36, 0.98)")
        .style("color", "white")
        .style("padding", "16px 20px")
        .style("border-radius", "14px")
        .style("font-family", "'Inter', system-ui, sans-serif")
        .style("font-size", "13px")
        .style("font-weight", "500")
        .style("pointer-events", "none")
        .style("z-index", "99999")
        .style("opacity", 0)
        .style("border", "2px solid #FF6B9D")
        .style("box-shadow", "0 15px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 107, 157, 0.4)")
        .style("min-width", "240px")
        .style("max-width", "320px")
        .style("text-align", "left")
        .style("backdrop-filter", "blur(15px)")
    },

    clearMap() {
      if (this.svg) {
        d3.select(this.$refs.mapContainer).selectAll("*").remove()
        this.svg = null
      }
      this.zoom = null
      this.projection = null
      this.path = null
      this.zoomTransform = d3.zoomIdentity
      this.currentScale = 1
      this.countriesData = null
      this.legendData = null
      this.g = null
    },

    async renderWorldMap() {
      console.log('🗺️ Rendering world map...')
      console.log('📊 Current chartData:', this.chartData)
      
      if (!this.chartData || this.chartData.length === 0) {
        console.warn('⚠️ No chartData available')
        this.showMessage('No country data available. Please select a year range.', 'info')
        return
      }

      const container = this.$refs.mapContainer
      if (!container) {
        console.error('❌ Map container not found')
        return
      }
      
      this.clearMap()
      
      // Create country map for quick lookup
      const countryMap = new Map()
      this.chartData.forEach(item => {
        if (item.name) {
          const countryKey = item.name.toLowerCase().trim()
          countryMap.set(countryKey, item)
          console.log(`📍 Country data for ${item.name}:`, {
            total_movies: item.total_movies,
            top_categories: item.top_categories?.length || 0,
            others_count: item.others_count
          })
        }
      })
      
      // Calculate max value for legend
      const maxValue = Math.max(...this.chartData.map(d => d.total_movies || d.value || 0), 1)
      this.legendData = { maxValue: maxValue }
      
      console.log(`📊 Country map created with ${countryMap.size} countries`)
      console.log(`📊 Max value for legend: ${maxValue}`)
      
      // Create SVG
      this.svg = d3.select(container)
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", [0, 0, this.width, this.height])
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("background", "linear-gradient(145deg, rgba(50, 42, 36, 0.95) 0%, rgba(38, 32, 26, 0.95) 100%)")
        .style("border-radius", "18px")
        .style("border", "2px solid rgba(216, 160, 165, 0.15)")
        .style("box-shadow", "0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)")
        .style("cursor", "grab")

      try {
        // Load world map data
        const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json")
        this.countriesData = topojson.feature(world, world.objects.countries).features
        
        console.log(`🗺️ Loaded ${this.countriesData.length} countries from world atlas`)
        
        // Create color scale (blue to pink based on total movies)
        const colorScale = d3.scaleSequential()
          .domain([0, maxValue])
          .interpolator(t => {
            // Gradient from dark blue to pink
            const colors = [
              "#2a2a4a",   // Dark blue
              "#3a2a5a",
              "#5a2a7a",
              "#7B1FA2",   // Purple
              "#BA68C8",   // Light purple
              "#EC407A",   // Pink
              "#FF6B9D",   // Hot pink
              "#FF4081"    // Bright pink
            ]
            return d3.interpolateRgbBasis(colors)(t)
          })

        // Create map container group
        this.g = this.svg.append("g")
          .attr("class", "map-container")

        // Set up projection
        this.projection = d3.geoMercator()
          .scale(this.initialScale)
          .translate([this.width / 2, this.height / 1.5])
          .center([0, 20])

        this.path = d3.geoPath().projection(this.projection)

        // Set up zoom
        this.zoom = d3.zoom()
          .scaleExtent([0.5, 8])
          .translateExtent([
            [-this.width * 0.5, -this.height * 0.5],
            [this.width * 1.5, this.height * 1.5]
          ])
          .on("zoom", (event) => {
            this.handleZoom(event)
          })

        this.svg.call(this.zoom)

        // Draw countries
        this.drawCountries(countryMap, colorScale)

        console.log('✅ World map rendered successfully!')

      } catch (error) {
        console.error('❌ Error rendering world map:', error)
        this.showMessage('Error loading world map. Please check your internet connection.', 'error')
      }
    },

    drawCountries(countryMap, colorScale) {
      console.log('🎨 Drawing countries...')
      
      const countryPaths = this.g.selectAll(".country")
        .data(this.countriesData)
        .enter()
        .append("path")
        .attr("class", "country")
        .attr("d", this.path)
        .attr("fill", d => this.getCountryColor(d, countryMap, colorScale))
        .attr("stroke", "rgba(255, 255, 255, 0.1)")
        .attr("stroke-width", 0.8)
        .style("cursor", "pointer")
        .style("transition", "fill 0.3s ease, stroke 0.3s ease")

      // Add hover events
      this.addCountryEvents(countryPaths, countryMap)
      
      console.log(`✅ Drew ${countryPaths.size()} countries`)
    },

    getCountryColor(d, countryMap, colorScale) {
      const countryName = d.properties?.name || ''
      if (!countryName) {
        return "#2a2a4a" // Default dark blue for no data
      }
      
      const lowerName = countryName.toLowerCase()
      const countryData = countryMap.get(lowerName)
      
      if (!countryData) {
        console.log(`❌ No data found for country: ${countryName}`)
        return "#2a2a4a" // Default dark blue
      }
      
      const totalMovies = countryData.total_movies || 0
      console.log(`🎨 Color for ${countryName}: total_movies=${totalMovies}`)
      
      return colorScale(totalMovies)
    },

    handleZoom(event) {
      this.zoomTransform = event.transform
      this.currentScale = event.transform.k
      
      this.g.attr("transform", event.transform)
      
      const strokeWidth = event.transform.k > 3 ? 0.5 : 0.8
      this.g.selectAll(".country")
        .attr("stroke-width", strokeWidth)
    },

    addCountryEvents(countryPaths, countryMap) {
      console.log('🖱️ Adding hover events to countries...')
      
      countryPaths.on("mouseover", (event, d) => {
        const countryName = d.properties?.name || 'Unknown'
        const lowerName = countryName.toLowerCase()
        const countryData = countryMap.get(lowerName)
        
        console.log(`🖱️ Hover over ${countryName}:`, countryData)
        
        if (countryData && this.tooltip) {
          // Highlight country
          d3.select(event.currentTarget)
            .attr("stroke", "#FF6B9D")
            .attr("stroke-width", this.currentScale > 3 ? "2" : "3")
            .style("filter", "drop-shadow(0 0 15px rgba(255, 107, 157, 0.6))")

          // Prepare tooltip content
          let categoriesHTML = ''
          const topCategories = countryData.top_categories || []
          const othersCount = countryData.others_count || 0
          
          console.log(`📋 ${countryName} data:`, {
            total_movies: countryData.total_movies,
            top_categories_count: topCategories.length,
            others_count: othersCount
          })
          
          if (topCategories.length > 0) {
            categoriesHTML = `
              <div style="margin: 12px 0;">
                <div style="font-size: 11px; color: #FFB6C1; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">
                  Top 3 ${this.categoryType}:
                </div>
                ${topCategories.map(cat => `
                  <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding: 3px 0;">
                    <span style="color: #FFD1DC; font-size: 12px;">${cat.value || cat.name}</span>
                    <span style="color: #FF6B9D; font-weight: 700; font-size: 12px;">${(cat.count || 0).toLocaleString()}</span>
                  </div>
                `).join('')}
                ${othersCount > 0 ? `
                  <div style="display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255, 107, 157, 0.2);">
                    <span style="color: #BA68C8; font-style: italic; font-size: 12px;">Others</span>
                    <span style="color: #BA68C8; font-weight: 700; font-size: 12px;">${othersCount.toLocaleString()}</span>
                  </div>
                ` : ''}
              </div>
            `
          } else if (countryData.has_data === false) {
            categoriesHTML = `
              <div style="margin: 12px 0; padding: 10px; background: rgba(255, 107, 157, 0.1); border-radius: 8px; border: 1px solid rgba(255, 107, 157, 0.2);">
                <div style="font-size: 11px; color: #FFB6C1; text-align: center;">
                  No ${this.categoryType} data available for this country
                </div>
              </div>
            `
          }

          // Create tooltip HTML
          const tooltipHTML = `
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
              <div style="
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #FF6B9D, #BA68C8);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                color: white;
                font-weight: 900;
              ">
                ${countryData.code?.substring(0, 2) || countryName.substring(0, 2).toUpperCase()}
              </div>
              <div>
                <div style="font-size: 16px; color: #FFD1DC; font-weight: 900; line-height: 1.1;">
                  ${countryName}
                </div>
                <div style="font-size: 11px; color: #FFB6C1; opacity: 0.9; margin-top: 3px;">
                  Total Movies: <span style="color: #FF6B9D; font-weight: 700;">${(countryData.total_movies || 0).toLocaleString()}</span>
                </div>
              </div>
            </div>
            
            ${categoriesHTML}
            
            <div style="
              background: linear-gradient(135deg, rgba(255, 107, 157, 0.1), rgba(186, 104, 200, 0.05));
              border-radius: 8px;
              padding: 8px 10px;
              margin-top: 12px;
              border: 1px solid rgba(255, 107, 157, 0.2);
              font-size: 10px;
              color: #FFB6C1;
              text-align: center;
            ">
              Showing: <span style="color: #BA68C8; font-weight: 600;">${this.categoryType.toUpperCase()}</span>
            </div>
          `

          // Show tooltip
          this.tooltip
            .html(tooltipHTML)
            .style("opacity", 1)
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 200) + "px")
            
          console.log(`✅ Tooltip shown for ${countryName}`)
        } else {
          console.log(`❌ No data found for ${countryName}`)
        }
      })

      countryPaths.on("mousemove", (event) => {
        if (this.tooltip) {
          this.tooltip
            .style("left", (event.pageX + 15) + "px")
            .style("top", (event.pageY - 200) + "px")
        }
      })

      countryPaths.on("mouseout", (event) => {
        d3.select(event.currentTarget)
          .attr("stroke", "rgba(255, 255, 255, 0.1)")
          .attr("stroke-width", this.currentScale > 3 ? "0.5" : "0.8")
          .style("filter", "none")
          
        if (this.tooltip) {
          this.tooltip.style("opacity", 0)
        }
      })
    },

    zoomIn() {
      if (this.svg && this.zoom) {
        this.svg.transition()
          .duration(250)
          .ease(d3.easeCubic)
          .call(this.zoom.scaleBy, 1.5)
      }
    },

    zoomOut() {
      if (this.svg && this.zoom) {
        this.svg.transition()
          .duration(250)
          .ease(d3.easeCubic)
          .call(this.zoom.scaleBy, 0.67)
      }
    },

    resetZoom() {
      if (this.svg && this.zoom) {
        this.svg.transition()
          .duration(350)
          .ease(d3.easeCubicOut)
          .call(this.zoom.transform, d3.zoomIdentity)
        this.currentScale = 1
      }
    },

    showMessage(message, type = 'info') {
      const container = this.$refs.mapContainer
      
      const color = type === 'error' ? '#FF6B9D' : '#FF6B9D'
      
      container.innerHTML = `
        <div style="
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100%;
          background: linear-gradient(145deg, rgba(50, 42, 36, 0.95) 0%, rgba(38, 32, 26, 0.95) 100%);
          color: ${color};
          text-align: center;
          padding: 40px;
          border-radius: 18px;
          border: 2px solid rgba(216, 160, 165, 0.15);
        ">
          <div style="font-size: 48px; margin-bottom: 20px;">🗺️</div>
          <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">
            ${message}
          </div>
        </div>
      `
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  min-height: 320px;
}

.world-map {
  width: 100%;
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
}

.zoom-controls {
  position: absolute;
  top: 15px;
  left: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
  background: rgba(50, 42, 36, 0.85);
  padding: 12px;
  border-radius: 12px;
  border: 1px solid rgba(255, 107, 157, 0.3);
  backdrop-filter: blur(10px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  min-width: 120px;
}

.zoom-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 8px;
}

.zoom-level-display {
  font-size: 12px;
  color: #FF6B9D;
  font-weight: 700;
  text-align: center;
  padding: 4px 8px;
  background: rgba(255, 107, 157, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 157, 0.2);
}

.zoom-instruction {
  font-size: 9px;
  color: #FFB6C1;
  text-align: center;
  opacity: 0.8;
  font-weight: 500;
}

.zoom-buttons {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.zoom-btn {
  width: 32px;
  height: 32px;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95), 
    rgba(38, 32, 26, 0.95));
  border: 2px solid rgba(255, 107, 157, 0.4);
  border-radius: 6px;
  color: #FF6B9D;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

.zoom-btn:hover {
  background: linear-gradient(145deg, 
    rgba(255, 107, 157, 0.2), 
    rgba(186, 104, 200, 0.15));
  border-color: #FF6B9D;
  transform: translateY(-2px);
  box-shadow: 0 5px 12px rgba(255, 107, 157, 0.3);
}

.zoom-btn:active {
  transform: translateY(0);
}

.zoom-btn.reset-btn {
  background: linear-gradient(145deg, 
    rgba(186, 104, 200, 0.2), 
    rgba(152, 57, 68, 0.15));
  border-color: rgba(186, 104, 200, 0.5);
  color: #BA68C8;
}

.zoom-btn.reset-btn:hover {
  background: linear-gradient(145deg, 
    rgba(186, 104, 200, 0.3), 
    rgba(152, 57, 68, 0.2));
  border-color: #BA68C8;
}

.category-legend {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10;
  background: rgba(50, 42, 36, 0.9);
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid rgba(255, 107, 157, 0.4);
  backdrop-filter: blur(15px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  min-width: 140px;
  display: flex;
  flex-direction: column;
}

.legend-title {
  font-size: 10px;
  color: #FF6B9D;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  text-align: center;
  margin-bottom: 6px;
  width: 100%;
}

.legend-subtitle {
  font-size: 9px;
  color: #FFB6C1;
  text-align: center;
  margin-bottom: 12px;
  padding: 3px 6px;
  background: rgba(255, 107, 157, 0.1);
  border-radius: 4px;
  border: 1px solid rgba(255, 107, 157, 0.2);
}

.legend-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.legend-bar-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100px;
}

.legend-bar {
  width: 18px;
  height: 80px;
  background: linear-gradient(to top, 
    #2a2a4a 0%,
    #3a2a5a 20%,
    #5a2a7a 40%,
    #7B1FA2 60%,
    #BA68C8 80%,
    #FF6B9D 100%
  );
  border-radius: 4px;
  border: 1px solid rgba(255, 107, 157, 0.8);
  position: relative;
  overflow: hidden;
  margin: 0 15px;
}

.legend-gradient {
  width: 100%;
  height: 100%;
}

.legend-label {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: center;
  pointer-events: none;
}

.bottom-label {
  bottom: 0;
  align-items: flex-end;
  height: 20px;
}

.top-label {
  top: 5px;
  align-items: flex-start;
  height: 20px;
}

.label-text {
  font-size: 9px;
  color: #FFB6C1;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
}

.bottom-label .label-text {
  transform: translateY(8px);
}

.top-label .label-text {
  transform: translateY(-8px);
}

.legend-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 9px;
  color: #FFD1DC;
}

.info-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.debug-info {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
  z-index: 100;
  max-width: 300px;
  max-height: 200px;
  overflow: auto;
}
</style>

<style>
.category-map-tooltip {
  pointer-events: none !important;
}

.country:hover {
  stroke: #FF6B9D !important;
  filter: drop-shadow(0 0 15px rgba(255, 107, 157, 0.6)) !important;
  transition: all 0.2s ease !important;
}

.world-map svg:active {
  cursor: grabbing !important;
}

.world-map svg {
  touch-action: none;
}

.map-container {
  transition: transform 0.3s ease;
}
</style>