<template>
  <div class="marketing-charts">
    <!-- Loading State -->
    <div v-if="isLoading" class="global-loading">
      <div class="loading-spinner"></div>
      <p>Loading charts data...</p>
    </div>

    <!-- Charts Grid -->
    <div v-else class="charts-grid">
      <!-- Row 1: Movies Growth per Year -->
      <div class="chart-row">
        <div class="chart-card wide-chart" 
            @mouseenter="hoveredChart = 'moviesGrowth'" 
            @mouseleave="hoveredChart = null"
            :class="{ 'is-hovered': hoveredChart === 'moviesGrowth' }">
          <div class="chart-header">
            <div class="chart-title-container">
              <div class="chart-icon">📈</div>
              <div class="chart-title-content">
                <h3>Movies Growth per Year</h3>
                <div v-if="yearRange && yearRange.startYear && yearRange.endYear" class="year-range-display">
                  <span class="range-label">Year Range:</span>
                  <span class="range-value">{{ yearRange.startYear }} - {{ yearRange.endYear }}</span>
                  <span class="range-years">{{ yearSpan }} years</span>
                </div>
              </div>
            </div>
            <div class="chart-header-right">
              <span class="chart-status" :class="chartStatus.moviesGrowth">
                {{ getStatusText(chartStatus.moviesGrowth) }}
              </span>
            </div>
          </div>
          <div class="chart-container line-chart-container">
            <LineChart 
              v-if="charts.moviesGrowth && chartStatus.moviesGrowth === 'loaded'" 
              :chartData="charts.moviesGrowth" 
              :options="lineChartOptions"
            />
            <div v-else-if="chartStatus.moviesGrowth === 'loading'" class="chart-loading">
              <div class="spinner-small"></div>
              <p>Loading growth data...</p>
            </div>
            <div v-else-if="chartStatus.moviesGrowth === 'empty'" class="no-data">
              <div class="empty-icon">📈</div>
              <p>No growth data available</p>
            </div>
            <div v-else class="no-data">
              <div class="error-icon-small">❌</div>
              <p>Failed to load growth chart</p>
            </div>
          </div>
          <div class="chart-description">
            <p>Number of new movies released each year</p>
          </div>
        </div>
      </div>

      <!-- Row 2: 2 charts kecil -->
      <div class="chart-row">
        <!-- Genre Distribution -->
        <div class="chart-card" 
             @mouseenter="hoveredChart = 'genreDistribution'" 
             @mouseleave="hoveredChart = null"
             :class="{ 'is-hovered': hoveredChart === 'genreDistribution' }">
          <div class="chart-header">
            <div class="chart-title-container">
              <div class="chart-icon">🎭</div>
              <div class="chart-title-content">
                <h3>Genre Distribution</h3>
              </div>
            </div>
            <div class="chart-header-right">
              <span class="chart-status" :class="chartStatus.genreDistribution">
                {{ getStatusText(chartStatus.genreDistribution) }}
              </span>
            </div>
          </div>
          <div class="chart-container">
            <PieChart 
              v-if="charts.genreDistribution && chartStatus.genreDistribution === 'loaded'" 
              :chartData="charts.genreDistribution" 
              :options="pieChartOptions"
            />
            <div v-else-if="chartStatus.genreDistribution === 'loading'" class="chart-loading">
              <div class="spinner-small"></div>
              <p>Loading data...</p>
            </div>
            <div v-else-if="chartStatus.genreDistribution === 'empty'" class="no-data">
              <div class="empty-icon">📭</div>
              <p>No genre data available</p>
            </div>
            <div v-else class="no-data">
              <div class="error-icon-small">❌</div>
              <p>Failed to load chart</p>
            </div>
          </div>
          <div class="chart-description">
            <p>Distribution across movie genres</p>
          </div>
        </div>

        <!-- Top 10 Streaming Platforms (SEKARANG Horizontal Bar Chart) -->
        <div class="chart-card" 
             @mouseenter="hoveredChart = 'topPlatforms'" 
             @mouseleave="hoveredChart = null"
             :class="{ 'is-hovered': hoveredChart === 'topPlatforms' }">
          <div class="chart-header">
            <div class="chart-title-container">
              <div class="chart-icon">📺</div>
              <div class="chart-title-content">
                <h3>Top 10 Streaming Platforms</h3>
              </div>
            </div>
            <div class="chart-header-right">
              <span class="chart-status" :class="chartStatus.topPlatforms">
                {{ getStatusText(chartStatus.topPlatforms) }}
              </span>
            </div>
          </div>
          <div class="chart-container">
            <!-- BERUBAH: Sekarang pakai HorizontalBarChart -->
            <HorizontalBarChart 
              v-if="charts.topPlatforms && chartStatus.topPlatforms === 'loaded'" 
              :chartData="charts.topPlatforms" 
              :options="horizontalBarOptions"
            />
            <div v-else-if="chartStatus.topPlatforms === 'loading'" class="chart-loading">
              <div class="spinner-small"></div>
              <p>Loading data...</p>
            </div>
            <div v-else-if="chartStatus.topPlatforms === 'empty'" class="no-data">
              <div class="empty-icon">📭</div>
              <p>No platform data available</p>
            </div>
            <div v-else class="no-data">
              <div class="error-icon-small">❌</div>
              <p>Failed to load chart</p>
            </div>
          </div>
          <div class="chart-description">
            <p>Platforms with most movie content</p>
          </div>
        </div>
      </div>

      <!-- Row 3: 1 chart besar horizontal saja -->
      <div class="chart-row tall-charts-row">
        <!-- Top 10 Most Rated Movies (SEKARANG Vertical Bar Chart) -->
        <div class="chart-card tall-chart" 
             @mouseenter="hoveredChart = 'mostRated'" 
             @mouseleave="hoveredChart = null"
             :class="{ 'is-hovered': hoveredChart === 'mostRated' }">
          <div class="chart-header">
            <div class="chart-title-container">
              <div class="chart-icon">🏆</div>
              <div class="chart-title-content">
                <h3>Top 10 Most Rated Movies</h3>
              </div>
            </div>
            <div class="chart-header-right">
              <span class="chart-status" :class="chartStatus.mostRated">
                {{ getStatusText(chartStatus.mostRated) }}
              </span>
            </div>
          </div>
          <div class="chart-container vertical-bar-container tall-chart-container">
            <!-- BERUBAH: Sekarang pakai VerticalBarChart -->
            <VerticalBarChart 
              v-if="charts.mostRated && chartStatus.mostRated === 'loaded'" 
              :chartData="charts.mostRated" 
              :options="verticalBarOptions"
            />
            <div v-else-if="chartStatus.mostRated === 'loading'" class="chart-loading">
              <div class="spinner-small"></div>
              <p>Loading data...</p>
            </div>
            <div v-else-if="chartStatus.mostRated === 'empty'" class="no-data">
              <div class="empty-icon">📭</div>
              <p>No movie rating data available</p>
            </div>
            <div v-else class="no-data">
              <div class="error-icon-small">❌</div>
              <p>Failed to load chart</p>
            </div>
          </div>
          <div class="chart-description">
            <p>Movies with highest number of votes</p>
          </div>
        </div>
      </div>

      <!-- Row 4: Country Distribution Map -->
      <div class="chart-row">
        <div class="chart-card full-width map-chart" 
             @mouseenter="hoveredChart = 'countryCategory'" 
             @mouseleave="hoveredChart = null"
             :class="{ 'is-hovered': hoveredChart === 'countryCategory' }">
          
          <!-- Header dengan SATU dropdown -->
          <div class="chart-header">
            <div class="chart-title-container">
              <div class="chart-icon">🌍</div>
              <div class="chart-title-content">
                <h3>Country Distribution Map</h3>
                <div class="map-controls">
                  <!-- HANYA SATU DROPDOWN -->
                  <div class="dropdown-container">
                    <label class="dropdown-label">Show by:</label>
                    <select v-model="selectedCategoryType" @change="onCategoryTypeChange" class="category-dropdown">
                      <option value="genre">Genres</option>
                      <option value="network">Networks</option>
                      <option value="status">Status</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="chart-header-right">
              <div class="map-info" v-if="totalCountries > 0">
                <span class="map-count">{{ totalCountries }} countries</span>
                <span class="map-total">{{ totalMoviesGlobal.toLocaleString() }} total movies</span>
              </div>
              <span class="chart-status" :class="chartStatus.countryCategory">
                {{ getStatusText(chartStatus.countryCategory) }}
              </span>
            </div>
          </div>
          
          <!-- Map Container -->
          <div class="chart-container country-chart-container">
            <CountryCategoryMap 
              v-if="charts.countryCategory && chartStatus.countryCategory === 'loaded'" 
              :chartData="charts.countryCategory" 
              :categoryType="selectedCategoryType"
            />
            <div v-else-if="chartStatus.countryCategory === 'loading'" class="chart-loading">
              <div class="spinner-small"></div>
              <p>Loading map data...</p>
            </div>
            <div v-else-if="chartStatus.countryCategory === 'empty'" class="no-data">
              <div class="empty-icon">📭</div>
              <p>No country data available</p>
            </div>
            <div v-else class="no-data">
              <div class="error-icon-small">❌</div>
              <p>Failed to load map</p>
            </div>
          </div>
          <div class="chart-description">
            <p>Map shows total movies per country. Hover to see top 3 {{ selectedCategoryType }} details.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "./charts/LineChart.vue";
