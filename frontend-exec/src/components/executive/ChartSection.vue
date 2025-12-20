<template>
  <section class="chart-section">
    <div class="chart-header">
      <h2 class="section-title">📈 Data Visualization Dashboard</h2>
    </div>

    <!-- Baris 1: Filter dan Bar Chart + Pie Chart -->
    <div class="chart-row">
      <!-- Filter dan Bar Chart Utama -->
      <div class="chart-card main-bar-card">
        <div class="card-header">
          <h3>{{ getChartTitle(selectedChart) }}</h3>
          <div class="card-badge">{{ getChartBadge(selectedChart) }}</div>
        </div>
        <!-- FILTER dipindahkan ke sini (di atas chart) -->
        <div class="filter-controls">
          <div class="control-group">
            <label class="control-label">Filter:</label>
            <select v-model="selectedChart" @change="loadChart" class="control-select">
              <option value="country">Top Production Countries</option>
              <option value="platform">Top Platforms</option>
              <option value="genre">Top Genres</option>
              <option value="status">Status Distribution</option>
            </select>
          </div>
        </div>
        <div class="chart-wrapper">
          <canvas id="execChart"></canvas>
        </div>
      </div>

      <!-- Pie Chart -->
      <div class="chart-card pie-card">
        <div class="card-header">
          <h3>Distribution</h3>
          <div class="chart-controls-small">
            <select v-model="selectedPieChart" @change="loadPieChart" class="control-select small">
              <option value="status">Status</option>
              <option value="genre">Genre</option>
              <option value="language">Language</option>
              <option value="country">Country</option>
            </select>
          </div>
        </div>
        <div class="chart-wrapper">
          <canvas id="execPieChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Baris 2: Stacked Bar Chart dan Scatter Plot -->
    <div class="chart-row double-row">
      <!-- Stacked Bar Chart (VERTICAL) -->
      <div class="chart-card stacked-card">
        <div class="card-header">
          <h3>Stacked Analysis (Vertical)</h3>
          <div class="chart-controls-small">
            <select v-model="selectedStackedCategory" @change="loadStackedChart" class="control-select small">
              <option value="genre">Genre by Status</option>
              <option value="country">Country by Status</option>
              <option value="language">Language by Status</option>
            </select>
          </div>
        </div>
        <div class="chart-wrapper">
          <canvas id="stackedChart"></canvas>
        </div>
        <p v-if="stackedError" class="error-message">{{ stackedError }}</p>
      </div>

      <!-- Scatter Plot -->
      <div class="chart-card scatter-card">
        <div class="card-header">
          <h3>Correlation Analysis</h3>
          <div class="chart-controls-small">
            <select v-model="selectedScatterType" @change="loadScatterPlot" class="control-select small">
              <option value="popularity_vs_votes">Popularity vs Votes</option>
              <option value="popularity_vs_rating">Popularity vs Rating</option>
              <option value="votes_vs_rating">Votes vs Rating</option>
            </select>
          </div>
        </div>
        <div class="chart-wrapper">
          <canvas id="scatterChart"></canvas>
        </div>
        <p v-if="scatterError" class="error-message">{{ scatterError }}</p>
      </div>
    </div>

    <!-- Status Messages -->
    <div class="status-messages">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <span>Loading charts...</span>
      </div>
      <div v-if="error" class="error-state">
        <span class="error-icon">⚠️</span>
        <span>{{ error }}</span>
      </div>
      <div v-if="pieError" class="error-state">
        <span class="error-icon">⚠️</span>
        <span>{{ pieError }}</span>
      </div>
    </div>
  </section>
</template>

<script>
import { getExecutiveChart, getExecutivePieChart } from "../../utils/api";
import { Chart } from "chart.js/auto";

