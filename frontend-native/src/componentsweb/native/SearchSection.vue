<template>
  <section class="search-section">
    <div class="search-container">
      
      <!-- Search Filters -->
      <div class="filters-panel">
        <button @click="showFilters = !showFilters" class="filters-toggle">
          <span>{{ showFilters ? '▼' : '▶' }}</span>
          <span>Filters</span>
        </button>

        <transition name="slide">
          <div v-show="showFilters" class="filters-content">
            
            <!-- Search Input -->
            <div class="filter-section">
              <label class="filter-label">Title Search</label>
              <input
                v-model="filters.keyword"
                type="text"
                placeholder="Search by title..."
                class="filter-input"
                @keydown.enter.prevent="searchShows"
                @input="handleSearchInput"
              />
            </div>

            <!-- Filters Row 1 -->
            <div class="filters-row">
              <div class="filter-section">
                <label class="filter-label">Genre</label>
                <select v-model="filters.genre" class="filter-select">
                  <option value="">All</option>
                  <option value="Drama">Drama</option>
                  <option value="Comedy">Comedy</option>
                  <option value="Action">Action & Adventure</option>
                  <option value="Sci-Fi">Sci-Fi & Fantasy</option>
                  <option value="Thriller">Thriller</option>
                  <option value="Horror">Horror</option>
                  <option value="Romance">Romance</option>
                  <option value="Documentary">Documentary</option>
                  <option value="Crime">Crime</option>
                  <option value="Mystery">Mystery</option>
                  <option value="Animation">Animation</option>
                </select>
              </div>

              <div class="filter-section">
                <label class="filter-label">Language</label>
                <select v-model="filters.language" class="filter-select">
                  <option value="">All Languages</option>
                  <option value="en">English</option>
                  <option value="id">Indonesian</option>
                  <option value="ko">Korean</option>
                  <option value="ja">Japanese</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="it">Italian</option>
                  <option value="zh">Chinese</option>
                </select>
              </div>

              <div class="filter-section">
                <label class="filter-label">Sort By</label>
                <select v-model="filters.sort_by" class="filter-select">
                  <option value="popularity">Popularity</option>
                  <option value="rating">IMDb Rating</option>
                  <option value="year">Release Date</option>
                  <option value="name">A-Z</option>
                </select>
              </div>
            </div>

            <!-- Filters Row 2 -->
            <div class="filters-row">
              <div class="filter-section">
                <label class="filter-label">Year From</label>
                <input
                  v-model.number="filters.start_year_from"
                  type="number"
                  placeholder="1990"
                  class="filter-input"
                  min="1900"
                  :max="currentYear"
                />
              </div>

              <div class="filter-section">
                <label class="filter-label">Year To</label>
                <input
                  v-model.number="filters.start_year_to"
                  type="number"
                  placeholder="2024"
                  class="filter-input"
                  min="1900"
                  :max="currentYear"
                />
              </div>

              <div class="filter-section">
                <label class="filter-label">Sort Order</label>
                <select v-model="filters.sort_order" class="filter-select">
                  <option value="DESC">High to Low</option>
                  <option value="ASC">Low to High</option>
                </select>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="filters-actions">
              <button @click="searchShows" class="btn-search" :disabled="searchLoading">
                {{ searchLoading ? 'Searching...' : 'Search' }}
              </button>
              <button @click="resetFilters" class="btn-reset">
                Clear All
              </button>
            </div>

          </div>
        </transition>
      </div>

      <!-- SEARCH RESULTS -->
      <div v-if="searched" class="results-container">
        
        <!-- Results Header -->
        <div v-if="!searchLoading && searchResults.length > 0" class="results-header">
          <h3 class="results-count">{{ pagination.total_rows }} titles found • Page {{ pagination.current_page }} of {{ pagination.total_pages }}</h3>
        </div>

        <!-- Loading -->
        <div v-if="searchLoading" class="loading-container">
          <div class="spinner"></div>
          <p class="loading-text">Searching...</p>
        </div>

        <!-- Error -->
        <div v-if="searchError" class="error-box">
          <span class="error-icon">⚠</span>
          <p>{{ searchError }}</p>
        </div>

        <!-- Results Grid - 2 Kolom -->
        <div v-if="!searchLoading && searchResults.length > 0" class="results-grid-container">
          <div class="results-grid">
            <!-- Kolom Kiri -->
            <div class="results-column">
              <div
                v-for="show in leftColumnResults"
                :key="show.ShowID"
                class="result-item compact-item"
                @click="viewShowDetail(show.ShowID)"
              >
                <div class="result-poster-col compact-poster">
                  <div class="result-poster compact-poster-img">📺</div>
                </div>

                <div class="result-content-col compact-content">
                  <div class="result-header compact-header">
                    <h3 class="result-title compact-title">{{ show.Name }}</h3>
                    <div class="result-rating compact-rating">
                      <span class="rating-star">⭐</span>
                      <span class="rating-value">{{ show.VoteAverage || 'N/A' }}</span>
                    </div>
                  </div>

                  <div class="result-meta-row compact-meta">
                    <span class="meta-item">{{ formatYear(show.FirstAirDate) }}</span>
                    <span class="meta-separator">•</span>
                    <span class="meta-item">{{ show.StatusName || 'Unknown' }}</span>
                    <span class="meta-separator">•</span>
                    <span class="meta-item genre-tags">{{ show.Genres || 'N/A' }}</span>
                  </div>

                  <p class="result-overview compact-overview">{{ truncate(show.Overview, 120) }}</p>

                  <div class="result-footer compact-footer">
                    <span class="votes-count">{{ formatVotes(show.VoteCount) }} votes</span>
                    <span class="meta-separator">•</span>
                    <span class="popularity">Popularity: {{ Math.round(show.Popularity) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Kolom Kanan -->
            <div class="results-column">
              <div
                v-for="show in rightColumnResults"
                :key="show.ShowID"
                class="result-item compact-item"
                @click="viewShowDetail(show.ShowID)"
              >
                <div class="result-poster-col compact-poster">
                  <div class="result-poster compact-poster-img">📺</div>
                </div>

                <div class="result-content-col compact-content">
                  <div class="result-header compact-header">
                    <h3 class="result-title compact-title">{{ show.Name }}</h3>
                    <div class="result-rating compact-rating">
                      <span class="rating-star">⭐</span>
                      <span class="rating-value">{{ show.VoteAverage || 'N/A' }}</span>
                    </div>
                  </div>

                  <div class="result-meta-row compact-meta">
                    <span class="meta-item">{{ formatYear(show.FirstAirDate) }}</span>
                    <span class="meta-separator">•</span>
                    <span class="meta-item">{{ show.StatusName || 'Unknown' }}</span>
                    <span class="meta-separator">•</span>
                    <span class="meta-item genre-tags">{{ show.Genres || 'N/A' }}</span>
                  </div>

                  <p class="result-overview compact-overview">{{ truncate(show.Overview, 120) }}</p>

                  <div class="result-footer compact-footer">
                    <span class="votes-count">{{ formatVotes(show.VoteCount) }} votes</span>
                    <span class="meta-separator">•</span>
                    <span class="popularity">Popularity: {{ Math.round(show.Popularity) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination Controls -->
        <PaginationControls 
          v-if="!searchLoading && searchResults.length > 0 && pagination.total_pages > 1"
          :pagination="pagination"
          :visible-pages="visiblePages"
          @page-change="goToPage"
        />

        <!-- No Results -->
        <div v-if="!searchLoading && searched && searchResults.length === 0" class="no-results">
          <div class="no-results-icon">🔍</div>
          <h3>No results found</h3>
          <p>Try different keywords or adjust your filters</p>
        </div>

      </div>

      <!-- Quick Search Prompt -->
      <div v-else-if="!searched" class="quick-search-prompt">
        <div class="prompt-icon">🎬</div>
        <h3>Find Your Next Favorite Show</h3>
        <p>Use the filters above to search through our TV show database</p>
      </div>
    </div>
  </section>
</template>

<script>
import PaginationControls from '../shared/PaginationControls.vue'

export default {
  name: 'SearchSection',
  components: {
    PaginationControls
  },
  mounted() {
    // listen window custom event (works cross-Vue-version)
    window.addEventListener('quick-search', this.performQuickSearchFromEvent)
    // fallback: jika ada event bus di root (Vue 2)
    if (this.$root && this.$root.$on) {
      this.$root.$on('quick-search', this.performQuickSearch)
      this._usedRootBus = true
    }
  },
  // untuk Vue 2 hooks
  beforeDestroy() {
    if (this._usedRootBus && this.$root && this.$root.$off) {
      this.$root.$off('quick-search', this.performQuickSearch)
    }
    window.removeEventListener('quick-search', this.performQuickSearchFromEvent)
  },
  // untuk Vue 3 hooks
  beforeUnmount() {
    if (this._usedRootBus && this.$root && this.$root.$off) {
      this.$root.$off('quick-search', this.performQuickSearch)
    }
    window.removeEventListener('quick-search', this.performQuickSearchFromEvent)
  },
  data() {
    return {
      showFilters: true,
      filters: {
        keyword: '',
        genre: '',
        language: '',
        start_year_from: null,
        start_year_to: null,
        sort_by: 'popularity',
        sort_order: 'DESC',
        page: 1,
        page_size: 10
      },
      searchResults: [],
      searchLoading: false,
      searched: false,
      searchError: null,
      currentYear: new Date().getFullYear(),
      pagination: {
        current_page: 1,
        page_size: 10,
        total_rows: 0,
        total_pages: 0
      }
    }
  },
  computed: {
    visiblePages() {
      const current = this.pagination.current_page;
      const total = this.pagination.total_pages;
      const range = [];
      
      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          range.push(i);
        }
      } else {
        range.push(1);
        
        if (current > 3) {
          range.push('...');
        }
        
        const start = Math.max(2, current - 1);
        const end = Math.min(total - 1, current + 1);
        
        for (let i = start; i <= end; i++) {
          range.push(i);
        }
        
        if (current < total - 2) {
          range.push('...');
        }
        
        range.push(total);
      }
      
      return range;
    },
    leftColumnResults() {
      const midIndex = Math.ceil(this.searchResults.length / 2);
      return this.searchResults.slice(0, midIndex);
    },
    rightColumnResults() {
      const midIndex = Math.ceil(this.searchResults.length / 2);
      return this.searchResults.slice(midIndex);
    }
  },
  methods: {
  async searchShows() {
  // Simpan keyword dulu sebelum di-clear
  const searchKeyword = this.filters.keyword.trim();
  
  if (!searchKeyword) return; // Jangan search jika kosong
  
  this.searchLoading = true;
  this.searchError = null;
  this.searched = true;

  try {
    const params = new URLSearchParams();
    
    params.append('keyword', searchKeyword); // ✅ Gunakan yang disimpan
    if (this.filters.genre) params.append('genre', this.filters.genre);
    if (this.filters.language) params.append('language', this.filters.language);
    if (this.filters.start_year_from) params.append('start_year_from', this.filters.start_year_from);
    if (this.filters.start_year_to) params.append('start_year_to', this.filters.start_year_to);
    params.append('sort_by', this.filters.sort_by);
    params.append('sort_order', this.filters.sort_order);
    params.append('page', this.filters.page);
    params.append('page_size', this.filters.page_size);

    const response = await fetch(`http://127.0.0.1:5000/api/native/search?${params}`);
    const data = await response.json();

    if (data.success) {
      this.searchResults = data.results;
      this.pagination = {
        current_page: data.pagination.page,
        page_size: data.pagination.page_size,
        total_rows: data.pagination.total_rows,
        total_pages: data.pagination.total_pages
      };
      
      // removed clearing keyword so input stays after search
      // this.filters.keyword = '';
      
    } else {
      this.searchError = data.error || 'Failed to fetch results';
    }
  } catch (err) {
    this.searchError = 'Network error: ' + err.message;
    console.error('Search error:', err);
  } finally {
    this.searchLoading = false;
  }
},
  handleSearchInput() {
    // Reset search results ketika user mulai mengetik lagi
    if (this.searched) {
      this.searchResults = [];
      this.searched = false;
    }
  },
    goToPage(page) {
      if (page === '...' || page < 1 || page > this.pagination.total_pages || page === this.pagination.current_page) {
        return;
      }
      
      this.filters.page = page;
      this.searchShows();
    },
    performQuickSearch(keyword) {
      this.filters.keyword = keyword;
      this.filters.page = 1;
      this.showFilters = true;
      this.searchShows();
    },
    resetFilters() {
      this.filters = {
        keyword: '',
        genre: '',
        language: '',
        start_year_from: null,
        start_year_to: null,
        sort_by: 'popularity',
        sort_order: 'DESC',
        page: 1,
        page_size: 10
      };
      this.searchResults = [];
      this.searched = false;
      this.searchError = null;
      this.pagination = {
        current_page: 1,
        page_size: 10,
        total_rows: 0,
        total_pages: 0
      };
    },
        performQuickSearch(keyword) {
      this.filters.keyword = keyword;
      this.filters.page = 1;
      this.showFilters = true;
      this.searchShows();
    },

      performQuickSearchFromEvent(e) {
      const kw = e && e.detail ? e.detail : ''
        if (!kw) return
        this.performQuickSearch(kw)
    },
    formatYear(dateStr) {
      if (!dateStr) return 'N/A';
      try {
        return new Date(dateStr).getFullYear();
      } catch {
        return 'N/A';
      }
    },
    formatVotes(votes) {
      if (!votes) return '0';
      if (votes >= 1000000) return (votes / 1000000).toFixed(1) + 'M';
      if (votes >= 1000) return (votes / 1000).toFixed(1) + 'K';
      return votes.toString();
    },
    truncate(text, length = 120) {
      if (!text) return 'No description available';
      if (text.length <= length) return text;
      return text.substring(0, length) + '...';
    },
    viewShowDetail(showId) {
      this.$emit('show-detail', showId);
    }
  }
}
</script>

<style scoped>
.search-section {
  background: linear-gradient(180deg, 
    rgba(20, 16, 12, 0.95) 0%, 
    rgba(26, 22, 18, 0.95) 100%);
  padding: 30px 40px 60px;
}

.search-container {
  max-width: 100%;
  margin: 0 auto;
}

.filters-panel {
  background: 
    linear-gradient(135deg, 
      rgba(31, 26, 20, 0.98) 0%, 
      rgba(42, 36, 30, 0.98) 100%);
  border-radius: 16px;
  margin-bottom: 32px;
  border: 1px solid rgba(152, 57, 68, 0.3);
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.6),
    0 0 25px rgba(152, 57, 68, 0.15);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.filters-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(152, 57, 68, 0.1),
    transparent
  );
  transition: left 0.8s ease;
}

