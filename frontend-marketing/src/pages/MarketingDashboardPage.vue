<template>
  <div class="dashboard-wrapper">
    <!-- Modern Header untuk Marketing Dashboard -->
    <div class="modern-header-marketing">
      <div class="header-content-marketing">
        <h1 class="main-title-marketing">Marketing Dashboard</h1>
        <p class="subtitle-marketing">Analytics & performance insights for strategic marketing decisions</p>
      </div>
      
      <!-- Decorative Elements -->
      <div class="header-decoration-marketing">
        <div class="decoration-circle-marketing"></div>
        <div class="decoration-circle-marketing"></div>
        <div class="decoration-circle-marketing"></div>
      </div>
    </div>

    <!-- Container utama untuk konten -->
    <div class="dashboard-content">
      <!-- ===== KPI CARDS ===== -->
      <div class="kpi-grid-marketing">
        <!-- Total Popularity -->
        <div class="kpi-card-marketing total-popularity">
          <div class="kpi-card-content">
            <div class="kpi-header-marketing">
              <span class="kpi-icon-marketing">📊</span>
              <div class="kpi-title-container">
                <span class="kpi-title-marketing">TOTAL POPULARITY</span>
              </div>
            </div>
            <div class="kpi-value-marketing">{{ kpi.TotalPopularity || '949,319' }}</div>
            <div class="kpi-description-marketing">Overall Popularity Score</div>
          </div>
          <div class="kpi-card-glow"></div>
        </div>

        <!-- Average Rating -->
        <div class="kpi-card-marketing average-rating">
          <div class="kpi-card-content">
            <div class="kpi-header-marketing">
              <span class="kpi-icon-marketing">⭐</span>
              <div class="kpi-title-container">
                <span class="kpi-title-marketing">AVERAGE RATING</span>
              </div>
            </div>
            <div class="kpi-value-marketing">{{ kpi.AverageRating || '2.41' }}</div>
            <div class="kpi-description-marketing">out of 10</div>
          </div>
          <div class="kpi-card-glow"></div>
        </div>

        <!-- Total Votes -->
        <div class="kpi-card-marketing total-votes">
          <div class="kpi-card-content">
            <div class="kpi-header-marketing">
              <span class="kpi-icon-marketing">🗳️</span>
              <div class="kpi-title-container">
                <span class="kpi-title-marketing">TOTAL VOTES</span>
              </div>
            </div>
            <div class="kpi-value-marketing">{{ formatNumber(kpi.TotalVotes) || '2.2M' }}</div>
            <div class="kpi-description-marketing">Total Audience Votes</div>
          </div>
          <div class="kpi-card-glow"></div>
        </div>

        <!-- Top Language -->
        <div class="kpi-card-marketing top-language">
          <div class="kpi-card-content">
            <div class="kpi-header-marketing">
              <span class="kpi-icon-marketing">🌐</span>
              <div class="kpi-title-container">
                <span class="kpi-title-marketing">TOP LANGUAGE</span>
              </div>
            </div>
            <div class="kpi-value-marketing">{{ kpi.TopLanguage || 'en' }}</div>
            <div class="kpi-description-marketing">{{ (kpi.LanguagePercentage || 0) }}% of content</div>
          </div>
          <div class="kpi-card-glow"></div>
        </div>

        <!-- Top Genre -->
        <div class="kpi-card-marketing top-genre">
          <div class="kpi-card-content">
            <div class="kpi-header-marketing">
              <span class="kpi-icon-marketing">🎬</span>
              <div class="kpi-title-container">
                <span class="kpi-title-marketing">TOP GENRE</span>
              </div>
            </div>
            <div class="kpi-value-marketing">{{ kpi.TopGenre || 'Drama' }}</div>
            <div class="kpi-description-marketing">{{ (kpi.GenrePercentage || 0) }}% distribution</div>
          </div>
          <div class="kpi-card-glow"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MarketingDashboard",
  data() {
    return {
      kpi: {}
    };
  },
  mounted() {
    this.getKpi();
  },
  methods: {
    async getKpi() {
      const token = localStorage.getItem("token");

      try {
        const response = await fetch("http://127.0.0.1:5000/marketing/kpi", {
          method: "GET",
          headers: {
            Authorization: "Bearer " + token
          }
        });

        const result = await response.json();
        this.kpi = result.data;
      } catch (err) {
        console.error(err);
      }
    },
    
    formatNumber(num) {
      if (!num) return '2.2M';
      if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
      }
      if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
      }
      return num.toString();
    }
  }
};
</script>

<style scoped>
/* BACKGROUND SAMA SEPERTI NATIVE */
.dashboard-wrapper {
  min-height: 100vh;
  padding: 15px;
  background: linear-gradient(135deg, #0c0a08 0%, #1a1512 50%, #0c0a08 100%);
  font-family: "Poppins", sans-serif;
  position: relative;
  overflow-x: hidden;
}

.dashboard-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(184, 124, 124, 0.3) 50%, 
    transparent 100%);
}

