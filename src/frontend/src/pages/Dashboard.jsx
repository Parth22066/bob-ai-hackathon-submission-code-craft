import { useState, useEffect } from "react";
import { Activity, AlertTriangle, Users } from "lucide-react";

import RiskMap from "../components/dashboard/RiskMap";
import GridRiskCard from "../components/dashboard/GridRiskCard";
import CriticalAssets from "../components/dashboard/CriticalAssets";
import OutageAreas from "../components/dashboard/OutageAreas";
import SensorTrends from "../components/dashboard/SensorTrends";

import { gridOverview as defaultGridOverview, criticalAssets as defaultCriticalAssets, outageAreas } from "../data/mockData";
import { getDashboardOverview, getAssetRiskRanking } from "../services/api";

import WeatherIntelligence from "../components/dashboard/WeatherIntelligence";
import MaintenanceRecommendations from "../components/dashboard/MaintenanceRecommendations";
import CrewIntelligence from "../components/dashboard/CrewIntelligence";
import AIRiskExplanation from "../components/dashboard/AIRiskExplanation";

function Dashboard() {
  const [overview, setOverview] = useState(defaultGridOverview);
  const [assets, setAssets] = useState(defaultCriticalAssets);

  useEffect(() => {
    let isMounted = true;

    async function loadData() {
      try {
        const data = await getDashboardOverview();
        if (isMounted && data) {
          setOverview((prev) => ({
            ...prev,
            riskLevel: data.overall_grid_risk || prev.riskLevel,
            criticalAssets: data.risk_summary?.critical_assets ?? prev.criticalAssets,
            highRiskAssets: data.risk_summary?.high_risk_assets ?? prev.highRiskAssets,
          }));
        }
      } catch {
        // use default fallback
      }

      try {
        const rankingData = await getAssetRiskRanking();
        if (isMounted && rankingData?.ranking?.length > 0) {
          const mapped = rankingData.ranking.map((a) => ({
            id: a.asset_id,
            name: a.asset_name,
            type: "Power Transformer",
            location: `Lat: ${a.latitude.toFixed(2)}, Lon: ${a.longitude.toFixed(2)}`,
            riskScore: Math.round(a.risk_score),
            failureProbability: Math.min(Math.round(a.risk_score * 0.95), 99),
            status: a.risk_level,
          }));
          setAssets(mapped.slice(0, 4));
        }
      } catch {
        // use default fallback
      }
    }

    loadData();
    return () => { isMounted = false; };
  }, []);
  return (
    <div className="space-y-6">
      {/* Page Heading */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          Grid Operations Center
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          GridGuard AI Dashboard
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Real-time overview of grid health, asset risk and outage threats.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 lg:grid-cols-4">
        {/* Overall Risk */}
        <GridRiskCard data={overview} />

        {/* Assets Monitored */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">
              Assets Monitored
            </p>

            <div className="rounded-xl bg-blue-50 p-2.5 text-blue-600">
              <Activity size={20} />
            </div>
          </div>

          <p className="mt-4 text-3xl font-bold text-slate-900">
            {overview.assetsMonitored}
          </p>

          <p className="mt-2 text-xs text-slate-500">
            Assets currently connected to GridGuard
          </p>
        </div>

        {/* Critical Assets */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">
              Critical Assets
            </p>

            <div className="rounded-xl bg-red-50 p-2.5 text-red-600">
              <AlertTriangle size={20} />
            </div>
          </div>

          <p className="mt-4 text-3xl font-bold text-slate-900">
            {overview.criticalAssets}
          </p>

          <p className="mt-2 text-xs text-red-600">
            Immediate attention required
          </p>
        </div>

        {/* Customers at Risk */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">
              Customers at Risk
            </p>

            <div className="rounded-xl bg-orange-50 p-2.5 text-orange-600">
              <Users size={20} />
            </div>
          </div>

          <p className="mt-4 text-3xl font-bold text-slate-900">
            {overview.affectedCustomers.toLocaleString()}
          </p>

          <p className="mt-2 text-xs text-orange-600">
            Based on current grid risk
          </p>
        </div>
      </div>

      {/* Critical Assets + Outage Areas */}
      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <CriticalAssets assets={assets} />

        <OutageAreas areas={outageAreas} />
      </div>

      {/* Risk Map */}
      <RiskMap />

      {/* Sensor Intelligence */}
      <SensorTrends />

      {/* Weather Intelligence */}
      <WeatherIntelligence />

      {/* Maintenance Recommendations */}
      <MaintenanceRecommendations />
      {/* Crew Intelligence */}
      <CrewIntelligence />
      <AIRiskExplanation />
    </div>
  );
}

export default Dashboard;