.filters-panel:hover::before {
  left: 100%;
}

.filters-toggle {
  width: 100%;
  background: transparent;
  border: none;
  color: #f8f4ed;
  padding: 20px 28px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.4s ease;
  border-radius: 16px;
  position: relative;
  z-index: 1;
  font-family: 'Poppins', sans-serif;
}

.filters-toggle:hover {
  background-color: rgba(152, 57, 68, 0.08);
}

.filters-content {
  padding: 0 28px 28px;
  position: relative;
  z-index: 1;
}

.filter-section {
  margin-bottom: 20px;
  position: relative;
}

.filter-label {
  display: block;
  color: #d8a0a5;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 3px rgba(0,0,0,0.4);
  font-family: 'Poppins', sans-serif;
}

.filter-input,
.filter-select {
  width: 100%;
  padding: 14px 18px;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.95) 0%, 
    rgba(53, 45, 37, 0.95) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 10px;
  color: #f8f4ed;
  font-size: 14px;
  transition: all 0.4s ease;
  box-shadow: 
    inset 0 2px 6px rgba(0,0,0,0.4),
    0 4px 12px rgba(152, 57, 68, 0.1);
  font-family: 'Poppins', sans-serif;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23d8a0a5'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 16px center;
  background-size: 16px;
  padding-right: 45px;
  cursor: pointer;
}