/* Dashboard Content Container */
.dashboard-content {
  max-width: 1600px;
  margin: 0 auto;
}

/* Modern Header untuk Marketing */
.modern-header-marketing {
  position: relative;
  text-align: center;
  margin-bottom: 25px;
  padding: 20px 0;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.95) 0%, 
    rgba(31, 26, 20, 0.95) 100%);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(152, 57, 68, 0.3);
  box-shadow: 
    0 4px 20px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.header-content-marketing {
  position: relative;
  z-index: 2;
  padding: 0 20px;
}

.main-title-marketing {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #f8f4ed 0%, #d8a0a5 50%, #b87c7c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  font-family: 'Poppins', sans-serif;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
}

.subtitle-marketing {
  font-size: 0.95rem;
  color: rgba(248, 244, 237, 0.8);
  margin-bottom: 0;
  font-weight: 400;
  font-family: 'Poppins', sans-serif;
  letter-spacing: 0.01em;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

.header-decoration-marketing {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.decoration-circle-marketing {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(152, 57, 68, 0.15) 0%, transparent 70%);
}

.decoration-circle-marketing:nth-child(1) {
  width: 100px;
  height: 100px;
  top: -20px;
  left: -20px;
}

.decoration-circle-marketing:nth-child(2) {
  width: 70px;
  height: 70px;
  bottom: -15px;
  right: 15%;
}

.decoration-circle-marketing:nth-child(3) {
  width: 50px;
  height: 50px;
  top: 30%;
  right: -15px;
}

/* KPI Grid - Lebih Kompak */
.kpi-grid-marketing {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 30px;
}

/* KPI Card - Lebih Kecil dengan Background Sama seperti Header */
.kpi-card-marketing {
  background: linear-gradient(145deg, 
    rgba(42, 36, 30, 0.95) 0%,
    rgba(31, 26, 20, 0.95) 50%,
    rgba(42, 36, 30, 0.95) 100%);
  border: 1px solid rgba(139, 87, 42, 0.4);
  border-radius: 12px;
  padding: 14px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  min-height: 110px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 
    0 3px 10px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.kpi-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(210, 180, 140, 0.6) 50%, 
    transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.kpi-card-marketing:hover {
  border-color: rgba(210, 180, 140, 0.6);
  transform: translateY(-3px);
  box-shadow: 
    0 6px 20px rgba(210, 180, 140, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
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
  gap: 10px;
  margin-bottom: 8px;
}

.kpi-icon-marketing {
  font-size: 1.1rem;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(139, 87, 42, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(139, 87, 42, 0.4);
  flex-shrink: 0;
  transition: all 0.3s ease;
  color: #e6d5b8;
}

.kpi-card-marketing:hover .kpi-icon-marketing {
  background: rgba(139, 87, 42, 0.3);
  border-color: rgba(210, 180, 140, 0.6);
  transform: scale(1.05);
}

/* Container untuk judul dengan background coklat seperti header */
.kpi-title-container {
  flex: 1;
  background: linear-gradient(135deg, 
    rgba(139, 87, 42, 0.15) 0%,
    rgba(160, 120, 80, 0.1) 100%);
  border-radius: 6px;
  padding: 5px 10px;
  border: 1px solid rgba(160, 120, 80, 0.3);
  box-shadow: 
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.kpi-card-marketing:hover .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(139, 87, 42, 0.25) 0%,
    rgba(160, 120, 80, 0.2) 100%);
  border-color: rgba(210, 180, 140, 0.4);
}

.kpi-title-marketing {
  font-size: 0.65rem;
  color: #f8f4ed;
  font-weight: 600;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  font-family: 'Inter', sans-serif;
  position: relative;
  z-index: 1;
}

/* KPI Value - Font Lebih Elegan dan Kecil */
.kpi-value-marketing {
  font-size: 1.4rem;
  font-weight: 700;
  color: #f8f4ed;
  line-height: 1;
  margin-bottom: 3px;
  font-family: 'Inter', sans-serif;
  padding-left: 42px;
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  letter-spacing: -0.02em;
}

.kpi-card-marketing:hover .kpi-value-marketing {
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
}

/* KPI Description */
.kpi-description-marketing {
  font-size: 0.7rem;
  color: rgba(248, 244, 237, 0.7);
  font-weight: 400;
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
  padding-left: 42px;
  letter-spacing: 0.01em;
}

/* Color Variations untuk Setiap Card dengan Nuansa Coklat Emas */
.total-popularity .kpi-icon-marketing {
  background: linear-gradient(135deg, 
    rgba(139, 87, 42, 0.25) 0%,
    rgba(160, 120, 80, 0.25) 100%);
  border-color: rgba(139, 87, 42, 0.5);
  color: #d4a574;
}

.average-rating .kpi-icon-marketing {
  background: linear-gradient(135deg, 
    rgba(184, 134, 88, 0.25) 0%,
    rgba(160, 120, 80, 0.25) 100%);
  border-color: rgba(184, 134, 88, 0.5);
  color: #e6b17e;
}

.total-votes .kpi-icon-marketing {
  background: linear-gradient(135deg, 
    rgba(210, 180, 140, 0.25) 0%,
    rgba(184, 134, 88, 0.25) 100%);
  border-color: rgba(210, 180, 140, 0.5);
  color: #f0c987;
}

.top-language .kpi-icon-marketing {
  background: linear-gradient(135deg, 
    rgba(139, 115, 85, 0.25) 0%,
    rgba(139, 87, 42, 0.25) 100%);
  border-color: rgba(139, 115, 85, 0.5);
  color: #d4b483;
}

.top-genre .kpi-icon-marketing {
  background: linear-gradient(135deg, 
    rgba(160, 120, 80, 0.25) 0%,
    rgba(139, 87, 42, 0.25) 100%);
  border-color: rgba(160, 120, 80, 0.5);
  color: #e6d5b8;
}

/* Background title container sesuai dengan icon */
.total-popularity .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(139, 87, 42, 0.15) 0%,
    rgba(160, 120, 80, 0.1) 100%);
  border-color: rgba(139, 87, 42, 0.3);
}

.average-rating .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(184, 134, 88, 0.15) 0%,
    rgba(160, 120, 80, 0.1) 100%);
  border-color: rgba(184, 134, 88, 0.3);
}

