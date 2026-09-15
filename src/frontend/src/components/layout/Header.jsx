import { Bell, Menu, Search, ChevronDown } from "lucide-react";

import { useLocation } from "react-router-dom";

function Header({ onMenuClick }) {
  const location = useLocation();

  const pageTitles = {
    "/": "Dashboard",
    "/assets": "Assets",
    "/risk": "Risk Analysis",
    "/sensors": "Sensors",
    "/weather": "Weather",
    "/maintenance": "Maintenance",
    "/crew": "Crew",
    "/ai": "AI Assistant",
  };

  const pageTitle = pageTitles[location.pathname] || "Dashboard";

  return (
    <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white px-4 md:px-6 lg:ml-64">
      {/* Left */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900 lg:hidden"
        >
          <Menu size={22} />
        </button>

        <div>
          <p className="text-xs font-medium text-slate-400">Grid Operations</p>

          <h2 className="text-lg font-semibold text-slate-900">{pageTitle}</h2>
        </div>
      </div>

      {/* Right */}
      <div className="flex items-center gap-2 md:gap-4">
        {/* Search */}
        <div className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
          <Search size={17} className="text-slate-400" />

          <input
            type="text"
            placeholder="Search assets..."
            className="w-40 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
          />

          <span className="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] text-slate-400">
            /
          </span>
        </div>

        {/* Mobile Search */}
        <button className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900 md:hidden">
          <Search size={20} />
        </button>

        {/* Notifications */}
        <button className="relative rounded-xl p-2.5 text-slate-500 hover:bg-slate-100 hover:text-slate-900">
          <Bell size={20} />

          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500 ring-2 ring-white" />
        </button>

        {/* Divider */}
        <div className="hidden h-8 w-px bg-slate-200 sm:block" />

        {/* Operator */}
        <button className="flex items-center gap-2 rounded-xl p-1.5 hover:bg-slate-50">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-sm font-bold text-white">
            OP
          </div>

          <div className="hidden text-left sm:block">
            <p className="text-sm font-semibold text-slate-800">Operator</p>

            <p className="text-[11px] text-slate-400">Control Room</p>
          </div>

          <ChevronDown size={16} className="hidden text-slate-400 sm:block" />
        </button>
      </div>
    </header>
  );
}

export default Header;