.filter-select option {
  background-color: #2a241e;
  color: #f8f4ed;
  border: none;
  padding: 12px 16px;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
}

.filter-select option:hover {
  background-color: rgba(152, 57, 68, 0.3) !important;
}

.filter-select option:checked {
  background-color: rgba(152, 57, 68, 0.5) !important;
}

.filter-select::-webkit-scrollbar {
  width: 8px;
}

.filter-select::-webkit-scrollbar-track {
  background: rgba(42, 36, 30, 0.8);
  border-radius: 4px;
}

.filter-select::-webkit-scrollbar-thumb {
  background: rgba(152, 57, 68, 0.5);
  border-radius: 4px;
}

.filter-input[type="number"] {
  font-family: 'Poppins', sans-serif;
}

.filter-input[type="number"]::-webkit-inner-spin-button,
.filter-input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.filter-input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

.filter-input::placeholder {
  color: rgba(175, 120, 125, 0.6);
  font-family: 'Poppins', sans-serif;
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  border-color: rgba(162, 67, 78, 0.5);
  box-shadow: 
    inset 0 2px 8px rgba(0,0,0,0.5),
    0 0 0 3px rgba(162, 67, 78, 0.15),
    0 6px 20px rgba(152, 57, 68, 0.2);
  background: linear-gradient(135deg, 
    rgba(53, 45, 37, 0.98) 0%, 
    rgba(63, 53, 43, 0.98) 100%);
  transform: translateY(-1px);
}

