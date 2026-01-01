<!-- src/components/marketing/SimpleYearRangeSelector.vue -->
<template>
  <div class="simple-year-selector">
    <div class="selector-card">
      <div class="selector-header">
        <span class="header-icon">📅</span>
        <h3>Filter by Year Range</h3>
      </div>
      
      <div class="range-inputs">
        <div class="input-group">
          <label for="startYear">Start Year</label>
          <select id="startYear" v-model="localStartYear" @change="onRangeChange">
            <option v-for="year in availableYears" :key="'start-' + year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        
        <div class="range-divider">
          <span>to</span>
        </div>
        
        <div class="input-group">
          <label for="endYear">End Year</label>
          <select id="endYear" v-model="localEndYear" @change="onRangeChange">
            <option v-for="year in availableYears" :key="'end-' + year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        
        <button class="apply-btn" @click="applyRange" :disabled="!hasChanged">
          {{ isApplying ? 'Applying...' : 'Apply' }}
        </button>
      </div>
      
      <div class="current-range">
        <span class="range-label">Current Range:</span>
        <span class="range-display">{{ currentDisplay }}</span>
        <span class="year-count">{{ yearSpan }} years</span>
      </div>
      
      <div class="quick-actions">
        <button 
          v-for="action in quickActions" 
          :key="action.label"
          @click="applyQuickAction(action)"
          class="quick-btn"
        >
          {{ action.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SimpleYearRangeSelector",
  emits: ['year-range-changed'],
  
  data() {
    return {
      localStartYear: 2000,
      localEndYear: 2024,
      availableYears: [],
      hasChanged: false,
      isApplying: false,
      loadingYears: false
    };
  },
  
  computed: {
    currentDisplay() {
      return `${this.localStartYear} - ${this.localEndYear}`;
    },
    
    yearSpan() {
      return Math.abs(this.localEndYear - this.localStartYear) + 1;
    },
    
    quickActions() {
      const currentYear = new Date().getFullYear();
      return [
        { label: 'Last 5 Years', start: currentYear - 4, end: currentYear },
        { label: 'Last 10 Years', start: currentYear - 9, end: currentYear },
        { label: '2000-2010', start: 2000, end: 2010 },
        { label: '2010-2020', start: 2010, end: 2020 },
        { label: 'All Years', start: null, end: null }
      ];
    }
  },
  
  async mounted() {
    await this.fetchAvailableYears();
    // Set default dari localStorage jika ada
    this.loadSavedRange();
  },
  
  methods: {
    async fetchAvailableYears() {
      try {
        this.loadingYears = true;
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:5000/api/marketing/available-years', {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.success && result.data && result.data.length > 0) {
            this.availableYears = result.data.sort((a, b) => a - b);
            
            // Set default values
            if (this.availableYears.length > 0) {
              this.localStartYear = this.availableYears[0];
              this.localEndYear = this.availableYears[this.availableYears.length - 1];
            }
          }
        }
      } catch (error) {
        console.error('Error fetching years:', error);
        // Fallback: generate tahun 1900-2025
        this.availableYears = Array.from({length: 126}, (_, i) => 1900 + i);
      } finally {
        this.loadingYears = false;
      }
    },
    
    onRangeChange() {
      // Validasi: startYear tidak boleh lebih besar dari endYear
      if (this.localStartYear > this.localEndYear) {
        [this.localStartYear, this.localEndYear] = [this.localEndYear, this.localStartYear];
      }
      this.hasChanged = true;
    },
    
    applyQuickAction(action) {
      if (action.start === null || action.end === null) {
        // "All Years"
        this.localStartYear = this.availableYears[0];
        this.localEndYear = this.availableYears[this.availableYears.length - 1];
      } else {
        this.localStartYear = action.start;
        this.localEndYear = action.end;
      }
      this.hasChanged = true;
      this.applyRange();
    },
    
    async applyRange() {
      if (!this.hasChanged) return;
      
      this.isApplying = true;
      
      // Simpan ke localStorage
      this.saveRange();
      
      // Emit ke parent
      this.$emit('year-range-changed', {
        startYear: this.localStartYear,
        endYear: this.localEndYear,
        yearSpan: this.yearSpan
      });
      
      // Reset status
      setTimeout(() => {
        this.hasChanged = false;
        this.isApplying = false;
      }, 500);
    },
    
    saveRange() {
      localStorage.setItem('marketing_year_range', JSON.stringify({
        startYear: this.localStartYear,
        endYear: this.localEndYear,
        savedAt: new Date().getTime()
      }));
    },
    
    loadSavedRange() {
      try {
        const saved = localStorage.getItem('marketing_year_range');
        if (saved) {
          const { startYear, endYear } = JSON.parse(saved);
          if (this.availableYears.includes(startYear) && this.availableYears.includes(endYear)) {
            this.localStartYear = startYear;
            this.localEndYear = endYear;
            this.hasChanged = false;
          }
        }
      } catch (error) {
        console.warn('Could not load saved range:', error);
      }
    },
    
    getDefaultRange() {
      return {
        startYear: this.availableYears[0] || 1900,
        endYear: this.availableYears[this.availableYears.length - 1] || 2025,
        yearSpan: (this.availableYears[this.availableYears.length - 1] || 2025) - (this.availableYears[0] || 1900) + 1
      };
    }
  }
};
</script>

