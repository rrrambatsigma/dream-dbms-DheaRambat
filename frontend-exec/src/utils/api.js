import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
});

// Inject token before every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ======================================================
// 1. EXECUTIVE KPI CARDS
// ======================================================
export const getExecutiveKPI = async () => {
  try {
    const res = await api.get("/api/executive/kpi");
    return res.data;
  } catch (err) {
    console.error("Error fetching Executive KPI:", err);
    throw err;
  }
};

// ======================================================
// 2. EXECUTIVE TABLE DATA
// ======================================================
export const getExecutiveTable = async (tableType) => {
  try {
    const res = await api.get("/api/executive/table", {
      params: { type: tableType },
    });
    return res.data;
  } catch (err) {
    console.error(`Error fetching Executive Table (${tableType}):`, err);
    throw err;
  }
};

// ======================================================
// 3. EXECUTIVE TABLE SEARCH
// ======================================================
export const searchExecutiveTable = async (tableType, keyword) => {
  try {
    const res = await api.get("/api/executive/table/search", {
      params: { type: tableType, keyword },
    });
    return res.data;
  } catch (err) {
    console.error(`Error searching Executive Table:`, err);
    throw err;
  }
};

// ======================================================
// 4. EXECUTIVE BAR CHART (Top 15)
// ======================================================
export const getExecutiveChart = async (chartType) => {
  try {
    const res = await api.get("/api/executive/chart", {
      params: { type: chartType },
    });
    return res.data;
  } catch (err) {
    console.error(`Error fetching Executive Chart (${chartType}):`, err);
    throw err;
  }
};

// ======================================================
// 5. EXECUTIVE PIE / DONUT CHART
// ======================================================
export const getExecutivePieChart = async (chartType) => {
  try {
    const res = await api.get("/api/executive/chart/pie", {
      params: { type: chartType },
    });
    return res.data;
  } catch (err) {
    console.error(`Error fetching Executive Pie Chart (${chartType}):`, err);
    throw err;
  }
};

// ======================================================
// 6. EXECUTIVE STACKED BAR CHARTS
// ======================================================
export const getStackedCountriesChart = async () => {
  try {
    const res = await api.get("/api/executive/stacked/countries");
    return res.data;
  } catch (err) {
    console.error("Error fetching Stacked Countries Chart:", err);
    throw err;
  }
};

export const getStackedStatusChart = async () => {
  try {
    const res = await api.get("/api/executive/stacked/status");
    return res.data;
  } catch (err) {
    console.error("Error fetching Stacked Status Chart:", err);
    throw err;
  }
};

export const getStackedGenresChart = async () => {
  try {
    const res = await api.get("/api/executive/stacked/genres");
    return res.data;
  } catch (err) {
    console.error("Error fetching Stacked Genres Chart:", err);
    throw err;
  }
};

export const getUniversalStackedChart = async (chartType, sortBy = "total", topN = 10) => {
  try {
    const res = await api.get("/api/executive/stacked/universal", {
      params: { 
        type: chartType,
        sort: sortBy,
        top: topN
      },
    });
    return res.data;
  } catch (err) {
    console.error(`Error fetching Universal Stacked Chart (${chartType}):`, err);
    throw err;
  }
};

// ======================================================
// 7. WORLD MAP DATA - REVISI SESUAI BACKEND BARU (SIMPLE VERSION)
// ======================================================

// 7.1 Get All World Map Data
export const getWorldMapData = async () => {
  try {
    const res = await api.get("/api/executive/map");
    return res.data;
  } catch (err) {
    console.error("Error fetching World Map Data:", err);
    throw err;
  }
};

// 7.2 Get Single Country Details
export const getCountryMapDetails = async (countryName) => {
  try {
    const res = await api.get(`/api/executive/map/${encodeURIComponent(countryName)}`);
    return res.data;
  } catch (err) {
    console.error(`Error fetching Country Details for ${countryName}:`, err);
    throw err;
  }
};

// 7.3 Get Country List (for dropdown)
export const getCountryList = async () => {
  try {
    const res = await api.get("/api/executive/map/countries");
    return res.data;
  } catch (err) {
    console.error("Error fetching Country List:", err);
    throw err;
  }
};

// 7.4 Get Map Statistics
export const getMapStatistics = async () => {
  try {
    const res = await api.get("/api/executive/map/stats");
    return res.data;
  } catch (err) {
    console.error("Error fetching Map Statistics:", err);
    throw err;
  }
};

// ======================================================
// 8. TEST & UTILITY
// ======================================================

// 8.1 Test Map Endpoint
export const testMapEndpoint = async () => {
  try {
    const res = await api.get("/api/executive/test/map");
    return res.data;
  } catch (err) {
    console.error("Error testing Map Endpoint:", err);
    throw err;
  }
};

