<template>
  <section class="chart-section">
    <div class="chart-header">
      <h2 class="section-title">🗺️ Executive Data Visualization</h2>
      <p class="section-subtitle">Interactive charts and world map for data analysis</p>
    </div>

    <!-- Status Messages -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <span>Loading all charts...</span>
    </div>

    <!-- Baris 1: World Map menggunakan WorldMapSection component -->
    <div class="chart-row">
      <div class="chart-card world-map-card">
        <WorldMapSection ref="worldMapComponent" />
      </div>
    </div>

    <!-- Baris 2: Bar Chart Utama -->
    <div class="chart-row">
      <div class="chart-card main-bar-card">
        <div class="card-header">
          <div class="header-left">
            <h3>{{ getChartTitle(selectedChart) }}</h3>
            <span class="chart-badge">Top 15</span>
          </div>
          <div class="header-right">
            <div class="control-group">
              <label class="control-label">Chart Type:</label>
              <select v-model="selectedChart" @change="loadBarChart" class="control-select">
                <option value="country">Top Production Countries</option>
                <option value="platform">Top Platforms</option>
                <option value="genre">Top Genres</option>
                <option value="status">Status Distribution</option>
              </select>
            </div>
          </div>
        </div>
        
        <div v-if="barChartError" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ barChartError }}
        </div>
        
        <div class="chart-wrapper">
          <canvas id="execChart" ref="barChartCanvas"></canvas>
        </div>
      </div>
    </div>

    <!-- Baris 3: Dua Kartu (Pie Chart & Stacked Chart) -->
    <div class="chart-row">
      <!-- Pie Chart -->
      <div class="chart-card pie-card">
        <div class="card-header">
          <div class="header-left">
            <h3>Distribution Overview</h3>
            <span class="chart-badge">Doughnut</span>
          </div>
          <div class="header-right">
            <select v-model="selectedPieChart" @change="loadPieChart" class="control-select small">
              <option value="status">Status Distribution</option>
              <option value="genre">Genre Distribution</option>
              <option value="language">Language Distribution</option>
              <option value="country">Country Distribution</option>
            </select>
          </div>
        </div>
        
        <div v-if="pieChartError" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ pieChartError }}
        </div>
        
        <div class="chart-wrapper">
          <canvas id="execPieChart" ref="pieChartCanvas"></canvas>
        </div>
      </div>

      <!-- Stacked Bar Chart -->
      <div class="chart-card stacked-card">
        <div class="card-header">
          <div class="header-left">
            <h3>{{ getStackedChartTitle(selectedStackedChart) }}</h3>
            <span class="chart-badge">Stacked Bar</span>
          </div>
          <div class="header-right">
            <div class="control-group">
              <label class="control-label">Type:</label>
              <select v-model="selectedStackedChart" @change="loadStackedChart" class="control-select small">
                <option value="countries">By Countries</option>
                <option value="status">By Status</option>
                <option value="genres">By Genres</option>
              </select>
            </div>
            <div class="control-group" v-if="selectedStackedChart === 'countries'">
              <label class="control-label">Top Countries:</label>
              <select v-model="topCountriesLimit" @change="loadStackedChart" class="control-select xs">
                <option value="5">Top 5</option>
                <option value="10">Top 10</option>
                <option value="15">Top 15</option>
                <option value="20">Top 20</option>
              </select>
            </div>
          </div>
        </div>
        
        <div v-if="stackedChartError" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ stackedChartError }}
        </div>
        
        <div v-if="chartInfo" class="chart-info">
          <span class="info-item">Companies: {{ chartInfo.companies }}</span>
          <span class="info-item">Categories: {{ chartInfo.categories }}</span>
          <span class="info-item">Data Points: {{ chartInfo.dataPoints }}</span>
        </div>
        
        <div class="chart-wrapper">
          <canvas id="execStackedChart" ref="stackedChartCanvas"></canvas>
        </div>
        
        <div v-if="stackedChartData" class="chart-footer">
          <small>Showing {{ getVisibleCategories() }} categories out of {{ getTotalCategories() }}</small>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { 
  getExecutiveChart, 
  getExecutivePieChart, 
  getStackedCountriesChart, 
  getStackedStatusChart, 
  getStackedGenresChart
} from "../../utils/api";
import { Chart } from "chart.js/auto";

