import { MapPin, Users, Wrench, Clock, Navigation } from "lucide-react";

const crews = [
  {
    id: "Crew A",
    members: 4,
    location: "Vadodara Central",
    status: "Assigned",
    assignment: "TR-002",
    distance: "1.2 km",
    recommendation: "On-site inspection",
  },
  {
    id: "Crew B",
    members: 3,
    location: "Makarpura",
    status: "Available",
    assignment: "TR-017",
    distance: "3.8 km",
    recommendation: "Position near TR-017",
  },
  {
    id: "Crew C",
    members: 4,
    location: "Nizampura",
    status: "Available",
    assignment: "CB-041",
    distance: "2.4 km",
    recommendation: "Position near CB-041",
  },
];

const statusStyles = {
  Assigned: "bg-blue-50 text-blue-700 border-blue-100",
  Available: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

function CrewIntelligence() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Crew Intelligence
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Crew availability and recommended positioning for high-risk assets
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl bg-slate-50 px-3 py-2 text-xs font-semibold text-slate-600">
          <Users size={15} />3 active crews
        </div>
      </div>

      {/* Crew Cards */}
      <div className="mt-5 grid gap-4 lg:grid-cols-3">
        {crews.map((crew) => (
          <div
            key={crew.id}
            className="rounded-xl border border-slate-200 p-4 transition hover:border-slate-300 hover:shadow-sm"
          >
            {/* Crew Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                  <Users size={19} />
                </div>

                <div>
                  <p className="text-sm font-bold text-slate-900">{crew.id}</p>

                  <p className="text-xs text-slate-500">
                    {crew.members} members
                  </p>
                </div>
              </div>

              <span
                className={`rounded-full border px-2 py-1 text-[10px] font-bold ${statusStyles[crew.status]}`}
              >
                {crew.status}
              </span>
            </div>

            {/* Location */}
            <div className="mt-5 flex items-start gap-3">
              <MapPin size={16} className="mt-0.5 text-slate-400" />

              <div>
                <p className="text-xs text-slate-500">Current location</p>

                <p className="mt-1 text-sm font-semibold text-slate-800">
                  {crew.location}
                </p>
              </div>
            </div>

            {/* Assignment */}
            <div className="mt-4 flex items-start gap-3">
              <Wrench size={16} className="mt-0.5 text-blue-500" />

              <div>
                <p className="text-xs text-slate-500">Priority assignment</p>

                <p className="mt-1 text-sm font-semibold text-slate-800">
                  {crew.assignment}
                </p>
              </div>
            </div>

            {/* Distance */}
            <div className="mt-4 flex items-start gap-3">
              <Navigation size={16} className="mt-0.5 text-orange-500" />

              <div>
                <p className="text-xs text-slate-500">Distance to asset</p>

                <p className="mt-1 text-sm font-semibold text-slate-800">
                  {crew.distance}
                </p>
              </div>
            </div>

            {/* Recommendation */}
            <div className="mt-4 rounded-lg bg-slate-50 p-3">
              <div className="flex items-center gap-2">
                <Clock size={14} className="text-slate-400" />

                <p className="text-[11px] font-semibold text-slate-600">
                  AI Recommendation
                </p>
              </div>

              <p className="mt-1 text-xs font-medium text-slate-800">
                {crew.recommendation}
              </p>
            </div>

            {/* Action */}
            <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 px-3 py-2.5 text-xs font-semibold text-slate-700 transition hover:bg-slate-50">
              <MapPin size={14} />
              View on Risk Map
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CrewIntelligence;
