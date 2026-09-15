import { AlertTriangle, ArrowRight, CloudRain, Gauge, ShieldAlert, Users, Wrench } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { criticalAssets } from "../data/mockData";

const riskDistribution = [{ level: "Low", assets: 103 }, { level: "Medium", assets: 18 }, { level: "High", assets: 18 }, { level: "Critical", assets: 7 }];
const decisionSteps = [
  ["Sensor data", "79°C temperature, 49 mm/s vibration and 36 pC discharge", "Abnormal"],
  ["Anomaly detection", "Three sensor signals are above their operating baseline", "Detected"],
  ["Failure probability", "TR-002 is estimated at 87% likelihood of failure", "87%"],
  ["Weather risk", "High humidity and strong winds increase equipment stress", "High"],
  ["Asset risk score", "Combined operational risk for Central Grid Transformer", "92 / 100"],
  ["Grid impact", "Vadodara Central could affect 5,200 customers", "Critical"],
  ["Maintenance priority", "Inspect cooling system and oil condition immediately", "Immediate"],
];
const styleFor = { Critical: "bg-red-50 text-red-700 border-red-100", High: "bg-orange-50 text-orange-700 border-orange-100" };

function RiskAnalysis() {
  const navigate = useNavigate();
  const createTask = (asset) => navigate("/maintenance", { state: { createTask: true, asset } });
  return <div className="space-y-6">
    <div><p className="text-sm font-medium text-blue-600">Predictive Risk Intelligence</p><h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">Risk Analysis</h1><p className="mt-1 text-sm text-slate-500">Trace how GridGuard AI translates operating signals into a prioritized field action.</p></div>
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <SummaryCard label="Overall Grid Risk" value="72 / 100" description="High operational risk" icon={ShieldAlert} iconClass="bg-orange-50 text-orange-600" />
      <SummaryCard label="TR-002 Risk Score" value="92 / 100" description="Central Grid Transformer" icon={AlertTriangle} iconClass="bg-red-50 text-red-600" />
      <SummaryCard label="Failure Probability" value="87%" description="Immediate inspection advised" icon={Gauge} iconClass="bg-red-50 text-red-600" />
      <SummaryCard label="Customers at Risk" value="5,200" description="Vadodara Central impact" icon={Users} iconClass="bg-blue-50 text-blue-600" />
    </div>
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><p className="text-sm font-semibold text-slate-900">GridGuard AI decision flow</p><p className="mt-1 text-xs text-slate-500">Mock operational intelligence for the highest-risk asset, TR-002.</p></div><span className="w-fit rounded-full border border-red-100 bg-red-50 px-3 py-1 text-xs font-bold text-red-700">Critical maintenance priority</span></div>
      <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-4">{decisionSteps.map(([title, description, value], index) => <div key={title} className="relative rounded-xl border border-slate-200 bg-slate-50 p-4"><p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{String(index + 1).padStart(2, "0")}</p><p className="mt-2 text-sm font-bold text-slate-900">{title}</p><p className="mt-2 min-h-10 text-xs leading-5 text-slate-500">{description}</p><span className="mt-3 inline-flex rounded-lg bg-white px-2.5 py-1 text-xs font-bold text-blue-700 shadow-sm">{value}</span>{index < decisionSteps.length - 1 && <ArrowRight size={16} className="absolute -right-5 top-1/2 hidden -translate-y-1/2 text-slate-300 xl:block" />}</div>)}</div>
    </section>
    <div className="grid gap-6 xl:grid-cols-[1.15fr_.85fr]">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm font-semibold text-slate-900">Risk Distribution</p><p className="mt-1 text-xs text-slate-500">Monitored assets by current risk level</p><div className="mt-5 h-72"><ResponsiveContainer width="100%" height="100%"><BarChart data={riskDistribution}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="level" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} /><YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} /><Tooltip /><Bar dataKey="assets" fill="#2563eb" radius={[6, 6, 0, 0]} /></BarChart></ResponsiveContainer></div></div>
      <div className="rounded-2xl border border-orange-100 bg-orange-50/60 p-5 shadow-sm"><div className="flex items-center gap-2"><CloudRain size={18} className="text-orange-600" /><p className="text-sm font-semibold text-slate-900">Recommended action</p></div><p className="mt-4 text-lg font-bold text-slate-900">Inspect TR-002 cooling system and oil condition.</p><p className="mt-3 text-sm leading-6 text-slate-600">Temperature, vibration and partial-discharge anomalies are amplified by high weather risk. Dispatch Crew A, 1.2 km away, before the next operating cycle.</p><div className="mt-5 grid grid-cols-2 gap-3"><Metric label="Weather risk" value="High" /><Metric label="Recommended crew" value="Crew A" /><Metric label="Grid impact" value="Critical" /><Metric label="Affected customers" value="5,200" /></div><div className="mt-5 flex flex-wrap gap-2"><Link to="/assets/TR-002" className="rounded-xl border border-blue-200 bg-white px-4 py-2.5 text-xs font-semibold text-blue-700">View TR-002</Link><button onClick={() => createTask(criticalAssets[0])} className="rounded-xl bg-blue-600 px-4 py-2.5 text-xs font-semibold text-white hover:bg-blue-700"><Wrench size={14} className="mr-1 inline" />Create task</button></div></div>
    </div>
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"><div className="border-b border-slate-200 p-5"><p className="text-sm font-semibold text-slate-900">At-risk assets</p><p className="mt-1 text-xs text-slate-500">Ranked by predicted failure and potential grid impact.</p></div><div className="overflow-x-auto"><table className="min-w-[760px] w-full"><thead><tr className="bg-slate-50 text-left text-[11px] uppercase tracking-wider text-slate-400"><th className="px-5 py-3">Asset</th><th className="px-5 py-3">Risk</th><th className="px-5 py-3">Failure probability</th><th className="px-5 py-3">Grid impact</th><th className="px-5 py-3">Action</th></tr></thead><tbody>{criticalAssets.map((asset) => <tr key={asset.id} className="border-t border-slate-100"><td className="px-5 py-4"><p className="font-bold text-slate-900">{asset.id}</p><p className="text-xs text-slate-500">{asset.name} · {asset.location}</p></td><td className="px-5 py-4 text-sm font-bold">{asset.riskScore}/100</td><td className="px-5 py-4 text-sm font-semibold">{asset.failureProbability}%</td><td className="px-5 py-4"><span className={`rounded-full border px-2.5 py-1 text-[10px] font-bold ${styleFor[asset.status]}`}>{asset.status}</span></td><td className="px-5 py-4"><Link className="text-xs font-semibold text-blue-700 hover:text-blue-800" to={`/assets/${asset.id}`}>Review asset</Link></td></tr>)}</tbody></table></div></div>
  </div>;
}
function SummaryCard({ label, value, description, icon: Icon, iconClass }) { return <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-center justify-between"><p className="text-sm font-medium text-slate-500">{label}</p><div className={`rounded-xl p-2.5 ${iconClass}`}><Icon size={19} /></div></div><p className="mt-4 text-3xl font-bold text-slate-900">{value}</p><p className="mt-1 text-xs text-slate-500">{description}</p></div>; }
function Metric({ label, value }) { return <div className="rounded-xl border border-orange-100 bg-white p-3"><p className="text-[10px] uppercase tracking-wider text-slate-400">{label}</p><p className="mt-1 text-sm font-bold text-slate-800">{value}</p></div>; }
export default RiskAnalysis;