// Import WorldMapSection component yang sudah ada
import WorldMapSection from "./WorldMapSection.vue";

export default {
  name: "ChartSection",

  components: {
    WorldMapSection
  },

  data() {
    return {
      // Existing Chart Data
      selectedChart: "country",
      selectedPieChart: "status",
      selectedStackedChart: "countries",
      topCountriesLimit: 10,
      
      // Chart instances
      barChartInstance: null,
      pieChartInstance: null,
      stackedChartInstance: null,
      
      // Loading & Error states
      loading: false,
      barChartError: null,
      pieChartError: null,
      stackedChartError: null,
      
      // Chart data cache
      chartData: null,
      pieChartData: null,
      stackedChartData: null,
      chartInfo: null,
      
      // Color palettes
      colorPalettes: {
        barChart: ['#b23397'],
        pieChart: [
          '#ff6fb2', '#f262a9', '#e556a0', '#d84997',
          '#cc3d8e', '#bf3185', '#b3257c', '#a61973',
          '#990d6a', '#8c0061', '#800058', '#730050',
          '#660047', '#59003e', '#4d0035', '#40002c'
        ],
        stackedChart: [
          '#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2',
          '#EF476F', '#7B68EE', '#20B2AA', '#FFA500', '#9B59B6',
          '#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f39c12',
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#8AC926', '#1982C4', '#6A4C93', '#FF595E',
          '#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD'
        ]
      }
    };
  },

  methods: {
    /* ============================================================
       UTILITY FUNCTIONS
    ============================================================ */
    formatNumber(value, decimals = 0) {
      if (value == null || value === undefined || value === '') return 'N/A';
      
      const num = Number(value);
      if (isNaN(num)) return 'N/A';
      
      if (decimals > 0) {
        return num.toFixed(decimals);
      }
      
      if (num >= 1000) {
        return num.toLocaleString();
      }
      
      return num.toString();
    },

    getChartTitle(type) {
      const titles = {
        'country': 'Top Production Countries',
        'platform': 'Top Platforms',
        'genre': 'Top Genres',
        'status': 'Status Distribution'
      };
      return titles[type] || 'Chart Analysis';
    },

    getChartLabel(type) {
      const labels = {
        'country': 'Production Count',
        'platform': 'Platform Count',
        'genre': 'Genre Count',
        'status': 'Status Count'
      };
      return labels[type] || 'Count';
    },

    getStackedChartTitle(type) {
      const titles = {
        'countries': 'Top 10 Companies by Countries',
        'status': 'Top 10 Companies by Status',
        'genres': 'Top 10 Companies by Genres (Top 3 + Others)'
      };
      return titles[type] || 'Stacked Analysis';
    },

    /* ============================================================
       CHART FUNCTIONS
    ============================================================ */
    async loadBarChart() {
      this.barChartError = null;
      
      try {
        const res = await getExecutiveChart(this.selectedChart);

        if (!res || !res.success) {
          this.barChartError = "Failed to load chart data";
          return;
        }

        this.chartData = res;
        this.renderBarChart();

      } catch (err) {
        console.error("Error loading bar chart:", err);
        this.barChartError = "Error loading chart data";
      }
    },

    renderBarChart() {
      if (!this.chartData) return;
      
      if (this.barChartInstance) {
        this.barChartInstance.destroy();
      }

      const ctx = this.$refs.barChartCanvas;
      if (!ctx) return;

      const labels = this.chartData.labels?.slice(0, 15) || [];
      const totals = this.chartData.totals?.slice(0, 15) || [];

      this.barChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: this.getChartLabel(this.selectedChart),
            data: totals,
            backgroundColor: this.colorPalettes.barChart[0],
            borderColor: this.colorPalettes.barChart[0],
            borderWidth: 1,
            borderRadius: 4,
            barPercentage: 0.7,
            categoryPercentage: 0.8,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                color: '#f5e6d3',
                font: { size: 12 },
                padding: 10
              }
            },
            tooltip: {
              backgroundColor: 'rgba(61, 37, 37, 0.95)',
              titleColor: '#ff6fb2',
              bodyColor: '#f5e6d3',
              borderColor: '#ff6fb2',
              borderWidth: 1,
              padding: 10,
              cornerRadius: 6,
              displayColors: false,
              callbacks: {
                label: (context) => {
                  return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                color: 'rgba(245, 230, 211, 0.08)',
                drawBorder: false
              },
              ticks: {
                color: '#f5e6d3',
                font: { size: 11 },
                maxRotation: 45
              }
            },
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(245, 230, 211, 0.08)',
                drawBorder: false
              },
              ticks: {
                color: '#f5e6d3',
                font: { size: 11 },
                callback: function(value) {
                  if (value >= 1000) return (value/1000).toFixed(1) + 'k';
                  return value;
                }
              }
            }
          }
        }
      });
    },

    async loadPieChart() {
      this.pieChartError = null;

      try {
        const res = await getExecutivePieChart(this.selectedPieChart);

        if (!res || !res.success) {
          this.pieChartError = "Failed to load pie chart data";
          return;
        }

        this.pieChartData = res;
        this.renderPieChart();

      } catch (err) {
        console.error("Error loading pie chart:", err);
        this.pieChartError = "Error loading pie chart data";
      }
    },

    renderPieChart() {
      if (!this.pieChartData) return;
      
      if (this.pieChartInstance) {
        this.pieChartInstance.destroy();
      }

      const ctx = this.$refs.pieChartCanvas;
      if (!ctx) return;

      const labels = this.pieChartData.labels || [];
      const totals = this.pieChartData.totals || [];

      this.pieChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: labels,
          datasets: [{
            data: totals,
            backgroundColor: this.colorPalettes.pieChart.slice(0, totals.length),
            borderWidth: 1,
            borderColor: '#3d2525',
            hoverOffset: 15
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '60%',
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f5e6d3',
                font: { size: 11 },
                padding: 8,
                boxWidth: 12,
                boxHeight: 12,
                usePointStyle: true,
                pointStyle: 'circle'
              }
            },
            tooltip: {
              backgroundColor: 'rgba(61, 37, 37, 0.95)',
              titleColor: '#ff6fb2',
              bodyColor: '#f5e6d3',
              borderColor: '#ff6fb2',
              borderWidth: 1,
              padding: 10,
              cornerRadius: 6,
              callbacks: {
                label: (context) => {
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                  return `${context.label}: ${context.parsed.toLocaleString()} (${percentage}%)`;
                }
              }
            }
          },
          animation: {
            animateScale: true,
            animateRotate: true
          }
        }
      });
    },

    async loadStackedChart() {
      this.stackedChartError = null;
      this.chartInfo = null;

      try {
        let apiFunction;
        
        switch (this.selectedStackedChart) {
          case 'countries':
            apiFunction = getStackedCountriesChart;
            break;
          case 'status':
            apiFunction = getStackedStatusChart;
            break;
          case 'genres':
            apiFunction = getStackedGenresChart;
            break;
          default:
            apiFunction = getStackedCountriesChart;
        }

        const res = await apiFunction();

        if (!res || !res.success) {
          this.stackedChartError = "Failed to load stacked chart data";
          return;
        }

        this.stackedChartData = res;
        
        // Calculate chart info
        this.chartInfo = {
          companies: res.labels?.length || 0,
          categories: res.datasets?.length || 0,
          dataPoints: (res.labels?.length || 0) * (res.datasets?.length || 0)
        };
        
        this.renderStackedChart();

      } catch (err) {
        console.error("Error loading stacked chart:", err);
        this.stackedChartError = "Error loading stacked chart data";
      }
    },

    renderStackedChart() {
      if (!this.stackedChartData) return;
      
      if (this.stackedChartInstance) {
        this.stackedChartInstance.destroy();
      }

      const ctx = this.$refs.stackedChartCanvas;
      if (!ctx) return;

      const chartData = this.prepareStackedChartData();
      
      this.stackedChartInstance = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#f5e6d3',
                font: { size: 10 },
                padding: 5,
                boxWidth: 10,
                boxHeight: 10,
                usePointStyle: true,
                maxHeight: 100
              }
            },
            tooltip: {
              backgroundColor: 'rgba(61, 37, 37, 0.95)',
              titleColor: '#ff6fb2',
              bodyColor: '#f5e6d3',
              borderColor: '#ff6fb2',
              borderWidth: 1,
              padding: 8,
              cornerRadius: 6,
              mode: 'index',
              intersect: false,
              callbacks: {
                label: (context) => {
                  const label = context.dataset.label || '';
                  const value = context.parsed.y;
                  const total = this.getStackedBarTotal(context);
                  const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                  return `${label}: ${value} (${percentage}%)`;
                }
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              grid: {
                color: 'rgba(245, 230, 211, 0.08)',
                drawBorder: false
              },
              ticks: {
                color: '#f5e6d3',
                font: { size: 11 },
                maxRotation: 45,
                autoSkip: true,
                maxTicksLimit: 15
              }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              grid: {
                color: 'rgba(245, 230, 211, 0.08)',
                drawBorder: false
              },
              ticks: {
                color: '#f5e6d3',
                font: { size: 11 },
                callback: (value) => {
                  if (value >= 1000) return (value/1000).toFixed(1) + 'k';
                  return value;
                }
              }
            }
          },
          interaction: {
            intersect: false,
            mode: 'index'
          }
        }
      });
    },

    prepareStackedChartData() {
      if (!this.stackedChartData.datasets || !this.stackedChartData.labels) {
        return { labels: [], datasets: [] };
      }

      if (this.selectedStackedChart === 'countries') {
        const limit = parseInt(this.topCountriesLimit) || 10;
        
        const datasetsWithTotals = this.stackedChartData.datasets.map(dataset => ({
          ...dataset,
          total: (dataset.data || []).reduce((sum, val) => sum + (Number(val) || 0), 0)
        }));
        
        const topDatasets = datasetsWithTotals
          .sort((a, b) => b.total - a.total)
          .slice(0, limit);
        
        return {
          labels: this.stackedChartData.labels,
          datasets: topDatasets.map((dataset, index) => ({
            label: dataset.label || `Dataset ${index + 1}`,
            data: dataset.data || [],
            backgroundColor: this.colorPalettes.stackedChart[index % this.colorPalettes.stackedChart.length],
            borderColor: '#ffffff',
            borderWidth: 1,
            borderRadius: 3,
            barPercentage: 0.8,
            categoryPercentage: 0.9
          }))
        };
      }
      
      return {
        labels: this.stackedChartData.labels,
        datasets: this.stackedChartData.datasets.map((dataset, index) => ({
          label: dataset.label || `Dataset ${index + 1}`,
          data: dataset.data || [],
          backgroundColor: this.colorPalettes.stackedChart[index % this.colorPalettes.stackedChart.length],
          borderColor: '#ffffff',
          borderWidth: 1,
          borderRadius: 3,
          barPercentage: 0.8,
          categoryPercentage: 0.9
        }))
      };
    },

    getStackedBarTotal(context) {
      const chart = context.chart;
      const dataIndex = context.dataIndex;
      
      let total = 0;
      chart.data.datasets.forEach((dataset, datasetIndex) => {
        if (chart.getDatasetMeta(datasetIndex).hidden) return;
        total += dataset.data[dataIndex] || 0;
      });
      
      return total;
    },

    getVisibleCategories() {
      if (!this.stackedChartInstance || !this.stackedChartInstance.data) return 0;
      return this.stackedChartInstance.data.datasets.length;
    },

    getTotalCategories() {
      if (!this.stackedChartData) return 0;
      return this.stackedChartData.datasets.length;
    },

    async loadAllCharts() {
      this.loading = true;
      try {
        await Promise.all([
          this.loadBarChart(),
          this.loadPieChart(),
          this.loadStackedChart()
        ]);
      } catch (err) {
        console.error("Error loading all charts:", err);
      } finally {
        this.loading = false;
      }
    },

    // Method untuk refresh world map dari parent component
    refreshWorldMap() {
      if (this.$refs.worldMapComponent && this.$refs.worldMapComponent.loadMapData) {
        this.$refs.worldMapComponent.loadMapData();
      }
    }
  },

  mounted() {
    this.loadAllCharts();
    
    window.addEventListener('resize', () => {
      if (this.barChartInstance) this.barChartInstance.resize();
      if (this.pieChartInstance) this.pieChartInstance.resize();
      if (this.stackedChartInstance) this.stackedChartInstance.resize();
    });
  },

  beforeUnmount() {
    if (this.barChartInstance) {
      this.barChartInstance.destroy();
      this.barChartInstance = null;
    }
    if (this.pieChartInstance) {
      this.pieChartInstance.destroy();
      this.pieChartInstance = null;
    }
    if (this.stackedChartInstance) {
      this.stackedChartInstance.destroy();
      this.stackedChartInstance = null;
    }
    
    window.removeEventListener('resize', () => {});
  }
};
</script>

