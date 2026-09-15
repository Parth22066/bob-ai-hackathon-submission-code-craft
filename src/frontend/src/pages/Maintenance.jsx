import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Clock,
  Search,
  UserRound,
  Wrench,
  X,
} from "lucide-react";

const initialMaintenanceTasks = [
  {
    id: "MT-001",
    asset: "TR-002",
    name: "Central Grid Transformer",
    location: "Vadodara Central",
    priority: "Critical",
    action: "Inspect cooling system and oil condition",
    reason:
      "High failure probability with abnormal temperature and partial discharge readings.",
    urgency: "Immediate",
    crew: "Crew A",
    status: "Pending",
    due: "Today",
  },
  {
    id: "MT-002",
    asset: "TR-017",
    name: "Industrial Feeder Transformer",
    location: "Makarpura",
    priority: "High",
    action: "Perform vibration and thermal inspection",
    reason:
      "Elevated vibration trend detected over the recent monitoring period.",
    urgency: "Within 24 hours",
    crew: "Crew B",
    status: "Assigned",
    due: "Tomorrow",
  },
  {
    id: "MT-003",
    asset: "CB-041",
    name: "North Substation Breaker",
    location: "Nizampura",
    priority: "High",
    action: "Check breaker contacts and operating mechanism",
    reason: "Asset risk is increasing and may affect a critical grid section.",
    urgency: "Within 48 hours",
    crew: "Crew C",
    status: "Assigned",
    due: "Wed",
  },
  {
    id: "MT-004",
    asset: "TX-031",
    name: "East Distribution Transformer",
    location: "Waghodia",
    priority: "Medium",
    action: "Perform routine thermal inspection",
    reason:
      "Moderate asset risk detected with increasing environmental exposure.",
    urgency: "Within 72 hours",
    crew: "Crew D",
    status: "Scheduled",
    due: "Thu",
  },
];

