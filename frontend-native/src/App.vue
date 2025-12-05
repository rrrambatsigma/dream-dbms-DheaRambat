<template>
  <div class="app-container">
    <HeaderNavigation 
      :active-tab="activeTab"
      @tab-change="setActiveTab"
      @quick-search="handleQuickSearch"
    />
    
    <HomeView 
      v-if="activeTab === 'home'"
      @show-detail="openDetailModal"
    />
    
    <MoviesView 
      v-if="activeTab === 'movies'"
      @show-detail="openDetailModal"
    />

    <DetailModal 
      v-if="showDetailModal"
      :show-id="selectedShowId"
      @close="closeDetailModal"
    />
  </div>
</template>

<script>
import HeaderNavigation from './componentsweb/common/HeaderNavigation.vue'
import HomeView from './views/native/HomeView.vue'
import MoviesView from './views/native/MoviesView.vue'
import DetailModal from './componentsweb/native/DetailModal.vue'

export default {
  name: 'App',
  components: {
    HeaderNavigation,
    HomeView,
    MoviesView,
    DetailModal
  },
  data() {
    return {
      activeTab: 'home',
      showDetailModal: false,
      selectedShowId: null
    }
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab
    },
    handleQuickSearch(keyword) {
      // Forward quick search to appropriate component
      if (this.activeTab === 'home') {
        this.$refs.homeView?.handleQuickSearch?.(keyword)
      }
    },
    openDetailModal(showId) {
      this.selectedShowId = showId
      this.showDetailModal = true
    },
    closeDetailModal() {
      this.showDetailModal = false
      this.selectedShowId = null
    }
  }
}
</script>

<style>
/* Global styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

.app-container {
  min-height: 100vh;
  background: 
    radial-gradient(ellipse at top left, rgba(152, 57, 68, 0.12) 0%, transparent 50%),
    radial-gradient(ellipse at bottom right, rgba(120, 45, 48, 0.08) 0%, transparent 50%),
    linear-gradient(135deg, #1a1612 0%, #14100c 100%);
  color: #f5f1e8;
  font-family: 'Poppins', sans-serif;
  position: relative;
}

.app-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(152, 57, 68, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(120, 45, 48, 0.06) 0%, transparent 50%),
    linear-gradient(45deg, transparent 65%, rgba(152, 57, 68, 0.03) 100%);
  pointer-events: none;
  z-index: 0;
}
</style>