// 8.2 Test All Endpoints
export const testAllEndpoints = async () => {
  try {
    const res = await api.get("/api/executive/test/all");
    return res.data;
  } catch (err) {
    console.error("Error testing All Endpoints:", err);
    throw err;
  }
};

// 8.3 Get Available Endpoints
export const getExecutiveEndpoints = async () => {
  try {
    const res = await api.get("/api/executive/endpoints");
    return res.data;
  } catch (err) {
    console.error("Error fetching Executive Endpoints:", err);
    throw err;
  }
};

// 8.4 Health Check
export const checkExecutiveHealth = async () => {
  try {
    const res = await api.get("/api/executive/health");
    return res.data;
  } catch (err) {
    console.error("Error checking Executive Health:", err);
    throw err;
  }
};

// ======================================================
// 9. BATCH REQUESTS
// ======================================================

// 9.1 Get All Stacked Charts
export const getAllStackedCharts = async () => {
  try {
    const [countries, status, genres] = await Promise.all([
      getStackedCountriesChart(),
      getStackedStatusChart(),
      getStackedGenresChart()
    ]);
    
    return {
      success: true,
      countries,
      status,
      genres
    };
  } catch (err) {
    console.error("Error fetching all stacked charts:", err);
    throw err;
  }
};

// 9.2 Get All Map Data
export const getAllMapData = async () => {
  try {
    const [mapData, countryList, mapStats] = await Promise.all([
      getWorldMapData(),
      getCountryList(),
      getMapStatistics()
    ]);
    
    return {
      success: true,
      mapData,
      countryList,
      mapStats
    };
  } catch (err) {
    console.error("Error fetching all map data:", err);
    throw err;
  }
};

// 9.3 Get Complete Dashboard Data
export const getAllExecutiveData = async () => {
  try {
    const [kpi, stacked, maps] = await Promise.all([
      getExecutiveKPI(),
      getAllStackedCharts(),
      getAllMapData()
    ]);
    
    return {
      success: true,
      kpi,
      stacked,
      maps,
      timestamp: new Date().toISOString()
    };
  } catch (err) {
    console.error("Error fetching all executive data:", err);
    throw err;
  }
};

// ======================================================
// 10. FORMATTER FUNCTIONS FOR FRONTEND (UPDATE UNTUK MAP BARU)
// ======================================================

// 10.1 Color Generators
export const generateChartColors = (count) => {
  const colors = [
    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
    "#FF9F40", "#8AC926", "#1982C4", "#6A4C93", "#FF595E",
    "#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD",
    "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"
  ];
  return colors.slice(0, count);
};

// 10.2 Format Map Data untuk D3/WorldMap (SESUAI BACKEND BARU)
export const formatMapDataForD3 = (apiData) => {
  if (!apiData.success || !apiData.data) return [];
  
  const countries = apiData.data || [];
  
  return countries.map(country => ({
    name: country.country || country.CountryName || 'Unknown',
    value: country.total_shows || country.TotalShows || 0,
    code: getCountryCode(country.country || country.CountryName || ''),
    topGenres: country.top_genres || country.Top3Genres || 'No genre data',
    topCompanies: country.top_companies || country.Top3ProductionCompanies || 'No company data',
    // Additional derived fields
    genreCount: country.genre_count || 0,
    companyCount: country.company_count || 0
  })).filter(item => item.value > 0 && item.name);
};

// 10.3 Format Country Details
export const formatCountryDetails = (apiData) => {
  if (!apiData.success) return null;
  
  return {
    country: apiData.country,
    total_shows: apiData.total_shows,
    genres: apiData.genres,
    production_companies: apiData.production_companies,
    timestamp: apiData.timestamp
  };
};

// 10.4 Format untuk Quick Map Display
export const formatQuickMapData = (apiData) => {
  if (!apiData.success || !apiData.data) return null;
  
  const { data, summary } = apiData;
  
  const formattedData = data.map(country => ({
    id: getCountryCode(country.country),
    name: country.country,
    value: country.total_shows,
    topGenres: country.top_genres,
    topCompanies: country.top_companies
  })).filter(d => d.value > 0);
  
  const maxValue = Math.max(...formattedData.map(d => d.value));
  
  return {
    data: formattedData,
    maxValue,
    summary: summary || {},
    count: formattedData.length
  };
};

