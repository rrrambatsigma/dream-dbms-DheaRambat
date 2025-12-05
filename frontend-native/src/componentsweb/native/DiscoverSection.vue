<template>
  <section class="discover-section">
    <div class="discover-container">
      <!-- Modern Header yang menampilkan kategori aktif -->
      <div class="modern-header">
        <div class="header-content">
          <h1 class="main-title">Explore Entertainment</h1>
          <p class="subtitle">Discover movies & TV shows across platforms and genres</p>
          
          <!-- Display Active Category Items -->
          <div class="category-display" v-if="!discoverLoading && !discoverError && discoverItems.length > 0">
            <div class="display-title">Popular {{ getActiveCategoryTitle() }}</div>
            <div class="items-scroll">
              <div
                v-for="(item, index) in displayedItems"
                :key="item[getCategoryIdField()]"
                class="display-item"
                @click="viewCategoryShows(item)"
              >
                <span class="item-name">{{ getCategoryName(item) }}</span>
                <span class="item-count">({{ item.TotalShows || 0 }})</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Decorative Elements -->
        <div class="header-decoration">
          <div class="decoration-circle"></div>
          <div class="decoration-circle"></div>
          <div class="decoration-circle"></div>
        </div>
      </div>

      <!-- Compact Category Navigation -->
      <div class="category-navigation">
        <div class="nav-header">
          <h2 class="nav-title">Browse By Category</h2>
        </div>
        
        <div class="category-grid-compact">
          <div 
            v-for="category in discoverCategories" 
            :key="category.type"
            @click="setActiveDiscoverCategory(category.type)"
            :class="{
              'category-card-compact': true,
              'active': activeDiscoverCategory === category.type
            }"
          >
            <div class="card-icon-compact">{{ category.icon }}</div>
            <div class="card-content-compact">
              <h3 class="card-title-compact">{{ category.name }}</h3>
              <p class="card-desc-compact">Browse by {{ category.name.toLowerCase() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Content Section -->
      <div class="content-section">
        <!-- Loading State -->
        <div v-if="discoverLoading" class="modern-loading">
          <div class="loading-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
          </div>
          <p class="loading-text">Loading {{ activeDiscoverCategory }}...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="discoverError" class="modern-error">
          <div class="error-icon">⚠️</div>
          <div class="error-content">
            <h3>Oops! Something went wrong</h3>
            <p>{{ discoverError }}</p>
            <button class="retry-btn" @click="loadDiscoverCategories">
              Try Again
            </button>
          </div>
        </div>

        <!-- Content Grid dengan Pagination -->
        <div v-else-if="discoverItems.length > 0" class="content-grid-section">
          <div class="grid-header">
            <h3 class="grid-title">All {{ getActiveCategoryTitle() }}</h3>
            <div class="grid-stats">
              <span class="stat-item">{{ discoverItems.length }} total items</span>
            </div>
          </div>

          <div class="items-grid-compact">
            <div
              v-for="item in paginatedItems"
              :key="item[getCategoryIdField()]"
              class="item-card-compact"
              @click="viewCategoryShows(item)"
            >
              <div class="card-content-compact">
                <div class="item-header-compact">
                  <h4 class="item-name-compact">{{ getCategoryName(item) }}</h4>
                  <div class="item-badge-compact">
                    {{ item.TotalShows || 0 }}
                  </div>
                </div>
                <p class="item-subtitle-compact">shows available</p>
              </div>
              <div class="view-indicator">→</div>
            </div>
          </div>

          <!-- Pagination Controls -->
          <div class="pagination-controls" v-if="totalPages > 1">
            <button 
              class="pagination-btn" 
              :disabled="currentPage === 1"
              @click="previousPage"
            >
              Previous
            </button>
            
            <div class="page-info">
              Page {{ currentPage }} of {{ totalPages }}
            </div>
            
            <button 
              class="pagination-btn" 
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              Next
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">📺</div>
          <h3 class="empty-title">No {{ getActiveCategoryTitle() }} Found</h3>
          <p class="empty-description">Try selecting a different category or check back later.</p>
        </div>
      </div>

      <!-- Category Results -->
      <CategoryResults 
        v-if="categoryShows.length > 0"
        :shows="categoryShows"
        :pagination="categoryPagination"
        :category-name="activeCategoryName"
        @show-detail="$emit('show-detail', $event)"
        @page-change="goToCategoryPage"
      />
    </div>
  </section>
</template>

<script>
import CategoryResults from './CategoryResults.vue'

export default {
  name: 'DiscoverSection',
  components: {
    CategoryResults
  },
  data() {
    return {
      discoverCategories: [
        { type: 'networks', name: 'Networks', icon: '📡' },
        { type: 'countries', name: 'Countries', icon: '🌍' },
        { type: 'types', name: 'Genres', icon: '🎬' },
        { type: 'statuses', name: 'Status', icon: '📊' }
      ],
      activeDiscoverCategory: 'networks',
      discoverItems: [],
      discoverLoading: false,
      discoverError: null,
      categoryShows: [],
      activeCategoryId: null,
      activeCategoryName: '',
      categoryPagination: {
        current_page: 1,
        page_size: 12,
        total_rows: 0,
        total_pages: 0
      },
      currentPage: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    displayedItems() {
      // Tampilkan maksimal 8 item di header
      return this.discoverItems.slice(0, 8);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.discoverItems.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.discoverItems.length / this.itemsPerPage);
    }
  },
  mounted() {
    this.loadDiscoverCategories();
  },
  methods: {
    async loadDiscoverCategories() {
      this.discoverLoading = true;
      this.discoverError = null;
      this.currentPage = 1; // Reset ke page 1 saat load kategori baru
      
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/api/native/discover/${this.activeDiscoverCategory}`
        );
        const data = await response.json();
        
        if (data.success) {
          this.discoverItems = data.data;
        } else {
          this.discoverError = data.error || 'Failed to load categories';
        }
      } catch (err) {
        this.discoverError = 'Network error: ' + err.message;
        console.error('Discover error:', err);
      } finally {
        this.discoverLoading = false;
      }
    },

    setActiveDiscoverCategory(category) {
      this.activeDiscoverCategory = category;
      this.categoryShows = [];
      this.activeCategoryId = null;
      this.activeCategoryName = '';
      this.currentPage = 1; // Reset pagination
      this.loadDiscoverCategories();
    },
    
    getCategoryIdField() {
      const fieldMap = {
        'networks': 'NetworkTypeID',
        'countries': 'ProductionCountryTypeID',
        'types': 'TypeID',
        'statuses': 'StatusID'
      };
      return fieldMap[this.activeDiscoverCategory];
    },
    
    getCategoryName(item) {
      const fieldMap = {
        'networks': 'NetworkName',
        'countries': 'ProductionCountryName',
        'types': 'TypeName',
        'statuses': 'StatusName'
      };
      return item[fieldMap[this.activeDiscoverCategory]];
    },

    getActiveCategoryTitle() {
      const titleMap = {
        'networks': 'Networks',
        'countries': 'Countries',
        'types': 'Genres',
        'statuses': 'Status'
      };
      return titleMap[this.activeDiscoverCategory];
    },

    // Pagination methods
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    async viewCategoryShows(item) {
      this.activeCategoryId = item[this.getCategoryIdField()];
      this.activeCategoryName = this.getCategoryName(item);
      this.categoryPagination.current_page = 1;
      
      await this.loadCategoryShows();
      
      setTimeout(() => {
        const resultsSection = document.querySelector('.category-results');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    },
    
    async loadCategoryShows() {
      if (!this.activeCategoryId) return;
      
      try {
        const categoryTypeMap = {
          'networks': 'network',
          'countries': 'country',
          'types': 'type',
          'statuses': 'status'
        };
        
        const categoryType = categoryTypeMap[this.activeDiscoverCategory];
        
        const params = new URLSearchParams({
          page: this.categoryPagination.current_page,
          page_size: this.categoryPagination.page_size
        });
        
        const response = await fetch(
          `http://127.0.0.1:5000/api/native/discover/${categoryType}/${this.activeCategoryId}?${params}`
        );
        
        const data = await response.json();
        
        if (data.success) {
          this.categoryShows = data.results;
          this.categoryPagination = {
            current_page: data.pagination.page,
            page_size: data.pagination.page_size,
            total_rows: data.pagination.total_rows,
            total_pages: data.pagination.total_pages
          };
        } else {
          this.discoverError = data.error || 'Failed to load category shows';
        }
      } catch (err) {
        this.discoverError = 'Network error: ' + err.message;
        console.error('Category shows error:', err);
      }
    },
    
    goToCategoryPage(page) {
      if (page === '...' || page < 1 || page > this.categoryPagination.total_pages || page === this.categoryPagination.current_page) {
        return;
      }
      
      this.categoryPagination.current_page = page;
      this.loadCategoryShows();
    }
  }
}
</script>

