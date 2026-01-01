<template>
  <div class="dashboard-wrapper">
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1 class="dashboard-title">Executive Dashboard</h1>
        <p class="dashboard-subtitle">Analytics & Performance Insights for Strategic Decisions</p>
      </div>

      <KPISection :kpi="kpi" />

      <ChartSection />

      <TableSection />
    </div>
  </div>
</template>

<script>
import api from "../utils/api.js";
import KPISection from "../components/executive/KPISection.vue";
import ChartSection from "../components/executive/ChartSection.vue";
import TableSection from "../components/executive/TableSection.vue";

export default {
  name: "ExecDashboard",

  components: {
    KPISection,
    ChartSection,
    TableSection,
  },

  data() {
    return {
      kpi: null,
    };
  },

  async mounted() {
    try {
      const res = await api.get("/api/executive/kpi");
      this.kpi = res.data.data;
    } catch (e) {
      console.error("KPI ERROR:", e);
      alert("Gagal mengambil KPI");
    }
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, #2a1a1a 0%, #1a0f0f 50%, #0f0505 100%);
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
}

/* Background decorative elements */
.dashboard-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(139, 0, 0, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.dashboard-wrapper::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -15%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(178, 34, 34, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 48px;
  padding: 30px 20px;
  background: linear-gradient(145deg, rgba(90, 56, 56, 0.3) 0%, rgba(74, 45, 45, 0.2) 100%);
  border-radius: 24px;
  border: 1px solid rgba(255, 182, 193, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
}

.dashboard-title {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffb6c1 0%, #ff69b4 50%, #ff1493 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 12px 0;
  letter-spacing: -1px;
  text-shadow: 0 0 30px rgba(255, 182, 193, 0.3);
}

.dashboard-subtitle {
  font-size: 1rem;
  color: #b8a8a8;
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.5px;
}

/* Global section styling */
.dashboard-container :deep(.section) {
  background: linear-gradient(145deg, rgba(90, 56, 56, 0.4) 0%, rgba(74, 45, 45, 0.3) 100%);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 28px;
  border: 1px solid rgba(255, 182, 193, 0.08);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.dashboard-container :deep(.section-title) {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffb6c1;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid rgba(255, 182, 193, 0.2);
  letter-spacing: 0.5px;
}

/* Scrollbar styling */
.dashboard-wrapper :deep(::-webkit-scrollbar) {
  width: 10px;
  height: 10px;
}

.dashboard-wrapper :deep(::-webkit-scrollbar-track) {
  background: rgba(42, 26, 26, 0.5);
  border-radius: 10px;
}

.dashboard-wrapper :deep(::-webkit-scrollbar-thumb) {
  background: linear-gradient(180deg, #8b0000, #b22222);
  border-radius: 10px;
  border: 2px solid rgba(42, 26, 26, 0.5);
}

.dashboard-wrapper :deep(::-webkit-scrollbar-thumb:hover) {
  background: linear-gradient(180deg, #b22222, #dc143c);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .dashboard-container {
    max-width: 100%;
    padding: 0 16px;
  }

  .dashboard-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .dashboard-wrapper {
    padding: 24px 12px;
  }

  .dashboard-header {
    padding: 24px 16px;
    margin-bottom: 32px;
  }

  .dashboard-title {
    font-size: 2rem;
  }

  .dashboard-subtitle {
    font-size: 0.9rem;
  }

  .dashboard-container :deep(.section) {
    padding: 20px;
    margin-bottom: 20px;
  }
}

@media (max-width: 480px) {
  .dashboard-wrapper {
    padding: 16px 8px;
  }

  .dashboard-header {
    padding: 20px 12px;
    border-radius: 16px;
  }

  .dashboard-title {
    font-size: 1.6rem;
  }

  .dashboard-subtitle {
    font-size: 0.8rem;
  }

  .dashboard-container :deep(.section) {
    padding: 16px;
    border-radius: 16px;
  }

  .dashboard-container :deep(.section-title) {
    font-size: 1.2rem;
  }
}

/* Animation for smooth entrance */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dashboard-header {
  animation: fadeInUp 0.6s ease-out;
}

.dashboard-container :deep(.kpi-section) {
  animation: fadeInUp 0.6s ease-out 0.1s backwards;
}

.dashboard-container :deep(.chart-section) {
  animation: fadeInUp 0.6s ease-out 0.2s backwards;
}

.dashboard-container :deep(.table-section) {
  animation: fadeInUp 0.6s ease-out 0.3s backwards;
}
</style>