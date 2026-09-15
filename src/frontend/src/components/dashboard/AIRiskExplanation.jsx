import {
  Bot,
  AlertTriangle,
  Thermometer,
  Activity,
  CloudRain,
  ArrowRight,
} from "lucide-react";

const riskFactors = [
  {
    label: "Failure Probability",
    value: "87%",
    description: "Higher than the normal threshold",
    icon: AlertTriangle,
  },
  {
    label: "Temperature",
    value: "79°C",
    description: "Above recommended operating range",
    icon: Thermometer,
  },
  {
    label: "Vibration",
    value: "49 mm/s",
    description: "Elevated vibration detected",
    icon: Activity,
  },
  {
    label: "Weather Risk",
    value: "High",
    description: "Wind and rainfall may increase stress",
    icon: CloudRain,
  },
];

function AIRiskExplanation() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
            <Bot size={21} />
          </div>

          <div>
            <p className="text-sm font-semibold text-slate-900">
              AI Risk Explanation
            </p>

            <p className="mt-1 text-xs text-slate-500">
              AI-generated explanation for the highest-risk asset
            </p>
          </div>
        </div>

        <span className="w-fit rounded-full border border-red-100 bg-red-50 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wide text-red-600">
          TR-002 • Critical
        </span>
      </div>

      {/* Explanation */}
      <div className="mt-5 rounded-xl border border-blue-100 bg-blue-50/50 p-4">
        <p className="text-sm leading-6 text-slate-700">
          <span className="font-semibold text-slate-900">AI Assessment:</span>{" "}
          TR-002 has a critical risk level because the predicted failure
          probability is high and recent sensor readings show abnormal
          temperature, vibration and partial discharge behavior. Current weather
          conditions may further increase the risk.
        </p>
      </div>

      {/* Risk Factors */}
      <div className="mt-5">
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-400">
          Key Risk Factors
        </p>

        <div className="mt-3 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {riskFactors.map((factor) => {
            const Icon = factor.icon;

            return (
              <div
                key={factor.label}
                className="rounded-xl border border-slate-200 p-4"
              >
                <div className="flex items-center gap-2">
                  <Icon size={16} className="text-slate-400" />

                  <p className="text-xs font-medium text-slate-500">
                    {factor.label}
                  </p>
                </div>

                <p className="mt-3 text-xl font-bold text-slate-900">
                  {factor.value}
                </p>

                <p className="mt-1 text-[11px] leading-4 text-slate-500">
                  {factor.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommendation */}
      <div className="mt-5 flex flex-col gap-3 rounded-xl border border-slate-200 bg-slate-50 p-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500">
            Recommended Action
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-900">
            Inspect TR-002 immediately and check cooling and oil condition.
          </p>
        </div>

        <button className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-blue-700">
          View Asset
          <ArrowRight size={14} />
        </button>
      </div>
    </div>
  );
}

export default AIRiskExplanation;
