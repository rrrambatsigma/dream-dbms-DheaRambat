<template>
  <section class="kpi-section">
    <div class="kpi-grid" v-if="kpiData">
      <!-- Card 1: Total Shows -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="15" rx="2" ry="2"></rect>
            <polyline points="17 2 12 7 7 2"></polyline>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOTAL SHOWS</p>
          <h3 class="kpi-value">{{ formatNumber(kpiData.TotalShows) }}</h3>
          <p class="kpi-subtitle">Total film & TV shows</p>
        </div>
      </div>

      <!-- Card 2: Total Votes -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOTAL VOTES</p>
          <h3 class="kpi-value">{{ formatNumber(kpiData.TotalVotes) }}</h3>
          <p class="kpi-subtitle">User engagement</p>
        </div>
      </div>

      <!-- Card 3: Production Companies -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">PRODUCTION COMPANIES</p>
          <h3 class="kpi-value">{{ formatNumber(kpiData.TotalProductionCompanies) }}</h3>
          <p class="kpi-subtitle">Unique companies</p>
        </div>
      </div>

      <!-- Card 4: Production Countries -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">PRODUCTION COUNTRIES</p>
          <h3 class="kpi-value">{{ kpiData.TotalProductionCountries }}</h3>
          <p class="kpi-subtitle">Global reach</p>
        </div>
      </div>

      <!-- Card 5: Top Production Company -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="2" ry="2"></rect>
            <line x1="8" y1="2" x2="8" y2="22"></line>
            <line x1="16" y1="2" x2="16" y2="22"></line>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOP PRODUCTION COMPANY</p>
          <h3 class="kpi-value company-name">{{ kpiData.TopProductionCompany || 'N/A' }}</h3>
          <p class="kpi-subtitle">{{ formatNumber(kpiData.ShowsFromTopCompany) }} shows</p>
        </div>
      </div>

      <!-- Card 6: Top Genre -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOP GENRE</p>
          <h3 class="kpi-value genre-name">{{ kpiData.TopGenre || 'N/A' }}</h3>
          <p class="kpi-subtitle">Most popular category</p>
        </div>
      </div>

      <!-- Card 7: Top Movie -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOP MOVIE/SHOW</p>
          <h3 class="kpi-value movie-name">{{ kpiData.TopMovie || 'N/A' }}</h3>
          <p class="kpi-subtitle">Highest rated</p>
        </div>
      </div>

      <!-- Card 8: Shows From Top Company -->
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="8" y1="6" x2="21" y2="6"></line>
            <line x1="8" y1="12" x2="21" y2="12"></line>
            <line x1="8" y1="18" x2="21" y2="18"></line>
            <line x1="3" y1="6" x2="3.01" y2="6"></line>
            <line x1="3" y1="12" x2="3.01" y2="12"></line>
            <line x1="3" y1="18" x2="3.01" y2="18"></line>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">SHOWS FROM TOP COMPANY</p>
          <h3 class="kpi-value">{{ formatNumber(kpiData.ShowsFromTopCompany) }}</h3>
          <p class="kpi-subtitle">By {{ kpiData.TopProductionCompany || 'N/A' }}</p>
        </div>
      </div>
    </div>

    <div v-else class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading KPI data...</p>
    </div>
  </section>
</template>

<script>
export default {
  name: "KPISection",
  props: {
    kpiResponse: Object
  },
  data() {
    return {
      kpiData: null
    };
  },
  watch: {
    kpiResponse: {
      immediate: true,
      handler(newResponse) {
        if (newResponse && newResponse.success) {
          this.kpiData = newResponse.data;
        }
      }
    }
  },
  mounted() {
    // Fallback data sesuai JSON yang baru
    if (!this.kpiResponse) {
      this.kpiData = {
        ShowsFromTopCompany: 1384,
        TopGenre: "Drama",
        TopMovie: "Breaking Bad",
        TopProductionCompany: "TVB",
        TotalProductionCompanies: 21636,
        TotalProductionCountries: 183,
        TotalShows: 162143,
        TotalVotes: 2243144
      };
    }
  },
  methods: {
    formatNumber(num) {
      if (num === null || num === undefined) return '0';
      
      // Jika string, coba convert ke number
      if (typeof num === 'string') {
        // Hapus koma jika ada
        const cleanNum = num.replace(/,/g, '');
        if (!isNaN(cleanNum) && cleanNum !== '') {
          num = parseFloat(cleanNum);
        } else {
          // Jika bukan angka, tampilkan langsung
          return num;
        }
      }
      
      if (typeof num !== 'number') {
        return String(num);
      }
      
      // Format untuk angka besar
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      
      return num.toLocaleString('en-US');
    }
  }
};
</script>

<style scoped>
.kpi-section {
  padding: 0;
  margin-bottom: 24px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 16px;
}

.kpi-card {
  background: linear-gradient(145deg, #5a3838 0%, #4a2d2d 100%);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 182, 193, 0.1);
  position: relative;
  overflow: hidden;
  min-height: 140px;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
  border-color: rgba(255, 182, 193, 0.3);
}

.kpi-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  background: rgba(255, 182, 193, 0.15);
  color: #ffb6c1;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(255, 182, 193, 0.2);
  transition: all 0.3s ease;
}

.kpi-card:hover .kpi-icon {
  background: rgba(255, 182, 193, 0.25);
  box-shadow: 0 6px 16px rgba(255, 182, 193, 0.3);
  transform: scale(1.1);
}

.kpi-icon svg {
  width: 20px;
  height: 20px;
}

.kpi-content {
  width: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.kpi-label {
  font-size: 0.7rem;
  color: #b8a8a8;
  margin: 0 0 8px 0;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  line-height: 1.2;
}

.kpi-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0 0 6px 0;
  line-height: 1.1;
  letter-spacing: -0.5px;
  transition: color 0.3s ease;
  min-height: 2.2rem;
  display: flex;
  align-items: center;
}

.kpi-value.company-name,
.kpi-value.genre-name,
.kpi-value.movie-name {
  font-size: 1.4rem;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-break: break-word;
}

.kpi-card:hover .kpi-value {
  color: #ffb6c1;
}

.kpi-subtitle {
  font-size: 0.8rem;
  color: #968888;
  margin: 0;
  font-weight: 400;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  background: linear-gradient(145deg, rgba(90, 56, 56, 0.4) 0%, rgba(74, 45, 45, 0.3) 100%);
  border-radius: 20px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 182, 193, 0.1);
  min-height: 400px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 182, 193, 0.2);
  border-top-color: #ffb6c1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-state p {
  color: #b8a8a8;
  font-size: 1rem;
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 1920px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1400px) {
  .kpi-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .kpi-card {
    padding: 16px;
    min-height: 130px;
  }
  
  .kpi-value {
    font-size: 1.6rem;
  }
  
  .kpi-value.company-name,
  .kpi-value.genre-name,
  .kpi-value.movie-name {
    font-size: 1.2rem;
  }
}

@media (max-width: 576px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
  
  .kpi-card {
    min-height: 120px;
    padding: 14px;
  }
  
  .kpi-value {
    font-size: 1.5rem;
  }
}

/* Animasi tambahan untuk efek lebih smooth */
.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 182, 193, 0.1), transparent);
  transition: left 0.7s ease;
}

.kpi-card:hover::before {
  left: 100%;
}
</style>