const priorityStyles = {
  Critical: "bg-red-50 text-red-700 border-red-100",
  High: "bg-orange-50 text-orange-700 border-orange-100",
  Medium: "bg-yellow-50 text-yellow-700 border-yellow-100",
  Low: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

const statusStyles = {
  Pending: "bg-red-50 text-red-700",
  Assigned: "bg-blue-50 text-blue-700",
  Scheduled: "bg-purple-50 text-purple-700",
  Completed: "bg-emerald-50 text-emerald-700",
};

function Maintenance() {
  const location = useLocation();
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("All");
  const [tasks, setTasks] = useState(initialMaintenanceTasks);

  const selectedAsset = location.state?.asset;
  const shouldCreateTask = location.state?.createTask;

  // Add selected asset to maintenance queue
  const addToMaintenanceQueue = () => {
    if (!selectedAsset) return;

    const alreadyExists = tasks.some(
      (task) => task.asset === selectedAsset.id && task.status !== "Completed",
    );

    if (alreadyExists) {
      alert(`${selectedAsset.id} already has a maintenance task.`);
      return;
    }

    const newTask = {
      id: `MT-${String(tasks.length + 1).padStart(3, "0")}`,
      asset: selectedAsset.id,
      name: selectedAsset.name,
      location: selectedAsset.location,
      priority: selectedAsset.status,
      action:
        selectedAsset.status === "Critical"
          ? "Inspect cooling system and oil condition"
          : selectedAsset.status === "High"
            ? "Perform detailed inspection and preventive maintenance"
            : "Schedule routine asset inspection",
      reason: `Maintenance task created from the ${selectedAsset.id} asset risk analysis.`,
      urgency:
        selectedAsset.status === "Critical"
          ? "Immediate"
          : selectedAsset.status === "High"
            ? "Within 24 hours"
            : "Within 72 hours",
      crew: "Unassigned",
      status: "Pending",
      due: "Today",
    };

    setTasks((currentTasks) => [newTask, ...currentTasks]);

    // Close create-task panel
    navigate("/maintenance", { replace: true });
  };

  const markCompleted = (taskId) => {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === taskId ? { ...task, status: "Completed" } : task,
      ),
    );
  };

  const viewAsset = (assetId) => {
    navigate(`/assets/${assetId}`);
  };

  const closeCreateTask = () => {
    navigate("/maintenance", { replace: true });
  };

  const filteredTasks = tasks.filter((task) => {
    const searchValue = search.toLowerCase();

    const matchesSearch =
      task.asset.toLowerCase().includes(searchValue) ||
      task.name.toLowerCase().includes(searchValue) ||
      task.location.toLowerCase().includes(searchValue);

    const matchesPriority =
      priorityFilter === "All" || task.priority === priorityFilter;

    return matchesSearch && matchesPriority;
  });

  const pendingTasks = tasks.filter((task) => task.status !== "Completed");

  const criticalTasks = tasks.filter(
    (task) => task.priority === "Critical" && task.status !== "Completed",
  );

  const assignedTasks = tasks.filter(
    (task) => task.status === "Assigned" || task.status === "Scheduled",
  );

  const completedTasks = tasks.filter((task) => task.status === "Completed");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          Preventive Operations
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          Maintenance Management
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Prioritize maintenance actions based on asset risk and AI
          recommendations.
        </p>
      </div>

      {/* Create Task Panel */}
      {shouldCreateTask && selectedAsset && (
        <div className="rounded-2xl border border-blue-200 bg-white p-5 shadow-sm">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-blue-50 p-2.5 text-blue-600">
                <Wrench size={20} />
              </div>

              <div>
                <p className="text-sm font-bold text-slate-900">
                  Create Maintenance Task
                </p>

                <p className="text-xs text-slate-500">
                  Create a task for the selected asset
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={closeCreateTask}
              className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
            >
              <X size={19} />
            </button>
          </div>

          {/* Asset Information */}
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <TaskInfo label="Asset" value={selectedAsset.id} />

            <TaskInfo label="Asset Name" value={selectedAsset.name} />

            <TaskInfo label="Location" value={selectedAsset.location} />

            <TaskInfo
              label="Risk Score"
              value={`${selectedAsset.riskScore}/100`}
            />
          </div>

          {/* Recommended Action */}
          <div className="mt-5 rounded-xl bg-blue-50 p-4">
            <p className="text-xs font-bold uppercase tracking-wider text-blue-700">
              Recommended Action
            </p>

            <p className="mt-2 text-sm font-semibold text-slate-800">
              {selectedAsset.status === "Critical"
                ? "Immediate inspection of cooling system and oil condition"
                : selectedAsset.status === "High"
                  ? "Perform detailed inspection and preventive maintenance"
                  : "Schedule routine asset inspection"}
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Failure probability: {selectedAsset.failureProbability}%
            </p>
          </div>

          {/* Actions */}
          <div className="mt-4 flex flex-wrap justify-end gap-2">
            <button
              type="button"
              onClick={() => viewAsset(selectedAsset.id)}
              className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
            >
              View Asset
            </button>

            <button
              type="button"
              onClick={addToMaintenanceQueue}
              className="rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white hover:bg-blue-700 active:scale-95"
            >
              Add to Maintenance Queue
            </button>
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          label="Priority Actions"
          value={pendingTasks.length}
          description="Require attention"
          icon={AlertTriangle}
          iconClass="bg-red-50 text-red-600"
        />

        <SummaryCard
          label="Critical"
          value={criticalTasks.length}
          description="Immediate maintenance"
          icon={Wrench}
          iconClass="bg-red-50 text-red-600"
        />

        <SummaryCard
          label="Assigned"
          value={assignedTasks.length}
          description="Crew assigned"
          icon={UserRound}
          iconClass="bg-blue-50 text-blue-600"
        />

        <SummaryCard
          label="Completed"
          value={completedTasks.length}
          description="Tasks completed"
          icon={CheckCircle2}
          iconClass="bg-emerald-50 text-emerald-600"
        />
      </div>

      {/* AI Recommendation */}
      <div className="rounded-2xl border border-blue-100 bg-blue-50/60 p-5 shadow-sm">
        <div className="flex gap-4">
          <div className="rounded-xl bg-blue-600 p-3 text-white">
            <Wrench size={21} />
          </div>

          <div>
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-bold text-slate-900">
                AI Maintenance Recommendation
              </p>

              <span className="rounded-full bg-blue-100 px-2.5 py-1 text-[9px] font-bold text-blue-700">
                AI GENERATED
              </span>
            </div>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              TR-002 should be inspected immediately. Its high failure
              probability, abnormal temperature, vibration and partial discharge
              readings indicate elevated equipment risk.
            </p>

            <div className="mt-4 flex flex-wrap gap-3">
              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                Asset: TR-002
              </span>

              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-red-600">
                Priority: Critical
              </span>

              <span className="rounded-lg bg-white px-3 py-2 text-xs font-semibold text-slate-700">
                Crew: Crew A
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-900">
              Maintenance Tasks
            </p>

            <p className="mt-1 text-xs text-slate-500">
              AI-prioritized maintenance activities
            </p>
          </div>

          <div className="flex flex-col gap-3 sm:flex-row">
            <div className="relative">
              <Search
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search assets..."
                className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pl-9 pr-3 text-sm outline-none focus:border-blue-400 focus:bg-white sm:w-64"
              />
            </div>

            <select
              value={priorityFilter}
              onChange={(event) => setPriorityFilter(event.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5 text-sm text-slate-700 outline-none"
            >
              <option value="All">All Priorities</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>
        </div>
      </div>

      {/* Tasks */}
      <div className="space-y-4">
        {filteredTasks.map((task) => (
          <div
            key={task.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:shadow-md"
          >
            <div className="flex flex-col gap-5 xl:flex-row xl:justify-between">
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs font-bold text-slate-400">
                    {task.id}
                  </span>

                  <span
                    className={`rounded-full border px-2.5 py-1 text-[9px] font-bold ${priorityStyles[task.priority]}`}
                  >
                    {task.priority}
                  </span>

                  <span
                    className={`rounded-full px-2.5 py-1 text-[9px] font-bold ${statusStyles[task.status]}`}
                  >
                    {task.status}
                  </span>
                </div>

                <div className="mt-3">
                  <p className="text-base font-bold text-slate-900">
                    {task.asset} — {task.name}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">{task.location}</p>
                </div>

                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Recommended Action
                  </p>

                  <p className="mt-2 text-sm font-semibold text-slate-800">
                    {task.action}
                  </p>
                </div>

                <div className="mt-4 rounded-xl bg-slate-50 p-4">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    Why this action?
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-600">
                    {task.reason}
                  </p>
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-3 xl:w-[360px] xl:grid-cols-1">
                <InfoBox icon={Clock} label="Urgency" value={task.urgency} />

                <InfoBox
                  icon={UserRound}
                  label="Assigned Crew"
                  value={task.crew}
                />

                <InfoBox icon={Calendar} label="Due" value={task.due} />
              </div>
            </div>

            {/* Task Actions */}
            <div className="mt-5 flex flex-wrap justify-end gap-2 border-t border-slate-100 pt-4">
              {task.status !== "Completed" && (
                <button
                  type="button"
                  onClick={() => markCompleted(task.id)}
                  className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2.5 text-xs font-semibold text-emerald-700 hover:bg-emerald-600 hover:text-white"
                >
                  Mark Completed
                </button>
              )}

              <button
                type="button"
                onClick={() => viewAsset(task.asset)}
                className="rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white hover:bg-blue-700"
              >
                View Asset
              </button>
            </div>
          </div>
        ))}

        {filteredTasks.length === 0 && (
          <div className="rounded-2xl border border-slate-200 bg-white p-10 text-center">
            <p className="text-sm font-semibold text-slate-700">
              No maintenance tasks found
            </p>

            <p className="mt-1 text-xs text-slate-400">
              Try changing the search or priority filter.
            </p>
          </div>
        )}
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

function InfoBox({ icon: Icon, label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 p-3">
      <div className="flex items-center gap-2">
        <Icon size={15} className="text-slate-400" />

        <span className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
          {label}
        </span>
      </div>

      <p className="mt-2 text-sm font-bold text-slate-800">{value}</p>
    </div>
  );
}

function TaskInfo({ label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
      <p className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-bold text-slate-800">{value}</p>
    </div>
  );
}

export default Maintenance;
