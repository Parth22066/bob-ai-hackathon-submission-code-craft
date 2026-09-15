import { useMemo, useState } from "react";
import {
  Activity,
  Thermometer,
  Gauge,
  Droplets,
  Search,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const sensorAssets = [
  {
    id: "TR-002",
    name: "Central Grid Transformer",
    location: "Vadodara Central",
    temperature: 79,
    vibration: 49,
    discharge: 36,
    oilQuality: "Poor",
    health: "Critical",
    anomaly: "Detected",
  },
  {
    id: "TR-017",
    name: "Industrial Feeder Transformer",
    location: "Makarpura",
    temperature: 71,
    vibration: 43,
    discharge: 27,
    oilQuality: "Fair",
    health: "High",
    anomaly: "Detected",
  },
  {
    id: "CB-041",
    name: "North Substation Breaker",
    location: "Nizampura",
    temperature: 66,
    vibration: 38,
    discharge: 22,
    oilQuality: "Good",
    health: "High",
    anomaly: "Detected",
  },
  {
    id: "TX-031",
    name: "East Distribution Transformer",
    location: "Waghodia",
    temperature: 61,
    vibration: 31,
    discharge: 18,
    oilQuality: "Good",
    health: "Medium",
    anomaly: "Normal",
  },
  {
    id: "TR-009",
    name: "South Distribution Transformer",
    location: "Gotri",
    temperature: 54,
    vibration: 24,
    discharge: 12,
    oilQuality: "Good",
    health: "Low",
    anomaly: "Normal",
  },
];

const trendData = [
  { time: "08:00", temperature: 64, vibration: 32, discharge: 18 },
  { time: "09:00", temperature: 67, vibration: 35, discharge: 21 },
  { time: "10:00", temperature: 71, vibration: 39, discharge: 24 },
  { time: "11:00", temperature: 74, vibration: 42, discharge: 29 },
  { time: "12:00", temperature: 78, vibration: 48, discharge: 34 },
  { time: "13:00", temperature: 81, vibration: 52, discharge: 38 },
  { time: "14:00", temperature: 79, vibration: 49, discharge: 36 },
];

const healthStyles = {
  Critical: "bg-red-50 text-red-700 border-red-100",
  High: "bg-orange-50 text-orange-700 border-orange-100",
  Medium: "bg-yellow-50 text-yellow-700 border-yellow-100",
  Low: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

function Sensors() {
  const [search, setSearch] = useState("");
  const [selectedAsset, setSelectedAsset] = useState("TR-002");

  const filteredAssets = useMemo(() => {
    return sensorAssets.filter(
      (asset) =>
        asset.id.toLowerCase().includes(search.toLowerCase()) ||
        asset.name.toLowerCase().includes(search.toLowerCase()) ||
        asset.location.toLowerCase().includes(search.toLowerCase()),
    );
  }, [search]);

  const selected = sensorAssets.find((asset) => asset.id === selectedAsset);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          Real-Time Monitoring
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          Sensor Monitoring
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Monitor sensor readings, abnormal behavior and asset health.
        </p>
      </div>

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          label="Sensors Online"
          value="624"
          description="All systems reporting"
          icon={Activity}
          iconClass="bg-blue-50 text-blue-600"
        />

        <SummaryCard
          label="Temperature Alerts"
          value="12"
          description="Above normal range"
          icon={Thermometer}
          iconClass="bg-orange-50 text-orange-600"
        />

        <SummaryCard
          label="Vibration Alerts"
          value="8"
          description="Elevated vibration"
          icon={Gauge}
          iconClass="bg-red-50 text-red-600"
        />

        <SummaryCard
          label="Sensor Anomalies"
          value="15"
          description="Requires investigation"
          icon={AlertTriangle}
          iconClass="bg-red-50 text-red-600"
        />
      </div>

      {/* Selected Asset */}
      {selected && (
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-lg font-bold text-slate-900">
                  {selected.id}
                </p>

                <span
                  className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${healthStyles[selected.health]}`}
                >
                  {selected.health}
                </span>
              </div>

              <p className="mt-1 text-sm text-slate-600">{selected.name}</p>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-500">
              <CheckCircle2 size={16} className="text-emerald-500" />
              Live sensor data
            </div>
          </div>

          {/* Sensor Cards */}
          <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <SensorCard
              label="Temperature"
              value={`${selected.temperature}°C`}
              status="Above normal"
              icon={Thermometer}
              iconClass="bg-orange-50 text-orange-600"
            />

            <SensorCard
              label="Vibration"
              value={`${selected.vibration} mm/s`}
              status="Elevated"
              icon={Activity}
              iconClass="bg-red-50 text-red-600"
            />

            <SensorCard
              label="Partial Discharge"
              value={`${selected.discharge} pC`}
              status="Abnormal"
              icon={AlertTriangle}
              iconClass="bg-red-50 text-red-600"
            />

            <SensorCard
              label="Oil Quality"
              value={selected.oilQuality}
              status="Current condition"
              icon={Droplets}
              iconClass="bg-blue-50 text-blue-600"
            />
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-900">
              Sensor Trends
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Recent sensor behavior for {selectedAsset}
            </p>
          </div>

          <span className="w-fit rounded-full bg-red-50 px-3 py-1.5 text-[10px] font-bold text-red-600">
            Anomaly detected
          </span>
        </div>

        <div className="mt-5 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />

              <XAxis
                dataKey="time"
                tick={{ fontSize: 11 }}
                tickLine={false}
                axisLine={false}
              />

              <YAxis
                tick={{ fontSize: 11 }}
                tickLine={false}
                axisLine={false}
              />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="temperature"
                stroke="#ef4444"
                strokeWidth={2}
                dot={false}
                name="Temperature"
              />

              <Line
                type="monotone"
                dataKey="vibration"
                stroke="#f97316"
                strokeWidth={2}
                dot={false}
                name="Vibration"
              />

              <Line
                type="monotone"
                dataKey="discharge"
                stroke="#2563eb"
                strokeWidth={2}
                dot={false}
                name="Partial Discharge"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 flex flex-wrap gap-5 text-xs text-slate-500">
          <LegendItem label="Temperature" className="bg-red-500" />
          <LegendItem label="Vibration" className="bg-orange-500" />
          <LegendItem label="Partial Discharge" className="bg-blue-600" />
        </div>
      </div>

      {/* Asset Sensor Table */}
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-col gap-3 border-b border-slate-200 p-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-900">
              Asset Sensor Status
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Current readings across monitored assets
            </p>
          </div>

          <div className="relative w-full md:max-w-xs">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search assets..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-blue-400 focus:bg-white"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Asset
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Temperature
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Vibration
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Discharge
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Oil Quality
                </th>

                <th className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Health
                </th>

                <th className="px-5 py-3"></th>
              </tr>
            </thead>

            <tbody>
              {filteredAssets.map((asset) => (
                <tr
                  key={asset.id}
                  className={`border-b border-slate-100 last:border-0 ${
                    selectedAsset === asset.id
                      ? "bg-blue-50/40"
                      : "hover:bg-slate-50"
                  }`}
                >
                  <td className="px-5 py-4">
                    <p className="text-sm font-bold text-slate-900">
                      {asset.id}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">{asset.name}</p>
                  </td>

                  <td className="px-5 py-4 text-sm font-semibold text-slate-800">
                    {asset.temperature}°C
                  </td>

                  <td className="px-5 py-4 text-sm font-semibold text-slate-800">
                    {asset.vibration} mm/s
                  </td>

                  <td className="px-5 py-4 text-sm font-semibold text-slate-800">
                    {asset.discharge} pC
                  </td>

                  <td className="px-5 py-4 text-xs font-semibold text-slate-700">
                    {asset.oilQuality}
                  </td>

                  <td className="px-5 py-4">
                    <span
                      className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${healthStyles[asset.health]}`}
                    >
                      {asset.health}
                    </span>
                  </td>

                  <td className="px-5 py-4">
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedAsset(asset.id);
                        window.scrollTo({
                          top: 0,
                          behavior: "smooth",
                        });
                      }}
                      className="rounded-lg border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700 transition hover:bg-blue-600 hover:text-white active:scale-95"
                    >
                      Monitor
                    </button>
                  </td>
                </tr>
              ))}

              {filteredAssets.length === 0 && (
                <tr>
                  <td colSpan="7" className="p-10 text-center">
                    <p className="text-sm font-semibold text-slate-700">
                      No assets found
                    </p>

                    <p className="mt-1 text-xs text-slate-400">
                      Try another asset ID or name.
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function SummaryCard({ label, value, description, icon: Icon, iconClass }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>

        <div className={`rounded-xl p-2.5 ${iconClass}`}>
          <Icon size={19} />
        </div>
      </div>

      <p className="mt-4 text-3xl font-bold text-slate-900">{value}</p>

      <p className="mt-1 text-xs text-slate-500">{description}</p>
    </div>
  );
}

function SensorCard({ label, value, status, icon: Icon, iconClass }) {
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <div className="flex items-center justify-between">
        <p className="text-xs font-medium text-slate-500">{label}</p>

        <div className={`rounded-lg p-2 ${iconClass}`}>
          <Icon size={16} />
        </div>
      </div>

      <p className="mt-3 text-xl font-bold text-slate-900">{value}</p>

      <p className="mt-1 text-[11px] text-slate-500">{status}</p>
    </div>
  );
}

function LegendItem({ label, className }) {
  return (
    <div className="flex items-center gap-2">
      <span className={`h-2.5 w-2.5 rounded-full ${className}`} />
      <span>{label}</span>
    </div>
  );
}

export default Sensors;