<style scoped>
.discover-section {
  padding: 0;
  background: transparent;
  min-height: 100vh;
}

.discover-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Modern Header Styles */
.modern-header {
  position: relative;
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0 30px;
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.05) 0%, 
    rgba(177, 79, 29, 0.05) 100%);
  border-radius: 20px;
  overflow: hidden;
}

.header-content {
  position: relative;
  z-index: 2;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f8f4ed 0%, #d8a0a5 50%, #b87c7c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
  font-family: 'Poppins', sans-serif;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1.1rem;
  color: rgba(248, 244, 237, 0.8);
  margin-bottom: 24px;
  font-weight: 400;
  font-family: 'Poppins', sans-serif;
}

/* Category Display in Header */
.category-display {
  margin-top: 20px;
}

.display-title {
  font-size: 1rem;
  color: rgba(248, 244, 237, 0.7);
  margin-bottom: 12px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
}

.items-scroll {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 800px;
  margin: 0 auto;
}

.display-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background: rgba(42, 36, 30, 0.6);
  border: 1px solid rgba(152, 57, 68, 0.2);
  border-radius: 12px;
  color: #f8f4ed;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.display-item:hover {
  background: rgba(152, 57, 68, 0.1);
  border-color: rgba(152, 57, 68, 0.4);
  transform: translateY(-1px);
}