.filters-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.filters-actions {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.btn-search,
.btn-reset {
  padding: 14px 28px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
}

.btn-search {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.9) 0%, 
    rgba(177, 79, 29, 0.9) 100%);
  color: #f8f4ed;
  flex: 1;
  font-weight: 700;
  box-shadow: 
    0 6px 20px rgba(152, 57, 68, 0.4),
    0 0 20px rgba(152, 57, 68, 0.25);
}

.btn-search::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.25),
    transparent
  );
  transition: left 0.6s ease;
}

.btn-search:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    rgba(162, 67, 78, 0.95) 0%, 
    rgba(187, 89, 39, 0.95) 100%);
  transform: translateY(-3px);
  box-shadow: 
    0 8px 25px rgba(152, 57, 68, 0.5),
    0 0 25px rgba(152, 57, 68, 0.3);
}

.btn-search:hover::before {
  left: 100%;
}

.btn-reset {
  background: linear-gradient(135deg, 
    rgba(66, 58, 50, 0.8) 0%, 
    rgba(84, 73, 61, 0.8) 100%);
  border: 2px solid rgba(152, 57, 68, 0.3);
  color: #d8a0a5;
  min-width: 140px;
  font-weight: 600;
}

.btn-reset:hover {
  border-color: rgba(162, 67, 78, 0.5);
  color: #f8f4ed;
  background: linear-gradient(135deg, 
    rgba(76, 66, 58, 0.9) 0%, 
    rgba(94, 81, 69, 0.9) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(152, 57, 68, 0.2);
}

/* SEARCH RESULTS */
.results-container {
  margin-top: 32px;
}

.results-header {
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 2px solid rgba(152, 57, 68, 0.25);
}

.results-header h3 {
  color: #f8f4ed;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 0 2px 6px rgba(0,0,0,0.4);
  font-family: 'Poppins', sans-serif;
}

.results-grid-container {
  margin-top: 20px;
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

.results-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.results-column .compact-item {
  flex: 1;
  min-height: 160px;
}

.result-item {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  gap: 28px;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid rgba(152, 57, 68, 0.2);
  box-shadow: 
    0 4px 20px rgba(0,0,0,0.3),
    0 0 15px rgba(152, 57, 68, 0.1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  backdrop-filter: blur(5px);
}

.result-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(152, 57, 68, 0.05),
    transparent
  );
  transition: left 0.8s ease;
}

.result-item:hover {
  background: linear-gradient(135deg, 
    rgba(53, 45, 37, 0.95) 0%, 
    rgba(42, 36, 30, 0.95) 100%);
  border-color: rgba(162, 67, 78, 0.4);
  transform: translateX(8px) translateY(-2px);
  box-shadow: 
    0 12px 35px rgba(0,0,0,0.4),
    0 0 25px rgba(152, 57, 68, 0.15);
}

.result-item:hover::before {
  left: 100%;
}

.compact-item {
  padding: 20px !important;
  gap: 20px !important;
  border-radius: 12px !important;
  align-items: flex-start !important;
  height: auto !important;
  min-height: 140px !important;
}

.compact-poster {
  flex-shrink: 0;
}

.compact-poster-img {
  width: 90px !important;
  height: 120px !important;
  font-size: 36px !important;
  border-radius: 8px !important;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.9) 0%, 
    rgba(74, 66, 55, 0.9) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(175, 120, 125, 0.4);
  box-shadow: 
    0 6px 20px rgba(0,0,0,0.4),
    inset 0 2px 4px rgba(255,255,255,0.1);
  transition: all 0.4s ease;
}

