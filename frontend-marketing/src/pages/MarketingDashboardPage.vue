<!-- src/pages/MarketingDashboardPage.vue - UPDATED -->
<template>
  <div class="dashboard-wrapper">
    <!-- HEADER -->
    <div class="modern-header-marketing">
      <div class="header-content-marketing">
        <h1 class="main-title-marketing">Marketing Dashboard</h1>
        <p class="subtitle-marketing">
          Analytics & performance insights for strategic marketing decisions
        </p>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="dashboard-content">
      <!-- YEAR RANGE SELECTOR (SIMPLE) -->
      <SimpleYearRangeSelector 
        @year-range-changed="handleYearRangeChange"
        ref="yearRangeSelectorRef"
      />

      <!-- KPI -->
      <KPISection
        :kpi="kpi"
        :loading="loading"
        :error="error"
        :year-range="currentYearRange"
        @retry="getKpi"
      />

      <!-- CHARTS -->
      <ChartSection 
        :year-range="currentYearRange"
        ref="chartSectionRef"
      />
    </div>
  </div>
</template>

<script>
import SimpleYearRangeSelector from "../components/marketing/SimpleYearRangeSelector.vue";
import KPISection from "../components/marketing/KPISection.vue";
import ChartSection from "../components/marketing/ChartSection.vue";

export default {
  name: "MarketingDashboardPage",
  components: {
    SimpleYearRangeSelector,
    KPISection,
    ChartSection
  },
  data() {
    return {
      loading: false,
      error: null,
      currentYearRange: null,
      kpi: {
        total_movies: 0,
        top_film: { name: "-", total_votes: 0 },
        top_rating: { name: "-", average_rating: 0 },
        top_platform: "-",
        top_country: "-",
        top_genre: "-"
      }
    };
  },
  mounted() {
    // Tunggu sedikit untuk mendapatkan default range dari selector
    setTimeout(() => {
      this.getKpi();
    }, 500);
  },
  methods: {
    async getKpi() {
      this.loading = true;
      this.error = null;

      try {
        const token = localStorage.getItem("token");
        if (!token) {
          throw new Error("No token found. Please login again.");
        }

        // Gunakan currentYearRange jika ada, jika tidak gunakan default
        let startYear, endYear;
        
        if (this.currentYearRange) {
          startYear = this.currentYearRange.startYear;
          endYear = this.currentYearRange.endYear;
        } else if (this.$refs.yearRangeSelectorRef) {
          // Ambil default dari selector
          const defaultRange = this.$refs.yearRangeSelectorRef.getDefaultRange();
          if (defaultRange) {
            this.currentYearRange = defaultRange;
            startYear = defaultRange.startYear;
            endYear = defaultRange.endYear;
          }
        }
        
        // Jika masih null, gunakan default
        if (!startYear || !endYear) {
          startYear = 2000;
          endYear = 2024;
        }
        
        const url = `http://127.0.0.1:5000/api/marketing/kpi?start_year=${startYear}&end_year=${endYear}`;
        console.log('📊 Fetching KPI from:', url);
        
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }

        const result = await response.json();
        console.log('📊 KPI Response:', result);

        if (!result.success) {
          throw new Error(result.message || "Failed to load KPI");
        }

        this.kpi = result.data;
        
        // Update year range dari response
        if (result.data.year_range) {
          this.currentYearRange = result.data.year_range;
        }

      } catch (err) {
        console.error("KPI Error:", err);
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },
    
    handleYearRangeChange(range) {
      console.log('🎯 Year range changed:', range);
      this.currentYearRange = range;
      
      // Reload KPI dengan filter baru
      this.getKpi();
      
      // Force reload charts dengan timeout sedikit
      setTimeout(() => {
        if (this.$refs.chartSectionRef && typeof this.$refs.chartSectionRef.loadAllCharts === 'function') {
          console.log('🔄 Triggering charts reload...');
          this.$refs.chartSectionRef.loadAllCharts();
        }
      }, 500); // Tambah delay sedikit
    }
  }
};
</script>

<style scoped>
/* Styles remain the same */
.dashboard-wrapper {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #0c0a08, #1a1512, #0c0a08);
  font-family: "Poppins", sans-serif;
}

.dashboard-content {
  max-width: 1600px;
  margin: 0 auto;
}

.modern-header-marketing {
  background: rgba(30, 25, 20, 0.95);
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  text-align: center;
  border: 1px solid rgba(216, 160, 165, 0.4);
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.main-title-marketing {
  font-size: 2.5rem;
  font-weight: 800;
  color: #ff9eb5;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(255, 158, 181, 0.3);
  background: linear-gradient(135deg, #FF6B9D, #BA68C8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle-marketing {
  color: #FFB6C1;
  font-size: 1rem;
  opacity: 0.9;
}
</style>