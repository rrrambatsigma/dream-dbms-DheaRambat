<template>
  <section class="chart-box">
    <h2 class="chart-title">Charts</h2>

    <!-- Dropdown pilih chart -->
    <div class="controls">
      <label>Pilih Chart:</label>
      <select v-model="selectedChart" @change="loadChart">
        <option value="country">Top 15 Production Countries</option>
        <option value="platform">Top 15 Platforms / Networks</option>
        <option value="genre">Top 15 Genres</option>
        <option value="status">Show Status Distribution</option>
      </select>
    </div>

    <!-- GRID UNTUK BAR + PIE -->
    <div class="chart-grid">
      
      <!-- BAR CHART -->
      <div class="chart-container">
        <canvas id="execChart"></canvas>
      </div>

      <!-- PIE / DONUT CHART (BARU DITAMBAHKAN) -->
      <div class="chart-pie-wrapper">
        <!-- DROPDOWN PIE CHART -->
        <div class="pie-controls">
          <label>Pie Chart:</label>
          <select v-model="selectedPieChart" @change="loadPieChart">
            <option value="status">Status Distribution</option>
            <option value="genre">Genre Distribution</option>
            <option value="language">Language Distribution</option>
            <option value="country">Country Distribution</option>
          </select>
        </div>

        <div class="chart-pie-container">
          <canvas id="execPieChart"></canvas>
        </div>
      </div>
    </div>

    <!-- ========================================== -->
    <!-- 📊 STACKED BAR CHART (FITUR BARU) -->
    <!-- ========================================== -->
    <div class="stacked-chart-section">
      <h3 class="stacked-title">Stacked Bar Chart</h3>
      
      <div class="stacked-controls">
        <label>Category:</label>
        <select v-model="selectedStackedCategory" @change="loadStackedChart">
          <option value="genre">Genre by Status</option>
          <option value="country">Country by Status</option>
          <option value="language">Language by Status</option>
        </select>
      </div>

      <div class="stacked-chart-container">
        <canvas id="stackedChart"></canvas>
      </div>
      
      <p v-if="stackedError" class="error">{{ stackedError }}</p>
    </div>

    <p v-if="loading" class="loading-text">Loading chart...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="pieError" class="error">{{ pieError }}</p>
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
      selectedStackedCategory: "genre",  // STACKED CHART CATEGORY
      chartInstance: null,
      pieChartInstance: null,
      stackedChartInstance: null,  // STACKED CHART INSTANCE
      loading: false,
      error: null,
      pieError: null,
      stackedError: null,
    };
  },

  methods: {
    /* ============================================================
       🔥 LOAD BAR CHART  (KODE ASLI – TIDAK DIUBAH)
    ============================================================ */
    async loadChart() {
      this.loading = true;
      this.error = null;

      try {
        const res = await getExecutiveChart(this.selectedChart);

        if (!res.success) {
          this.error = "Gagal mengambil data chart";
          return;
        }

        const labels = res.labels;
        const totals = res.raw.map((item) => item.Total);

        if (this.chartInstance) {
          this.chartInstance.destroy();
        }

        const ctx = document.getElementById("execChart");
        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, '#ff6fb2');
        gradient.addColorStop(1, '#c74d88');

        this.chartInstance = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [
              {
                label: res.chart_type.toUpperCase(),
                data: totals,
                backgroundColor: gradient,
                borderColor: '#ff6fb2',
                borderWidth: 2,
                borderRadius: 6,
                hoverBackgroundColor: '#ff8fc7',
                hoverBorderColor: '#ff8fc7',
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { 
                display: true,
                labels: { color: '#f5e6d3', font: { size: 13, weight: '500' }, padding: 15 }
              },
              tooltip: {
                backgroundColor: 'rgba(61, 37, 37, 0.95)',
                titleColor: '#ff6fb2',
                bodyColor: '#f5e6d3',
                borderColor: '#ff6fb2',
                borderWidth: 1,
                padding: 12,
              }
            },
            scales: {
              x: { 
                ticks: { color: '#f5e6d3', font: { size: 11 } },
                grid: { color: 'rgba(245, 230, 211, 0.1)', drawBorder: false }
              },
              y: { 
                ticks: { color: '#f5e6d3', font: { size: 11 } },
                grid: { color: 'rgba(245, 230, 211, 0.1)', drawBorder: false },
                beginAtZero: true
              },
            },
          },
        });

      } catch (err) {
        this.error = "Error loading chart.";
      } finally {
        this.loading = false;
      }
    },

    /* ============================================================
       🍩 PIE / DONUT CHART  (KODE ASLI – TIDAK DIUBAH)
    ============================================================ */
    async loadPieChart() {
      this.pieError = null;

      try {
        const res = await getExecutivePieChart(this.selectedPieChart);

        if (!res.success) {
          this.pieError = "Gagal memuat pie chart.";
          return;
        }

        const labels = res.labels;
        const totals = res.totals;

        if (this.pieChartInstance) {
          this.pieChartInstance.destroy();
        }

        const ctx = document.getElementById("execPieChart");

        this.pieChartInstance = new Chart(ctx, {
          type: "doughnut",
          data: {
            labels,
            datasets: [
              {
                data: totals,
                backgroundColor: [
                  "#ff6fb2","#ff85c1","#ff9ad0",
                  "#ffb0e0","#ffc6ef","#e79fd5",
                  "#c27fb8","#d891c3","#f0a8d8"
                ],
                borderWidth: 2,
                borderColor: "#ffffff22",
                hoverBorderColor: "#ff6fb2",
                hoverBorderWidth: 3,
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'right',
                labels: {
                  color: "#f5e6d3",
                  font: { size: 11 },
                  padding: 10,
                  boxWidth: 15,
                  boxHeight: 15,
                }
              },
              tooltip: {
                backgroundColor: 'rgba(61, 37, 37, 0.95)',
                titleColor: '#ff6fb2',
                bodyColor: '#f5e6d3',
                borderColor: '#ff6fb2',
                borderWidth: 1,
                padding: 10,
                callbacks: {
                  label: function(context) {
                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                    const percentage = ((context.parsed / total) * 100).toFixed(1);
                    return `${context.label}: ${context.parsed} (${percentage}%)`;
                  }
                }
              }
            }
          }
        });

      } catch (err) {
        this.pieError = "Error loading pie chart.";
      }
    },

    /* ============================================================
       📊 STACKED BAR CHART (FITUR BARU)
    ============================================================ */
    async loadStackedChart() {
      this.stackedError = null;

      try {
        // Simulate API call - ganti dengan API real kamu
        const stackedData = await this.getStackedData(this.selectedStackedCategory);

        if (this.stackedChartInstance) {
          this.stackedChartInstance.destroy();
        }

        const ctx = document.getElementById("stackedChart");

        // Color palette untuk stacked bars (status colors)
        const statusColors = {
          'Ended': '#ff6fb2',
          'Returning Series': '#ff85c1',
          'Canceled': '#ff9ad0',
          'In Production': '#ffb0e0',
          'Planned': '#ffc6ef',
          'Pilot': '#e79fd5'
        };

        const datasets = stackedData.statuses.map(status => ({
          label: status,
          data: stackedData.data[status] || [],
          backgroundColor: statusColors[status] || '#c27fb8',
          borderColor: 'rgba(255, 111, 178, 0.3)',
          borderWidth: 1,
        }));

        this.stackedChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: stackedData.labels,
            datasets: datasets
          },
          options: {
            indexAxis: 'y',  // 🔥 HORIZONTAL CHART
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
                labels: {
                  color: '#f5e6d3',
                  font: { size: 12, weight: '500' },
                  padding: 15,
                  boxWidth: 20,
                  boxHeight: 12,
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
                padding: 12,
                callbacks: {
                  footer: (tooltipItems) => {
                    const sum = tooltipItems.reduce((acc, item) => acc + item.parsed.x, 0);
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
                  callback: function(value) {
                    return value.toLocaleString();
                  }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.1)', 
                  drawBorder: false 
                },
                beginAtZero: true
              },
              y: {
                stacked: true,
                ticks: { 
                  color: '#f5e6d3', 
                  font: { size: 12, weight: '500' }
                },
                grid: { 
                  color: 'rgba(245, 230, 211, 0.05)', 
                  drawBorder: false 
                }
              }
            }
          }
        });

      } catch (err) {
        this.stackedError = "Error loading stacked chart.";
        console.error(err);
      }
    },

    /* ============================================================
       📦 SIMULATE STACKED DATA (Ganti dengan API real)
    ============================================================ */
    async getStackedData(category) {
      // SIMULASI DATA - Ganti dengan API call real kamu
      // Format: GET /api/executive/stacked?type=genre
      
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
        }, 300);
      });
    },
  },

  mounted() {
    this.loadChart();
    this.loadPieChart();
    this.loadStackedChart();  // Load stacked chart
  },

  beforeUnmount() {
    if (this.chartInstance) this.chartInstance.destroy();
    if (this.pieChartInstance) this.pieChartInstance.destroy();
    if (this.stackedChartInstance) this.stackedChartInstance.destroy();
  }
};
</script>