.compact-item:hover .compact-poster-img {
  border-color: rgba(175, 120, 125, 0.6);
  transform: scale(1.05);
  box-shadow: 
    0 8px 25px rgba(0,0,0,0.5),
    inset 0 2px 6px rgba(255,255,255,0.15);
}

.compact-content {
  min-width: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 120px;
}

.compact-header {
  margin-bottom: 8px !important;
  align-items: flex-start !important;
  gap: 12px;
}

.compact-title {
  font-size: 16px !important;
  font-weight: 700 !important;
  line-height: 1.3 !important;
  margin-bottom: 0 !important;
  flex: 1;
  color: #f8f4ed !important;
}

.compact-rating {
  padding: 6px 12px !important;
  font-size: 13px !important;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.9) 0%, 
    rgba(74, 66, 55, 0.9) 100%) !important;
  border-radius: 8px !important;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid rgba(175, 120, 125, 0.4);
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.compact-item:hover .compact-rating {
  background: linear-gradient(135deg, 
    rgba(103, 92, 77, 0.95) 0%, 
    rgba(84, 76, 65, 0.95) 100%);
  transform: scale(1.05);
}

.rating-star {
  font-size: 18px;
}

.rating-value {
  color: #f8f4ed;
  font-weight: 700;
  font-size: 16px;
  font-family: 'Poppins', sans-serif;
}