.item-count {
  color: #b87c7c;
  font-size: 0.8rem;
  font-weight: 600;
}

.header-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(152, 57, 68, 0.1) 0%, transparent 70%);
}

.decoration-circle:nth-child(1) {
  width: 150px;
  height: 150px;
  top: -30px;
  left: -30px;
}

.decoration-circle:nth-child(2) {
  width: 120px;
  height: 120px;
  bottom: -20px;
  right: 15%;
}

.decoration-circle:nth-child(3) {
  width: 80px;
  height: 80px;
  top: 25%;
  right: -20px;
}

/* Compact Category Navigation */
.category-navigation {
  margin-bottom: 40px;
}

.nav-header {
  margin-bottom: 24px;
}

.nav-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.category-grid-compact {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  max-width: 800px;
  margin: 0 auto;
}

.category-card-compact {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.8) 0%, 
    rgba(31, 26, 20, 0.8) 100%);
  border: 1px solid rgba(152, 57, 68, 0.2);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.category-card-compact:hover {
  border-color: rgba(152, 57, 68, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(152, 57, 68, 0.15);
}

.category-card-compact.active {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.15) 0%, 
    rgba(177, 79, 29, 0.15) 100%);
  border-color: rgba(152, 57, 68, 0.6);
}

.card-icon-compact {
  font-size: 2rem;
}

.card-content-compact {
  flex: 1;
}

.card-title-compact {
  font-size: 1rem;
  font-weight: 600;
  color: #f8f4ed;
  margin-bottom: 4px;
  font-family: 'Poppins', sans-serif;
}

.card-desc-compact {
  font-size: 0.8rem;
  color: rgba(248, 244, 237, 0.6);
  font-family: 'Poppins', sans-serif;
}

/* Content Section */
.content-section {
  margin-bottom: 60px;
}

/* Modern Loading */
.modern-loading {
  text-align: center;
  padding: 60px 20px;
}

.loading-spinner {
  position: relative;
  width: 50px;
  height: 50px;
  margin: 0 auto 20px;
}

