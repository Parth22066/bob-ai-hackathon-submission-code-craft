import { AlertTriangle, MapPin } from "lucide-react";

function OutageAreas({ areas }) {
  const getRiskStyle = (level) => {
    if (level === "Critical") {
      return "bg-red-50 text-red-700";
    }

    if (level === "High") {
      return "bg-orange-50 text-orange-700";
    }

    return "bg-yellow-50 text-yellow-700";
  };

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-100 px-5 py-4">
        <div className="flex items-center gap-2">
          <AlertTriangle size={18} className="text-orange-500" />

          <h3 className="font-semibold text-slate-900">Outage-Prone Areas</h3>
        </div>

        <p className="mt-1 text-xs text-slate-500">
          Geographic areas with elevated outage risk
        </p>
      </div>

      <div className="divide-y divide-slate-100">
        {areas.map((area) => (
          <div key={area.name} className="px-5 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <MapPin size={16} className="text-slate-400" />

                <span className="text-sm font-semibold text-slate-800">
                  {area.name}
                </span>
              </div>

              <span
                className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ${getRiskStyle(
                  area.riskLevel,
                )}`}
              >
                {area.riskLevel}
              </span>
            </div>

            <div className="mt-3 flex gap-6">
              <div>
                <p className="text-[11px] text-slate-400">Assets at risk</p>

                <p className="mt-0.5 text-sm font-semibold text-slate-700">
                  {area.assetsAtRisk}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-slate-400">Customers affected</p>

                <p className="mt-0.5 text-sm font-semibold text-slate-700">
                  {area.customersAffected.toLocaleString()}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default OutageAreas;