<style scoped>
/* ============================================================
   BASE STYLES
============================================================ */
.chart-section {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ============================================================
   HEADER SECTION
============================================================ */
.chart-header {
  background: linear-gradient(135deg, rgba(61, 37, 37, 0.8), rgba(41, 24, 24, 0.9));
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid rgba(255, 111, 178, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-bottom: 10px;
}

.section-title {
  color: #f5e6d3;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
}

.section-subtitle {
  color: rgba(245, 230, 211, 0.7);
  font-size: 14px;
  margin: 0;
}

/* ============================================================
   CHART ROW LAYOUT
============================================================ */
.chart-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  width: 100%;
}

.chart-row:first-of-type {
  /* World Map row */
  grid-template-columns: 1fr;
}

.chart-row:nth-of-type(2) {
  /* Bar chart row */
  grid-template-columns: 1fr;
}

.chart-row:last-of-type {
  /* Pie and Stacked charts */
  grid-template-columns: 1fr 1fr;
}

/* ============================================================
   CHART CARD STYLES
============================================================ */
.chart-card {
  background: linear-gradient(145deg, rgba(61, 37, 37, 0.6), rgba(41, 24, 24, 0.7));
  border-radius: 12px;
  border: 1px solid rgba(255, 111, 178, 0.15);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
}

.chart-card:hover {
  border-color: rgba(255, 111, 178, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 111, 178, 0.15);
}

.world-map-card {
  height: auto;
  min-height: 600px;
}

.main-bar-card, .stacked-card {
  height: 450px;
}

.pie-card {
  height: 450px;
}

/* ============================================================
   CARD HEADER (Untuk charts lain, bukan WorldMap)
============================================================ */
.card-header {
  padding: 12px 16px;
  background: rgba(41, 24, 24, 0.8);
  border-bottom: 1px solid rgba(255, 111, 178, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  min-height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.header-left h3 {
  color: #f5e6d3;
  font-size: 15px;
  font-weight: 600;
  margin: 0;
}

.chart-badge {
  background: linear-gradient(135deg, #ff6fb2, #ff85c1);
  color: white;
  padding: 3px 8px;
  border-radius: 16px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  white-space: nowrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

/* ============================================================
   FORM CONTROLS (Untuk charts lain)
============================================================ */
.control-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: nowrap;
}

.control-label {
  color: #ff6fb2;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.control-select {
  padding: 6px 12px;
  background: rgba(41, 24, 24, 0.9);
  border-radius: 6px;
  color: #f5e6d3;
  font-size: 12px;
  border: 1px solid rgba(255, 111, 178, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
  min-width: 120px;
  font-family: inherit;
}

.control-select:hover {
  border-color: #ff6fb2;
  background: rgba(61, 37, 37, 0.95);
  box-shadow: 0 0 6px rgba(255, 111, 178, 0.2);
}

.control-select:focus {
  border-color: #ff6fb2;
  box-shadow: 0 0 0 2px rgba(255, 111, 178, 0.3);
}

.control-select.small {
  min-width: 100px;
  padding: 5px 10px;
  font-size: 11px;
}

.control-select.xs {
  min-width: 70px;
  padding: 4px 8px;
  font-size: 11px;
}

/* ============================================================
   CHART WRAPPER
============================================================ */
.chart-wrapper {
  flex: 1;
  padding: 12px;
  position: relative;
  min-height: 300px;
}

/* ============================================================
   CHART INFO
============================================================ */
.chart-info {
  display: flex;
  justify-content: space-around;
  padding: 8px 16px;
  background: rgba(41, 24, 24, 0.5);
  border-top: 1px solid rgba(255, 111, 178, 0.1);
  font-size: 11px;
  color: rgba(245, 230, 211, 0.7);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.chart-footer {
  padding: 6px 16px;
  background: rgba(41, 24, 24, 0.5);
  border-top: 1px solid rgba(255, 111, 178, 0.1);
  text-align: center;
  font-size: 10px;
  color: rgba(245, 230, 211, 0.6);
}

/* ============================================================
   LOADING & ERROR STATES
============================================================ */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #ff6fb2;
  font-size: 13px;
  font-weight: 500;
  padding: 15px;
  background: rgba(255, 111, 178, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  margin: 10px 0;
  animation: pulse 1.5s ease-in-out infinite;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 111, 178, 0.3);
  border-top: 2px solid #ff6fb2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ff8585;
  font-size: 12px;
  padding: 8px 12px;
  background: rgba(255, 133, 133, 0.1);
  border-radius: 5px;
  border: 1px solid rgba(255, 133, 133, 0.3);
  margin: 8px 12px;
}

.error-icon {
  font-size: 12px;
}

/* ============================================================
   ANIMATIONS
============================================================ */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* ============================================================
   RESPONSIVE DESIGN
============================================================ */
@media (max-width: 1200px) {
  .chart-row:last-of-type {
    grid-template-columns: 1fr;
  }
  
  .world-map-card {
    height: auto;
    min-height: 550px;
  }
  
  .main-bar-card, .stacked-card, .pie-card {
    height: 420px;
  }
}

@media (max-width: 992px) {
  .chart-section {
    padding: 15px;
  }
  
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .chart-row:last-of-type {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .chart-section {
    padding: 12px;
    gap: 15px;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .section-subtitle {
    font-size: 13px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 12px;
  }
  
  .header-left,
  .header-right {
    width: 100%;
  }
  
  .header-right {
    justify-content: flex-start;
  }
  
  .control-group {
    width: 100%;
  }
  
  .control-select {
    width: 100%;
    min-width: unset;
  }
  
  .world-map-card {
    min-height: 500px;
  }
  
  .main-bar-card, .stacked-card, .pie-card {
    height: 400px;
  }
  
  .chart-wrapper {
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .chart-section {
    padding: 10px;
  }
  
  .section-title {
    font-size: 18px;
  }
  
  .chart-badge {
    font-size: 9px;
    padding: 2px 6px;
  }
  
  .control-select {
    padding: 5px 10px;
    font-size: 11px;
  }
  
  .control-select.small {
    padding: 4px 8px;
  }
  
  .control-select.xs {
    padding: 3px 6px;
  }
  
  .world-map-card {
    min-height: 450px;
  }
  
  .main-bar-card, .stacked-card, .pie-card {
    height: 350px;
  }
}

/* ============================================================
   WorldMapSection Component Customization
============================================================ */
:deep(.world-map-section) {
  height: 100%;
  padding: 0;
  background: transparent;
  border: none;
  box-shadow: none;
}

:deep(.world-map-section .section-header) {
  padding: 12px 16px;
  margin: 0;
}

:deep(.world-map-section .map-controls) {
  margin: 0 12px 12px 12px;
}

:deep(.world-map-section .chart-container) {
  height: 450px;
  margin: 0 12px 12px 12px;
}

:deep(.world-map-section .map-stats-panel) {
  margin: 0 12px 12px 12px;
}
</style>