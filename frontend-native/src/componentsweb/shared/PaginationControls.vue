<template>
  <div class="pagination-container">
    <div class="pagination-controls">
      <button 
        @click="$emit('page-change', pagination.current_page - 1)" 
        :disabled="pagination.current_page === 1"
        class="pagination-btn"
      >
        ← Previous
      </button>
      
      <div class="page-numbers">
        <span 
          v-for="page in visiblePages" 
          :key="page"
          @click="$emit('page-change', page)"
          :class="{
            'page-number': true,
            'active': page === pagination.current_page,
            'ellipsis': page === '...'
          }"
        >
          {{ page }}
        </span>
      </div>
      
      <button 
        @click="$emit('page-change', pagination.current_page + 1)" 
        :disabled="pagination.current_page === pagination.total_pages"
        class="pagination-btn"
      >
        Next →
      </button>
    </div>
    
    <div class="pagination-info">
      <span>Showing {{ (pagination.current_page - 1) * pagination.page_size + 1 }}-{{ Math.min(pagination.current_page * pagination.page_size, pagination.total_rows) }} of {{ pagination.total_rows }} results</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaginationControls',
  props: {
    pagination: {
      type: Object,
      required: true
    },
    visiblePages: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.pagination-container {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid rgba(152, 57, 68, 0.2);
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.pagination-btn {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.9) 0%, 
    rgba(31, 26, 20, 0.9) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  color: #d8a0a5;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
  font-weight: 500;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    rgba(53, 45, 37, 0.95) 0%, 
    rgba(42, 36, 30, 0.95) 100%);
  border-color: rgba(162, 67, 78, 0.5);
  color: #f8f4ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(152, 57, 68, 0.2);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.page-numbers {
  display: flex;
  gap: 6px;
  align-items: center;
}

.page-number {
  padding: 8px 14px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
  min-width: 40px;
  text-align: center;
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.7) 0%, 
    rgba(31, 26, 20, 0.7) 100%);
  border: 1px solid rgba(152, 57, 68, 0.2);
  color: #d8a0a5;
}

.page-number:hover:not(.active):not(.ellipsis) {
  background: linear-gradient(135deg, 
    rgba(53, 45, 37, 0.8) 0%, 
    rgba(42, 36, 30, 0.8) 100%);
  border-color: rgba(162, 67, 78, 0.4);
  color: #f8f4ed;
}

.page-number.active {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.8) 0%, 
    rgba(177, 79, 29, 0.8) 100%);
  border-color: rgba(162, 67, 78, 0.6);
  color: #f8f4ed;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(152, 57, 68, 0.3);
}

.page-number.ellipsis {
  background: transparent;
  border: none;
  cursor: default;
  color: #b87c7c;
}

.pagination-info {
  text-align: center;
  color: #b87c7c;
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
}

/* Responsive Pagination */
@media (max-width: 768px) {
  .pagination-controls {
    gap: 8px;
  }
  
  .pagination-btn {
    padding: 8px 14px;
    font-size: 13px;
  }
  
  .page-number {
    padding: 6px 10px;
    min-width: 36px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .pagination-controls {
    flex-direction: column;
    gap: 12px;
  }
  
  .page-numbers {
    order: -1;
  }
}
</style>