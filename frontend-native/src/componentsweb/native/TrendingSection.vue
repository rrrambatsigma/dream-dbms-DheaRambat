<template>
  <section class="trending-section">
    <div class="section-header">
      <h1 class="section-title">
        <span class="fire-icon">🔥</span>
        <span class="trending-text">TRENDING NOW</span>
      </h1>
      <p class="section-subtitle">Top 10 Most Popular TV Shows This Week • By IMDb Votes</p>
    </div>

    <!-- Loading State -->
    <div v-if="trendingLoading" class="loading-container">
      <div class="spinner"></div>
      <p class="loading-text">Loading Trending Shows...</p>
    </div>

    <!-- Trending Horizontal Scroll Container -->
    <div v-else class="trending-scroll-container">
      <div class="trending-scroll">
        <div 
          v-for="(show, index) in trendingShows" 
          :key="show.ShowID"
          class="trending-card"
          :class="{ 'top-three': index < 3 }"
          @click="viewShowDetail(show.ShowID)"
        >
          <div class="card-rank-badge">
            <span class="rank-number">{{ index + 1 }}</span>
            <span class="rank-icon" v-if="index === 0">🏆</span>
          </div>
          
          <div class="card-image-wrapper">
            <div class="card-poster">
              <span class="poster-icon">📺</span>
            </div>
            <div class="rating-overlay">
              <div class="rating-badge">
                <span class="star">⭐</span>
                <span class="rating-num">{{ show.VoteAverage || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <div class="card-info">
            <h3 class="show-title">{{ show.Name }}</h3>
            <div class="show-meta">
              <span class="year">{{ formatYear(show.FirstAirDate) }}</span>
              <span class="separator">•</span>
              <span class="votes">{{ formatVotes(show.VoteCount) }} votes</span>
            </div>
            <p class="show-genres">{{ show.Genres || 'No genre' }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TrendingSection',
  data() {
    return {
      trendingShows: [],
      trendingLoading: true
    }
  },
  mounted() {
    this.loadTrending();
  },
  methods: {
async loadTrending() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/native/top-trending');
    const payload = await response.json();

    // ✅ AMAN & SESUAI RESPONSE BACKEND
    this.trendingShows = Array.isArray(payload.data)
      ? payload.data.slice(0, 10)
      : [];

    console.log('Trending loaded:', this.trendingShows);
  } catch (err) {
    console.error('Error loading trending:', err);
    this.trendingShows = [];
  } finally {
    this.trendingLoading = false;
  }
},
    formatYear(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        return new Date(dateStr).getFullYear();
      } catch {
        return 'N/A';
      }
    },
    formatVotes(votes) {
      if (!votes) return '0';
      if (votes >= 1000000) return (votes / 1000000).toFixed(1) + 'M';
      if (votes >= 1000) return (votes / 1000).toFixed(1) + 'K';
      return votes.toString();
    },
    viewShowDetail(showId) {
      this.$emit('show-detail', showId);
    }
  }
}
</script>

<style scoped>
.trending-section {
  padding: 32px 40px 48px;
  background: linear-gradient(180deg, #1a1612 0%, #0f0c09 100%);
  border-top: 1px solid rgba(152, 57, 68, 0.15);
}

.section-header {
  margin-bottom: 32px;
  text-align: center;
}

.section-title {
  font-size: 28px;
  font-weight: 800;
  color: #f8f4ed;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-family: 'Poppins', sans-serif;
}

.fire-icon {
  font-size: 32px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.trending-text {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 50%, #ff4081 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  font-size: 28px;
  letter-spacing: 1px;
  text-shadow: 0 2px 10px rgba(255, 107, 107, 0.3);
  font-family: 'Poppins', sans-serif;
}

.section-subtitle {
  color: #d8a0a5;
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.3px;
  font-family: 'Poppins', sans-serif;
  margin-top: 8px;
}

/* Horizontal Scroll Container */
.trending-scroll-container {
  overflow-x: auto;
  padding-bottom: 16px;
  margin: 0 -8px;
}

.trending-scroll-container::-webkit-scrollbar {
  height: 6px;
}

.trending-scroll-container::-webkit-scrollbar-track {
  background: rgba(42, 36, 30, 0.5);
  border-radius: 3px;
}

.trending-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(152, 57, 68, 0.4);
  border-radius: 3px;
}

.trending-scroll-container::-webkit-scrollbar-thumb:hover {
  background: rgba(162, 67, 78, 0.6);
}

.trending-scroll {
  display: flex;
  gap: 16px;
  padding: 0 8px;
  min-width: min-content;
}

.trending-card {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  min-width: 200px;
  max-width: 200px;
  flex-shrink: 0;
}

.trending-card:hover {
  transform: translateY(-4px);
  border-color: rgba(152, 57, 68, 0.4);
  box-shadow: 0 8px 20px rgba(152, 57, 68, 0.15);
}

.trending-card.top-three:hover {
  border-color: rgba(152, 57, 68, 0.6);
  box-shadow: 0 8px 20px rgba(152, 57, 68, 0.2);
}

.card-rank-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.85) 0%, 
    rgba(177, 79, 29, 0.85) 100%);
  color: #f8f4ed;
  font-weight: 900;
  font-size: 16px;
  padding: 4px 10px;
  border-radius: 6px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.top-three .card-rank-badge {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.9) 0%, 
    rgba(177, 79, 29, 0.9) 100%);
  color: #f8f4ed;
}

.rank-number {
  line-height: 1;
}

.rank-icon {
  font-size: 14px;
}

.card-image-wrapper {
  position: relative;
  width: 100%;
}

.card-poster {
  width: 100%;
  height: 240px;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.8) 0%, 
    rgba(74, 66, 55, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 2px solid rgba(152, 57, 68, 0.2);
}

.poster-icon {
  font-size: 48px;
}

.rating-overlay {
  position: absolute;
  bottom: 8px;
  right: 8px;
}

.rating-badge {
  background-color: rgba(26, 22, 18, 0.85);
  padding: 4px 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(152, 57, 68, 0.2);
}

.star {
  font-size: 14px;
}

.rating-num {
  color: #f8f4ed;
  font-weight: 700;
  font-size: 13px;
  font-family: 'Poppins', sans-serif;
}

.card-info {
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.show-title {
  font-size: 14px;
  font-weight: 600;
  color: #f8f4ed;
  margin-bottom: 6px;
  line-height: 1.3;
  min-height: 36px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  text-align: center;
  width: 100%;
}

.show-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 12px;
  color: #b87c7c;
  font-family: 'Poppins', sans-serif;
  text-align: center;
  flex-wrap: wrap;
}

.separator {
  color: rgba(152, 57, 68, 0.4);
}

.show-genres {
  color: #d8a0a5;
  font-size: 12px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(152, 57, 68, 0.15);
  border-top-color: #b87c7c;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #b87c7c;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
}

/* Responsive */
@media (max-width: 768px) {
  .trending-section {
    padding-left: 20px;
    padding-right: 20px;
  }

  .trending-card {
    min-width: 160px;
    max-width: 160px;
  }

  .card-poster {
    height: 200px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 20px;
  }

  .trending-card {
    min-width: 140px;
    max-width: 140px;
  }

  .card-poster {
    height: 180px;
  }
}
</style>