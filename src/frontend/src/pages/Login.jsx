import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import {
  Activity,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
  Zap,
} from "lucide-react";
import { useAuth } from "../services/auth.jsx";

function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  if (user)
    return <Navigate to={user.role === "admin" ? "/" : "/user"} replace />;
  const update = (field) => (event) => {
    setForm({ ...form, [field]: event.target.value });
    setErrors((current) => ({ ...current, [field]: "", credentials: "" }));
  };
  const useDemo = (email, password) => {
    setForm({ email, password });
    setErrors({});
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    const nextErrors = {};
    if (!form.email.trim())
      nextErrors.email = "Please enter your email address.";
    if (!form.password) nextErrors.password = "Please enter your password.";
    if (Object.keys(nextErrors).length) {
      setErrors(nextErrors);
      return;
    }
    setIsSubmitting(true);
    window.setTimeout(() => {
      const authenticatedUser = login(form.email, form.password);
      if (!authenticatedUser) {
        setErrors({
          credentials:
            "Invalid email or password. Please check your credentials and try again.",
        });
        setIsSubmitting(false);
        return;
      }
      navigate(authenticatedUser.role === "admin" ? "/" : "/user", {
        replace: true,
      });
    }, 350);
  };
  return (
    <main className="min-h-screen bg-slate-50 lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(460px,0.9fr)]">
      <BrandPanel />
      <section className="flex min-h-screen items-center justify-center px-4 py-10 sm:px-8">
        <div className="w-full max-w-md">
          <Link
            to="/login"
            className="mb-8 flex w-fit items-center gap-2 text-slate-900 lg:hidden"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
              <Zap size={21} fill="currentColor" />
            </span>
            <span className="text-lg font-bold">GridGuard AI</span>
          </Link>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
            <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600 text-white">
              <Zap size={22} fill="currentColor" />
            </span>
            <div className="mt-6">
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                Welcome back
              </h1>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                Sign in to continue to your GridGuard AI workspace.
              </p>
            </div>
            <form onSubmit={handleSubmit} className="mt-7 space-y-5" noValidate>
              <LoginField
                id="email"
                label="Email Address"
                placeholder="Enter your email address"
                icon={Mail}
                type="email"
                value={form.email}
                onChange={update("email")}
                error={errors.email}
              />
              <LoginField
                id="password"
                label="Password"
                placeholder="Enter your Password"
                icon={LockKeyhole}
                type={showPassword ? "text" : "password"}
                value={form.password}
                onChange={update("password")}
                error={errors.password}
                trailing={
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={
                      showPassword ? "Hide password" : "Show password"
                    }
                    className="rounded-md p-1 text-slate-400 hover:text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-200"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                }
              />
              {errors.credentials && (
                <p
                  role="alert"
                  className="rounded-lg border border-red-200 bg-red-50 px-3 py-2.5 text-sm leading-5 text-red-700"
                >
                  {errors.credentials}
                </p>
              )}
              <button
                disabled={isSubmitting}
                className="w-full rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:ring-offset-2 active:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-300"
              >
                {isSubmitting ? "Signing in..." : "Sign In"}
              </button>
            </form>
            <DemoAccess onUse={useDemo} />
            <p className="mt-6 text-center text-sm text-slate-500">
              Don&apos;t have an account?{" "}
              <Link
                to="/signup"
                className="font-semibold text-blue-600 hover:text-blue-700 focus:outline-none focus:underline"
              >
                Sign up
              </Link>
            </p>
            <p className="mt-6 border-t border-slate-100 pt-5 text-center text-xs text-slate-400">
              GridGuard AI · Secure operator and customer access
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

function BrandPanel() {
  const capabilities = [
    [Sparkles, "Predictive Risk Intelligence"],
    [Activity, "Real-time Grid Monitoring"],
    [ShieldCheck, "AI-powered Recommendations"],
  ];
  return (
    <section className="relative hidden overflow-hidden bg-slate-900 px-10 py-12 text-white lg:flex lg:flex-col lg:justify-between xl:px-16">
      <div className="absolute inset-0 opacity-30" aria-hidden="true">
        <span className="absolute left-[13%] top-[20%] h-2 w-2 rounded-full bg-blue-300" />
        <span className="absolute left-[31%] top-[32%] h-2 w-2 rounded-full bg-blue-300" />
        <span className="absolute left-[53%] top-[18%] h-2 w-2 rounded-full bg-blue-300" />
        <span className="absolute left-[70%] top-[40%] h-2 w-2 rounded-full bg-blue-300" />
        <span className="absolute left-[45%] top-[62%] h-2 w-2 rounded-full bg-blue-300" />
        <span className="absolute left-[17%] top-[20.5%] h-px w-[15%] rotate-[22deg] bg-blue-300" />
        <span className="absolute left-[34%] top-[31%] h-px w-[18%] -rotate-[26deg] bg-blue-300" />
        <span className="absolute left-[55%] top-[19%] h-px w-[15%] rotate-[44deg] bg-blue-300" />
      </div>
      <Link to="/login" className="relative flex w-fit items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
          <Zap size={21} fill="currentColor" />
        </span>
        <span>
          <span className="block text-lg font-bold">GridGuard AI</span>
          <span className="block text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-400">
            Power Grid Intelligence
          </span>
        </span>
      </Link>
      <div className="relative max-w-xl">
        <p className="text-sm font-semibold text-blue-300">
          Power Grid Intelligence Platform
        </p>
        <h2 className="mt-4 text-4xl font-bold leading-tight tracking-tight">
          Predictive intelligence for a more resilient power grid.
        </h2>
        <p className="mt-5 max-w-lg text-base leading-7 text-slate-300">
          Monitor grid health, identify emerging risks, and make faster
          maintenance decisions with AI-powered insights.
        </p>
        <div className="mt-9 space-y-4">
          {capabilities.map(([Icon, label]) => (
            <div
              key={label}
              className="flex items-center gap-3 text-sm font-medium text-slate-200"
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-700 bg-slate-800">
                <Icon size={16} className="text-blue-300" />
              </span>
              {label}
            </div>
          ))}
        </div>
      </div>
      <p className="relative text-xs text-slate-500">
        GridGuard AI · Operational intelligence for modern utilities
      </p>
    </section>
  );
}
function LoginField({
  id,
  label,
  icon: Icon,
  type,
  value,
  onChange,
  error,
  trailing,
  placeholder,
}) {
  return (
    <div>
      <label
        htmlFor={id}
        className="block text-sm font-semibold text-slate-700"
      >
        {label}
      </label>

      <div className="relative mt-2">
        <Icon
          size={18}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />

        <input
          id={id}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${id}-error` : undefined}
          className={`w-full rounded-lg border py-2.5 pl-10 ${
            trailing ? "pr-11" : "pr-3"
          } text-slate-900 outline-none transition
          placeholder:text-slate-400
          focus:border-blue-500
          focus:ring-2
          focus:ring-blue-100
          ${
            error ? "border-red-300 bg-red-50/30" : "border-slate-300 bg-white"
          }`}
        />

        {trailing && (
          <span className="absolute right-2 top-1/2 -translate-y-1/2">
            {trailing}
          </span>
        )}
      </div>

      {error && (
        <p id={`${id}-error`} className="mt-1.5 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}
function DemoAccess({ onUse }) {
  return (
    <div className="mt-7 border-t border-slate-100 pt-5">
      <p className="text-xs font-bold uppercase tracking-[0.14em] text-slate-400">
        Demo Access
      </p>
      <p className="mt-1 text-xs text-slate-500">
        Use a demo workspace account to explore the platform.
      </p>
      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        <button
          type="button"
          onClick={() => onUse("admin@gridguard.ai", "admin123")}
          className="rounded-lg border border-slate-200 p-3 text-left transition hover:border-blue-200 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-100"
        >
          <span className="block text-sm font-semibold text-slate-800">
            Admin Demo
          </span>
          <span className="mt-1 block text-xs text-slate-500">
            admin@gridguard.ai
          </span>
        </button>
        <button
          type="button"
          onClick={() => onUse("user@gridguard.ai", "user123")}
          className="rounded-lg border border-slate-200 p-3 text-left transition hover:border-blue-200 hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-100"
        >
          <span className="block text-sm font-semibold text-slate-800">
            User Demo
          </span>
          <span className="mt-1 block text-xs text-slate-500">
            user@gridguard.ai
          </span>
        </button>
      </div>
    </div>
  );
}

function AuthPage({ children }) {
  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10 sm:flex sm:items-center sm:justify-center">
      <div className="w-full max-w-md">
        <Link
          to="/login"
          className="mb-8 flex items-center justify-center gap-2 text-slate-900"
        >
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
            <Zap size={21} fill="currentColor" />
          </span>
          <span className="text-lg font-bold">GridGuard AI</span>
        </Link>
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          {children}
        </section>
      </div>
    </div>
  );
}
function Field({ label, icon: Icon, type, value, onChange }) {
  return (
    <label className="block text-sm font-medium text-slate-700">
      {label}
      <span className="relative mt-2 block">
        <Icon
          size={18}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />
        <input
          required
          type={type}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className="w-full rounded-lg border border-slate-300 py-2.5 pl-10 pr-3 text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </span>
    </label>
  );
}
export { AuthPage, Field };
export default Login;
