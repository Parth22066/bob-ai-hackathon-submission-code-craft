import {
  ArrowLeft,
  AlertTriangle,
  Activity,
  Thermometer,
  Gauge,
  CloudRain,
  MapPin,
  Wrench,
  Bot,
  Clock,
} from "lucide-react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { criticalAssets } from "../data/mockData";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const sensorData = [
  { time: "08:00", temperature: 64, vibration: 32, discharge: 18 },
  { time: "09:00", temperature: 67, vibration: 35, discharge: 21 },
  { time: "10:00", temperature: 71, vibration: 39, discharge: 24 },
  { time: "11:00", temperature: 74, vibration: 42, discharge: 29 },
  { time: "12:00", temperature: 78, vibration: 48, discharge: 34 },
  { time: "13:00", temperature: 81, vibration: 52, discharge: 38 },
  { time: "14:00", temperature: 79, vibration: 49, discharge: 36 },
];

function AssetDetails() {
  const { assetId } = useParams();
  const navigate = useNavigate();

  const selectedAsset = criticalAssets.find((item) => item.id === assetId);
  const asset = selectedAsset
    ? { ...selectedAsset, health: selectedAsset.status === "Critical" ? "Poor" : "Fair" }
    : { id: assetId || "TR-002", name: "Central Grid Transformer", type: "Power Transformer", location: "Vadodara Central", riskScore: 92, failureProbability: 87, status: "Critical", health: "Poor" };

  return (
    <div className="space-y-6">
      {/* Back */}
      <Link
        to="/assets"
        className="inline-flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-slate-900"
      >
        <ArrowLeft size={17} />
        Back to Assets
      </Link>

      {/* Asset Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-red-50 text-red-600">
              <AlertTriangle size={23} />
            </div>

            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h1 className="text-2xl font-bold text-slate-900">
                  {asset.id}
                </h1>

                <span className="rounded-full border border-red-100 bg-red-50 px-2.5 py-1 text-[10px] font-bold text-red-700">
                  {asset.status}
                </span>
              </div>

              <p className="mt-1 text-sm font-medium text-slate-700">
                {asset.name}
              </p>

              <div className="mt-2 flex flex-wrap gap-4 text-xs text-slate-500">
                <span>{asset.type}</span>

                <span className="flex items-center gap-1">
                  <MapPin size={13} />
                  {asset.location}
                </span>
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() =>
              navigate("/maintenance", {
                state: {
                  createTask: true,
                  asset: asset,
                },
              })
            }
            className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 active:scale-95"
          >
            <Wrench size={16} />
            Create Maintenance Task
          </button>
        </div>
      </div>

      {/* Risk Overview */}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Risk Score"
          value={`${asset.riskScore}/100`}
          description="Critical risk level"
          icon={AlertTriangle}
          iconClass="bg-red-50 text-red-600"
        />

        <MetricCard
          label="Failure Probability"
          value={`${asset.failureProbability}%`}
          description="Predicted failure probability"
          icon={Gauge}
          iconClass="bg-orange-50 text-orange-600"
        />

        <MetricCard
          label="Asset Health"
          value={asset.health}
          description="Current health condition"
          icon={Activity}
          iconClass="bg-red-50 text-red-600"
        />

        <MetricCard
          label="Weather Risk"
          value="High"
          description="Environmental stress detected"
          icon={CloudRain}
          iconClass="bg-orange-50 text-orange-600"
        />
      </div>

      {/* Risk + Sensor Chart */}
      <div className="grid gap-6 xl:grid-cols-[1fr_1.6fr]">
        {/* Risk Factors */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">Risk Factors</p>

          <p className="mt-1 text-xs text-slate-500">
            Main factors contributing to the current asset risk
          </p>

          <div className="mt-5 space-y-5">
            <RiskFactor
              label="Temperature"
              value="79°C"
              percentage={82}
              icon={Thermometer}
            />

            <RiskFactor
              label="Vibration"
              value="49 mm/s"
              percentage={74}
              icon={Activity}
            />

            <RiskFactor
              label="Partial Discharge"
              value="36 pC"
              percentage={68}
              icon={Activity}
            />

            <RiskFactor
              label="Weather Stress"
              value="High"
              percentage={76}
              icon={CloudRain}
            />
          </div>
        </div>

        {/* Sensor Chart */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Sensor Trends
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Recent sensor behavior for {asset.id}
              </p>
            </div>

            <span className="rounded-lg bg-red-50 px-2.5 py-1 text-[10px] font-bold text-red-600">
              Abnormal
            </span>
          </div>

          <div className="mt-5 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={sensorData}>
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
                  name="Discharge"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* AI Explanation */}
      <div className="rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <Bot size={20} />
          </div>

          <div>
            <p className="text-sm font-semibold text-slate-900">
              AI Risk Explanation
            </p>

            <p className="mt-1 text-xs text-slate-500">
              AI-generated analysis of the asset condition
            </p>
          </div>
        </div>

        <div className="mt-4 rounded-xl bg-blue-50/60 p-4">
          <p className="text-sm leading-6 text-slate-700">
            TR-002 is currently classified as a critical-risk asset. The
            predicted failure probability is 87%. The recent increase in
            temperature, vibration and partial discharge indicates abnormal
            operating behavior. High weather stress may further increase the
            probability of failure.
          </p>
        </div>
      </div>

      {/* Grid Impact + Maintenance */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">Grid Impact</p>

          <div className="mt-5 space-y-4">
            <InfoRow label="Grid Importance" value="Very High" />
            <InfoRow label="Customer Impact" value="5,200 customers" />
            <InfoRow label="Geographic Impact" value="Vadodara Central" />
            <InfoRow label="Connected Load" value="High" />
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-sm font-semibold text-slate-900">
            Maintenance Priority
          </p>

          <div className="mt-5 rounded-xl border border-red-100 bg-red-50 p-4">
            <div className="flex items-center gap-2">
              <Clock size={16} className="text-red-600" />

              <span className="text-xs font-bold uppercase tracking-wide text-red-600">
                Immediate
              </span>
            </div>

            <p className="mt-3 text-sm font-semibold text-slate-900">
              Inspect cooling system and oil condition.
            </p>

            <p className="mt-2 text-xs leading-5 text-slate-500">
              Perform detailed sensor inspection and verify transformer
              operating conditions before the risk increases further.
            </p>

            <p className="mt-3 text-xs font-semibold text-slate-600">
              Recommended Crew: Crew A
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, description, icon: Icon, iconClass }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>

        <div className={`rounded-xl p-2.5 ${iconClass}`}>
          <Icon size={19} />
        </div>
      </div>

      <p className="mt-4 text-2xl font-bold text-slate-900">{value}</p>

      <p className="mt-1 text-xs text-slate-500">{description}</p>
    </div>
  );
}

function RiskFactor({ label, value, percentage, icon: Icon }) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon size={15} className="text-slate-400" />

          <span className="text-xs font-medium text-slate-600">{label}</span>
        </div>

        <span className="text-xs font-bold text-slate-800">{value}</span>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-orange-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 last:pb-0">
      <span className="text-xs text-slate-500">{label}</span>

      <span className="text-xs font-semibold text-slate-800">{value}</span>
    </div>
  );
}

export default AssetDetails;
