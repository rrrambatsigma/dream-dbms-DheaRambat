<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'

export default {
  name: 'VerticalBarChart',
  
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
      
      // PURPLE yang lebih VIVID dan CONTRAST
      const createVividPurpleGradient = (ctx) => {
        const gradient = ctx.createLinearGradient(0, 0, 0, 250)
        gradient.addColorStop(0, '#9C27B0')     // Bright Purple
        gradient.addColorStop(0.7, '#BA68C8')   // Main Purple
        gradient.addColorStop(1, '#CE93D8')     // Light Purple
        return gradient
      }
      
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          ...this.chartData,
          datasets: this.chartData.datasets.map(dataset => ({
            ...dataset,
            backgroundColor: createVividPurpleGradient(ctx),
            borderColor: '#FFFFFF',
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false,
            // Tambahkan hover effect yang jelas
            hoverBackgroundColor: '#9C27B0'
          }))
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'x',
          plugins: {
            legend: {
              position: 'top',
              labels: {
                color: '#FFFFFF',
                font: { 
                  size: 13,
                  family: "'Inter', sans-serif",
                  weight: '600'
                },
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle',
                boxWidth: 12,
                boxHeight: 12
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              backgroundColor: '#9C27B0',
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
                  return `${context.dataset.label || 'Value'}: ${context.parsed.y.toLocaleString()}`
                }
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: '#E1BEE7',
                font: { 
                  size: 12,
                  family: "'Inter', sans-serif",
                  weight: '600'
                },
                maxRotation: 45,
                padding: 10
              },
              grid: { 
                color: 'rgba(156, 39, 176, 0.2)',
                drawBorder: false, // Tidak ada border axis
                lineWidth: 1
              },
              border: {
                display: false // DISINI: Hapus border X axis
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: '#FFFFFF',
                font: { 
                  size: 12,
                  family: "'Inter', sans-serif",
                  weight: '600'
                },
                padding: 8,
                callback: function(value) {
                  return value.toLocaleString()
                }
              },
              grid: { 
                color: 'rgba(156, 39, 176, 0.2)',
                drawBorder: false, // Tidak ada border axis
                lineWidth: 1,
                borderDash: [2, 3]
              },
              border: {
                display: false // DISINI: Hapus border Y axis
              }
            }
          },
          layout: {
            padding: {
              left: 10,
              right: 15,
              top: 20,
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
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  filter: drop-shadow(0 2px 8px rgba(156, 39, 176, 0.3));
}
</style>