// 10.5 Country Code Helper
export const getCountryCode = (countryName) => {
  const countryCodes = {
    'United States': 'US',
    'United States of America': 'US',
    'USA': 'US',
    'United Kingdom': 'GB',
    'UK': 'GB',
    'Great Britain': 'GB',
    'Canada': 'CA',
    'Australia': 'AU',
    'Germany': 'DE',
    'France': 'FR',
    'Japan': 'JP',
    'China': 'CN',
    'India': 'IN',
    'Brazil': 'BR',
    'Russia': 'RU',
    'Italy': 'IT',
    'Spain': 'ES',
    'Mexico': 'MX',
    'South Korea': 'KR',
    'Korea': 'KR',
    'Netherlands': 'NL',
    'Sweden': 'SE',
    'Switzerland': 'CH',
    'Norway': 'NO',
    'Denmark': 'DK',
    'Finland': 'FI',
    'Indonesia': 'ID',
    'Singapore': 'SG',
    'Malaysia': 'MY',
    'Thailand': 'TH',
    'Vietnam': 'VN',
    'Philippines': 'PH'
  };
  
  return countryCodes[countryName] || countryName?.substring(0, 2).toUpperCase() || 'XX';
};

// 10.6 Get Country Name dari Code
export const getCountryName = (countryCode) => {
  const countryNames = {
    'US': 'United States',
    'GB': 'United Kingdom',
    'CA': 'Canada',
    'AU': 'Australia',
    'DE': 'Germany',
    'FR': 'France',
    'JP': 'Japan',
    'CN': 'China',
    'IN': 'India',
    'BR': 'Brazil',
    'RU': 'Russia',
    'IT': 'Italy',
    'ES': 'Spain',
    'MX': 'Mexico',
    'KR': 'South Korea',
    'NL': 'Netherlands',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'NO': 'Norway',
    'DK': 'Denmark',
    'FI': 'Finland',
    'ID': 'Indonesia',
    'SG': 'Singapore',
    'MY': 'Malaysia',
    'TH': 'Thailand',
    'VN': 'Vietnam',
    'PH': 'Philippines'
  };
  
  return countryNames[countryCode?.toUpperCase()] || countryCode || 'Unknown Country';
};

// 10.7 Parse Genre/Company Data
export const parseTopItems = (text) => {
  if (!text || text === 'No genre data' || text === 'No company data') {
    return [];
  }
  
  const items = text.split(', ');
  return items.map(item => {
    // Format: "1. Drama (450 shows)" atau "1. Warner Bros. (180 shows)"
    const match = item.match(/(\d+)\.\s+(.+?)\s+\((\d+)\s+shows\)/);
    if (match) {
      return {
        rank: parseInt(match[1]),
        name: match[2],
        shows: parseInt(match[3])
      };
    }
    return { raw: item };
  });
};

// 10.8 Chart Data Formatters
export const formatStackedChartData = (apiData) => {
  if (!apiData.success || !apiData.datasets) return null;
  
  const colors = generateChartColors(apiData.datasets.length);
  
  const datasets = apiData.datasets.map((dataset, index) => ({
    ...dataset,
    backgroundColor: colors[index],
    borderColor: '#ffffff',
    borderWidth: 1
  }));
  
  return {
    labels: apiData.labels || [],
    datasets
  };
};

export const formatUniversalStackedChart = (apiData) => {
  if (!apiData.success || !apiData.datasets) return null;
  
  const chartColors = {
    countries: ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"],
    status: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
    genres: ["#FF6B6B", "#4ECDC4", "#FFD166", "#06D6A0", "#118AB2"]
  };
  
  const colors = chartColors[apiData.chart_type] || generateChartColors(apiData.datasets.length);
  
  const datasets = apiData.datasets.map((dataset, index) => ({
    ...dataset,
    backgroundColor: colors[index % colors.length],
    borderColor: '#ffffff',
    borderWidth: 1
  }));
  
  return {
    labels: apiData.labels || [],
    datasets
  };
};

// ======================================================
// 11. MAP CONFIGURATIONS (SIMPLE VERSION)
// ======================================================

export const worldMapConfig = {
  // Warna gradient untuk map berdasarkan jumlah show
  colorScale: [
    { threshold: 0, color: "#f7f7f7" },
    { threshold: 1, color: "#e3f2fd" },
    { threshold: 5, color: "#bbdefb" },
    { threshold: 10, color: "#90caf9" },
    { threshold: 20, color: "#64b5f6" },
    { threshold: 50, color: "#42a5f5" },
    { threshold: 100, color: "#2196f3" },
    { threshold: 200, color: "#1e88e5" },
    { threshold: 500, color: "#1976d2" },
    { threshold: 1000, color: "#1565c0" }
  ],
  
  // Tooltip configuration
  tooltip: {
    backgroundColor: "rgba(0, 0, 0, 0.85)",
    textColor: "#ffffff",
    fontSize: "14px",
    padding: "10px",
    borderRadius: "4px"
  },
  
  // Map styling
  mapStyle: {
    defaultFill: "#e0e0e0",
    borderColor: "#ffffff",
    borderWidth: 1,
    hoverColor: "#ff7043",
    hoverBorderColor: "#ff5722"
  },
  
  // Legend configuration
  legend: {
    position: "bottom-left",
    title: "Number of Shows",
    labels: ["0", "1-4", "5-9", "10-19", "20-49", "50-99", "100-199", "200-499", "500-999", "1000+"]
  }
};

