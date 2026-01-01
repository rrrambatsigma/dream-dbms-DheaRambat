<template>
  <div class="horizontal-bar-wrapper">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'

export default {
  name: 'HorizontalBarChart',
  
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
      if (!this.$refs.chartCanvas || !this.chartData) return

      const ctx = this.$refs.chartCanvas.getContext('2d')
      
      // PINK yang lebih VIVID dan CONTRAST
      const createVividPinkGradient = (ctx) => {
        const gradient = ctx.createLinearGradient(0, 0, 350, 0)
        gradient.addColorStop(0, '#FF4081')     // Bright Pink
        gradient.addColorStop(0.7, '#FF6B9D')   // Main Pink
        gradient.addColorStop(1, '#FF8FAD')     // Light Pink
        return gradient
      }
      
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          ...this.chartData,
          datasets: this.chartData.datasets.map(dataset => ({
            ...dataset,
            backgroundColor: createVividPinkGradient(ctx),
            borderColor: '#FFFFFF',
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false,
            hoverBackgroundColor: '#FF4081'
          }))
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              backgroundColor: '#FF4081',
              titleColor: '#FFFFFF',
              bodyColor: '#FFFFFF',
              borderColor: '#FFFFFF',
              borderWidth: 2,
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
                  return `Votes: ${context.parsed.x.toLocaleString()}`
                },
                title: function(tooltipItems) {
                  const label = tooltipItems[0].label
                  return label.length > 40 ? label.substring(0, 37) + '...' : label
                }
              }
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              ticks: {
                color: '#FFB6C1',
                font: { 
                  size: 11,
                  family: "'Inter', sans-serif",
                  weight: '600'
                },
                callback: function(value) {
                  return value.toLocaleString()
                },
                padding: 8
              },
              grid: { 
                color: 'rgba(255, 64, 129, 0.2)',
                drawBorder: false, // Tidak ada border axis
                lineWidth: 1
              },
              border: {
                display: false // DISINI: Hapus border X axis
              }
            },
            y: {
              ticks: {
                color: '#FFFFFF',
                font: { 
                  size: 12,
                  family: "'Inter', sans-serif",
                  weight: '600'
                },
                autoSkip: false,
                maxRotation: 0,
                padding: 10,
                mirror: false,
                callback: function(value, index, values) {
                  const label = this.getLabelForValue(value)
                  if (label.length > 25) {
                    return label.substring(0, 22) + '...'
                  }
                  return label
                }
              },
              grid: { 
                color: 'rgba(255, 64, 129, 0.15)',
                drawBorder: false, // Tidak ada border axis
                display: false
              },
              border: {
                display: false // DISINI: Hapus border Y axis
              }
            }
          },
          layout: {
            padding: {
              left: 8,
              right: 20,
              top: 10,
              bottom: 10
            }
          },
          animation: {
            duration: 1000,
            easing: 'easeOutQuart'
          },
          elements: {
            bar: {
              borderRadius: 8,
              borderSkipped: false,
              borderWidth: 2
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
.horizontal-bar-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  filter: drop-shadow(0 2px 8px rgba(255, 64, 129, 0.3));
}

:deep(canvas) {
  display: block;
  max-width: 100%;
  max-height: 100%;
}
</style>