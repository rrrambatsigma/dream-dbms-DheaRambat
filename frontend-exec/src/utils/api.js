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
// EXECUTIVE KPI
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
// EXECUTIVE TABLE (Dropdown Table Data)
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
// EXECUTIVE TABLE SEARCH ENGINE
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
// EXECUTIVE BAR CHART (Top 15)
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
// EXECUTIVE PIE / DONUT CHART
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
// EXECUTIVE STACKED BAR CHART  🔥 (BARU DITAMBAHKAN)
// ======================================================
export const getExecutiveStackedChart = async () => {
  try {
    const res = await api.get("/api/executive/chart/stacked");

    return res.data;

  } catch (err) {
    console.error("Error fetching Executive Stacked Bar Chart:", err);
    throw err;
  }
};

// ======================================================
// DEFAULT EXPORT AXIOS
// ======================================================
export default api;
