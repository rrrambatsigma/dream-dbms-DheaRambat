<template>
  <header class="header-nav">
    <div class="nav-container">
      <div class="nav-left">
        <a href="#" class="logo">
          <span class="logo-im">DREAM</span>
        </a>
        <nav class="nav-menu">
          <a 
            v-for="tab in tabs" 
            :key="tab.id"
            href="#" 
            class="nav-link" 
            :class="{ active: activeTab === tab.id }"
            @click.prevent="$emit('tab-change', tab.id)"
          >
            {{ tab.name }}
          </a>
        </nav>
      </div>
      
      <div class="nav-search-about">
        <div class="nav-search-bar">
          <input 
            v-model="quickSearch" 
            @keyup.enter="performQuickSearch"
            type="text" 
            placeholder="Search"
          />
          <span class="search-icon">🔍</span>
        </div>
        <!-- Tombol About pindah ke halaman About -->
        <button 
          class="nav-btn" 
          @click="$emit('tab-change', 'about')"
          :class="{ active: activeTab === 'about' }"
        >
          About
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderNavigation',
  props: {
    activeTab: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      quickSearch: '',
      tabs: [
        { id: 'home', name: 'Home' },
        { id: 'movies', name: 'Movies' }
        // HAPUS TAB ABOUT DARI SINI
      ]
    }
  },
  methods: {
    performQuickSearch() {
      const kw = this.quickSearch && this.quickSearch.trim()
      if (!kw) return
      this.$emit('quick-search', kw)
      window.dispatchEvent(new CustomEvent('quick-search', { detail: kw }))
    }
  }
}
</script>

<style scoped>
/* TAMBAHKAN INI UNTUK TOMBOL ABOUT AKTIF */
.nav-btn.active {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.3) 0%, 
    rgba(177, 79, 29, 0.3) 100%);
  border-color: rgba(152, 57, 68, 0.8);
  color: #f8f4ed;
  box-shadow: 
    0 4px 15px rgba(152, 57, 68, 0.4),
    0 0 15px rgba(152, 57, 68, 0.3);
}

/* CSS LAINNYA TETAP SAMA SEPERTI DI ATAS */
.header-nav {
  background: 
    linear-gradient(135deg, 
      rgba(20, 16, 12, 0.98) 0%, 
      rgba(28, 23, 18, 0.98) 100%);
  border-bottom: 1px solid rgba(152, 57, 68, 0.35);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 
    0 6px 25px rgba(0,0,0,0.9),
    0 0 25px rgba(152, 57, 68, 0.2);
  backdrop-filter: blur(20px);
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  height: 64px;
  position: relative;
  z-index: 1;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 48px;
}

.logo {
  background: 
    linear-gradient(135deg, 
      rgba(152, 57, 68, 0.9) 0%, 
      rgba(177, 79, 29, 0.9) 50%,
      rgba(120, 45, 48, 0.8) 100%);
  color: #f8f4ed;
  font-weight: 800;
  font-size: 20px;
  padding: 8px 18px;
  border-radius: 8px;
  letter-spacing: 1.2px;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  cursor: pointer;
  box-shadow: 
    0 4px 15px rgba(152, 57, 68, 0.5),
    0 0 20px rgba(152, 57, 68, 0.3),
    inset 0 1px 0 rgba(255,255,255,0.2);
  position: relative;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  text-decoration: none;
}

.logo::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.6s ease;
}

.logo:hover::before {
  left: 100%;
}

.logo:hover {
  background: linear-gradient(135deg, 
    rgba(162, 67, 78, 0.95) 0%, 
    rgba(187, 89, 39, 0.95) 50%,
    rgba(130, 55, 58, 0.85) 100%);
  box-shadow: 
    0 6px 20px rgba(152, 57, 68, 0.6),
    0 0 25px rgba(152, 57, 68, 0.4),
    inset 0 1px 0 rgba(255,255,255,0.3);
  transform: translateY(-2px) scale(1.02);
}

.nav-menu {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #d8a0a5;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 8px 0;
  font-family: 'Poppins', sans-serif;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #983944, #b13f1d);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-link:hover,
.nav-link.active {
  color: #f8f4ed;
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.nav-search-about {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  max-width: 500px;
  justify-content: flex-end;
  margin-left: auto;
}

.nav-search-bar {
  flex: 1;
  max-width: 380px;
  min-width: 280px;
  position: relative;
}

.nav-search-bar input {
  width: 100%;
  padding: 12px 45px 12px 18px;
  background: 
    linear-gradient(135deg, 
      rgba(42, 36, 30, 0.95) 0%, 
      rgba(53, 45, 37, 0.95) 100%);
  border: 1px solid rgba(152, 57, 68, 0.4);
  border-radius: 10px;
  color: #f5f1e8;
  font-size: 14px;
  transition: all 0.4s ease;
  box-shadow: 
    inset 0 2px 6px rgba(0,0,0,0.4),
    0 4px 12px rgba(152, 57, 68, 0.15);
  font-family: 'Poppins', sans-serif;
}

.nav-search-bar input:focus {
  outline: none;
  border-color: rgba(162, 67, 78, 0.6);
  box-shadow: 
    inset 0 2px 8px rgba(0,0,0,0.5),
    0 0 0 3px rgba(162, 67, 78, 0.2),
    0 8px 20px rgba(152, 57, 68, 0.25);
  background: linear-gradient(135deg, 
    rgba(53, 45, 37, 0.98) 0%, 
    rgba(63, 53, 43, 0.98) 100%);
  transform: translateY(-1px);
}

.nav-search-bar input::placeholder {
  color: rgba(175, 120, 125, 0.7);
  font-family: 'Poppins', sans-serif;
}

.search-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 16px;
  cursor: pointer;
  color: #b87c7c;
  transition: all 0.3s ease;
}

.nav-search-bar:hover .search-icon {
  color: #d8a0a5;
  transform: translateY(-50%) scale(1.1);
}

.nav-btn {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.15) 0%, 
    rgba(177, 79, 29, 0.15) 100%);
  border: 1px solid rgba(152, 57, 68, 0.4);
  color: #d8a0a5;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.4s ease;
  font-family: 'Poppins', sans-serif;
  white-space: nowrap;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.nav-btn:hover {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.25) 0%, 
    rgba(177, 79, 29, 0.25) 100%);
  border-color: rgba(162, 67, 78, 0.6);
  color: #f8f4ed;
  box-shadow: 
    0 4px 15px rgba(152, 57, 68, 0.3),
    0 0 15px rgba(152, 57, 68, 0.2);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 20px;
    flex-wrap: wrap;
    height: auto;
    padding-top: 12px;
    padding-bottom: 12px;
  }

  .nav-left {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .nav-menu {
    gap: 16px;
  }

  .nav-search-bar {
    max-width: 100%;
    order: 3;
  }

  .nav-search-about {
    order: 2;
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .nav-menu {
    gap: 12px;
  }

  .nav-link {
    font-size: 13px;
  }

  .nav-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>