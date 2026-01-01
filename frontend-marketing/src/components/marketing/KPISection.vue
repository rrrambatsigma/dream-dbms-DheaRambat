<!-- src/components/marketing/KPISection.vue -->
<template>
  <div class="kpi-section">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading dashboard data...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <h3>Error Loading Data</h3>
      <p>{{ error }}</p>
      <button @click="$emit('retry')" class="retry-button">Retry</button>
    </div>
    
    <!-- KPI Cards -->
    <div v-else class="kpi-grid-marketing">
      <!-- Total Movies -->
      <div class="kpi-card-marketing total-movies">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">🎬</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOTAL MOVIES</span>
            </div>
          </div>
          <div class="kpi-value-marketing">{{ formatNumber(kpi.total_movies) }}</div>
          <div class="kpi-description-marketing">Total Shows in Database</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>

      <!-- Top Film by Votes -->
      <div class="kpi-card-marketing top-film">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">🏆</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOP FILM BY VOTES</span>
            </div>
          </div>
          <div class="kpi-value-marketing" :class="{ 'small-font': isLongTitle(kpi.top_film.name) }">
            {{ kpi.top_film.name || '-' }}
          </div>
          <div class="kpi-description-marketing">{{ formatNumber(kpi.top_film.total_votes) }} votes</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>

      <!-- Top Rating -->
      <div class="kpi-card-marketing top-rating">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">⭐</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOP RATING</span>
            </div>
          </div>
          <div class="kpi-value-marketing" :class="{ 'small-font': isLongTitle(kpi.top_rating.name) }">
            {{ kpi.top_rating.name || '-' }}
          </div>
          <div class="kpi-description-marketing">{{ kpi.top_rating.average_rating?.toFixed(2) || '0.00' }}/10 rating</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>

      <!-- Top Platform -->
      <div class="kpi-card-marketing top-platform">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">📺</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOP PLATFORM</span>
            </div>
          </div>
          <div class="kpi-value-marketing">{{ kpi.top_platform || '-' }}</div>
          <div class="kpi-description-marketing">Most popular network</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>

      <!-- Top Country -->
      <div class="kpi-card-marketing top-country">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">🌍</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOP COUNTRY</span>
            </div>
          </div>
          <div class="kpi-value-marketing">{{ kpi.top_country || '-' }}</div>
          <div class="kpi-description-marketing">Most productions</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>

      <!-- Top Genre -->
      <div class="kpi-card-marketing top-genre">
        <div class="kpi-card-content">
          <div class="kpi-header-marketing">
            <span class="kpi-icon-marketing">🎭</span>
            <div class="kpi-title-container">
              <span class="kpi-title-marketing">TOP GENRE</span>
            </div>
          </div>
          <div class="kpi-value-marketing">{{ kpi.top_genre || '-' }}</div>
          <div class="kpi-description-marketing">Most common genre</div>
        </div>
        <div class="kpi-card-glow"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "KPISection",
  props: {
    kpi: {
      type: Object,
      required: true,
      default: () => ({
        total_movies: 0,
        top_film: { name: '-', total_votes: 0 },
        top_rating: { name: '-', average_rating: 0 },
        top_platform: '-',
        top_country: '-',
        top_genre: '-'
      })
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  },
  emits: ['retry'],
  methods: {
    formatNumber(num) {
      if (!num && num !== 0) return '0';
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return num.toLocaleString();
    },
    
    isLongTitle(title) {
      return title && title.length > 20;
    }
  }
}
</script>

<style scoped>
.kpi-section {
  margin-bottom: 40px;
}

/* Loading State */
.loading-container {
  text-align: center;
  padding: 60px 20px;
  border-radius: 18px;
  background: rgba(50, 42, 36, 0.7);
  border: 2px solid rgba(216, 160, 165, 0.3);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 107, 157, 0.2);
  border-top: 4px solid #FF6B9D;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