import PieChart from "./charts/PieChart.vue";
import VerticalBarChart from "./charts/VerticalBarChart.vue";
import HorizontalBarChart from "./charts/HorizontalBarChart.vue";
import CountryCategoryMap from "./charts/CountryCategoryMap.vue";

export default {
  name: 'MarketingCharts',
  components: {
    LineChart,
    PieChart,
    VerticalBarChart,
    HorizontalBarChart,
    CountryCategoryMap
  },
  
  props: {
    yearRange: {
      type: Object,
      default: null
    }
  },

  data() {
    return {
      hoveredChart: null,
      isLoading: false,
      totalCountries: 0,
      totalMoviesGlobal: 0,
      debounceTimer: null,
      
      // Hanya satu dropdown
      selectedCategoryType: 'genre',
      
      charts: {
        moviesGrowth: null,
        genreDistribution: null,
        topPlatforms: null,
        mostRated: null,
        countryCategory: null
      },
      
      chartStatus: {
        moviesGrowth: 'idle',
        genreDistribution: 'idle',
        topPlatforms: 'idle',
        mostRated: 'idle',
        countryCategory: 'idle'
      },
      
      // Chart Options (DIPERBARUI untuk tukar bentuk)
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(50, 42, 36, 0.95)',
            titleColor: '#FF6B9D',
            bodyColor: '#FFD1DC',
            borderColor: '#BA68C8',
            borderWidth: 1,
            callbacks: {
              title: function(context) {
                return `Year: ${context[0].label}`;
              },
              label: function(context) {
                return `Movies: ${context.parsed.y.toLocaleString()}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Year',
              color: '#FFB6C1',
              font: { size: 12, weight: 'bold' }
            },
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 }
            },
            grid: { 
              color: 'rgba(216, 160, 165, 0.1)',
              drawBorder: false
            }
          },
          y: {
            title: {
              display: true,
              text: 'Number of Movies',
              color: '#FFB6C1',
              font: { size: 12, weight: 'bold' }
            },
            beginAtZero: true,
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 },
              callback: function(value) {
                if (value >= 1000) {
                  return (value / 1000).toFixed(1) + 'k';
                }
                return value;
              }
            },
            grid: { 
              color: 'rgba(216, 160, 165, 0.1)',
              drawBorder: false
            }
          }
        }
      },
      
      // Opsi untuk Vertical Bar Chart (Most Rated Movies)
      verticalBarOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(50, 42, 36, 0.95)',
            titleColor: '#FF6B9D',
            bodyColor: '#FFD1DC',
            borderColor: '#BA68C8',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                return `Votes: ${context.parsed.y.toLocaleString()}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Movie Titles',
              color: '#FFB6C1',
              font: { size: 12, weight: 'bold' }
            },
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 }
            },
            grid: { 
              color: 'rgba(216, 160, 165, 0.1)',
              drawBorder: false
            }
          },
          y: {
            title: {
              display: true,
              text: 'Number of Votes',
              color: '#FFB6C1',
              font: { size: 12, weight: 'bold' }
            },
            beginAtZero: true,
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 },
              callback: function(value) {
                if (value >= 1000000) {
                  return (value / 1000000).toFixed(1) + 'M';
                }
                if (value >= 1000) {
                  return (value / 1000).toFixed(1) + 'k';
                }
                return value;
              }
            },
            grid: { 
              color: 'rgba(216, 160, 165, 0.1)',
              drawBorder: false
            }
          }
        }
      },
      
      // Opsi untuk Horizontal Bar Chart (Streaming Platforms)
      horizontalBarOptions: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(50, 42, 36, 0.95)',
            titleColor: '#FF6B9D',
            bodyColor: '#FFD1DC',
            borderColor: '#BA68C8',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                return `Movies: ${context.parsed.x.toLocaleString()}`;
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Number of Movies',
              color: '#FFB6C1',
              font: { size: 12, weight: 'bold' }
            },
            beginAtZero: true,
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 },
              callback: function(value) {
                if (value >= 1000) {
                  return (value / 1000).toFixed(1) + 'k';
                }
                return value;
              }
            },
            grid: { 
              color: 'rgba(216, 160, 165, 0.1)',
              drawBorder: false
            }
          },
          y: {
            title: {
              display: false
            },
            ticks: {
              color: '#FFB6C1',
              font: { size: 11 }
            },
            grid: { 
              display: false,
              drawBorder: false
            }
          }
        }
      },
      
      pieChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              color: '#FFD1DC',
              padding: 15,
              font: { size: 11 },
              usePointStyle: true,
              pointStyle: 'circle',
              generateLabels: function(chart) {
                const data = chart.data;
                if (data.labels.length && data.datasets.length) {
                  return data.labels.map((label, i) => {
                    const value = data.datasets[0].data[i];
                    const percentage = ((value / data.datasets[0].data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                    return {
                      text: `${label}: ${value} (${percentage}%)`,
                      fillStyle: data.datasets[0].backgroundColor[i],
                      strokeStyle: data.datasets[0].borderColor[i],
                      lineWidth: 1,
                      hidden: false,
                      index: i
                    };
                  });
                }
                return [];
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(50, 42, 36, 0.95)',
            titleColor: '#FF6B9D',
            bodyColor: '#FFD1DC',
            borderColor: '#BA68C8',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                const label = context.label || '';
                const value = context.parsed;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = Math.round((value / total) * 100);
                return `${label}: ${value} (${percentage}%)`;
              }
            }
          }
        }
      }
    };
  },

  computed: {
    yearSpan() {
      if (!this.yearRange) return 0;
      return this.yearRange.yearSpan || Math.abs(this.yearRange.endYear - this.yearRange.startYear) + 1;
    }
  },

  watch: {
    yearRange: {
      handler(newRange) {
        console.log('🎯 Year range changed:', newRange);
        if (newRange && newRange.startYear && newRange.endYear) {
          if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
          }
          this.debounceTimer = setTimeout(() => {
            this.loadAllCharts();
          }, 300);
        }
      },
      deep: true,
      immediate: false
    }
  },

  mounted() {
    console.log('🚀 MarketingCharts Component Mounted');
    if (this.yearRange && this.yearRange.startYear && this.yearRange.endYear) {
      setTimeout(() => {
        this.loadAllCharts();
      }, 500);
    }
  },

  methods: {
    getStatusText(status) {
      const statusMap = {
        'idle': 'Ready',
        'loading': 'Loading...',
        'loaded': 'Loaded',
        'empty': 'No Data',
        'error': 'Error'
      };
      return statusMap[status] || status;
    },

    async refreshCharts() {
      console.log('🔄 Manual refresh');
      if (this.yearRange) {
        await this.loadAllCharts();
      }
    },

    async loadAllCharts() {
      console.log('📊 Loading all charts');
      this.isLoading = true;
      
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('❌ No token found');
        this.setAllChartsError('Please login first');
        this.isLoading = false;
        return;
      }

      let yearParams = '';
      if (this.yearRange && this.yearRange.startYear && this.yearRange.endYear) {
        yearParams = `?start_year=${this.yearRange.startYear}&end_year=${this.yearRange.endYear}`;
      } else {
        yearParams = '?start_year=2000&end_year=2024';
      }
      
      const API_BASE = "http://127.0.0.1:5000/api/marketing/charts";

      const endpoints = [
        { 
          key: 'moviesGrowth', 
          url: `${API_BASE}/movies-growth-year${yearParams}`,
          name: 'Movies Growth per Year'
        },
        { 
          key: 'genreDistribution', 
          url: `${API_BASE}/genre-distribution${yearParams}`,
          name: 'Genre Distribution'
        },
        { 
          key: 'topPlatforms', 
          url: `${API_BASE}/top-platforms${yearParams}`,
          name: 'Top Platforms'
        },
        { 
          key: 'mostRated', 
          url: `${API_BASE}/top-most-rated${yearParams}`,
          name: 'Top Most Rated'
        }
      ];

      try {
        // Reset chart status
        Object.keys(this.chartStatus).forEach(key => {
          if (key !== 'countryCategory') {
            this.chartStatus[key] = 'loading';
            this.charts[key] = null;
          }
        });

        // Load charts biasa
        const loadPromises = endpoints.map(endpoint => 
          this.loadChart(endpoint.key, endpoint.url, endpoint.name, token)
        );
        
        await Promise.all(loadPromises);
        
        // Load country category map
        await this.loadCountryCategoryMap();
        
        console.log('✅ All charts loaded');
        
      } catch (error) {
        console.error('❌ Error loading charts:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async loadChart(chartKey, url, chartName, token) {
      console.log(`📥 Fetching ${chartName}`);
      
      try {
        const cacheBuster = `&_=${Date.now()}`;
        const urlWithCache = url + cacheBuster;
        
        const response = await fetch(urlWithCache, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          cache: 'no-cache'
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        if (result.success && result.data && Array.isArray(result.data) && result.data.length > 0) {
          const chartData = this.prepareChartData(chartKey, result.data);
          if (chartData) {
            this.charts[chartKey] = chartData;
            this.chartStatus[chartKey] = 'loaded';
            console.log(`✅ ${chartName} loaded`);
          } else {
            this.chartStatus[chartKey] = 'empty';
          }
        } else {
          this.chartStatus[chartKey] = 'empty';
          this.charts[chartKey] = null;
        }

      } catch (error) {
        console.error(`❌ Error loading ${chartName}:`, error.message);
        this.chartStatus[chartKey] = 'error';
        this.charts[chartKey] = null;
      }
    },

    prepareChartData(chartKey, rawData) {
      if (!Array.isArray(rawData) || rawData.length === 0) {
        return null;
      }

      const colors = {
        pink: '#FF6B9D',
        purple: '#BA68C8',
        blue: '#4FC3F7',
        teal: '#4DB6AC',
        orange: '#FFB74D'
      };

      switch(chartKey) {
        case 'moviesGrowth':
          const sortedData = [...rawData].sort((a, b) => 
            (a.Year || a.year || 0) - (b.Year || b.year || 0)
          );
          
          return {
            labels: sortedData.map(item => (item.Year || item.year || 'N/A').toString()),
            datasets: [{
              label: 'Total Movies',
              data: sortedData.map(item => item.TotalShows || item.total_movies || item.count || 0),
              borderColor: colors.pink,
              backgroundColor: 'rgba(255, 107, 157, 0.2)',
              borderWidth: 3,
              fill: true,
              tension: 0.4,
              pointBackgroundColor: colors.pink,
              pointBorderColor: '#FFFFFF',
              pointBorderWidth: 2,
              pointRadius: 4,
              pointHoverRadius: 6
            }]
          };

        case 'genreDistribution':
          return {
            labels: rawData.map(item => item.GenreName || item.genre || 'Unknown'),
            datasets: [{
              data: rawData.map(item => item.TotalMovies || item.count || item.value || 0),
              backgroundColor: [
                colors.pink, colors.purple, colors.blue, 
                colors.teal, colors.orange, '#FFD54F',
                '#00BCD4', '#CDDC39', '#FF8A65', '#AED581'
              ],
              borderWidth: 1,
              borderColor: 'rgba(255, 255, 255, 0.2)',
              hoverOffset: 15
            }]
          };

        case 'topPlatforms':
          const platformsData = rawData.slice(0, 10);
          return {
            labels: platformsData.map(item => {
              const name = item.Platform || item.platform || item.name || 'Unknown';
              return name.length > 20 ? name.substring(0, 17) + '...' : name;
            }),
            datasets: [{
              label: 'Total Movies',
              data: platformsData.map(item => item.TotalMovies || item.count || item.value || 0),
              backgroundColor: platformsData.map((_, index) => 
                index < 3 ? colors.purple : colors.pink
              ),
              borderColor: platformsData.map((_, index) => 
                index < 3 ? colors.purple : colors.pink
              ),
              borderWidth: 1,
              borderRadius: 6,
              barPercentage: 0.7
            }]
          };

        case 'mostRated':
          const ratedData = rawData.slice(0, 10);
          return {
            labels: ratedData.map(item => {
              const name = item.Movie || item.movie || item.name || 'Unknown';
              return name.length > 25 ? name.substring(0, 22) + '...' : name;
            }),
            datasets: [{
              label: 'Vote Count',
              data: ratedData.map(item => item.VoteCount || item.votes || item.value || 0),
              backgroundColor: ratedData.map((_, index) => 
                index < 3 ? colors.purple : colors.pink
              ),
              borderColor: ratedData.map((_, index) => 
                index < 3 ? colors.purple : colors.pink
              ),
              borderWidth: 1,
              borderRadius: 4,
              barPercentage: 0.8
            }]
          };

        default:
          return null;
      }
    },

    async onCategoryTypeChange() {
      console.log('🔄 Category type changed to:', this.selectedCategoryType);
      await this.loadCountryCategoryMap();
    },

    async loadCountryCategoryMap() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('❌ No token found');
        return;
      }

      const url = `http://127.0.0.1:5000/api/marketing/charts/country-category-map?start_year=${this.yearRange.startYear}&end_year=${this.yearRange.endYear}&category_type=${this.selectedCategoryType}`;

      console.log('🗺️ Loading map:', url);
      
      this.chartStatus.countryCategory = 'loading';
      
      try {
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          },
          cache: 'no-cache'
        });

        if (response.ok) {
          const result = await response.json();
          
          if (result.success && result.data && result.data.length > 0) {
            this.charts.countryCategory = result.data;
            this.chartStatus.countryCategory = 'loaded';
            this.totalCountries = result.countries_count || result.data.length;
            this.totalMoviesGlobal = result.total_movies_global || 0;
            console.log(`✅ Loaded ${this.totalCountries} countries`);
          } else {
            this.chartStatus.countryCategory = 'empty';
            this.charts.countryCategory = null;
          }
        } else {
          throw new Error(`HTTP ${response.status}`);
        }
      } catch (error) {
        console.error('❌ Error loading map:', error);
        this.chartStatus.countryCategory = 'error';
        this.charts.countryCategory = null;
      }
    },

    setAllChartsError(message) {
      Object.keys(this.chartStatus).forEach(key => {
        this.chartStatus[key] = 'error';
      });
      console.error('❌ All charts failed:', message);
    }
  }
};
</script>

