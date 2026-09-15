import { Bell, FileWarning, LayoutDashboard, LogOut, Menu, TriangleAlert, UserRound, Wrench, Zap } from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../../services/auth.jsx";

const navigation = [
  ["Dashboard", "/user", LayoutDashboard], ["My Service", "/user/service", Zap],
  ["Outages", "/user/outages", TriangleAlert], ["Alerts", "/user/alerts", Bell],
  ["Report Issue", "/user/report", Wrench],
];

function UserLayout() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-64 flex-col border-r border-slate-200 bg-white lg:flex">
        <NavLink to="/user" className="flex h-20 items-center gap-2.5 border-b border-slate-200 px-5">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white"><Zap size={19} fill="currentColor" /></span>
          <span><span className="block text-sm font-bold">GridGuard AI</span><span className="block text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">Customer Portal</span></span>
        </NavLink>
        <nav className="flex-1 space-y-1 px-3 py-5">{navigation.map(([name, path, Icon]) => <NavLink key={path} to={path} end={path === "/user"} className={({ isActive }) => `flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium ${isActive ? "bg-blue-50 text-blue-700" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"}`}><Icon size={18} />{name}</NavLink>)}</nav>
        <div className="border-t border-slate-200 p-3"><NavLink to="/user/profile" className="mb-2 flex items-center gap-3 rounded-xl px-3 py-2 hover:bg-slate-50"><span className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-600"><UserRound size={16} /></span><span className="min-w-0"><span className="block truncate text-sm font-semibold">GridGuard Customer</span><span className="block text-xs text-slate-400">Profile</span></span></NavLink><button onClick={handleLogout} className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 hover:bg-slate-50"><LogOut size={18} />Logout</button></div>
      </aside>
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white lg:ml-64">
        <div className="flex h-16 items-center justify-between px-4 sm:px-6">
          <NavLink to="/user" className="flex items-center gap-2.5 lg:hidden">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-white">
              <Zap size={19} fill="currentColor" />
            </span>
            <span>
              <span className="block text-sm font-bold">GridGuard AI</span>
              <span className="block text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400">Customer Portal</span>
            </span>
          </NavLink>
          <div className="flex items-center gap-2">
            <button aria-label="Notifications" className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"><Bell size={19} /></button>
            <button onClick={() => setIsMenuOpen((open) => !open)} className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden" aria-label="Toggle navigation"><Menu size={21} /></button>
            <button onClick={handleLogout} className="hidden items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 sm:flex lg:hidden"><LogOut size={17} /> Logout</button>
          </div>
        </div>
        <nav className={`${isMenuOpen ? "flex" : "hidden"} flex-col gap-1 border-t border-slate-100 px-4 py-3 lg:hidden`}>
          {navigation.map(([name, path, Icon]) => <NavLink key={path} to={path} end={path === "/user"} onClick={() => setIsMenuOpen(false)} className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium ${isActive ? "bg-blue-50 text-blue-700" : "text-slate-600 hover:bg-slate-50"}`}><Icon size={17} />{name}</NavLink>)}
          <NavLink to="/user/profile" onClick={() => setIsMenuOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50"><UserRound size={17} />Profile</NavLink>
          <button onClick={handleLogout} className="flex items-center gap-2 rounded-lg px-3 py-2.5 text-left text-sm font-medium text-slate-600 hover:bg-slate-50"><LogOut size={17} /> Logout</button>
        </nav>
      </header>
      <main className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:ml-64 lg:w-[calc(100%-16rem)]"><Outlet /></main>
      <footer className="mx-auto flex max-w-7xl items-center gap-2 px-4 pb-6 text-xs text-slate-400 sm:px-6 lg:ml-64 lg:w-[calc(100%-16rem)]"><FileWarning size={14} /> Need urgent help? Report an outage through your local utility emergency line.</footer>
    </div>
  );
}

export default UserLayout;
