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

    <!-- Canvas Chart -->
    <div class="chart-container">
      <canvas id="execChart"></canvas>
    </div>

    <p v-if="loading" class="loading-text">Loading chart...</p>
    <p v-if="error" class="error">{{ error }}</p>
  </section>
</template>

<script>
import { getExecutiveChart } from "../../utils/api";
import { Chart } from "chart.js/auto";

export default {
  name: "ChartSection",

  data() {
    return {
      selectedChart: "country",
      chartInstance: null,
      loading: false,
      error: null,
    };
  },

  methods: {
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

        // Destroy previous chart untuk mencegah error
        if (this.chartInstance) {
          this.chartInstance.destroy();
        }

        const ctx = document.getElementById("execChart");

        // Gradient untuk bar chart
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
                labels: {
                  color: '#f5e6d3',
                  font: {
                    size: 13,
                    weight: '500'
                  },
                  padding: 15
                }
              },
              tooltip: {
                backgroundColor: 'rgba(61, 37, 37, 0.95)',
                titleColor: '#ff6fb2',
                bodyColor: '#f5e6d3',
                borderColor: '#ff6fb2',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
                callbacks: {
                  label: function(context) {
                    return context.parsed.y.toLocaleString() + ' shows';
                  }
                }
              }
            },
            scales: {
              x: { 
                ticks: { 
                  color: '#f5e6d3',
                  font: {
                    size: 11
                  }
                },
                grid: {
                  color: 'rgba(245, 230, 211, 0.1)',
                  drawBorder: false
                }
              },
              y: { 
                ticks: { 
                  color: '#f5e6d3',
                  font: {
                    size: 11
                  },
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
            },
          },
        });
      } catch (err) {
        this.error = "Error loading chart.";
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    this.loadChart();
  },
  
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }
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
  border-radius: 8px;
  border: 1px solid rgba(255, 111, 178, 0.3);
  background: rgba(61, 37, 37, 0.8);
  color: #f5e6d3;
  font-size: 13px;
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

.chart-container {
  width: 100%;
  height: 400px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid rgba(255, 111, 178, 0.1);
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