<style scoped>
.simple-year-selector {
  margin-bottom: 25px;
}

.selector-card {
  background: linear-gradient(145deg, 
    rgba(50, 42, 36, 0.95) 0%,
    rgba(38, 32, 26, 0.95) 50%,
    rgba(50, 42, 36, 0.95) 100%);
  border: 2px solid rgba(216, 160, 165, 0.2);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.selector-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(216, 160, 165, 0.15);
}

.header-icon {
  font-size: 1.5rem;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: linear-gradient(135deg, #FF6B9D, #BA68C8);
  color: white;
  box-shadow: 0 4px 12px rgba(255, 107, 157, 0.3);
}

.selector-header h3 {
  margin: 0;
  color: #FFD1DC;
  font-size: 1.2rem;
  font-weight: 700;
}

.range-inputs {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.input-group {
  flex: 1;
  min-width: 150px;
}

.input-group label {
  display: block;
  color: #FFB6C1;
  font-size: 0.85rem;
  margin-bottom: 6px;
  font-weight: 600;
}

.input-group select {
  width: 100%;
  padding: 10px 15px;
  border-radius: 10px;
  border: 2px solid rgba(216, 160, 165, 0.3);
  background: rgba(30, 25, 20, 0.9);
  color: #FFD1DC;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.input-group select:focus {
  outline: none;
  border-color: #FF6B9D;
  box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2);
}

.range-divider {
  display: flex;
  align-items: center;
  height: 40px;
  color: #BA68C8;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0 5px;
}

.apply-btn {
  background: linear-gradient(135deg, #FF6B9D, #EC407A);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 25px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 42px;
  white-space: nowrap;
}

.apply-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.apply-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 107, 157, 0.4);
}

.current-range {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding: 12px 15px;
  background: rgba(216, 160, 165, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(216, 160, 165, 0.2);
}

.range-label {
  color: #FFB6C1;
  font-size: 0.85rem;
  font-weight: 600;
}

.range-display {
  color: #FFD1DC;
  font-size: 1.1rem;
  font-weight: 700;
  flex: 1;
}

.year-count {
  background: rgba(77, 182, 172, 0.15);
  color: #4DB6AC;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid rgba(77, 182, 172, 0.3);
}

.quick-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.quick-btn {
  background: rgba(216, 160, 165, 0.1);
  color: #FFB6C1;
  border: 1px solid rgba(216, 160, 165, 0.2);
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.quick-btn:hover {
  background: rgba(255, 107, 157, 0.15);
  color: #FFD1DC;
  border-color: #FF6B9D;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .range-inputs {
    flex-direction: column;
    align-items: stretch;
  }
  
  .input-group {
    min-width: auto;
  }
  
  .range-divider {
    justify-content: center;
    height: auto;
    padding: 10px 0;
  }
  
  .apply-btn {
    width: 100%;
    margin-top: 10px;
  }
  
  .current-range {
    flex-wrap: wrap;
  }
  
  .quick-actions {
    justify-content: center;
  }
}
</style>