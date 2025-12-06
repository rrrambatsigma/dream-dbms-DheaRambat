<template>
  <div>
    <h1>Executive Dashboard</h1>

    <p>Selamat datang Executive!</p>

    <p style="color: gray; font-style: italic;">
      (Endpoint KPI dinonaktifkan sementara)
    </p>

    <!-- Tambahkan konten dashboard di sini nanti -->
  </div>
</template>

<script>
export default {
  name: "ExecDashboard",

  mounted() {
    console.log("Executive Dashboard loaded — KPI API disabled.");
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 10px;
}
</style>
