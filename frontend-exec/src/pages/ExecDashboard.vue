<template>
  <div>
    <h1>Executive Dashboard</h1>

    <div v-if="error" style="color:red;">
      {{ error }}
    </div>

    <div v-else-if="kpi">
      <p>Total Shows: {{ kpi.TotalShows }}</p>
      <p>Average Rating: {{ kpi.AverageRating }}</p>
      <p>Total Votes: {{ kpi.TotalVotes }}</p>
      <p>Total Production Companies: {{ kpi.TotalProductionCompanies }}</p>
      <p>Total Production Countries: {{ kpi.TotalProductionCountries }}</p>
      <p>Total Networks: {{ kpi.TotalNetworks }}</p>
    </div>

    <div v-else>
      Loading...
    </div>
  </div>
</template>

<script>
import api from "../utils/api.js";  // <-- harus .js agar Vite tidak error

export default {
  data() {
    return {
      kpi: null,
      error: "",
    };
  },
  async mounted() {
    const token = localStorage.getItem("token");

    try {
      const res = await api.get("/executive/kpi", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      this.kpi = res.data.data;

    } catch (err) {
      this.error = "Gagal mengambil data. Akses ditolak.";
      console.error("Dashboard error:", err);
    }
  },
};
</script>