/* Error State */
.error-container {
  text-align: center;
  padding: 40px 20px;
  border-radius: 18px;
  background: rgba(50, 42, 36, 0.7);
  border: 2px solid rgba(236, 64, 122, 0.4);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.error-container h3 {
  color: #F48FB1;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.error-container p {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 20px;
}

.retry-button {
  background: linear-gradient(135deg, #FF6B9D, #EC407A);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 107, 157, 0.4);
}

/* ===== KPI CARDS ===== */
.kpi-grid-marketing {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

/* KPI Card */
.kpi-card-marketing {
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(38, 32, 26, 0.95) 50%,
    rgba(50, 42, 36, 0.95) 100%);
  border: 2px solid;
  border-radius: 18px;
  padding: 18px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  min-height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.5),
    inset 0 2px 0 rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.kpi-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.kpi-card-marketing:hover {
  transform: translateY(-6px);
  box-shadow: 
    0 20px 50px rgba(0, 0, 0, 0.6),
    inset 0 2px 0 rgba(255, 255, 255, 0.15);
}

.kpi-card-marketing:hover .kpi-card-glow {
  opacity: 1;
}

.kpi-card-content {
  position: relative;
  z-index: 2;
}

/* KPI Header dengan Icon dan Title */
.kpi-header-marketing {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.kpi-icon-marketing {
  font-size: 1.1rem;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  border: 2px solid;
  flex-shrink: 0;
  transition: all 0.3s ease;
  font-weight: bold;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

.kpi-card-marketing:hover .kpi-icon-marketing {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 0 20px currentColor;
}

/* Container untuk judul */
.kpi-title-container {
  flex: 1;
  border-radius: 10px;
  padding: 6px 12px;
  border: 2px solid;
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 3px 10px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  min-height: 36px;
  display: flex;
  align-items: center;
}

.kpi-card-marketing:hover .kpi-title-container {
  transform: translateY(-2px);
  box-shadow: 
    inset 0 2px 4px rgba(0, 0, 0, 0.3),
    0 5px 15px rgba(0, 0, 0, 0.4);
}

/* JUDUL KPI */
.kpi-title-marketing {
  font-size: 0.65rem;
  color: #ffffff;
  font-weight: 900;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-family: 'Inter', sans-serif;
  position: relative;
  z-index: 1;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* KPI Value */
.kpi-value-marketing {
  font-size: 1.15rem;
  font-weight: 900;
  line-height: 1.15;
  margin-bottom: 3px;
  font-family: 'Inter', sans-serif;
  padding-left: 46px;
  transition: all 0.3s ease;
  letter-spacing: -0.01em;
  word-break: break-word;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-shadow: 0 2px 5px rgba(0, 0, 0, 0.8);
}

/* KELAS UNTUK FONT KECIL JIKA JUDUL PANJANG */
.kpi-value-marketing.small-font {
  font-size: 0.85rem !important;
  line-height: 1.1 !important;
  padding-left: 46px !important;
  -webkit-line-clamp: 3 !important;
}

/* KPI Description */
.kpi-description-marketing {
  font-size: 0.75rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  line-height: 1.15;
  padding-left: 46px;
  letter-spacing: 0.02em;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

/* WARNA-WARNA UNTUK SETIAP CARD */
.total-movies {
  border-color: #FF6B9D !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(255, 107, 157, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.total-movies .kpi-icon-marketing {
  background: linear-gradient(135deg, #FF6B9D, #FF4081) !important;
  border-color: #FF4081 !important;
  color: white !important;
}

.total-movies .kpi-title-container {
  background: linear-gradient(135deg, rgba(255, 107, 157, 0.35), rgba(255, 64, 129, 0.25)) !important;
  border-color: #FF6B9D !important;
}

.total-movies .kpi-value-marketing {
  color: #FFD1DC !important;
}

.total-movies .kpi-description-marketing {
  color: #FFB6C1 !important;
}

.total-movies .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #FF6B9D 50%, 
    transparent 100%) !important;
}

.top-film {
  border-color: #9C27B0 !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(156, 39, 176, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.top-film .kpi-icon-marketing {
  background: linear-gradient(135deg, #BA68C8, #9C27B0) !important;
  border-color: #9C27B0 !important;
  color: white !important;
}

.top-film .kpi-title-container {
  background: linear-gradient(135deg, rgba(186, 104, 200, 0.35), rgba(156, 39, 176, 0.25)) !important;
  border-color: #BA68C8 !important;
}

.top-film .kpi-value-marketing {
  color: #E1BEE7 !important;
}

.top-film .kpi-description-marketing {
  color: #CE93D8 !important;
}

.top-film .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #BA68C8 50%, 
    transparent 100%) !important;
}

.top-rating {
  border-color: #EC407A !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(236, 64, 122, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.top-rating .kpi-icon-marketing {
  background: linear-gradient(135deg, #F48FB1, #EC407A) !important;
  border-color: #EC407A !important;
  color: white !important;
}

.top-rating .kpi-title-container {
  background: linear-gradient(135deg, rgba(244, 143, 177, 0.35), rgba(236, 64, 122, 0.25)) !important;
  border-color: #F48FB1 !important;
}

.top-rating .kpi-value-marketing {
  color: #FCE4EC !important;
}

.top-rating .kpi-description-marketing {
  color: #F8BBD0 !important;
}

.top-rating .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #F48FB1 50%, 
    transparent 100%) !important;
}

.top-platform {
  border-color: #7B1FA2 !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(123, 31, 162, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.top-platform .kpi-icon-marketing {
  background: linear-gradient(135deg, #AB47BC, #7B1FA2) !important;
  border-color: #7B1FA2 !important;
  color: white !important;
}

.top-platform .kpi-title-container {
  background: linear-gradient(135deg, rgba(171, 71, 188, 0.35), rgba(123, 31, 162, 0.25)) !important;
  border-color: #AB47BC !important;
}

.top-platform .kpi-value-marketing {
  color: #D1C4E9 !important;
}

.top-platform .kpi-description-marketing {
  color: #B39DDB !important;
}

.top-platform .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #AB47BC 50%, 
    transparent 100%) !important;
}

.top-country {
  border-color: #D81B60 !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(216, 27, 96, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.top-country .kpi-icon-marketing {
  background: linear-gradient(135deg, #F06292, #D81B60) !important;
  border-color: #D81B60 !important;
  color: white !important;
}

.top-country .kpi-title-container {
  background: linear-gradient(135deg, rgba(240, 98, 146, 0.35), rgba(216, 27, 96, 0.25)) !important;
  border-color: #F06292 !important;
}

.top-country .kpi-value-marketing {
  color: #F8BBD0 !important;
}

.top-country .kpi-description-marketing {
  color: #F48FB1 !important;
}

.top-country .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #F06292 50%, 
    transparent 100%) !important;
}

.top-genre {
  border-color: #8E24AA !important;
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(142, 36, 170, 0.12) 50%,
    rgba(50, 42, 36, 0.95) 100%) !important;
}

