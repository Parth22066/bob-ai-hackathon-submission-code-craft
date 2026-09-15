import { AlertTriangle, ArrowUpRight, ShieldCheck } from "lucide-react";

function GridRiskCard({ data }) {
  const isHighRisk = data.riskLevel === "High";

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">
            Overall Grid Risk
          </p>

          <div className="mt-3 flex items-end gap-2">
            <span className="text-4xl font-bold tracking-tight text-slate-900">
              {data.riskScore}
            </span>

            <span className="mb-1 text-sm text-slate-400">/ 100</span>
          </div>
        </div>

        <div
          className={`flex h-11 w-11 items-center justify-center rounded-xl ${
            isHighRisk
              ? "bg-orange-50 text-orange-600"
              : "bg-emerald-50 text-emerald-600"
          }`}
        >
          {isHighRisk ? <AlertTriangle size={22} /> : <ShieldCheck size={22} />}
        </div>
      </div>

      <div className="mt-5 flex items-center justify-between">
        <div>
          <span
            className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${
              isHighRisk
                ? "bg-orange-50 text-orange-700"
                : "bg-emerald-50 text-emerald-700"
            }`}
          >
            <span className="h-1.5 w-1.5 rounded-full bg-current" />
            {data.riskLevel} Risk
          </span>
        </div>

        <div className="flex items-center gap-1 text-xs font-medium text-orange-600">
          <ArrowUpRight size={14} />
          Requires attention
        </div>
      </div>

      <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-orange-500"
          style={{ width: `${data.riskScore}%` }}
        />
      </div>
    </div>
  );
}

export default GridRiskCard;