<style scoped>
.chart-box {
  padding: 24px;
  background: rgba(61, 37, 37, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 111, 178, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* GRID UNTUK BAR & PIE CHART */
.chart-grid {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 32px;
}

/* BAR CHART (ASLI — TIDAK DIUBAH) */
.chart-container {
  flex: 3;
  height: 400px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid rgba(255, 111, 178, 0.1);
}

/* PIE CHART WRAPPER (BARU) */
.chart-pie-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* DROPDOWN PIE CHART */
.pie-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: rgba(61, 37, 37, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(255, 111, 178, 0.15);
}

.pie-controls label {
  color: #f5e6d3;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

.pie-controls select {
  flex: 1;
  padding: 6px 10px;
  background: rgba(61, 37, 37, 0.9);
  border-radius: 6px;
  color: #f5e6d3;
  font-size: 12px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.pie-controls select:hover {
  border-color: #ff6fb2;
  background: rgba(61, 37, 37, 1);
}

.pie-controls select:focus {
  outline: none;
  border-color: #ff6fb2;
  box-shadow: 0 0 0 2px rgba(255, 111, 178, 0.2);
}

/* PIE CHART CONTAINER */
.chart-pie-container {
  height: 350px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid rgba(255, 111, 178, 0.1);
}

/* ========================================== */
/* 📊 STACKED BAR CHART SECTION (FITUR BARU) */
/* ========================================== */
.stacked-chart-section {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 2px solid rgba(255, 111, 178, 0.2);
}

.stacked-title {
  color: #f5e6d3;
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 0.5px;
}

.stacked-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: rgba(61, 37, 37, 0.5);
  border-radius: 8px;
  border: 1px solid rgba(255, 111, 178, 0.15);
  width: fit-content;
}

.stacked-controls label {
  color: #f5e6d3;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.stacked-controls select {
  padding: 8px 14px;
  background: rgba(61, 37, 37, 0.9);
  border-radius: 6px;
  color: #f5e6d3;
  font-size: 13px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
}

.stacked-controls select:hover {
  border-color: #ff6fb2;
  background: rgba(61, 37, 37, 1);
}

.stacked-controls select:focus {
  outline: none;
  border-color: #ff6fb2;
  box-shadow: 0 0 0 2px rgba(255, 111, 178, 0.2);
}

.stacked-chart-container {
  width: 100%;
  height: 450px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid rgba(255, 111, 178, 0.1);
}

/* ========================================== */
/* EXISTING STYLES */
/* ========================================== */

.chart-title {
  color: #f5e6d3;
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  letter-spacing: 0.5px;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.controls label {
  color: #f5e6d3;
  font-size: 14px;
  font-weight: 500;
}

select {
  padding: 8px 14px;
  background: rgba(61, 37, 37, 0.8);
  border-radius: 8px;
  color: #f5e6d3;
  font-size: 13px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

select:hover {
  border-color: #ff6fb2;
  background: rgba(61, 37, 37, 0.95);
}

select:focus {
  border-color: #ff6fb2;
  box-shadow: 0 0 0 2px rgba(255, 111, 178, 0.2);
}

select option {
  background: #3d2525;
  color: #f5e6d3;
  padding: 8px;
}

.loading-text {
  color: #ff6fb2;
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.error {
  color: #ff6fb2;
  font-weight: 600;
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  background: rgba(255, 111, 178, 0.1);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 111, 178, 0.3);
}
</style>