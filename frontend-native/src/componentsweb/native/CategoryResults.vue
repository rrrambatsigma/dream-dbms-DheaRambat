<template>
  <div class="category-results">
    <div class="category-results-header">
      <h2 class="results-title">
        {{ categoryName }} Shows
        <span class="results-count">({{ pagination.total_rows }} results)</span>
      </h2>
      
      <!-- Sort Controls -->
      <div class="sort-controls">
        <select v-model="sortBy" class="sort-select" @change="handleSortChange">
          <option value="popularity">Popularity</option>
          <option value="rating">Rating</option>
          <option value="name">Name</option>
        </select>
        <select v-model="sortOrder" class="sort-select" @change="handleSortChange">
          <option value="DESC">High to Low</option>
          <option value="ASC">Low to High</option>
        </select>
      </div>
    </div>

    <!-- Category Shows Grid -->
    <div class="category-shows-grid">
      <div
        v-for="show in shows"
        :key="show.ShowID"
        class="category-show-card"
        @click="$emit('show-detail', show.ShowID)"
      >
        <div class="show-poster">
          <span class="poster-icon">📺</span>
        </div>
        <div class="show-info">
          <h3 class="show-title">{{ show.Name }}</h3>
          <div class="show-rating">
            <span class="star">⭐</span>
            <span class="rating">{{ show.VoteAverage || 'N/A' }}</span>
          </div>
          <p class="show-genres">{{ show.Genres || 'No genre' }}</p>
          <p class="show-overview">{{ truncate(show.Overview, 80) }}</p>
        </div>
      </div>
    </div>

    <!-- ✅ MODERN PAGINATION - GANTI YANG INI -->
    <div v-if="pagination.total_pages > 1" class="modern-pagination">
      <div class="pagination-info">
        Page {{ pagination.current_page }} of {{ pagination.total_pages }} • 
        Showing {{ getStartIndex() }}-{{ getEndIndex() }} of {{ pagination.total_rows }} results
      </div>
      
      <div class="pagination-controls">
        <button 
          @click="$emit('page-change', pagination.current_page - 1)"
          :disabled="pagination.current_page === 1"
          class="pagination-btn prev-btn"
        >
          ‹ Previous
        </button>
        
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="$emit('page-change', page)"
            :class="{
              'page-btn': true,
              'active': pagination.current_page === page,
              'ellipsis': page === '...'
            }"
            :disabled="page === '...'"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          @click="$emit('page-change', pagination.current_page + 1)"
          :disabled="pagination.current_page === pagination.total_pages"
          class="pagination-btn next-btn"
        >
          Next ›
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryResults',
  props: {
    shows: {
      type: Array,
      required: true
    },
    pagination: {
      type: Object,
      required: true
    },
    categoryName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      sortBy: 'popularity',
      sortOrder: 'DESC'
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
    }
  },
  methods: {
    truncate(text, length = 80) {
      if (!text) return 'No description available';
      if (text.length <= length) return text;
      return text.substring(0, length) + '...';
    },
    handleSortChange() {
      this.$emit('sort-change', {
        sortBy: this.sortBy,
        sortOrder: this.sortOrder
      })
    },
    // ✅ TAMBAHKAN METHOD INI
    getStartIndex() {
      return ((this.pagination.current_page - 1) * this.pagination.page_size) + 1;
    },
    getEndIndex() {
      const end = this.pagination.current_page * this.pagination.page_size;
      return end > this.pagination.total_rows ? this.pagination.total_rows : end;
    }
  }
}
</script>

<style scoped>
.category-results {
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid rgba(152, 57, 68, 0.2);
}

.category-results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.results-title {
  font-size: 24px;
  font-weight: 600;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
}

.results-count {
  font-size: 16px;
  color: #b87c7c;
  font-weight: 400;
}

.sort-controls {
  display: flex;
  gap: 12px;
}

.sort-select {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.95) 0%, 
    rgba(53, 45, 37, 0.95) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 8px;
  padding: 10px 16px;
  color: #f8f4ed;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
  cursor: pointer;
}

/* Category Shows Grid */
.category-shows-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.category-show-card {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border: 1px solid rgba(152, 57, 68, 0.2);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
}

.category-show-card:hover {
  border-color: rgba(162, 67, 78, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(152, 57, 68, 0.15);
}

.show-poster {
  width: 100px;
  height: 140px;
  background: linear-gradient(135deg, 
    rgba(93, 82, 67, 0.8) 0%, 
    rgba(74, 66, 55, 0.8) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  flex-shrink: 0;
}

.show-info {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.show-title {
  font-size: 16px;
  font-weight: 600;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
  line-height: 1.3;
}

.show-rating {
  display: flex;
  align-items: center;
  gap: 6px;
}

.show-rating .star {
  font-size: 14px;
}

.show-rating .rating {
  font-size: 14px;
  color: #f8f4ed;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
}

.show-genres {
  font-size: 12px;
  color: #d8a0a5;
  font-family: 'Poppins', sans-serif;
}

.show-overview {
  font-size: 12px;
  color: #b87c7c;
  line-height: 1.4;
  font-family: 'Poppins', sans-serif;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ✅ MODERN PAGINATION STYLES */
.modern-pagination {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid rgba(152, 57, 68, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.pagination-info {
  color: #b87c7c;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.pagination-btn {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 8px;
  padding: 12px 20px;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 100px;
}

.pagination-btn:hover:not(:disabled) {
  border-color: rgba(162, 67, 78, 0.6);
  background: rgba(152, 57, 68, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(152, 57, 68, 0.2);
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.page-numbers {
  display: flex;
  gap: 8px;
}

.page-btn {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 8px;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f8f4ed;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled):not(.ellipsis) {
  border-color: rgba(162, 67, 78, 0.6);
  background: rgba(152, 57, 68, 0.15);
  transform: translateY(-1px);
}

.page-btn.active {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.4) 0%, 
    rgba(177, 79, 29, 0.4) 100%);
  border-color: rgba(162, 67, 78, 0.8);
  color: #f8f4ed;
  font-weight: 600;
  transform: scale(1.05);
}

.page-btn.ellipsis {
  background: transparent;
  border: none;
  cursor: default;
  width: 30px;
}

.page-btn.ellipsis:hover {
  background: transparent;
  border: none;
  transform: none;
}

/* Responsive */
@media (max-width: 768px) {
  .category-results-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .category-shows-grid {
    grid-template-columns: 1fr;
  }
  
  .category-show-card {
    flex-direction: column;
  }
  
  .show-poster {
    width: 100%;
    height: 200px;
  }
  
  /* Responsive Pagination */
  .pagination-controls {
    flex-direction: column;
    gap: 12px;
  }
  
  .page-numbers {
    order: -1;
  }
  
  .pagination-btn {
    min-width: 80px;
    padding: 10px 16px;
    font-size: 13px;
  }
  
  .page-btn {
    width: 38px;
    height: 38px;
    font-size: 13px;
  }
  
  .pagination-info {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .page-numbers {
    gap: 4px;
  }
  
  .page-btn {
    width: 35px;
    height: 35px;
    font-size: 12px;
  }
  
  .pagination-btn {
    min-width: 70px;
    padding: 8px 12px;
    font-size: 12px;
  }
}
</style>