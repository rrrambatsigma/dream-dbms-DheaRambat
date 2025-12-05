<template>
  <aside class="sidebar">
    <!-- Sidebar content -->
    <ul class="menu">
      <li class="menu-item">Home</li>
      <li class="menu-item">Movies</li>
      <li class="menu-item">Celebs</li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
};
</script>

<style scoped>
.sidebar {
  width: 240px;
  padding: 20px;
  background: #1a1512;
  border-right: 1px solid rgba(152, 57, 68, 0.35);
  color: #fff;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  padding: 12px 0;
  cursor: pointer;
  transition: 0.3s ease;
}

.menu-item:hover {
  color: #e68a9c;
}
</style>