.top-genre .kpi-icon-marketing {
  background: linear-gradient(135deg, #CE93D8, #8E24AA) !important;
  border-color: #8E24AA !important;
  color: white !important;
}

.top-genre .kpi-title-container {
  background: linear-gradient(135deg, rgba(206, 147, 216, 0.35), rgba(142, 36, 170, 0.25)) !important;
  border-color: #CE93D8 !important;
}

.top-genre .kpi-value-marketing {
  color: #EDE7F6 !important;
}

.top-genre .kpi-description-marketing {
  color: #D1C4E9 !important;
}

.top-genre .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #CE93D8 50%, 
    transparent 100%) !important;
}

/* Responsive untuk KPI Section */
@media (max-width: 1400px) {
  .kpi-grid-marketing {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .kpi-grid-marketing {
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }
  
  .kpi-value-marketing {
    font-size: 1.05rem;
  }
  
  .kpi-value-marketing.small-font {
    font-size: 0.8rem !important;
  }
}

@media (max-width: 768px) {
  .kpi-grid-marketing {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .kpi-value-marketing {
    font-size: 1rem;
  }
  
  .kpi-value-marketing.small-font {
    font-size: 0.75rem !important;
  }
  
  .kpi-title-marketing {
    font-size: 0.6rem;
    letter-spacing: 0.8px;
  }
}

@media (max-width: 480px) {
  .kpi-value-marketing {
    font-size: 0.95rem;
  }
  
  .kpi-value-marketing.small-font {
    font-size: 0.7rem !important;
  }
  
  .kpi-title-marketing {
    font-size: 0.55rem;
    letter-spacing: 0.7px;
  }
  
  .kpi-card-marketing {
    padding: 15px;
    min-height: 90px;
  }
}
</style>