.spinner-ring {
  position: absolute;
  border: 2px solid transparent;
  border-top: 2px solid #b87c7c;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-ring:nth-child(1) {
  width: 100%;
  height: 100%;
  animation-duration: 1s;
}

.spinner-ring:nth-child(2) {
  width: 70%;
  height: 70%;
  top: 15%;
  left: 15%;
  animation-duration: 1.2s;
  animation-direction: reverse;
}

.spinner-ring:nth-child(3) {
  width: 40%;
  height: 40%;
  top: 30%;
  left: 30%;
  animation-duration: 0.8s;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #b87c7c;
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
}

/* Modern Error */
.modern-error {
  display: flex;
  align-items: center;
  gap: 20px;
  background: linear-gradient(135deg, 
    rgba(74, 61, 47, 0.9) 0%, 
    rgba(61, 51, 40, 0.9) 100%);
  border: 1px solid rgba(212, 124, 92, 0.3);
  border-radius: 12px;
  padding: 24px;
  margin: 30px 0;
}

.error-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.error-content h3 {
  color: #ffd8c8;
  margin-bottom: 6px;
  font-family: 'Poppins', sans-serif;
  font-size: 1.1rem;
}

.error-content p {
  color: rgba(255, 216, 200, 0.8);
  margin-bottom: 12px;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
}

.retry-btn {
  background: linear-gradient(135deg, #d47c5c 0%, #b87c7c 100%);
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(212, 124, 92, 0.4);
}

/* Content Grid Compact */
.content-grid-section {
  background: rgba(42, 36, 30, 0.3);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(152, 57, 68, 0.1);
}

.grid-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.grid-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
}

.grid-stats {
  color: rgba(248, 244, 237, 0.6);
  font-size: 0.85rem;
}

.items-grid-compact {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.item-card-compact {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border: 1px solid rgba(152, 57, 68, 0.2);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s ease;
}

.item-card-compact:hover {
  border-color: rgba(152, 57, 68, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(152, 57, 68, 0.15);
}

.card-content-compact {
  flex: 1;
}

.item-header-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.item-name-compact {
  font-size: 0.95rem;
  font-weight: 600;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
  margin: 0;
}

.item-badge-compact {
  background: linear-gradient(135deg, #b87c7c 0%, #d47c5c 100%);
  color: white;
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}

.item-subtitle-compact {
  color: rgba(248, 244, 237, 0.6);
  font-size: 0.8rem;
  font-family: 'Poppins', sans-serif;
  margin: 0;
}

.view-indicator {
  color: #b87c7c;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.item-card-compact:hover .view-indicator {
  transform: translateX(3px);
  color: #f8f4ed;
}

/* Pagination Controls */
.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid rgba(152, 57, 68, 0.2);
}

.pagination-btn {
  background: rgba(42, 36, 30, 0.8);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 8px;
  padding: 8px 16px;
  color: #f8f4ed;
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: rgba(152, 57, 68, 0.1);
  border-color: rgba(152, 57, 68, 0.5);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: rgba(248, 244, 237, 0.7);
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
  font-weight: 500;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 1.3rem;
  color: #f8f4ed;
  margin-bottom: 8px;
  font-family: 'Poppins', sans-serif;
}

.empty-description {
  color: rgba(248, 244, 237, 0.6);
  font-size: 0.9rem;
  font-family: 'Poppins', sans-serif;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-title {
    font-size: 2.2rem;
  }
  
  .category-grid-compact {
    grid-template-columns: repeat(2, 1fr);
    max-width: 500px;
  }
}

@media (max-width: 768px) {
  .discover-container {
    padding: 20px 16px;
  }
  
  .modern-header {
    padding: 30px 20px;
    margin-bottom: 30px;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .items-scroll {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 10px;
  }
  
  .display-item {
    flex-shrink: 0;
  }
  
  .items-grid-compact {
    grid-template-columns: 1fr;
  }
  
  .grid-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .modern-error {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .pagination-controls {
    flex-direction: column;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .category-grid-compact {
    grid-template-columns: 1fr;
  }
  
  .nav-title {
    font-size: 1.3rem;
  }
  
  .content-grid-section {
    padding: 16px;
  }
}
</style>