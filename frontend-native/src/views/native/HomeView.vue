<template>
  <div>
    <!-- Modern Header untuk Find Your Story -->
    <div class="modern-header-home">
      <div class="header-content-home">
        <h1 class="main-title-home">Find Your Story</h1>
        <p class="subtitle-home">Discover movies & TV shows across platforms and genres</p>
      </div>
      
      <!-- Decorative Elements -->
      <div class="header-decoration-home">
        <div class="decoration-circle-home"></div>
        <div class="decoration-circle-home"></div>
        <div class="decoration-circle-home"></div>
      </div>
    </div>

    <!-- Search Section -->
    <SearchSection 
      ref="searchSection"
      @show-detail="handleShowDetail"
    />

    <!-- Trending Section -->
    <TrendingSection 
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
import SearchSection from '../../componentsweb/native/SearchSection.vue'
import TrendingSection from '../../componentsweb/native/TrendingSection.vue'
import DetailModal from '../../componentsweb/native/DetailModal.vue'

export default {
  name: 'HomeView',
  components: {
    SearchSection,
    TrendingSection,
    DetailModal
  },
  data() {
    return {
      selectedShowId: null,
      showModal: false
    }
  },
  methods: {
    handleQuickSearch(keyword) {
      this.$refs.searchSection?.performQuickSearch?.(keyword)
    },
    
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
/* Modern Header Styles untuk Home */
.modern-header-home {
  position: relative;
  text-align: center;
  margin-bottom: 40px;
  padding: 60px 0 40px;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.95) 0%, 
    rgba(31, 26, 20, 0.95) 100%);
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid rgba(152, 57, 68, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  margin: 20px;
}

.header-content-home {
  position: relative;
  z-index: 2;
}

.main-title-home {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f8f4ed 0%, #d8a0a5 50%, #b87c7c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  font-family: 'Poppins', sans-serif;
  letter-spacing: -0.02em;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.subtitle-home {
  font-size: 1.2rem;
  color: rgba(248, 244, 237, 0.9);
  margin-bottom: 0;
  font-weight: 400;
  font-family: 'Poppins', sans-serif;
  letter-spacing: 0.02em;
}

.header-decoration-home {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.decoration-circle-home {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(152, 57, 68, 0.15) 0%, transparent 70%);
}

.decoration-circle-home:nth-child(1) {
  width: 200px;
  height: 200px;
  top: -50px;
  left: -50px;
}

.decoration-circle-home:nth-child(2) {
  width: 150px;
  height: 150px;
  bottom: -30px;
  right: 20%;
}

.decoration-circle-home:nth-child(3) {
  width: 100px;
  height: 100px;
  top: 30%;
  right: -30px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-title-home {
    font-size: 3rem;
  }
  
  .modern-header-home {
    margin: 15px;
  }
}

@media (max-width: 768px) {
  .modern-header-home {
    padding: 40px 0 30px;
    margin: 10px;
    border-radius: 20px;
  }
  
  .main-title-home {
    font-size: 2.5rem;
  }
  
  .subtitle-home {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .main-title-home {
    font-size: 2rem;
  }
  
  .subtitle-home {
    font-size: 1rem;
  }
  
  .modern-header-home {
    padding: 30px 0 25px;
    margin: 8px;
    border-radius: 16px;
  }
  
  .decoration-circle-home:nth-child(1) {
    width: 120px;
    height: 120px;
  }
  
  .decoration-circle-home:nth-child(2) {
    width: 80px;
    height: 80px;
  }
  
  .decoration-circle-home:nth-child(3) {
    width: 60px;
    height: 60px;
  }
}
</style>