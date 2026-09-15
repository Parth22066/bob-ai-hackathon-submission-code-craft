import { ArrowUpRight, MapPin } from "lucide-react";

function CriticalAssets({ assets }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4">
        <div>
          <h3 className="font-semibold text-slate-900">Critical Assets</h3>

          <p className="mt-0.5 text-xs text-slate-500">
            Assets requiring immediate attention
          </p>
        </div>

        <button className="flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-700">
          View all
          <ArrowUpRight size={14} />
        </button>
      </div>

      <div className="divide-y divide-slate-100">
        {assets.map((asset) => (
          <div
            key={asset.id}
            className="flex items-center justify-between px-5 py-4 transition hover:bg-slate-50"
          >
            <div className="flex min-w-0 items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-50 text-sm font-bold text-red-600">
                {asset.id.split("-")[0]}
              </div>

              <div className="min-w-0">
                <p className="truncate text-sm font-semibold text-slate-800">
                  {asset.id} — {asset.name}
                </p>

                <div className="mt-1 flex items-center gap-1 text-xs text-slate-400">
                  <MapPin size={12} />
                  {asset.location}
                </div>
              </div>
            </div>

            <div className="ml-4 flex shrink-0 items-center gap-4">
              <div className="hidden text-right sm:block">
                <p className="text-[11px] text-slate-400">
                  Failure probability
                </p>

                <p className="text-sm font-semibold text-slate-700">
                  {asset.failureProbability}%
                </p>
              </div>

              <div className="text-right">
                <p className="text-[11px] text-slate-400">Risk</p>

                <p className="text-lg font-bold text-red-600">
                  {asset.riskScore}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CriticalAssets;