.compact-meta {
  margin-bottom: 8px !important;
  font-size: 12px !important;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  color: #b87c7c;
  font-family: 'Poppins', sans-serif;
}

.meta-item {
  color: #d8a0a5;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.meta-separator {
  color: rgba(175, 120, 125, 0.4);
}

.genre-tags {
  font-size: 11px !important;
  opacity: 0.9;
  color: #d8a0a5 !important;
}

.compact-overview {
  font-size: 13px !important;
  line-height: 1.4 !important;
  margin-bottom: 8px !important;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: #e8e0d0 !important;
  flex: 1;
}

.compact-footer {
  font-size: 11px !important;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #b87c7c !important;
}

.votes-count,
.popularity {
  color: #b87c7c;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.error-box {
  background: linear-gradient(135deg, 
    rgba(74, 61, 47, 0.9) 0%, 
    rgba(61, 51, 40, 0.9) 100%);
  border-left: 4px solid #d47c5c;
  color: #ffd8c8;
  padding: 18px 24px;
  border-radius: 10px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 
    0 4px 12px rgba(0,0,0,0.3),
    0 0 15px rgba(212, 124, 92, 0.2);
  font-family: 'Poppins', sans-serif;
}

.error-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(152, 57, 68, 0.15);
  border-top-color: #b87c7c;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: #b87c7c;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
}

.no-results {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.85) 0%, 
    rgba(31, 26, 20, 0.85) 100%);
  border-radius: 12px;
  border: 1px solid rgba(152, 57, 68, 0.15);
  box-shadow: 
    0 4px 12px rgba(0,0,0,0.3),
    0 0 10px rgba(152, 57, 68, 0.04);
}

.no-results-icon {
  font-size: 72px;
  margin-bottom: 24px;
  opacity: 0.4;
}

.no-results h3 {
  color: #f8f4ed;
  font-size: 26px;
  margin-bottom: 14px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  font-family: 'Poppins', sans-serif;
}

.no-results p {
  color: #b87c7c;
  font-size: 16px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
  font-family: 'Poppins', sans-serif;
}

.quick-search-prompt {
  text-align: center;
  padding: 80px 20px;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.85) 0%, 
    rgba(31, 26, 20, 0.85) 100%);
  border-radius: 12px;
  border: 1px solid rgba(152, 57, 68, 0.15);
  box-shadow: 
    0 4px 12px rgba(0,0,0,0.3),
    0 0 10px rgba(152, 57, 68, 0.04);
  margin-top: 32px;
}

.prompt-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.7;
}

.quick-search-prompt h3 {
  color: #f8f4ed;
  font-size: 24px;
  margin-bottom: 12px;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
}

.quick-search-prompt p {
  color: #b87c7c;
  font-size: 16px;
  font-family: 'Poppins', sans-serif;
}

/* Responsive */
@media (max-width: 1024px) {
  .results-grid {
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .search-section {
    padding-left: 20px;
    padding-right: 20px;
  }

  .filters-row {
    grid-template-columns: 1fr;
  }

  .results-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .results-column {
    gap: 12px;
  }
  
  .results-column .compact-item {
    min-height: 140px;
  }

  .compact-item {
    padding: 16px !important;
    min-height: 140px !important;
  }
  
  .compact-poster-img {
    width: 70px !important;
    height: 100px !important;
    font-size: 28px !important;
  }
  
  .compact-content {
    height: 100px;
  }
  
  .compact-overview {
    -webkit-line-clamp: 2;
    font-size: 12px !important;
  }
}

@media (max-width: 480px) {
  .compact-item {
    padding: 12px 16px !important;
    gap: 16px !important;
  }
  
  .compact-poster-img {
    width: 60px !important;
    height: 80px !important;
    font-size: 24px !important;
  }
  
  .compact-title {
    font-size: 14px !important;
  }
  
  .compact-overview {
    -webkit-line-clamp: 2;
  }
}
</style>