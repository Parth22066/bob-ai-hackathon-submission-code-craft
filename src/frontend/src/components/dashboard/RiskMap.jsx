import {
  AlertTriangle,
  Layers,
  MapPin,
  Maximize2,
  Minus,
  Plus,
} from "lucide-react";

const riskAssets = [
  {
    id: "TR-002",
    name: "Central Grid Transformer",
    x: "43%",
    y: "42%",
    risk: "Critical",
    score: 92,
  },
  {
    id: "TR-017",
    name: "Industrial Feeder",
    x: "67%",
    y: "58%",
    risk: "High",
    score: 86,
  },
  {
    id: "CB-041",
    name: "North Substation Breaker",
    x: "52%",
    y: "25%",
    risk: "High",
    score: 81,
  },
  {
    id: "TX-031",
    name: "East Distribution Transformer",
    x: "78%",
    y: "43%",
    risk: "Medium",
    score: 78,
  },
  {
    id: "TR-009",
    name: "West Grid Transformer",
    x: "25%",
    y: "61%",
    risk: "Low",
    score: 31,
  },
];

const riskStyles = {
  Critical: {
    marker: "bg-red-600",
    ring: "ring-red-200",
  },
  High: {
    marker: "bg-orange-500",
    ring: "ring-orange-200",
  },
  Medium: {
    marker: "bg-yellow-500",
    ring: "ring-yellow-200",
  },
  Low: {
    marker: "bg-emerald-500",
    ring: "ring-emerald-200",
  },
};

function RiskMap() {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div>
          <div className="flex items-center gap-2">
            <MapPin size={18} className="text-blue-600" />

            <h3 className="font-semibold text-slate-900">Grid Risk Map</h3>
          </div>

          <p className="mt-1 text-xs text-slate-500">
            Geographic view of asset and outage risk
          </p>
        </div>

        <button className="rounded-lg border border-slate-200 p-2 text-slate-500 hover:bg-slate-50">
          <Layers size={17} />
        </button>
      </div>

      {/* Map */}
      <div className="relative h-[420px] overflow-hidden bg-slate-100">
        {/* Map grid */}
        <div
          className="absolute inset-0 opacity-50"
          style={{
            backgroundImage: `
              linear-gradient(#dbe3ec 1px, transparent 1px),
              linear-gradient(90deg, #dbe3ec 1px, transparent 1px)
            `,
            backgroundSize: "50px 50px",
          }}
        />

        {/* Roads / grid lines */}
        <div className="absolute left-[10%] top-[30%] h-[2px] w-[80%] rotate-12 bg-slate-300" />

        <div className="absolute left-[5%] top-[65%] h-[2px] w-[90%] -rotate-6 bg-slate-300" />

        <div className="absolute left-[48%] top-[5%] h-[90%] w-[2px] rotate-[8deg] bg-slate-300" />

        <div className="absolute left-[20%] top-[5%] h-[90%] w-[2px] -rotate-[18deg] bg-slate-300" />

        {/* Risk zone */}
        <div className="absolute left-[31%] top-[27%] h-36 w-36 rounded-full bg-red-400/10 blur-sm" />

        <div className="absolute left-[55%] top-[45%] h-40 w-40 rounded-full bg-orange-400/10 blur-sm" />

        {/* Asset markers */}
        {riskAssets.map((asset) => {
          const style = riskStyles[asset.risk];

          return (
            <div
              key={asset.id}
              className="group absolute -translate-x-1/2 -translate-y-1/2"
              style={{
                left: asset.x,
                top: asset.y,
              }}
            >
              {/* Marker */}
              <div
                className={`h-4 w-4 cursor-pointer rounded-full ${style.marker} ring-4 ${style.ring} transition group-hover:scale-125`}
              />

              {/* Tooltip */}
              <div className="pointer-events-none absolute bottom-7 left-1/2 hidden w-48 -translate-x-1/2 rounded-xl border border-slate-200 bg-white p-3 shadow-lg group-hover:block">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-800">
                    {asset.id}
                  </span>

                  <span className="text-xs font-bold text-slate-700">
                    {asset.score}
                  </span>
                </div>

                <p className="mt-1 text-[11px] text-slate-500">{asset.name}</p>

                <span className="mt-2 inline-block text-[10px] font-semibold text-slate-600">
                  {asset.risk} Risk
                </span>
              </div>
            </div>
          );
        })}

        {/* Map Controls */}
        <div className="absolute right-4 top-4 flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <button className="p-2.5 text-slate-600 hover:bg-slate-50">
            <Plus size={17} />
          </button>

          <div className="h-px bg-slate-200" />

          <button className="p-2.5 text-slate-600 hover:bg-slate-50">
            <Minus size={17} />
          </button>

          <div className="h-px bg-slate-200" />

          <button className="p-2.5 text-slate-600 hover:bg-slate-50">
            <Maximize2 size={16} />
          </button>
        </div>

        {/* Warning */}
        <div className="absolute left-4 top-4 rounded-xl border border-red-100 bg-white/95 px-3 py-2 shadow-sm backdrop-blur">
          <div className="flex items-center gap-2">
            <AlertTriangle size={15} className="text-red-500" />

            <span className="text-xs font-semibold text-slate-700">
              7 critical assets
            </span>
          </div>
        </div>

        {/* Legend */}
        <div className="absolute bottom-4 left-4 rounded-xl border border-slate-200 bg-white/95 p-3 shadow-sm backdrop-blur">
          <p className="mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Risk Level
          </p>

          <div className="flex flex-wrap gap-3">
            <Legend color="bg-emerald-500" label="Low" />
            <Legend color="bg-yellow-500" label="Medium" />
            <Legend color="bg-orange-500" label="High" />
            <Legend color="bg-red-600" label="Critical" />
          </div>
        </div>
      </div>
    </div>
  );
}

function Legend({ color, label }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={`h-2.5 w-2.5 rounded-full ${color}`} />

      <span className="text-[11px] font-medium text-slate-600">{label}</span>
    </div>
  );
}

export default RiskMap;
