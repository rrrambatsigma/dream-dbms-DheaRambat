<template>
  <div class="bar-chart-container">
    <!-- Chart Header -->
    <div class="chart-header">
      <div class="title-section">
        <div class="title-icon">🏢</div>
        <h2 class="chart-title">Top 10 Production Companies</h2>
      </div>
      <div class="chart-subtitle">Ranked by movie count, ratings & votes</div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>LOADING DATA...</p>
    </div>

    <!-- Bar Chart -->
    <div v-else class="chart-content">
      <div 
        v-for="(company, index) in displayData" 
        :key="company.id || index" 
        class="chart-bar"
        :class="{ 'first-place': index === 0 }"
      >
        <div class="bar-info">
          <div class="rank">#{{ index + 1 }}</div>
          <div class="name">{{ company.company || 'Unknown Company' }}</div>
          <div class="stats">
            <span class="movie-count">{{ company.total_movies || 0 }} movies</span>
            <span class="rating">⭐ {{ company.avg_rating?.toFixed(1) || '0.0' }}</span>
          </div>
        </div>

        <div class="bar-wrapper">
          <div class="bar-track">
            <div 
              class="bar-fill" 
              :style="{ width: calculateBarWidth(company.total_movies) + '%' }"
            >
              <div class="votes-info">
                <span class="votes-icon">👤</span>
                <span class="votes-count">{{ company.total_votes?.toLocaleString() || '0' }} votes</span>
              </div>
            </div>
          </div>
          <div class="bar-value">{{ company.total_movies?.toLocaleString() || '0' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductionCompaniesChart',
  props: {
    chartData: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      displayData: [],
      maxValue: 0
    };
  },
  watch: {
    chartData: {
      immediate: true,
      handler(newData) {
        if (newData && newData.length > 0) {
          // Take top 10 and sort by total_movies
          this.displayData = [...newData]
            .sort((a, b) => (b.total_movies || 0) - (a.total_movies || 0))
            .slice(0, 10);
          this.calculateMaxValue();
        } else {
          this.displayData = [];
        }
      }
    }
  },
  methods: {
    calculateMaxValue() {
      if (this.displayData.length === 0) {
        this.maxValue = 0;
        return;
      }
      this.maxValue = Math.max(...this.displayData.map(c => c.total_movies || 0));
    },

    calculateBarWidth(value) {
      if (this.maxValue === 0 || !value) return 0;
      const percentage = (value / this.maxValue) * 100;
      return Math.min(Math.max(percentage, 1), 100); // At least 1% width
    }
  }
};
</script>

<style scoped>
.bar-chart-container {
  width: 100%;
  height: 100%;
  background: rgba(15, 15, 25, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-family: 'Segoe UI', system-ui, sans-serif;
}

/* Header Styles */
.chart-header {
  margin-bottom: 28px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.title-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 8px;
}

.title-icon {
  font-size: 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.chart-title {
  color: #fff;
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.5px;
}

.chart-subtitle {
  color: #b0b7d4;
  font-size: 0.95rem;
  font-weight: 500;
  margin-left: 68px;
  opacity: 0.8;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  gap: 20px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(102, 126, 234, 0.2);
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.loading-state p {
  color: #b0b7d4;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 1px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Chart Content */
.chart-content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.chart-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 18px 20px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.chart-bar:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.chart-bar.first-place {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.05));
  border-color: rgba(102, 126, 234, 0.3);
}

/* Bar Info */
.bar-info {
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 320px;
}

.rank {
  font-size: 1.3rem;
  font-weight: 900;
  color: #667eea;
  width: 40px;
  text-align: center;
}

.name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  flex-grow: 1;
  letter-spacing: -0.3px;
}

.stats {
  display: flex;
  align-items: center;
  gap: 20px;
  color: #b0b7d4;
  font-size: 0.9rem;
  font-weight: 600;
}

.movie-count {
  background: rgba(255, 255, 255, 0.08);
  padding: 4px 12px;
  border-radius: 20px;
  color: #a5b4fc;
}

.rating {
  color: #ffd700;
  display: flex;
  align-items: center;
  gap: 5px;
}

/* Bar Wrapper */
.bar-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 400px;
  max-width: 600px;
}

.bar-track {
  flex: 1;
  height: 28px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  height: 100%;
  border-radius: 14px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  position: relative;
  animation: fillAnimation 1.5s ease-out;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 15px;
  min-width: 80px;
}

@keyframes fillAnimation {
  from { width: 0; }
}

.bar-value {
  font-size: 1.2rem;
  font-weight: 800;
  color: #fff;
  min-width: 60px;
  text-align: right;
}

/* Votes Info inside bar */
.votes-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 0.85rem;
  font-weight: 600;
  opacity: 0.9;
}

.votes-icon {
  font-size: 0.9rem;
}

.votes-count {
  white-space: nowrap;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .bar-info {
    min-width: 260px;
  }
  
  .bar-wrapper {
    min-width: 300px;
  }
}

@media (max-width: 768px) {
  .bar-chart-container {
    padding: 16px;
  }
  
  .chart-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }
  
  .bar-info {
    min-width: auto;
    flex-wrap: wrap;
    gap: 12px;
  }
  
  .bar-wrapper {
    min-width: auto;
    max-width: none;
  }
  
  .chart-title {
    font-size: 1.5rem;
  }
  
  .title-icon {
    width: 44px;
    height: 44px;
    font-size: 22px;
  }
}
</style>