import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Users,
  MapPin,
  Navigation,
  CheckCircle2,
  Clock,
  Wrench,
  Search,
} from "lucide-react";

const initialCrews = [
  {
    id: "Crew A",
    members: 4,
    location: "Vadodara Central",
    status: "Assigned",
    asset: "TR-002",
    distance: "1.2 km",
    task: "On-site inspection",
    recommendation: "Continue inspection at TR-002",
  },
  {
    id: "Crew B",
    members: 3,
    location: "Makarpura",
    status: "Available",
    asset: "TR-017",
    distance: "3.8 km",
    task: "Position near TR-017",
    recommendation: "Position near high-risk transformer",
  },
  {
    id: "Crew C",
    members: 4,
    location: "Nizampura",
    status: "Available",
    asset: "CB-041",
    distance: "2.4 km",
    task: "Position near CB-041",
    recommendation: "Prepare for breaker inspection",
  },
  {
    id: "Crew D",
    members: 3,
    location: "Waghodia",
    status: "Assigned",
    asset: "TX-031",
    distance: "2.1 km",
    task: "Thermal inspection",
    recommendation: "Complete scheduled inspection",
  },
];

const statusStyles = {
  Assigned: "bg-blue-50 text-blue-700 border-blue-100",
  Available: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

function Crew() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [crews, setCrews] = useState(initialCrews);

  const filteredCrews = crews.filter(
    (crew) =>
      crew.id.toLowerCase().includes(search.toLowerCase()) ||
      crew.location.toLowerCase().includes(search.toLowerCase()) ||
      crew.asset.toLowerCase().includes(search.toLowerCase()),
  );

  const positionCrew = (crew) => {
    setCrews((current) => current.map((item) => item.id === crew.id ? {
      ...item,
      status: "Assigned",
      task: `Positioned for ${item.asset}`,
      recommendation: `Positioned for rapid response at ${item.asset}`,
    } : item));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">Field Operations</p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          Crew Management
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Monitor field crews and position teams based on asset risk and
          maintenance priorities.
        </p>
      </div>

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          label="Total Crews"
          value="4"
          description="Field teams monitored"
          icon={Users}
          iconClass="bg-blue-50 text-blue-600"
        />

        <SummaryCard
          label="Available"
          value={crews.filter((crew) => crew.status === "Available").length}
          description="Ready for deployment"
          icon={CheckCircle2}
          iconClass="bg-emerald-50 text-emerald-600"
        />

        <SummaryCard
          label="Assigned"
          value={crews.filter((crew) => crew.status === "Assigned").length}
          description="Currently working"
          icon={Wrench}
          iconClass="bg-orange-50 text-orange-600"
        />

        <SummaryCard
          label="Priority Response"
          value="2"
          description="Crews near high-risk assets"
          icon={Navigation}
          iconClass="bg-red-50 text-red-600"
        />
      </div>

      {/* AI Crew Recommendation */}
      <div className="rounded-2xl border border-blue-100 bg-blue-50/60 p-5 shadow-sm">
        <div className="flex flex-col gap-4 md:flex-row md:items-start">
          <div className="rounded-xl bg-blue-600 p-3 text-white">
            <Navigation size={21} />
          </div>

          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-bold text-slate-900">
                AI Crew Positioning Recommendation
              </p>

              <span className="rounded-full bg-blue-100 px-2.5 py-1 text-[9px] font-bold text-blue-700">
                AI GENERATED
              </span>
            </div>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              Crew A should remain near TR-002 because it has the highest asset
              risk. Crew B and Crew C should remain positioned near TR-017 and
              CB-041 for rapid response.
            </p>

            <div className="mt-4 flex flex-wrap gap-3">
              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                Crew A → TR-002
              </span>

              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                Crew B → TR-017
              </span>

              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                Crew C → CB-041
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-900">Field Crews</p>

            <p className="mt-1 text-xs text-slate-500">
              Current location and assignment status
            </p>
          </div>

          <div className="relative w-full sm:w-64">
            <Search
              size={16}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search crew or asset..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-blue-400 focus:bg-white"
            />
          </div>
        </div>
      </div>

      {/* Crew Cards */}
      <div className="grid gap-5 lg:grid-cols-2">
        {filteredCrews.map((crew) => (
          <div
            key={crew.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md"
          >
            {/* Top */}
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-100 text-slate-700">
                  <Users size={21} />
                </div>

                <div>
                  <p className="text-base font-bold text-slate-900">
                    {crew.id}
                  </p>

                  <p className="text-xs text-slate-500">
                    {crew.members} field members
                  </p>
                </div>
              </div>

              <span
                className={`rounded-full border px-2.5 py-1 text-[9px] font-bold ${statusStyles[crew.status]}`}
              >
                {crew.status}
              </span>
            </div>

            {/* Location */}
            <div className="mt-5 rounded-xl bg-slate-50 p-4">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-white p-2 text-blue-600 shadow-sm">
                  <MapPin size={17} />
                </div>

                <div>
                  <p className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
                    Current Location
                  </p>

                  <p className="mt-1 text-sm font-semibold text-slate-800">
                    {crew.location}
                  </p>
                </div>
              </div>
            </div>

            {/* Assignment */}
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <InfoBox icon={Wrench} label="Asset" value={crew.asset} />

              <InfoBox
                icon={Navigation}
                label="Distance"
                value={crew.distance}
              />

              <InfoBox icon={Clock} label="Task" value={crew.task} />
            </div>

            {/* Recommendation */}
            <div className="mt-4 border-l-2 border-blue-500 bg-blue-50/60 p-3">
              <p className="text-[10px] font-bold uppercase tracking-wider text-blue-600">
                AI Recommendation
              </p>

              <p className="mt-1 text-xs leading-5 text-slate-600">
                {crew.recommendation}
              </p>
            </div>

            {/* Actions */}
            <div className="mt-5 flex flex-wrap justify-end gap-2 border-t border-slate-100 pt-4">
              {crew.status === "Available" && (
                <button
                  type="button"
                  onClick={() => positionCrew(crew)}
                  className="flex items-center gap-2 rounded-xl border border-blue-200 bg-blue-50 px-4 py-2.5 text-xs font-semibold text-blue-700 transition hover:bg-blue-600 hover:text-white active:scale-95"
                >
                  <Navigation size={15} />
                  Position Crew
                </button>
              )}

              <button
                type="button"
                onClick={() => navigate(`/assets/${crew.asset}`)}
                className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-700 transition hover:border-blue-200 hover:text-blue-700 active:scale-95"
              >
                <Wrench size={15} />
                View Asset
              </button>

              <button
                type="button"
                onClick={() => navigate("/risk")}
                className="flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-blue-700 active:scale-95"
              >
                <MapPin size={15} />
                View on Risk Map
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredCrews.length === 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center">
          <p className="text-sm font-semibold text-slate-700">No crews found</p>

          <p className="mt-1 text-xs text-slate-400">
            Try another crew name, location or asset.
          </p>
        </div>
      )}
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

function InfoBox({ icon: Icon, label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 p-3">
      <div className="flex items-center gap-2">
        <Icon size={14} className="text-slate-400" />

        <span className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
          {label}
        </span>
      </div>

      <p className="mt-2 text-sm font-bold text-slate-800">{value}</p>
    </div>
  );
}

export default Crew;