<style scoped>
.marketing-charts {
  padding: 20px;
  background: linear-gradient(135deg, 
    rgba(28, 24, 20, 0.95) 0%, 
    rgba(38, 32, 26, 0.95) 100%);
  border-radius: 18px;
  border: 2px solid rgba(216, 160, 165, 0.2);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: relative;
  min-height: 600px;
}

.global-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(28, 24, 20, 0.9);
  border-radius: 18px;
  z-index: 100;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(216, 160, 165, 0.2);
  border-top: 4px solid #FF6B9D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.global-loading p {
  color: #FFD1DC;
  font-size: 1rem;
  font-weight: 600;
}

.year-range-display {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 5px;
  flex-wrap: wrap;
}

.range-label {
  color: #FFB6C1;
  font-size: 0.8rem;
  font-weight: 500;
}

.range-value {
  color: #BA68C8;
  font-size: 0.85rem;
  font-weight: 600;
  background: rgba(186, 104, 200, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid rgba(186, 104, 200, 0.2);
}

.range-years {
  color: #4DB6AC;
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(77, 182, 172, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid rgba(77, 182, 172, 0.2);
}

.charts-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.chart-row:not(:first-child):not(:last-child):not(.tall-charts-row) {
  grid-template-columns: 1fr 1fr;
}

.chart-row.tall-charts-row {
  grid-template-columns: 1fr;
  min-height: 400px;
}

.chart-card {
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(38, 32, 26, 0.95) 50%,
    rgba(50, 42, 36, 0.95) 100%);
  border: 2px solid rgba(216, 160, 165, 0.15);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.chart-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 107, 157, 0.5) 50%, 
    transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.chart-card.is-hovered::before {
  opacity: 1;
}

.chart-card.wide-chart {
  grid-column: 1 / -1;
  min-height: 380px;
  height: 380px;
}

.chart-card:not(.tall-chart):not(.wide-chart):not(.full-width) {
  min-height: 360px;
  height: 360px;
}

.chart-card.tall-chart {
  min-height: 420px;
  height: auto;
}

.chart-card.full-width.map-chart {
  grid-column: 1 / -1;
  min-height: 450px;
  height: auto;
}

.chart-card.is-hovered {
  transform: translateY(-4px);
  border-color: rgba(255, 107, 157, 0.4);
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.5),
    0 0 20px rgba(255, 107, 157, 0.1),
    inset 0 0 30px rgba(255, 107, 157, 0.05);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(216, 160, 165, 0.2);
  min-height: 60px;
  flex-shrink: 0;
}