// ======================================================
// 12. HELPER FUNCTIONS untuk WorldMapSection.vue (SIMPLE VERSION)
// ======================================================

// Helper untuk menentukan warna berdasarkan jumlah show
export const getColorForValue = (value) => {
  const config = worldMapConfig.colorScale;
  
  for (let i = config.length - 1; i >= 0; i--) {
    if (value >= config[i].threshold) {
      return config[i].color;
    }
  }
  
  return config[0].color;
};

// Helper untuk format tooltip (SIMPLE VERSION - sesuai data baru)
export const formatMapTooltip = (countryData) => {
  if (!countryData) return '';
  
  const { name, value, topGenres, topCompanies } = countryData;
  const countryName = getCountryName(name) || name;
  
  let tooltip = `
    <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #ffffff;">
      ${countryName}
    </div>
    <div style="margin-bottom: 4px;">
      <span style="color: #bbbbbb;">Total Shows:</span> 
      <span style="color: #ffffff; font-weight: bold;"> ${value}</span>
    </div>
  `;
  
  if (topGenres && topGenres !== 'No genre data') {
    tooltip += `
      <div style="margin-bottom: 4px;">
        <span style="color: #bbbbbb;">Top Genres:</span> 
        <span style="color: #ffffff;"> ${topGenres}</span>
      </div>
    `;
  }
  
  if (topCompanies && topCompanies !== 'No company data') {
    tooltip += `
      <div style="margin-bottom: 4px;">
        <span style="color: #bbbbbb;">Top Companies:</span> 
        <span style="color: #ffffff;"> ${topCompanies}</span>
      </div>
    `;
  }
  
  return tooltip;
};

// Helper untuk filter map data
export const filterMapData = (data, filters) => {
  if (!data || !data.length) return [];
  
  return data.filter(country => {
    // Filter by country name
    if (filters.countryQuery && filters.countryQuery.trim() !== '') {
      const query = filters.countryQuery.toLowerCase();
      const countryName = (getCountryName(country.code) || country.name || '').toLowerCase();
      
      if (!countryName.includes(query)) {
        return false;
      }
    }
    
    // Filter by min shows
    if (filters.minShows && (country.value || 0) < filters.minShows) {
      return false;
    }
    
    // Filter by genre
    if (filters.genre && country.topGenres) {
      const genreQuery = filters.genre.toLowerCase();
      if (!country.topGenres.toLowerCase().includes(genreQuery)) {
        return false;
      }
    }
    
    return true;
  });
};

// Helper untuk mendapatkan data country yang dihover
export const getHoveredCountryData = (countryCode, mapData) => {
  if (!countryCode || !mapData || !mapData.length) return null;
  
  return mapData.find(country => 
    country.code === countryCode.toUpperCase() || 
    getCountryCode(country.name) === countryCode.toUpperCase()
  );
};

// ======================================================
// 13. CHART CONFIGURATIONS (Chart.js)
// ======================================================

export const stackedChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      stacked: true,
      grid: {
        display: false
      }
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  }
};

export const universalStackedChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      stacked: true,
      grid: {
        display: false
      }
    },
    y: {
      stacked: true,
      beginAtZero: true
    }
  },
  plugins: {
    legend: {
      position: 'top',
      maxHeight: 100
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y;
          }
          return label;
        }
      }
    }
  }
};

export const pieChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label || '';
          const value = context.raw || 0;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = Math.round((value / total) * 100);
          return `${label}: ${value} (${percentage}%)`;
        }
      }
    }
  }
};

// ======================================================
// 14. MAIN MAP FUNCTIONS untuk WorldMapSection.vue
// ======================================================

// Load map data utama
export const loadMapData = async () => {
  try {
    const data = await getWorldMapData();
    return formatQuickMapData(data);
  } catch (error) {
    console.error("Error loading map data:", error);
    return null;
  }
};

// Load country details saat dihover/klik
export const loadCountryDetails = async (countryName) => {
  try {
    const data = await getCountryMapDetails(countryName);
    return formatCountryDetails(data);
  } catch (error) {
    console.error(`Error loading details for ${countryName}:`, error);
    return null;
  }
};

// Get country list untuk dropdown
export const loadCountryList = async () => {
  try {
    const data = await getCountryList();
    return data.countries || [];
  } catch (error) {
    console.error("Error loading country list:", error);
    return [];
  }
};

// ======================================================
// 15. EXPORT DEFAULT
// ======================================================
export default api;