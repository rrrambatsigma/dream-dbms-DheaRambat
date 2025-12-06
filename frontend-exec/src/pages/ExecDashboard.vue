<template>
  <div>
    <h1>Executive Dashboard</h1>

    <div v-if="error" style="color:red;">
      {{ error }}
    </div>

    <div v-else-if="kpi">
      <h3>KPI Overview</h3>
      <ul>
        <li><strong>Total Shows:</strong> {{ kpi.TotalShows }}</li>
        <li><strong>Average Rating:</strong> {{ kpi.AverageRating }}</li>
        <li><strong>Total Votes:</strong> {{ kpi.TotalVotes }}</li>
        <li><strong>Total Production Companies:</strong> {{ kpi.TotalProductionCompanies }}</li>
        <li><strong>Total Production Countries:</strong> {{ kpi.TotalProductionCountries }}</li>
        <li><strong>Total Networks:</strong> {{ kpi.TotalNetworks }}</li>
      </ul>
    </div>

    <div v-else>
      Loading KPI...
    </div>
  </div>
</template>

<script>
import api from "../utils/api.js";

export default {
  name: "ExecDashboard",

  data() {
    return {
      kpi: null,
      error: "",
    };
  },

  async mounted() {
    console.log("📡 Fetching KPI...");
    try {
      const res = await api.get("/api/executive/kpi");

      console.log("KPI Response:", res.data);

      this.kpi = res.data.data;
    } catch (err) {
      console.error("KPI Error:", err);
      this.error = "Gagal mengambil KPI. Token invalid atau akses ditolak.";
    }
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 12px;
}
</style>
