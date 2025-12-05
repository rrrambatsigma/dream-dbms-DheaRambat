<template>
  <div class="movies-view">
    <!-- Discover Section -->
    <DiscoverSection 
      @show-detail="handleShowDetail"
    />

    <!-- Detail Modal -->
    <DetailModal 
      :show="showModal"
      :show-id="selectedShowId"
      @close="closeModal"
    />
  </div>
</template>

<script>
import DiscoverSection from '../../componentsweb/native/DiscoverSection.vue'
import DetailModal from '../../componentsweb/native/DetailModal.vue'

export default {
  name: 'MoviesView',
  components: {
    DiscoverSection,
    DetailModal
  },
  data() {
    return {
      selectedShowId: null,
      showModal: false
    }
  },
  methods: {
    handleShowDetail(showId) {
      console.log('Show detail clicked:', showId);
      this.selectedShowId = showId;
      this.showModal = true;
    },
    
    closeModal() {
      this.showModal = false;
      this.selectedShowId = null;
    }
  }
}
</script>

<style scoped>
.movies-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0c0a08 0%, #1a1512 50%, #0c0a08 100%);
  position: relative;
  overflow-x: hidden;
}

.movies-view::before {
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

/* Responsive */
@media (max-width: 768px) {
  .movies-view {
    padding: 0;
  }
}
</style>