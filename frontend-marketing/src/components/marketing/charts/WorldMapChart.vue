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
    
    <!-- Scale Legend - POSISI 4.9M DIPERBAIKI -->
    <div class="scale-legend" v-if="legendData">
      <div class="legend-title">SCALE</div>
      <div class="legend-wrapper">
        <div class="legend-bar-wrapper">
          <!-- Bar gradient -->
          <div class="legend-bar">
            <div class="legend-gradient"></div>
          </div>
          
          <!-- Label 0 di BAWAH - POSISI SUDAH PAS -->
          <div class="legend-label bottom-label">
            <span class="label-text">0</span>
          </div>
          
          <!-- Label max di ATAS - DINAIKKAN POSISINYA -->
          <div class="legend-label top-label">
            <span class="label-text">{{ formatLegendMax(legendData.maxValue) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import * as topojson from 'topojson-client'

export default {
  name: 'WorldMapChart',
  
  props: {
    chartData: {
      type: Array,
      default: () => []
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
      g: null
    }
  },

  mounted() {
    console.log('🗺️ Mounted with data:', this.chartData)
    this.$nextTick(() => {
      this.createTooltip()
      this.renderWorldMap()
    })
  },

  watch: {
    chartData: {
      handler(newData) {
        console.log('🔄 Data updated:', newData)
        this.clearMap()
        if (newData && newData.length > 0) {
          this.renderWorldMap()
        }
      },
      deep: true
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
        .attr("class", "world-map-tooltip")
        .style("position", "absolute")
        .style("background", "rgba(50, 42, 36, 0.98)")
        .style("color", "white")
        .style("padding", "14px 18px")
        .style("border-radius", "12px")
        .style("font-family", "'Inter', system-ui, sans-serif")
        .style("font-size", "14px")
        .style("font-weight", "700")
        .style("pointer-events", "none")
        .style("z-index", "99999")
        .style("opacity", 0)
        .style("border", "2px solid #FF6B9D")
        .style("box-shadow", "0 12px 35px rgba(0, 0, 0, 0.5), 0 0 25px rgba(255, 107, 157, 0.4)")
        .style("min-width", "170px")
        .style("text-align", "center")
        .style("backdrop-filter", "blur(12px)")
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
      console.log('🗺️ Rendering map with adjusted scale legend...')
      
      if (!this.chartData || this.chartData.length === 0) {
        this.showMessage('No country data available', 'info')
        return
      }

      const container = this.$refs.mapContainer
      if (!container) return
      
      this.clearMap()
      
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
        const world = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json")
        this.countriesData = topojson.feature(world, world.objects.countries).features
        
        const nameToDataMap = new Map()
        this.chartData.forEach(item => {
          const countryName = (item.name || item.Country || '').toLowerCase().trim()
          const value = Number(item.value || item.TotalMovies || 0)
          
          if (countryName && value > 0) {
            nameToDataMap.set(countryName, {
              originalName: item.name || item.Country || 'Unknown',
              value: value,
              code: item.code || 'XX'
            })
          }
        })

        const values = Array.from(nameToDataMap.values()).map(d => d.value)
        const maxValue = Math.max(...values, 1)
        
        this.legendData = { maxValue: maxValue }
        
        this.g = this.svg.append("g")
          .attr("class", "map-container")

        this.projection = d3.geoMercator()
          .scale(this.initialScale)
          .translate([this.width / 2, this.height / 1.5])
          .center([0, 20])

        this.path = d3.geoPath().projection(this.projection)

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

        const colorScale = d3.scaleSequential()
          .domain([0, maxValue])
          .interpolator(t => {
            const colors = [
              "#2a2a4a",
              "#3a2a5a",
              "#5a2a7a",
              "#7B1FA2",
              "#BA68C8",
              "#EC407A",
              "#FF6B9D",
              "#FF4081"
            ]
            return d3.interpolateRgbBasis(colors)(t)
          })

        this.drawCountries(nameToDataMap, colorScale)

        console.log('✅ Map with adjusted scale legend rendered!')

      } catch (error) {
        console.error('❌ Error:', error)
        this.showMessage('Error loading world map', 'error')
      }
    },

    drawCountries(nameToDataMap, colorScale) {
      const countryPaths = this.g.selectAll(".country")
        .data(this.countriesData)
        .enter()
        .append("path")
        .attr("class", "country")
        .attr("d", this.path)
        .attr("fill", d => this.getCountryColor(d, nameToDataMap, colorScale))
        .attr("stroke", "rgba(255, 255, 255, 0.1)")
        .attr("stroke-width", 0.8)
        .style("cursor", "pointer")
        .style("transition", "fill 0.3s ease, stroke 0.3s ease")

      this.addCountryEvents(countryPaths, nameToDataMap)
    },

    getCountryColor(d, nameToDataMap, colorScale) {
      const countryName = d.properties?.name || ''
      if (!countryName) return "#2a2a4a"
      
      const lowerName = countryName.toLowerCase()
      let data = nameToDataMap.get(lowerName)
      
      if (!data) {
        for (const [key, value] of nameToDataMap.entries()) {
          if (lowerName.includes(key) || key.includes(lowerName)) {
            data = value
            break
          }
        }
      }
      
      return data ? colorScale(data.value) : "#2a2a4a"
    },

    handleZoom(event) {
      this.zoomTransform = event.transform
      this.currentScale = event.transform.k
      
      this.g.attr("transform", event.transform)
      
      const strokeWidth = event.transform.k > 3 ? 0.5 : 0.8
      this.g.selectAll(".country")
        .attr("stroke-width", strokeWidth)
    },

    addCountryEvents(countryPaths, nameToDataMap) {
      countryPaths.on("mouseover", (event, d) => {
        const countryName = d.properties?.name || 'Unknown'
        const lowerName = countryName.toLowerCase()
        
        let countryData = nameToDataMap.get(lowerName)
        
        if (!countryData) {
          for (const [key, value] of nameToDataMap.entries()) {
            if (lowerName.includes(key) || key.includes(lowerName)) {
              countryData = value
              break
            }
          }
        }
        
        if (countryData && this.tooltip) {
          d3.select(event.currentTarget)
            .attr("stroke", "#FF6B9D")
            .attr("stroke-width", this.currentScale > 3 ? "2" : "3")
            .style("filter", "drop-shadow(0 0 15px rgba(255, 107, 157, 0.6))")

          this.tooltip
            .html(`
              <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <div style="
                  width: 32px;
                  height: 32px;
                  background: linear-gradient(135deg, #FF6B9D, #BA68C8);
                  border-radius: 8px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  font-size: 14px;
                  color: white;
                  font-weight: 900;
                ">
                  ${countryData.code.substring(0, 2)}
                </div>
                <div>
                  <div style="font-size: 15px; color: #FFD1DC; font-weight: 900; line-height: 1.1;">
                    ${countryData.originalName}
                  </div>
                  <div style="font-size: 11px; color: #FFB6C1; opacity: 0.9;">
                    ${countryName}
                  </div>
                </div>
              </div>
              
              <div style="
                background: linear-gradient(135deg, rgba(255, 107, 157, 0.15), rgba(186, 104, 200, 0.1));
                border-radius: 8px;
                padding: 10px;
                margin-top: 6px;
                border: 2px solid rgba(255, 107, 157, 0.3);
              ">
                <div style="font-size: 24px; color: #FF6B9D; font-weight: 900; line-height: 1;">
                  ${countryData.value.toLocaleString()}
                </div>
                <div style="font-size: 12px; color: #FFB6C1; text-transform: uppercase; letter-spacing: 0.5px;">
                  MOVIES
                </div>
              </div>
            `)
            .style("opacity", 1)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 130) + "px")
        }
      })

      countryPaths.on("mousemove", (event) => {
        if (this.tooltip) {
          this.tooltip
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 130) + "px")
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
  min-height: 450px;
}

.world-map {
  width: 100%;
  height: 100%;
  border-radius: 18px;
  overflow: hidden;
  position: relative;
}

/* ZOOM CONTROLS - ATAS KIRI */
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

/* SCALE LEGEND - POSISI 4.9M DINAIIKKAN */
.scale-legend {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10;
  background: rgba(50, 42, 36, 0.85);
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 107, 157, 0.3);
  backdrop-filter: blur(10px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  min-width: 90px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.legend-title {
  font-size: 9px;
  color: #FFD1DC;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-align: center;
  margin-bottom: 12px;
  width: 100%;
}

.legend-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.legend-bar-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 120px;
}

.legend-bar {
  width: 16px;
  height: 100px;
  background: linear-gradient(to top, 
    #2a2a4a 0%,
    #3a2a5a 20%,
    #5a2a7a 40%,
    #7B1FA2 60%,
    #BA68C8 80%,
    #FF6B9D 100%
  );
  border-radius: 3px;
  border: 1px solid rgba(255, 107, 157, 0.7);
  position: relative;
  overflow: hidden;
  margin: 0 15px;
}

.legend-gradient {
  width: 100%;
  height: 100%;
}

/* Label positioning - 4.9M DINAIIKKAN LEBIH KE ATAS */
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
  top: 3px; /* ⬅️ DIUBAH: Dinaikkan 5px lebih tinggi */
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

/* Adjustment untuk alignment */
.bottom-label .label-text {
  transform: translateY(8px); /* ⬅️ DIUBAH: 0 lebih dekat ke bawah */
}

.top-label .label-text {
  transform: translateY(-10px); /* ⬅️ DIUBAH: 4.9M lebih ke atas */
}

/* Pastikan bar tidak overlap dengan label */
.legend-bar {
  margin-top: 10px; /* ⬅️ DIUBAH: Bar diturunkan sedikit */
  margin-bottom: 10px; /* ⬅️ DIUBAH: Bar diberi ruang di bawah */
}
</style>

<style>
.world-map-tooltip {
  position: absolute !important;
  z-index: 999999 !important;
  transition: opacity 0.2s ease !important;
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