import { Wrench, AlertTriangle, Clock, ArrowRight } from "lucide-react";

const recommendations = [
  {
    asset: "TR-002",
    name: "Central Grid Transformer",
    priority: "Critical",
    action: "Inspect cooling system and oil condition",
    reason:
      "High failure probability with abnormal temperature and discharge readings.",
    urgency: "Immediate",
    crew: "Crew A",
  },
  {
    asset: "TR-017",
    name: "Industrial Feeder Transformer",
    priority: "High",
    action: "Perform vibration and thermal inspection",
    reason:
      "Elevated vibration trend detected over the recent monitoring period.",
    urgency: "Within 24 hours",
    crew: "Crew B",
  },
  {
    asset: "CB-041",
    name: "North Substation Breaker",
    priority: "High",
    action: "Check breaker contacts and operating mechanism",
    reason: "Asset risk is increasing and may affect a critical grid section.",
    urgency: "Within 48 hours",
    crew: "Crew C",
  },
];

const priorityStyles = {
  Critical: "bg-red-50 text-red-700 border-red-100",
  High: "bg-orange-50 text-orange-700 border-orange-100",
  Medium: "bg-yellow-50 text-yellow-700 border-yellow-100",
};

function MaintenanceRecommendations() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Maintenance Recommendations
          </p>

          <p className="mt-1 text-xs text-slate-500">
            AI-prioritized actions for assets requiring attention
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700">
          <Wrench size={15} />3 actions recommended
        </div>
      </div>

      {/* Recommendations */}
      <div className="mt-5 space-y-3">
        {recommendations.map((item) => (
          <div
            key={item.asset}
            className="rounded-xl border border-slate-200 p-4 transition hover:border-slate-300 hover:shadow-sm"
          >
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              {/* Asset information */}
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-bold text-slate-900">
                    {item.asset}
                  </span>

                  <span
                    className={`rounded-full border px-2 py-0.5 text-[10px] font-bold uppercase ${priorityStyles[item.priority]}`}
                  >
                    {item.priority}
                  </span>
                </div>

                <p className="mt-1 text-sm font-semibold text-slate-700">
                  {item.name}
                </p>

                <div className="mt-3 flex items-start gap-2">
                  <Wrench size={15} className="mt-0.5 shrink-0 text-blue-600" />

                  <div>
                    <p className="text-xs font-semibold text-slate-800">
                      Recommended Action
                    </p>

                    <p className="mt-0.5 text-xs text-slate-500">
                      {item.action}
                    </p>
                  </div>
                </div>

                <div className="mt-3 flex items-start gap-2">
                  <AlertTriangle
                    size={15}
                    className="mt-0.5 shrink-0 text-orange-500"
                  />

                  <div>
                    <p className="text-xs font-semibold text-slate-800">
                      Why this is recommended
                    </p>

                    <p className="mt-0.5 text-xs leading-5 text-slate-500">
                      {item.reason}
                    </p>
                  </div>
                </div>
              </div>

              {/* Action information */}
              <div className="flex shrink-0 flex-col gap-3 border-t border-slate-100 pt-3 sm:flex-row sm:items-center lg:w-64 lg:border-l lg:border-t-0 lg:pl-5 lg:pt-0">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Clock size={15} className="text-slate-400" />

                    <p className="text-xs font-medium text-slate-500">
                      Urgency
                    </p>
                  </div>

                  <p className="mt-1 text-sm font-semibold text-slate-800">
                    {item.urgency}
                  </p>

                  <p className="mt-3 text-xs text-slate-500">Assigned crew</p>

                  <p className="mt-1 text-sm font-semibold text-slate-800">
                    {item.crew}
                  </p>
                </div>

                <button className="flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-blue-700">
                  View Asset
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MaintenanceRecommendations;