.chart-title-container {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.chart-title-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  height: 100%;
}

.chart-icon {
  font-size: 1.3rem;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: linear-gradient(135deg, #FF6B9D, #BA68C8);
  border: 2px solid rgba(255, 255, 255, 0.1);
  color: white;
  box-shadow: 0 4px 12px rgba(255, 107, 157, 0.3);
  flex-shrink: 0;
}

.chart-header h3 {
  margin: 0;
  color: #FFD1DC;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  line-height: 1.3;
  display: flex;
  align-items: center;
  min-height: 45px;
}

.chart-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: auto;
  flex-shrink: 0;
  flex-direction: column;
  align-items: flex-end;
  height: 100%;
  justify-content: center;
}

.map-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.map-count {
  color: #4DB6AC;
  font-size: 0.8rem;
  font-weight: 600;
  background: rgba(77, 182, 172, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(77, 182, 172, 0.2);
}

.map-total {
  color: #FF6B9D;
  font-size: 0.8rem;
  font-weight: 600;
  background: rgba(255, 107, 157, 0.1);
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 157, 0.2);
}

.map-controls {
  margin-top: 8px;
  padding: 8px 0;
}

.dropdown-container {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  background: rgba(50, 42, 36, 0.6);
  padding: 10px 14px;
  border-radius: 10px;
  border: 1px solid rgba(255, 107, 157, 0.2);
}

