<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'

export default {
  props: {
    chartData: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      chart: null
    }
  },

  mounted() {
    Chart.register(...registerables)
    this.renderChart()
  },

  watch: {
    chartData: {
      handler() {
        if (this.chart) {
          this.chart.destroy()
        }
        this.renderChart()
      },
      deep: true
    }
  },

  methods: {
    renderChart() {
      if (!this.$refs.chartCanvas) return

      const ctx = this.$refs.chartCanvas.getContext('2d')
      
      this.chart = new Chart(ctx, {
        type: 'line',
        data: this.chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Total Movies'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Year'
              }
            }
          }
        }
      })
    }
  },

  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 300px;
}
</style>