export default {
  name: "ChartSection",

  data() {
    return {
      selectedChart: "country",
      selectedPieChart: "status",
      selectedStackedCategory: "genre",
      selectedScatterType: "popularity_vs_votes",
      chartInstance: null,
      pieChartInstance: null,
      stackedChartInstance: null,
      scatterChartInstance: null,
      loading: false,
      error: null,
      pieError: null,
      stackedError: null,
      scatterError: null,
    };
  },

  methods: {
    /* ============================================================
       🔥 LOAD BAR CHART UTAMA dengan satu warna ungu solid
    ============================================================ */
    async loadChart() {
      this.loading = true;
      this.error = null;

      try {
        const res = await getExecutiveChart(this.selectedChart);

        if (!res.success) {
          this.error = "Failed to fetch chart data";
          return;
        }

        const labels = res.labels;
        const totals = res.raw.map((item) => item.Total);

        if (this.chartInstance) {
          this.chartInstance.destroy();
        }

        const ctx = document.getElementById("execChart");
        
        // SATU WARNA UNGU SOLID untuk Bar Chart
        const solidPurple = '#b23397';

        this.chartInstance = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels.slice(0, 15),
            datasets: [
              {
                label: this.getChartLabel(this.selectedChart),
                data: totals.slice(0, 15),
                backgroundColor: solidPurple,
                borderColor: solidPurple,
                borderWidth: 1,
                borderRadius: 6,
                hoverBackgroundColor: '#c147a0',
                hoverBorderColor: '#c147a0',
                hoverBorderWidth: 2,
              },
            ],
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
                  padding: 15,
                  boxWidth: 15,
                  boxHeight: 8
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
                  label: function(context) {
                    return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`;
                  }
                }
              }
            },
            scales: {
              x: { 
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 11 },
                  maxRotation: 45
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                }
              },
              y: { 
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 11 },
                  callback: function(value) {
                    if (value >= 1000) return (value/1000).toFixed(0) + 'k';
                    return value;
                  }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                },
                beginAtZero: true
              },
            },
          },
        });

      } catch (err) {
        console.error("Error loading chart:", err);
        this.error = "Error loading chart data";
      } finally {
        this.loading = false;
      }
    },

    /* ============================================================
       🍩 LOAD PIE / DONUT CHART dengan warna pink-ungu gradasi
    ============================================================ */
    async loadPieChart() {
      this.pieError = null;

      try {
        const res = await getExecutivePieChart(this.selectedPieChart);

        if (!res.success) {
          this.pieError = "Failed to load pie chart data";
          return;
        }

        const labels = res.labels;
        const totals = res.totals;

        if (this.pieChartInstance) {
          this.pieChartInstance.destroy();
        }

        const ctx = document.getElementById("execPieChart");

        // PALETTE WARNA PINK KE UNGU GRADASI (16 warna)
        const pinkToPurpleGradient = [
          '#ff6fb2', '#f262a9', '#e556a0', '#d84997',
          '#cc3d8e', '#bf3185', '#b3257c', '#a61973',
          '#990d6a', '#8c0061', '#800058', '#730050',
          '#660047', '#59003e', '#4d0035', '#40002c'
        ];

        this.pieChartInstance = new Chart(ctx, {
          type: "doughnut",
          data: {
            labels,
            datasets: [
              {
                data: totals,
                backgroundColor: pinkToPurpleGradient.slice(0, totals.length),
                borderWidth: 1,
                borderColor: '#3d2525',
                hoverBorderColor: '#ff6fb2',
                hoverBorderWidth: 2,
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
              legend: {
                position: 'right',
                labels: {
                  color: "#f5e6d3",
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
                  label: function(context) {
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((context.parsed / total) * 100).toFixed(1);
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

      } catch (err) {
        console.error("Error loading pie chart:", err);
        this.pieError = "Error loading pie chart";
      }
    },

    /* ============================================================
       📊 LOAD STACKED BAR CHART dengan warna pink-ungu gradasi
    ============================================================ */
    async loadStackedChart() {
      this.stackedError = null;

      try {
        const stackedData = await this.getStackedData(this.selectedStackedCategory);

        if (this.stackedChartInstance) {
          this.stackedChartInstance.destroy();
        }

        const ctx = document.getElementById("stackedChart");

        // WARNA PINK-UNGU GRADASI untuk status berbeda
        const pinkPurpleColors = [
          '#ff6fb2', '#e55ba9', '#cc47a0', '#b23397',
          '#99218e', '#800f85', '#690072', '#52005f'
        ];

        const statusColors = {
          'Ended': pinkPurpleColors[0],
          'Returning Series': pinkPurpleColors[2],
          'Canceled': pinkPurpleColors[4],
          'In Production': pinkPurpleColors[6],
          'Planned': pinkPurpleColors[7],
          'Pilot': '#ff9f40'
        };

        const datasets = stackedData.statuses.map((status, index) => ({
          label: status,
          data: stackedData.data[status] || [],
          backgroundColor: statusColors[status] || pinkPurpleColors[index % pinkPurpleColors.length],
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 0,
          borderRadius: 4,
        }));

        this.stackedChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: stackedData.labels,
            datasets: datasets
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            plugins: {
              legend: {
                position: 'top',
                labels: {
                  color: '#f5e6d3',
                  font: { size: 11 },
                  padding: 10,
                  boxWidth: 15,
                  boxHeight: 10
                }
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(61, 37, 37, 0.95)',
                titleColor: '#ff6fb2',
                bodyColor: '#f5e6d3',
                borderColor: '#ff6fb2',
                borderWidth: 1,
                padding: 10,
                cornerRadius: 6,
                callbacks: {
                  label: function(context) {
                    return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`;
                  },
                  footer: (tooltipItems) => {
                    const sum = tooltipItems.reduce((acc, item) => acc + item.parsed.y, 0);
                    return `Total: ${sum.toLocaleString()}`;
                  }
                }
              }
            },
            scales: {
              x: {
                stacked: true,
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 11 },
                  maxRotation: 45
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                },
              },
              y: {
                stacked: true,
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 11 },
                  callback: function(value) {
                    if (value >= 1000) return (value/1000).toFixed(0) + 'k';
                    return value;
                  }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                },
                beginAtZero: true
              }
            }
          }
        });

      } catch (err) {
        console.error("Error loading stacked chart:", err);
        this.stackedError = "Error loading stacked chart";
      }
    },

    /* ============================================================
       ⭐ LOAD SCATTER PLOT dengan warna pink
    ============================================================ */
    async loadScatterPlot() {
      this.scatterError = null;

      try {
        const scatterData = await this.getScatterData(this.selectedScatterType);

        if (this.scatterChartInstance) {
          this.scatterChartInstance.destroy();
        }

        const ctx = document.getElementById("scatterChart");

        this.scatterChartInstance = new Chart(ctx, {
          type: 'scatter',
          data: {
            datasets: [{
              label: this.getScatterLabel(this.selectedScatterType),
              data: scatterData,
              backgroundColor: 'rgba(255, 111, 178, 0.6)',
              borderColor: '#ff6fb2',
              borderWidth: 1,
              pointRadius: 5,
              pointHoverRadius: 8,
              pointHoverBackgroundColor: '#ff8fc7',
              pointHoverBorderColor: '#ffffff',
              pointHoverBorderWidth: 2,
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
                  padding: 10,
                  usePointStyle: true,
                  pointStyle: 'circle',
                  boxWidth: 8,
                  boxHeight: 8
                }
              },
              tooltip: {
                backgroundColor: 'rgba(61, 37, 37, 0.95)',
                titleColor: '#ff6fb2',
                bodyColor: '#f5e6d3',
                borderColor: '#ff6fb2',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 6,
                callbacks: {
                  title: () => '',
                  label: function(context) {
                    const xLabel = context.chart.options.scales.x.title.text;
                    const yLabel = context.chart.options.scales.y.title.text;
                    return [
                      `${xLabel}: ${context.parsed.x.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`,
                      `${yLabel}: ${context.parsed.y.toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 })}`
                    ];
                  }
                }
              }
            },
            scales: {
              x: {
                type: 'linear',
                position: 'bottom',
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 10 },
                  callback: function(value) {
                    if (value >= 10000) return (value/1000).toFixed(0) + 'k';
                    return value.toLocaleString();
                  }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                },
                title: {
                  display: true,
                  text: this.getScatterXLabel(this.selectedScatterType),
                  color: '#ff6fb2',
                  font: { size: 11, weight: '500' },
                  padding: { top: 10, bottom: 5 }
                }
              },
              y: {
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 10 },
                  callback: function(value) {
                    if (value >= 10000) return (value/1000).toFixed(0) + 'k';
                    return value.toLocaleString();
                  }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.08)', 
                  drawBorder: false 
                },
                title: {
                  display: true,
                  text: this.getScatterYLabel(this.selectedScatterType),
                  color: '#ff6fb2',
                  font: { size: 11, weight: '500' },
                  padding: { top: 5, bottom: 10 }
                }
              }
            }
          }
        });

      } catch (err) {
        console.error("Error loading scatter plot:", err);
        this.scatterError = "Error loading scatter plot";
      }
    },

    /* ============================================================
       📦 HELPER FUNCTIONS
    ============================================================ */
    getChartTitle(type) {
      const titles = {
        'country': 'Top Production Countries',
        'platform': 'Top Platforms/Networks',
        'genre': 'Top Genres',
        'status': 'Status Distribution'
      };
      return titles[type] || 'Chart Analysis';
    },

    getChartBadge(type) {
      const badges = {
        'country': '15 Countries',
        'platform': '15 Platforms',
        'genre': '15 Genres',
        'status': 'Status'
      };
      return badges[type] || 'Data';
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

    getScatterLabel(type) {
      const labels = {
        'popularity_vs_votes': 'Popularity vs Votes',
        'popularity_vs_rating': 'Popularity vs Rating',
        'votes_vs_rating': 'Votes vs Rating'
      };
      return labels[type] || 'Scatter Plot';
    },

    getScatterXLabel(type) {
      const labels = {
        'popularity_vs_votes': 'Popularity Score',
        'popularity_vs_rating': 'Popularity Score',
        'votes_vs_rating': 'Vote Count'
      };
      return labels[type] || 'X Axis';
    },

    getScatterYLabel(type) {
      const labels = {
        'popularity_vs_votes': 'Vote Count',
        'popularity_vs_rating': 'Average Rating',
        'votes_vs_rating': 'Average Rating'
      };
      return labels[type] || 'Y Axis';
    },

    /* ============================================================
       📦 SIMULATE STACKED DATA (Vertical)
    ============================================================ */
    async getStackedData(category) {
      return new Promise((resolve) => {
        setTimeout(() => {
          if (category === 'genre') {
            resolve({
              labels: ['Drama', 'Comedy', 'Action', 'Thriller', 'Sci-Fi', 'Romance', 'Horror', 'Documentary'],
              statuses: ['Ended', 'Returning Series', 'Canceled', 'In Production', 'Planned'],
              data: {
                'Ended': [5200, 3800, 2900, 2400, 1800, 1600, 1200, 900],
                'Returning Series': [3100, 2900, 2100, 1800, 1400, 1200, 800, 600],
                'Canceled': [1800, 1600, 1300, 1100, 900, 700, 500, 300],
                'In Production': [900, 800, 650, 550, 450, 350, 250, 150],
                'Planned': [500, 450, 380, 320, 250, 200, 150, 100]
              }
            });
          } else if (category === 'country') {
            resolve({
              labels: ['USA', 'Japan', 'China', 'UK', 'Germany', 'France', 'Canada', 'South Korea'],
              statuses: ['Ended', 'Returning Series', 'Canceled', 'In Production', 'Planned'],
              data: {
                'Ended': [6200, 4800, 3200, 2800, 2200, 1900, 1600, 1400],
                'Returning Series': [4100, 3200, 2400, 2100, 1700, 1500, 1200, 1000],
                'Canceled': [2200, 1800, 1500, 1300, 1100, 900, 700, 600],
                'In Production': [1100, 900, 750, 650, 550, 450, 350, 300],
                'Planned': [600, 500, 420, 360, 300, 250, 200, 180]
              }
            });
          } else if (category === 'language') {
            resolve({
              labels: ['English', 'Japanese', 'Mandarin', 'Spanish', 'Korean', 'French', 'German', 'Hindi'],
              statuses: ['Ended', 'Returning Series', 'Canceled', 'In Production', 'Planned'],
              data: {
                'Ended': [7500, 4200, 3500, 2900, 2400, 2100, 1800, 1600],
                'Returning Series': [5200, 3100, 2600, 2200, 1900, 1600, 1400, 1200],
                'Canceled': [2800, 1700, 1500, 1300, 1100, 950, 850, 750],
                'In Production': [1400, 850, 720, 620, 550, 480, 420, 380],
                'Planned': [750, 450, 400, 350, 320, 280, 240, 220]
              }
            });
          }
        }, 200);
      });
    },

    /* ============================================================
       📦 SIMULATE SCATTER DATA
    ============================================================ */
    async getScatterData(type) {
      return new Promise((resolve) => {
        setTimeout(() => {
          const dataPoints = [];
          const numPoints = 100;
          
          for (let i = 0; i < numPoints; i++) {
            if (type === 'popularity_vs_votes') {
              const pop = Math.random() * 100;
              dataPoints.push({
                x: pop,
                y: Math.random() * 50000 + (pop * 150)
              });
            } else if (type === 'popularity_vs_rating') {
              const pop = Math.random() * 100;
              dataPoints.push({
                x: pop,
                y: 4 + (Math.random() * 6) + (pop / 100 * 1)
              });
            } else if (type === 'votes_vs_rating') {
              const votes = Math.random() * 50000;
              dataPoints.push({
                x: votes,
                y: 5 + (Math.random() * 4) + (votes / 50000 * 2)
              });
            }
          }
          
          resolve(dataPoints);
        }, 200);
      });
    },
  },

  mounted() {
    this.loadChart();
    this.loadPieChart();
    this.loadStackedChart();
    this.loadScatterPlot();
  },

  beforeUnmount() {
    if (this.chartInstance) this.chartInstance.destroy();
    if (this.pieChartInstance) this.pieChartInstance.destroy();
    if (this.stackedChartInstance) this.stackedChartInstance.destroy();
    if (this.scatterChartInstance) this.scatterChartInstance.destroy();
  }
};
</script>

