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
      
      const kpiColors = {
        pink: '#FF6B9D',
        purple: '#BA68C8',
        lightPink: '#F48FB1',
        deepPurple: '#AB47BC',
        magenta: '#F06292',
        violet: '#CE93D8',
        blue: '#4FC3F7',
        teal: '#4DB6AC',
        orange: '#FFB74D',
        brown: '#A1887F'
      }
      
      const donutColors = [
        kpiColors.pink,
        kpiColors.purple,
        kpiColors.lightPink,
        kpiColors.deepPurple,
        kpiColors.magenta,
        kpiColors.violet,
        kpiColors.blue,
        kpiColors.teal,
        kpiColors.orange,
        kpiColors.brown
      ]

      const chartConfig = {
        type: 'doughnut',
        data: {
          ...this.chartData,
          datasets: this.chartData.datasets ? this.chartData.datasets.map(dataset => ({
            ...dataset,
            backgroundColor: donutColors,
            // ⭐⭐⭐ SUBTLE GLOW BORDER ⭐⭐⭐
            borderColor: 'rgba(255, 255, 255, 0.5)', // Putih dengan opacity 0.5
            borderWidth: 2,
            borderRadius: 6,
            // ⭐⭐⭐ HOVER EFFECT RINGAN ⭐⭐⭐
            hoverBorderColor: '#FFFFFF', // Putih solid saat hover
            hoverBorderWidth: 3,
            hoverOffset: 8
          })) : []
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '60%',
          plugins: {
            // ⭐⭐⭐ LEGEND SEPERTI SEBELUMNYA (YANG SUDAH BAGUS) ⭐⭐⭐
            legend: {
              position: 'right',
              labels: {
                color: '#FFFFFF',
                padding: 15,
                font: {
                  size: 12,
                  family: "'Inter', sans-serif",
                  weight: '500'
                },
                usePointStyle: true,
                pointStyle: 'circle',
                boxWidth: 10,
                boxHeight: 10
              }
            },
            tooltip: {
              backgroundColor: 'rgba(50, 42, 36, 0.98)',
              titleColor: '#FFFFFF',
              bodyColor: '#FFFFFF',
              borderColor: kpiColors.purple,
              borderWidth: 1,
              cornerRadius: 8,
              padding: 12,
              titleFont: {
                family: "'Inter', sans-serif",
                size: 13,
                weight: 'bold'
              },
              bodyFont: {
                family: "'Inter', sans-serif",
                size: 12
              },
              callbacks: {
                label: function(context) {
                  let label = context.label || ''
                  if (label) {
                    label += ': '
                  }
                  const value = context.raw
                  const total = context.dataset.data.reduce((a, b) => a + b, 0)
                  const percentage = Math.round((value / total) * 100)
                  return `${label}${value} (${percentage}%)`
                }
              }
            }
          }
        }
      }
      
      this.chart = new Chart(ctx, chartConfig)
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
  height: 100%;
  position: relative;
  /* ⭐⭐⭐ GLOW SUBTLE - HANYA 1 LAYER RINGAN ⭐⭐⭐ */
  filter: drop-shadow(0 2px 6px rgba(255, 107, 157, 0.2));
}

/* LEGEND STYLING (SAMA SEPERTI SEBELUMNYA) */
:deep(.chartjs-render-monitor) .chartjs-legend-text {
  color: #FFFFFF !important;
  text-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.8),
    0 0 1px rgba(0, 0, 0, 0.5) !important;
  font-weight: 600 !important;
  font-family: 'Inter', sans-serif !important;
}

:deep(.chartjs-legend) {
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.5));
}
</style>