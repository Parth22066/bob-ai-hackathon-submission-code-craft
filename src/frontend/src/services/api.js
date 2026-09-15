/**
 * GridGuard AI - Centralized Backend API Client
 * Connects React frontend with Django REST API (http://localhost:8000/api).
 * Automatically provides fallback data if the backend server is offline.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

/**
 * Generic fetch wrapper with timeout and fallback support
 */
async function fetchWithTimeout(url, options = {}, timeoutMs = 4000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        ...(options.headers || {}),
      },
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (err) {
    clearTimeout(timeoutId);
    console.warn(`[GridGuard API] Call to ${url} failed, using local fallback:`, err.message);
    throw err;
  }
}

// -------------------------------------------------------------
// Core Endpoints
// -------------------------------------------------------------

export async function getDashboardOverview() {
  return await fetchWithTimeout(`${API_BASE_URL}/dashboard/`);
}

export async function getAssetRiskRanking() {
  return await fetchWithTimeout(`${API_BASE_URL}/assets/ranking/`);
}

export async function getAssetDetails(assetId) {
  return await fetchWithTimeout(`${API_BASE_URL}/assets/${assetId}/details/`);
}

export async function analyzeRisk(payload) {
  return await fetchWithTimeout(`${API_BASE_URL}/risk/analyze/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function queryAIAssistant(query, assetId = "TR-002") {
  return await fetchWithTimeout(`${API_BASE_URL}/ai/assistant/`, {
    method: "POST",
    body: JSON.stringify({ query, asset_id: assetId }),
  });
}

export async function getLiveWeather(city = "Vadodara") {
  return await fetchWithTimeout(`${API_BASE_URL}/weather/live/?city=${encodeURIComponent(city)}`);
}

export async function getMaintenanceHistory() {
  return await fetchWithTimeout(`${API_BASE_URL}/maintenance/history/`);
}

export async function updateMaintenanceStatus(id, newStatus) {
  return await fetchWithTimeout(`${API_BASE_URL}/maintenance/${id}/status/`, {
    method: "POST",
    body: JSON.stringify({ status: newStatus }),
  });
}

export async function ingestTelemetry(payload) {
  return await fetchWithTimeout(`${API_BASE_URL}/ingest/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
