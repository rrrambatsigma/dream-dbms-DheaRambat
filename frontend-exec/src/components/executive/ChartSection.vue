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
      selectedPieChart: "status",  // DEFAULT PIE CHART
      chartInstance: null,     // bar chart
      pieChartInstance: null,  // pie chart
      loading: false,
      error: null,
      pieError: null,
    };
  },

  methods: {
    /* ============================================================
       🔥 LOAD BAR CHART  (KODE ASLI MU – TIDAK DIUBAH SATUPUN)
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
       🍩 PIE / DONUT CHART  (DITAMBAHKAN DENGAN DROPDOWN FILTER)
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
  },

  mounted() {
    this.loadChart();
    this.loadPieChart();  // Load pie chart saat mounted
  },

  beforeUnmount() {
    if (this.chartInstance) this.chartInstance.destroy();
    if (this.pieChartInstance) this.pieChartInstance.destroy();
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