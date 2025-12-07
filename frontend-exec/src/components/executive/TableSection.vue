<template>
  <section class="table-box">
    <h2 class="table-title">Executive Data Table</h2>

    <!-- DROPDOWN PILIHAN TABEL -->
    <div class="controls">
      <div class="control-group">
        <label>Pilih Jenis Tabel:</label>
        <select v-model="selectedType" @change="fetchTableData" class="select-input">
          <option value="overview">Overview</option>
          <option value="genres">Genre Distribution</option>
          <option value="languages">Language Distribution</option>
          <option value="production">Production Companies</option>
          <option value="networks">Networks / Platforms</option>
          <option value="performance">Content Performance</option>
        </select>
      </div>

      <!-- 🔍 SEARCH ENGINE -->
      <div class="search-group">
        <input 
          type="text" 
          placeholder="Search..." 
          v-model="keyword" 
          @input="handleSearch"
          class="search-box"
        />
        <span class="search-icon">🔍</span>
      </div>
    </div>

    <!-- LOADING -->
    <p v-if="loading" class="status-message">Loading data...</p>

    <!-- ERROR -->
    <p v-if="error" class="error-message">{{ error }}</p>

    <!-- TABEL DINAMIS -->
    <div v-if="rows.length > 0" class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="col in columns" :key="col">
              {{ col }}
            </th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(row, index) in paginatedData" :key="index">
            <td v-for="col in columns" :key="col">
              {{ row[col] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- PAGINATION -->
    <div v-if="rows.length > 0" class="pagination">
      <button class="pagination-btn" :disabled="page === 1" @click="page--">
        ← Prev
      </button>
      <span class="page-info">Page {{ page }} / {{ totalPages }}</span>
      <button class="pagination-btn" :disabled="page === totalPages" @click="page++">
        Next →
      </button>
    </div>

    <!-- NO DATA -->
    <p v-if="!loading && rows.length === 0" class="no-data">Tidak ada data tersedia.</p>
  </section>
</template>

<script>
import { getExecutiveTable, searchExecutiveTable } from "../../utils/api";

export default {
  name: "TableSection",

  data() {
    return {
      selectedType: "overview",
      keyword: "",
      columns: [],
      rows: [],
      loading: false,
      error: null,
      page: 1,
      pageSize: 20,
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.rows.length / this.pageSize);
    },

    paginatedData() {
      const start = (this.page - 1) * this.pageSize;
      return this.rows.slice(start, start + this.pageSize);
    },
  },

  methods: {
    async fetchTableData() {
      this.loading = true;
      this.error = null;
      this.rows = [];
      this.columns = [];
      this.page = 1;

      try {
        const res = await getExecutiveTable(this.selectedType);

        if (!res.success) {
          this.error = "Gagal mengambil data tabel.";
          return;
        }

        this.columns = res.columns;
        this.rows = res.rows;

      } catch (err) {
        this.error = "Terjadi kesalahan saat mengambil data.";
      } finally {
        this.loading = false;
      }
    },

    async handleSearch() {
      if (this.keyword.trim() === "") {
        return this.fetchTableData();
      }

      this.loading = true;

      try {
        const res = await searchExecutiveTable(this.selectedType, this.keyword);

        if (res.success) {
          this.columns = res.columns;
          this.rows = res.rows;
          this.page = 1;
        }

      } catch (err) {
        console.log("Search error:", err);
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    this.fetchTableData();
  },
};
</script>

<style scoped>
.table-box {
  padding: 24px;
  background: linear-gradient(135deg, #2d2424 0%, #3a2d2d 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.table-title {
  color: #e8b4d4;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  text-align: left;
}

/* Controls */
.controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.control-group label {
  color: #c9a8a8;
  font-size: 14px;
  font-weight: 500;
}

.select-input {
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #5a4444;
  background: rgba(93, 70, 70, 0.5);
  color: #e8b4d4;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
}

.select-input:hover {
  border-color: #e8b4d4;
  background: rgba(93, 70, 70, 0.7);
}

.select-input:focus {
  outline: none;
  border-color: #e8b4d4;
  box-shadow: 0 0 0 3px rgba(232, 180, 212, 0.1);
}

.search-group {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box {
  padding: 10px 40px 10px 16px;
  border-radius: 8px;
  border: 1px solid #5a4444;
  background: rgba(93, 70, 70, 0.5);
  color: #e8b4d4;
  font-size: 14px;
  width: 250px;
  transition: all 0.3s ease;
}

.search-box::placeholder {
  color: #8a7070;
}

.search-box:focus {
  outline: none;
  border-color: #e8b4d4;
  background: rgba(93, 70, 70, 0.7);
  box-shadow: 0 0 0 3px rgba(232, 180, 212, 0.1);
}

.search-icon {
  position: absolute;
  right: 12px;
  font-size: 16px;
  pointer-events: none;
  opacity: 0.6;
}

/* Table Container */
.table-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

/* Table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 247, 230, 0.05);
}

.data-table th,
.data-table td {
  border: 1px solid rgba(90, 68, 68, 0.3);
  padding: 14px 16px;
  text-align: left;
  font-size: 14px;
}

.data-table th {
  background: linear-gradient(135deg, #5d4646 0%, #6d5252 100%);
  color: #e8b4d4;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.data-table tbody tr {
  background: rgba(61, 46, 46, 0.4);
  transition: all 0.2s ease;
}

.data-table tbody tr:nth-child(even) {
  background: rgba(51, 38, 38, 0.4);
}

.data-table tbody tr:hover {
  background: rgba(93, 70, 70, 0.6);
  transform: translateY(-1px);
}

.data-table td {
  color: #c9a8a8;
}

/* Pagination */
.pagination {
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.pagination-btn {
  padding: 10px 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #5d4646 0%, #6d5252 100%);
  border: 1px solid #7a5a5a;
  color: #e8b4d4;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #6d5252 0%, #7d6060 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.pagination-btn:active:not(:disabled) {
  transform: translateY(0);
}

.pagination-btn:disabled {
  background: rgba(61, 46, 46, 0.5);
  border-color: #4a3838;
  color: #6a5555;
  cursor: not-allowed;
  opacity: 0.5;
}

.page-info {
  color: #c9a8a8;
  font-size: 14px;
  font-weight: 500;
  padding: 0 8px;
}

/* Status Messages */
.status-message,
.no-data {
  color: #c9a8a8;
  text-align: center;
  padding: 40px 20px;
  font-size: 15px;
}

.error-message {
  color: #ff8a8a;
  font-weight: 600;
  text-align: center;
  padding: 20px;
  background: rgba(255, 68, 68, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(255, 68, 68, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .controls {
    flex-direction: column;
    align-items: stretch;
  }

  .control-group {
    flex-direction: column;
    align-items: stretch;
  }

  .select-input,
  .search-box {
    width: 100%;
  }

  .data-table th,
  .data-table td {
    padding: 10px 12px;
    font-size: 13px;
  }
}
</style>