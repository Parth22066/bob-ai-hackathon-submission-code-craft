import { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Search,
  Filter,
  MapPin,
  Activity,
  AlertTriangle,
  ChevronRight,
  Wrench,
} from "lucide-react";
import { criticalAssets } from "../data/mockData";

const allAssets = [
  ...criticalAssets,
  {
    id: "TR-009",
    name: "South Distribution Transformer",
    type: "Distribution Transformer",
    location: "Gotri",
    riskScore: 31,
    failureProbability: 18,
    status: "Low",
  },
  {
    id: "TX-044",
    name: "West Grid Transformer",
    type: "Power Transformer",
    location: "Alkapuri",
    riskScore: 64,
    failureProbability: 45,
    status: "Medium",
  },
  {
    id: "CB-028",
    name: "South Substation Breaker",
    type: "Circuit Breaker",
    location: "Manjalpur",
    riskScore: 55,
    failureProbability: 38,
    status: "Medium",
  },
];

const riskStyles = {
  Critical: "bg-red-50 text-red-700 border-red-100",
  High: "bg-orange-50 text-orange-700 border-orange-100",
  Medium: "bg-yellow-50 text-yellow-700 border-yellow-100",
  Low: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

function Assets() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");

  const filteredAssets = useMemo(() => {
    return allAssets.filter((asset) => {
      const matchesSearch =
        asset.id.toLowerCase().includes(search.toLowerCase()) ||
        asset.name.toLowerCase().includes(search.toLowerCase()) ||
        asset.location.toLowerCase().includes(search.toLowerCase());

      const matchesFilter = filter === "All" || asset.status === filter;

      return matchesSearch && matchesFilter;
    });
  }, [search, filter]);

  const createMaintenanceTask = (asset) => {
    navigate("/maintenance", {
      state: {
        createTask: true,
        asset: asset,
      },
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">Asset Management</p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          Grid Assets
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Monitor asset health, risk scores and predicted failure probability.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          label="Total Assets"
          value="128"
          icon={Activity}
          iconClass="bg-blue-50 text-blue-600"
        />

        <SummaryCard
          label="Critical"
          value="7"
          icon={AlertTriangle}
          iconClass="bg-red-50 text-red-600"
        />

        <SummaryCard
          label="High Risk"
          value="18"
          icon={AlertTriangle}
          iconClass="bg-orange-50 text-orange-600"
        />

        <SummaryCard
          label="Healthy / Low Risk"
          value="103"
          icon={Activity}
          iconClass="bg-emerald-50 text-emerald-600"
        />
      </div>

      {/* Asset Table */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        {/* Toolbar */}
        <div className="flex flex-col gap-3 border-b border-slate-200 p-4 md:flex-row md:items-center md:justify-between">
          <div className="relative w-full md:max-w-sm">
            <Search
              size={17}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search asset, ID or location..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-10 pr-3 text-sm text-slate-700 outline-none transition focus:border-blue-400 focus:bg-white"
            />
          </div>

          <div className="flex items-center gap-2">
            <Filter size={16} className="text-slate-400" />

            <select
              value={filter}
              onChange={(event) => setFilter(event.target.value)}
              className="rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-600 outline-none"
            >
              <option value="All">All Risk Levels</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden overflow-x-auto md:block">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Asset
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Type
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Location
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Risk Score
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Failure Probability
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Status
                </th>

                <th className="px-5 py-3 text-right text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              {filteredAssets.map((asset) => (
                <tr
                  key={asset.id}
                  className="border-b border-slate-100 last:border-0 hover:bg-slate-50"
                >
                  <td className="px-5 py-4">
                    <div>
                      <p className="text-sm font-bold text-slate-900">
                        {asset.id}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {asset.name}
                      </p>
                    </div>
                  </td>

                  <td className="px-5 py-4 text-xs text-slate-600">
                    {asset.type}
                  </td>

                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2 text-xs text-slate-600">
                      <MapPin size={14} className="text-slate-400" />
                      {asset.location}
                    </div>
                  </td>

                  <td className="px-5 py-4">
                    <span className="text-sm font-bold text-slate-900">
                      {asset.riskScore}
                    </span>
                    <span className="text-xs text-slate-400"> / 100</span>
                  </td>

                  <td className="px-5 py-4">
                    <span className="text-sm font-semibold text-slate-800">
                      {asset.failureProbability}%
                    </span>
                  </td>

                  <td className="px-5 py-4">
                    <span
                      className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${riskStyles[asset.status]}`}
                    >
                      {asset.status}
                    </span>
                  </td>

                  <td className="px-5 py-4">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        type="button"
                        onClick={() => createMaintenanceTask(asset)}
                        className="flex items-center gap-1.5 rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-600 hover:text-white active:scale-95"
                      >
                        <Wrench size={14} />
                        Create Task
                      </button>

                      <Link
                        to={`/assets/${asset.id}`}
                        className="flex items-center gap-1 rounded-lg px-2 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 hover:text-blue-600"
                      >
                        View
                        <ChevronRight size={14} />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile Cards */}
        <div className="divide-y divide-slate-100 md:hidden">
          {filteredAssets.map((asset) => (
            <div key={asset.id} className="p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm font-bold text-slate-900">{asset.id}</p>

                  <p className="mt-1 text-xs text-slate-500">{asset.name}</p>
                </div>

                <span
                  className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${riskStyles[asset.status]}`}
                >
                  {asset.status}
                </span>
              </div>

              <div className="mt-4 flex items-center gap-2 text-xs text-slate-500">
                <MapPin size={14} />
                {asset.location}
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-[10px] text-slate-400">Risk Score</p>

                  <p className="mt-1 text-lg font-bold text-slate-900">
                    {asset.riskScore}
                  </p>
                </div>

                <div className="rounded-xl bg-slate-50 p-3">
                  <p className="text-[10px] text-slate-400">
                    Failure Probability
                  </p>

                  <p className="mt-1 text-lg font-bold text-slate-900">
                    {asset.failureProbability}%
                  </p>
                </div>
              </div>

              <div className="mt-3 grid grid-cols-2 gap-2">
                <Link
                  to={`/assets/${asset.id}`}
                  className="flex items-center justify-center gap-1 rounded-xl border border-slate-200 py-2.5 text-xs font-semibold text-slate-600"
                >
                  View Asset
                  <ChevronRight size={14} />
                </Link>

                <button
                  type="button"
                  onClick={() => createMaintenanceTask(asset)}
                  className="flex items-center justify-center gap-1 rounded-xl bg-blue-600 py-2.5 text-xs font-semibold text-white transition hover:bg-blue-700 active:scale-95"
                >
                  <Wrench size={14} />
                  Create Task
                </button>
              </div>
            </div>
          ))}

          {filteredAssets.length === 0 && (
            <div className="p-10 text-center">
              <p className="text-sm font-semibold text-slate-700">
                No assets found
              </p>

              <p className="mt-1 text-xs text-slate-400">
                Try changing your search or risk filter.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function SummaryCard({ label, value, icon: Icon, iconClass }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>

        <div className={`rounded-xl p-2.5 ${iconClass}`}>
          <Icon size={19} />
        </div>
      </div>

      <p className="mt-4 text-3xl font-bold text-slate-900">{value}</p>
    </div>
  );
}

export default Assets;