.total-votes .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(210, 180, 140, 0.15) 0%,
    rgba(184, 134, 88, 0.1) 100%);
  border-color: rgba(210, 180, 140, 0.3);
}

.top-language .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(139, 115, 85, 0.15) 0%,
    rgba(139, 87, 42, 0.1) 100%);
  border-color: rgba(139, 115, 85, 0.3);
}

.top-genre .kpi-title-container {
  background: linear-gradient(135deg, 
    rgba(160, 120, 80, 0.15) 0%,
    rgba(139, 87, 42, 0.1) 100%);
  border-color: rgba(160, 120, 80, 0.3);
}

/* Glow efek untuk setiap card dengan nuansa coklat emas */
.total-popularity .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(139, 87, 42, 0.6) 50%, 
    transparent 100%);
}

.average-rating .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(184, 134, 88, 0.6) 50%, 
    transparent 100%);
}

.total-votes .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(210, 180, 140, 0.6) 50%, 
    transparent 100%);
}

.top-language .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(139, 115, 85, 0.6) 50%, 
    transparent 100%);
}

.top-genre .kpi-card-glow {
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(160, 120, 80, 0.6) 50%, 
    transparent 100%);
}

/* Responsive Design */
@media (max-width: 1400px) {
  .kpi-grid-marketing {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .main-title-marketing {
    font-size: 2rem;
  }
  
  .modern-header-marketing {
    padding: 18px 0;
  }
  
  .kpi-value-marketing {
    font-size: 1.3rem;
  }
}

@media (max-width: 1024px) {
  .main-title-marketing {
    font-size: 1.8rem;
  }
  
  .subtitle-marketing {
    font-size: 0.9rem;
  }
  
  .kpi-grid-marketing {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .modern-header-marketing {
    padding: 16px 0;
    margin-bottom: 20px;
  }
  
  .kpi-card-marketing {
    padding: 12px;
    min-height: 100px;
  }
  
  .kpi-value-marketing {
    font-size: 1.2rem;
    padding-left: 38px;
  }
  
  .kpi-icon-marketing {
    width: 28px;
    height: 28px;
    font-size: 1rem;
  }
  
  .kpi-description-marketing {
    padding-left: 38px;
    font-size: 0.65rem;
  }
  
  .kpi-title-marketing {
    font-size: 0.6rem;
  }
}

@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 12px;
  }
  
  .modern-header-marketing {
    padding: 14px 0;
    margin-bottom: 16px;
    border-radius: 14px;
  }
  
  .main-title-marketing {
    font-size: 1.5rem;
  }
  
  .subtitle-marketing {
    font-size: 0.8rem;
  }
  
  .kpi-grid-marketing {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .kpi-card-marketing {
    padding: 12px;
    min-height: 95px;
  }
  
  .kpi-value-marketing {
    font-size: 1.2rem;
    padding-left: 36px;
  }
  
  .kpi-icon-marketing {
    width: 26px;
    height: 26px;
    font-size: 0.9rem;
  }
  
  .kpi-description-marketing {
    padding-left: 36px;
  }
}

@media (max-width: 480px) {
  .main-title-marketing {
    font-size: 1.3rem;
  }
  
  .subtitle-marketing {
    font-size: 0.75rem;
  }
  
  .modern-header-marketing {
    padding: 12px 0;
    border-radius: 12px;
  }
  
  .kpi-value-marketing {
    font-size: 1.1rem;
    padding-left: 34px;
  }
  
  .kpi-title-marketing {
    font-size: 0.55rem;
  }
  
  .kpi-icon-marketing {
    width: 24px;
    height: 24px;
    font-size: 0.85rem;
  }
  
  .kpi-title-container {
    padding: 4px 8px;
  }
}
</style>