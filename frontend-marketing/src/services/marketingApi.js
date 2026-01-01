/**
 * =====================================================
 * MARKETING API SERVICE
 * Base URL: /api/marketing
 * =====================================================
 */

const BASE_URL = "http://127.0.0.1:5000/api/marketing";

/**
 * =====================================================
 * AUTH HEADER
 * =====================================================
 */
function getAuthHeaders() {
  const token = localStorage.getItem("token");

  return {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  };
}

/**
 * =====================================================
 * KPI & DASHBOARD
 * =====================================================
 */

// KPI utama marketing
export async function fetchMarketingKPI() {
  const res = await fetch(`${BASE_URL}/kpi`, {
    method: "GET",
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Alias dashboard (kalau kamu pakai /dashboard)
export async function fetchMarketingDashboard() {
  const res = await fetch(`${BASE_URL}/dashboard`, {
    method: "GET",
    headers: getAuthHeaders()
  });

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

/**
 * =====================================================
 * CHARTS
 * =====================================================
 */

// Movies Growth per Year (Line Chart)
export async function fetchMoviesGrowthPerYear() {
  const res = await fetch(
    `${BASE_URL}/charts/movies-growth-year`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Genre Distribution (Pie / Donut)
export async function fetchGenreDistribution() {
  const res = await fetch(
    `${BASE_URL}/charts/genre-distribution`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Country Distribution Map
export async function fetchCountryDistributionMap() {
  const res = await fetch(
    `${BASE_URL}/charts/country-distribution-map`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Top 10 Platforms
export async function fetchTopPlatforms() {
  const res = await fetch(
    `${BASE_URL}/charts/top-platforms`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Top 10 Most Rated Movies
export async function fetchTopMostRatedMovies() {
  const res = await fetch(
    `${BASE_URL}/charts/top-most-rated`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

// Top Highest Rated Movies (optional view)
export async function fetchTopHighestRatedMovies() {
  const res = await fetch(
    `${BASE_URL}/charts/top-highest-rated`,
    { headers: getAuthHeaders() }
  );

  if (!res.ok) {
    // view ini optional → jangan bikin dashboard crash
    return { success: true, data: [] };
  }

  return res.json();
}
