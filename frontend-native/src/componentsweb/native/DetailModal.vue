<template>
  <transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <button class="modal-close" @click="$emit('close')">✕</button>
        
        <!-- Loading -->
        <div v-if="detailLoading" class="modal-loading">
          <div class="spinner"></div>
          <p class="loading-text">Loading details...</p>
        </div>

        <!-- Error -->
        <div v-else-if="detailError" class="error-box">
          <span class="error-icon">⚠</span>
          <p>{{ detailError }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="selectedShow" class="modal-body">
          <div class="detail-header">
            <div class="detail-poster">📺</div>
            <div class="detail-info">
              <h1 class="detail-title">{{ selectedShow.Name }}</h1>
              <div class="detail-meta">
                <div class="rating-large">
                  <span class="star">⭐</span>
                  <span class="rating-value">{{ selectedShow.VoteAverage || 'N/A' }}</span>
                  <span class="votes-text">({{ formatVotes(selectedShow.VoteCount) }} votes)</span>
                </div>
                <span class="meta-separator">•</span>
                <span>{{ formatYear(selectedShow.FirstAirDate) }}</span>
                <span class="meta-separator">•</span>
                <span>{{ selectedShow.StatusName }}</span>
              </div>
              <div class="detail-genres">
                {{ selectedShow.Genres }}
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h3 class="section-heading">Overview</h3>
            <p class="detail-overview">{{ selectedShow.Overview || 'No overview available' }}</p>
          </div>

          <div class="detail-stats">
            <div class="stat-item">
              <span class="stat-label">Episodes</span>
              <span class="stat-value">{{ selectedShow.NumberOfEpisodes || 'N/A' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Seasons</span>
              <span class="stat-value">{{ selectedShow.NumberOfSeasons || 'N/A' }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Popularity</span>
              <span class="stat-value">{{ Math.round(selectedShow.Popularity || 0) }}</span>
            </div>
          </div>

          <div v-if="selectedShow.Languages" class="detail-section">
            <h3 class="section-heading">Languages</h3>
            <p>{{ selectedShow.Languages }}</p>
          </div>

          <div v-if="selectedShow.ProductionCompanies" class="detail-section">
            <h3 class="section-heading">Production Companies</h3>
            <p>{{ selectedShow.ProductionCompanies }}</p>
          </div>

          <div v-if="selectedShow.ProductionCountries" class="detail-section">
            <h3 class="section-heading">Production Countries</h3>
            <p>{{ selectedShow.ProductionCountries }}</p>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'DetailModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    showId: {
      type: [String, Number],
      default: null
    }
  },
  data() {
    return {
      selectedShow: null,
      detailLoading: false,
      detailError: null
    }
  },
  watch: {
    showId: {
      immediate: true,
      handler(newShowId) {
        if (newShowId && this.show) {
          this.loadShowDetail();
        }
      }
    },
    show: {
      handler(newVal) {
        if (newVal && this.showId) {
          this.loadShowDetail();
        } else {
          this.selectedShow = null;
          this.detailError = null;
        }
      }
    }
  },
  methods: {
    async loadShowDetail() {
  this.selectedShow = null;
  this.detailLoading = true;
  this.detailError = null;

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/native/detail/${this.showId}`
    );
    const data = await response.json();

    if (!data.success) {
      this.detailError = data.error || "Failed to load show details";
      return;
    }

    // 🔥 BACKEND RETURN ARRAY
    const showInfo = data.data?.show_info?.[0];

    if (!showInfo) {
      this.detailError = "Show detail not found";
      return;
    }

    this.selectedShow = showInfo;

  } catch (err) {
    this.detailError = "Network error: " + err.message;
    console.error("Detail error:", err);
  } finally {
    this.detailLoading = false;
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
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 12, 9, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
  overflow-y: auto;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: 
    linear-gradient(135deg, 
      rgba(42, 36, 30, 0.98) 0%, 
      rgba(31, 26, 20, 0.98) 100%);
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid rgba(152, 57, 68, 0.3);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.8),
    0 0 30px rgba(152, 57, 68, 0.2);
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(152, 57, 68, 0.8);
  border: none;
  color: #f8f4ed;
  font-size: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  z-index: 10;
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.modal-close:hover {
  background: rgba(162, 67, 78, 0.9);
  transform: rotate(90deg);
  box-shadow: 0 4px 12px rgba(152, 57, 68, 0.4);
}

.modal-loading {
  padding: 80px 20px;
  text-align: center;
}

.modal-body {
  padding: 32px;
}

.detail-header {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid rgba(152, 57, 68, 0.2);
}

.detail-poster {
  width: 200px;
  height: 300px;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.8) 0%, 
    rgba(74, 66, 55, 0.8) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 80px;
  flex-shrink: 0;
  border: 2px solid rgba(175, 120, 125, 0.3);
  box-shadow: 
    0 8px 24px rgba(0,0,0,0.4),
    inset 0 1px 3px rgba(255,255,255,0.1);
}

.detail-info {
  flex: 1;
}

.detail-title {
  font-size: 32px;
  font-weight: 700;
  color: #f8f4ed;
  margin-bottom: 16px;
  line-height: 1.3;
  text-shadow: 0 2px 4px rgba(0,0,0,0.4);
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
  font-size: 15px;
  color: #b87c7c;
}

.rating-large {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.8) 0%, 
    rgba(74, 66, 55, 0.8) 100%);
  padding: 10px 18px;
  border-radius: 8px;
  border: 1px solid rgba(175, 120, 125, 0.3);
}

.rating-large .star {
  font-size: 20px;
}

.rating-large .rating-value {
  color: #f8f4ed;
  font-weight: 700;
  font-size: 18px;
}

.votes-text {
  color: #b87c7c;
  font-size: 14px;
}

.detail-genres {
  color: #d8a0a5;
  font-size: 15px;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.detail-section {
  margin-bottom: 28px;
}

.section-heading {
  font-size: 20px;
  font-weight: 600;
  color: #f8f4ed;
  margin-bottom: 12px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.detail-overview {
  color: #e8e0d0;
  font-size: 15px;
  line-height: 1.7;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 28px;
  padding: 24px;
  background: linear-gradient(135deg, 
    rgba(31, 26, 20, 0.9) 0%, 
    rgba(42, 36, 30, 0.9) 100%);
  border-radius: 12px;
  border: 1px solid rgba(152, 57, 68, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  color: #b87c7c;
  font-size: 13px;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.stat-value {
  display: block;
  color: #f8f4ed;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.error-box {
  background: linear-gradient(135deg, 
    rgba(74, 61, 47, 0.9) 0%, 
    rgba(61, 51, 40, 0.9) 100%);
  border-left: 4px solid #d47c5c;
  color: #ffd8c8;
  padding: 18px 24px;
  border-radius: 10px;
  margin: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 
    0 4px 12px rgba(0,0,0,0.3),
    0 0 15px rgba(212, 124, 92, 0.2);
  font-family: 'Poppins', sans-serif;
}

.error-icon {
  font-size: 20px;
  flex-shrink: 0;
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

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.4s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
  opacity: 0;
}

/* Responsive Modal */
@media (max-width: 768px) {
  .modal-content {
    margin: 10px;
    max-height: 95vh;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .detail-header {
    flex-direction: column;
    text-align: center;
  }
  
  .detail-poster {
    width: 100%;
    height: 300px;
    margin: 0 auto;
  }
  
  .detail-title {
    font-size: 24px;
  }
  
  .detail-stats {
    grid-template-columns: 1fr;
  }
}
</style>