.dropdown-label {
  color: #FFD1DC;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: 0.3px;
}

.category-dropdown {
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95), 
    rgba(38, 32, 26, 0.95));
  border: 2px solid rgba(255, 107, 157, 0.4);
  border-radius: 8px;
  color: #FFD1DC;
  padding: 8px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 140px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23FF6B9D'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
  padding-right: 35px;
}

.category-dropdown:hover {
  border-color: #FF6B9D;
  background-color: rgba(50, 42, 36, 0.95);
  box-shadow: 0 4px 12px rgba(255, 107, 157, 0.2);
}

.category-dropdown:focus {
  outline: none;
  border-color: #FF6B9D;
  box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2);
}

.chart-status {
  font-size: 0.7rem;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  white-space: nowrap;
  min-width: 80px;
  text-align: center;
  margin-top: 4px;
}

.chart-status.loading {
  background: rgba(79, 195, 247, 0.15);
  color: #4FC3F7;
  border: 1px solid rgba(79, 195, 247, 0.3);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.chart-status.loaded {
  background: rgba(77, 182, 172, 0.15);
  color: #4DB6AC;
  border: 1px solid rgba(77, 182, 172, 0.3);
}

.chart-status.empty {
  background: rgba(255, 183, 77, 0.15);
  color: #FFB74D;
  border: 1px solid rgba(255, 183, 77, 0.3);
}

.chart-status.error {
  background: rgba(244, 143, 177, 0.15);
  color: #F48FB1;
  border: 1px solid rgba(244, 143, 177, 0.3);
}

.chart-status.idle {
  background: rgba(176, 190, 197, 0.15);
  color: #B0BEC5;
  border: 1px solid rgba(176, 190, 197, 0.3);
}

.chart-container {
  flex: 1;
  width: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.line-chart-container {
  height: 100%;
  min-height: 280px;
}

.vertical-bar-container.tall-chart-container {
  height: 100%;
  min-height: 350px;
}

.horizontal-bar-container {
  height: 100%;
  min-height: 280px;
}

.country-chart-container {
  height: 100%;
  min-height: 320px;
  position: relative;
}

.chart-loading {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  gap: 15px;
}

.spinner-small {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(216, 160, 165, 0.2);
  border-top: 3px solid #FF6B9D;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.chart-loading p {
  color: #FFB6C1;
  font-size: 0.9rem;
  font-weight: 500;
}

.no-data {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  gap: 12px;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.error-icon-small {
  font-size: 3rem;
  opacity: 0.7;
}

.no-data p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
  text-align: center;
  font-style: italic;
}

.chart-description {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(216, 160, 165, 0.1);
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chart-description p {
  margin: 0;
  color: #FFB6C1;
  font-size: 0.85rem;
  text-align: center;
  opacity: 0.8;
}

@media (max-width: 1400px) {
  .chart-row:not(:first-child):not(:last-child) {
    gap: 16px;
  }
  
  .chart-card.wide-chart {
    min-height: 380px;
    height: 380px;
  }
  
  .chart-card:not(.tall-chart):not(.wide-chart):not(.full-width) {
    min-height: 360px;
    height: 360px;
  }
  
  .chart-card.tall-chart {
    min-height: 400px;
  }
  
  .chart-card.full-width.map-chart {
    min-height: 420px;
  }
}

@media (max-width: 1200px) {
  .chart-row:not(:first-child):not(:last-child) {
    grid-template-columns: 1fr;
  }
  
  .chart-row.tall-charts-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .marketing-charts {
    padding: 16px;
  }
  
  .charts-grid {
    gap: 16px;
  }
  
  .chart-row {
    gap: 12px;
  }
  
  .chart-card {
    padding: 16px;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .chart-header-right {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
    flex-direction: row;
    align-items: center;
  }
  
  .dropdown-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    width: 100%;
  }
  
  .category-dropdown {
    width: 100%;
    min-width: unset;
  }
  
  .chart-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .chart-header h3 {
    font-size: 1.1rem;
    min-height: 40px;
  }
}

@media (max-width: 480px) {
  .marketing-charts {
    padding: 12px;
  }
  
  .charts-grid {
    gap: 12px;
  }
  
  .chart-row {
    gap: 10px;
  }
  
  .chart-card {
    padding: 14px;
  }
  
  .chart-header h3 {
    font-size: 1rem;
  }
  
  .chart-icon {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }
  
  .chart-status {
    font-size: 0.65rem;
    padding: 5px 8px;
    min-width: 70px;
  }
}
</style>