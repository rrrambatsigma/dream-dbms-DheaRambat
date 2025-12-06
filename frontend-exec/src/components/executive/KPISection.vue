<template>
  <section class="kpi-section">
    <div class="kpi-grid" v-if="kpi">
      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="15" rx="2" ry="2"></rect>
            <polyline points="17 2 12 7 7 2"></polyline>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOTAL SHOWS</p>
          <h3 class="kpi-value">{{ formatNumber(kpi.TotalShows) }}</h3>
          <p class="kpi-subtitle">Shows in Database</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">AVERAGE RATING</p>
          <h3 class="kpi-value">{{ kpi.AverageRating?.toFixed(2) || '0.00' }}<span class="rating-max">/10</span></h3>
          <p class="kpi-subtitle">Overall rating</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOTAL VOTES</p>
          <h3 class="kpi-value">{{ formatNumber(kpi.TotalVotes) }}</h3>
          <p class="kpi-subtitle">User engagement</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">PRODUCTION COMPANIES</p>
          <h3 class="kpi-value">{{ formatNumber(kpi.TotalProductionCompanies) }}</h3>
          <p class="kpi-subtitle">Unique companies</p>
        </div>
      </div>

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
          <h3 class="kpi-value">{{ formatNumber(kpi.TotalProductionCountries) }}</h3>
          <p class="kpi-subtitle">Global reach</p>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
            <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
            <line x1="6" y1="6" x2="6.01" y2="6"></line>
            <line x1="6" y1="18" x2="6.01" y2="18"></line>
          </svg>
        </div>
        <div class="kpi-content">
          <p class="kpi-label">TOTAL NETWORKS</p>
          <h3 class="kpi-value">{{ formatNumber(kpi.TotalNetworks) }}</h3>
          <p class="kpi-subtitle">Distribution channels</p>
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
    kpi: Object
  },
  methods: {
    formatNumber(num) {
      if (!num) return '0';
      if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
      if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
      return num.toLocaleString();
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
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 12px;
}

.kpi-card {
  background: linear-gradient(145deg, #5a3838 0%, #4a2d2d 100%);
  border-radius: 14px;
  padding: 18px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 182, 193, 0.1);
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, rgba(255, 182, 193, 0.08) 0%, rgba(255, 182, 193, 0) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.kpi-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 182, 193, 0.3);
}

.kpi-card:hover::before {
  opacity: 1;
}

.kpi-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  background: rgba(255, 182, 193, 0.15);
  color: #ffb6c1;
  padding: 10px;
  box-shadow: 0 2px 8px rgba(255, 182, 193, 0.2);
  transition: all 0.3s ease;
}

.kpi-card:hover .kpi-icon {
  background: rgba(255, 182, 193, 0.25);
  box-shadow: 0 4px 12px rgba(255, 182, 193, 0.3);
  transform: scale(1.05);
}

.kpi-icon svg {
  width: 20px;
  height: 20px;
}

.kpi-content {
  width: 100%;
}

.kpi-label {
  font-size: 0.65rem;
  color: #b8a8a8;
  margin: 0 0 6px 0;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.kpi-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 4px 0;
  line-height: 1.1;
  letter-spacing: -0.5px;
  transition: color 0.3s ease;
}

.kpi-card:hover .kpi-value {
  color: #ffb6c1;
}

.rating-max {
  font-size: 0.9rem;
  color: #b8a8a8;
  font-weight: 400;
}

.kpi-subtitle {
  font-size: 0.75rem;
  color: #968888;
  margin: 0;
  font-weight: 400;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: linear-gradient(145deg, rgba(90, 56, 56, 0.4) 0%, rgba(74, 45, 45, 0.3) 100%);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 182, 193, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 182, 193, 0.2);
  border-top-color: #ffb6c1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.loading-state p {
  color: #b8a8a8;
  font-size: 0.9rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 1400px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .kpi-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .kpi-card {
    padding: 16px 14px;
  }
  
  .kpi-value {
    font-size: 1.4rem;
  }
}
</style>