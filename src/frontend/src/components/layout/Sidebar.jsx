import {
  Activity,
  Bot,
  Cloud,
  Gauge,
  LayoutDashboard,
  LogOut,
  Map,
  Settings,
  ShieldAlert,
  Users,
  Wrench,
  X,
} from "lucide-react";

import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../services/auth.jsx";

const navigation = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    name: "Assets",
    icon: Gauge,
    path: "/assets",
  },
  {
    name: "Risk Analysis",
    icon: ShieldAlert,
    path: "/risk",
  },
  {
    name: "Sensors",
    icon: Activity,
    path: "/sensors",
  },
  {
    name: "Weather",
    icon: Cloud,
    path: "/weather",
  },
  {
    name: "Maintenance",
    icon: Wrench,
    path: "/maintenance",
  },
  {
    name: "Crew",
    icon: Users,
    path: "/crew",
  },
  {
    name: "AI Assistant",
    icon: Bot,
    path: "/ai",
  },
];

function Sidebar({ isOpen, onClose }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    onClose();
    navigate("/login", { replace: true });
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/30 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed inset-y-0 left-0 z-50 flex w-64 flex-col
          border-r border-slate-200 bg-white
          transition-transform duration-300
          lg:translate-x-0
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Brand */}
        <div className="flex h-20 items-center justify-between border-b border-slate-200 px-5">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
              <Map size={21} />
            </div>

            <div>
              <h1 className="text-base font-bold tracking-wide text-slate-900">
                GridGuard
              </h1>

              <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-400">
                AI Operations
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700 lg:hidden"
          >
            <X size={20} />
          </button>

        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-5">
          <p className="px-3 pb-3 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">
            Operations
          </p>

          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) => `
                  flex w-full items-center gap-3 rounded-xl px-3 py-3
                  text-sm font-medium transition
                  ${
                    isActive
                      ? "bg-blue-50 text-blue-700"
                      : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                  }
                `}
              >
                {({ isActive }) => (
                  <>
                    <Icon size={19} strokeWidth={isActive ? 2.2 : 1.8} />

                    <span>{item.name}</span>

                    {item.name === "AI Assistant" && (
                      <span className="ml-auto rounded-md bg-blue-50 px-1.5 py-0.5 text-[9px] font-bold text-blue-600">
                        AI
                      </span>
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Bottom */}
        <div className="border-t border-slate-200 p-3">
          <button className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-900">
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <button onClick={handleLogout} className="mt-1 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50 hover:text-slate-900">
            <LogOut size={19} />
            <span>Logout</span>
          </button>

          <div className="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-3">
            <p className="text-xs font-semibold text-slate-700">Grid Status</p>

            <div className="mt-2 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />

              <span className="text-xs text-slate-500">System operational</span>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;