<style scoped>
/* Reset dan Base Styles */
.chart-section {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Header Section */
.chart-header {
  background: linear-gradient(135deg, rgba(61, 37, 37, 0.8), rgba(41, 24, 24, 0.9));
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(255, 111, 178, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.section-title {
  color: #f5e6d3;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 0;
  letter-spacing: 0.5px;
  text-align: center;
}

/* Filter Controls di atas bar chart */
.filter-controls {
  padding: 15px 20px;
  background: rgba(41, 24, 24, 0.6);
  border-bottom: 1px solid rgba(255, 111, 178, 0.1);
  margin: 0 20px;
  border-radius: 8px 8px 0 0;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-label {
  color: #ff6fb2;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

.control-select {
  padding: 10px 16px;
  background: rgba(41, 24, 24, 0.9);
  border-radius: 8px;
  color: #f5e6d3;
  font-size: 14px;
  border: 1px solid rgba(255, 111, 178, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
  min-width: 200px;
  font-family: inherit;
}

.control-select:hover {
  border-color: #ff6fb2;
  background: rgba(61, 37, 37, 0.95);
  box-shadow: 0 0 12px rgba(255, 111, 178, 0.2);
}

.control-select:focus {
  border-color: #ff6fb2;
  box-shadow: 0 0 0 3px rgba(255, 111, 178, 0.3);
}

.control-select.small {
  min-width: 160px;
  padding: 8px 12px;
  font-size: 13px;
}

/* Chart Row */
.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  width: 100%;
}

/* Baris Double untuk Stacked dan Scatter */
.double-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  width: 100%;
}

/* Chart Card */
.chart-card {
  background: linear-gradient(145deg, rgba(61, 37, 37, 0.6), rgba(41, 24, 24, 0.7));
  border-radius: 12px;
  border: 1px solid rgba(255, 111, 178, 0.15);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 450px; /* Sedikit lebih tinggi untuk menampung filter */
  position: relative;
}

.chart-card:hover {
  border-color: rgba(255, 111, 178, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 111, 178, 0.15);
}

/* Card Header */
.card-header {
  padding: 16px 20px;
  background: rgba(41, 24, 24, 0.8);
  border-bottom: 1px solid rgba(255, 111, 178, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.card-header h3 {
  color: #f5e6d3;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-badge {
  background: linear-gradient(135deg, #ff6fb2, #ff85c1);
  color: white;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Chart Wrapper */
.chart-wrapper {
  flex: 1;
  padding: 16px;
  position: relative;
  min-height: 300px;
}

/* Specific Card Styles */
.main-bar-card {
  grid-column: 1;
}

.pie-card {
  grid-column: 2;
  height: 450px;
}

/* Stacked dan Scatter Card Styles */
.stacked-card,
.scatter-card {
  height: 420px;
  grid-column: auto;
}

/* Status Messages */
.status-messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
  margin-top: 10px;
}

.loading-state {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ff6fb2;
  font-size: 14px;
  font-weight: 500;
  padding: 12px 24px;
  background: rgba(255, 111, 178, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  animation: pulse 1.5s ease-in-out infinite;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 111, 178, 0.3);
  border-top: 2px solid #ff6fb2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-state {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff8585;
  font-size: 13px;
  padding: 10px 16px;
  background: rgba(255, 133, 133, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 133, 133, 0.3);
  width: 100%;
  max-width: 600px;
}

.error-icon {
  font-size: 14px;
}

.error-message {
  color: #ff8585;
  font-size: 13px;
  padding: 8px 12px;
  background: rgba(255, 133, 133, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(255, 133, 133, 0.3);
  margin: 8px 16px;
  text-align: center;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

/* Responsive Design */
@media (max-width: 1200px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .main-bar-card,
  .pie-card {
    grid-column: 1;
  }
  
  .pie-card {
    height: 420px;
  }
  
  .double-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .stacked-card,
  .scatter-card {
    height: 400px;
    grid-column: 1;
  }
}

@media (max-width: 768px) {
  .chart-section {
    padding: 15px;
    gap: 15px;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .chart-row {
    grid-template-columns: 1fr;
  }
  
  .filter-controls {
    padding: 12px 16px;
    margin: 0 16px;
  }
  
  .control-group {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .control-select {
    width: 100%;
    min-width: unset;
  }
  
  .chart-card {
    height: 400px;
  }
  
  .stacked-card,
  .scatter-card {
    height: 380px;
  }
  
  .card-header {
    padding: 12px 16px;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .card-header h3 {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .chart-section {
    padding: 12px;
  }
  
  .section-title {
    font-size: 18px;
    margin-bottom: 12px;
  }
  
  .chart-card {
    height: 380px;
  }
  
  .stacked-card,
  .scatter-card {
    height: 360px;
  }
  
  .chart-wrapper {
    padding: 12px;
  }
  
  .control-select {
    padding: 8px 12px;
    font-size: 13px;
  }
}

/* Print Styles */
@media print {
  .chart-section {
    background: white !important;
  }
  
  .chart-card {
    break-inside: avoid;
    border: 1px solid #ddd !important;
    box-shadow: none !important;
  }
  
  .section-title,
  .card-header h3 {
    color: #333 !important;
  }
  
  .double-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style>