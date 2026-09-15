import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Activity,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  Phone,
  ShieldCheck,
  Sparkles,
  UserRound,
  Zap,
} from "lucide-react";

function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    terms: false,
  });

  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const update = (field) => (event) => {
    const value =
      event.target.type === "checkbox"
        ? event.target.checked
        : event.target.value;

    setForm((current) => ({
      ...current,
      [field]: value,
    }));

    setErrors((current) => ({
      ...current,
      [field]: "",
      submit: "",
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const nextErrors = {};

    if (!form.name.trim()) {
      nextErrors.name = "Please enter your full name.";
    }

    if (!form.email.trim()) {
      nextErrors.email = "Please enter your email address.";
    } else if (!/^\S+@\S+\.\S+$/.test(form.email)) {
      nextErrors.email = "Enter a valid email address.";
    }

    if (!form.phone.trim()) {
      nextErrors.phone = "Please enter your phone number.";
    }

    if (!form.password) {
      nextErrors.password = "Please create a password.";
    } else if (form.password.length < 6) {
      nextErrors.password = "Use at least 6 characters.";
    }

    if (!form.confirmPassword) {
      nextErrors.confirmPassword = "Please confirm your password.";
    } else if (form.password !== form.confirmPassword) {
      nextErrors.confirmPassword = "Passwords do not match.";
    }

    if (!form.terms) {
      nextErrors.terms = "Please accept the Terms and Privacy Policy.";
    }

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    setIsSubmitting(true);

    window.setTimeout(() => {
      navigate("/login", { replace: true });
    }, 500);
  };

  return (
    <main className="min-h-screen bg-slate-50 lg:grid lg:grid-cols-[minmax(0,1fr)_minmax(520px,0.9fr)]">
      <BrandPanel />

      <section className="flex min-h-screen items-center justify-center px-4 py-6 sm:px-8">
        <div className="w-full max-w-2xl">
          {/* Mobile branding */}
          <Link
            to="/login"
            className="mb-5 flex w-fit items-center gap-2 text-slate-900 lg:hidden"
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
              <Zap size={21} fill="currentColor" />
            </span>

            <span className="text-lg font-bold">GridGuard AI</span>
          </Link>

          {/* Signup Card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
            {/* Heading */}
            <div>
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white">
                <Zap size={20} fill="currentColor" />
              </span>

              <div className="mt-4">
                <p className="text-sm font-semibold text-blue-600">
                  Create your portal account
                </p>

                <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
                  Join GridGuard AI
                </h1>

                <p className="mt-1.5 text-sm leading-5 text-slate-500">
                  Create your account to access the GridGuard AI customer
                  portal.
                </p>
              </div>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="mt-5" noValidate>
              {/* Row 1 */}
              <div className="grid gap-4 sm:grid-cols-2">
                <SignupField
                  id="name"
                  label="Full Name"
                  placeholder="Enter your full name"
                  icon={UserRound}
                  type="text"
                  value={form.name}
                  onChange={update("name")}
                  error={errors.name}
                />

                <SignupField
                  id="email"
                  label="Email Address"
                  placeholder="Enter your email address"
                  icon={Mail}
                  type="email"
                  value={form.email}
                  onChange={update("email")}
                  error={errors.email}
                />
              </div>

              {/* Row 2 */}
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <SignupField
                  id="phone"
                  label="Phone Number"
                  placeholder="Enter your phone number"
                  icon={Phone}
                  type="tel"
                  value={form.phone}
                  onChange={update("phone")}
                  error={errors.phone}
                />

                <div>
                  <SignupField
                    id="password"
                    label="Password"
                    placeholder="Create a password"
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
                        {showPassword ? (
                          <EyeOff size={17} />
                        ) : (
                          <Eye size={17} />
                        )}
                      </button>
                    }
                  />

                  {!errors.password && (
                    <p className="mt-1 text-xs text-slate-400">
                      Minimum 6 characters.
                    </p>
                  )}
                </div>
              </div>

              {/* Row 3 */}
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <SignupField
                  id="confirmPassword"
                  label="Confirm Password"
                  placeholder="Confirm your password"
                  icon={LockKeyhole}
                  type={showConfirmPassword ? "text" : "password"}
                  value={form.confirmPassword}
                  onChange={update("confirmPassword")}
                  error={errors.confirmPassword}
                  trailing={
                    <button
                      type="button"
                      onClick={() =>
                        setShowConfirmPassword(!showConfirmPassword)
                      }
                      aria-label={
                        showConfirmPassword ? "Hide password" : "Show password"
                      }
                      className="rounded-md p-1 text-slate-400 hover:text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-200"
                    >
                      {showConfirmPassword ? (
                        <EyeOff size={17} />
                      ) : (
                        <Eye size={17} />
                      )}
                    </button>
                  }
                />

                {/* Terms */}
                <div className="flex items-center">
                  <div>
                    <label className="flex cursor-pointer items-start gap-2.5">
                      <input
                        type="checkbox"
                        checked={form.terms}
                        onChange={update("terms")}
                        className="mt-0.5 h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                      />

                      <span className="text-xs leading-5 text-slate-500">
                        I agree to the{" "}
                        <button
                          type="button"
                          className="font-semibold text-blue-600 hover:text-blue-700"
                        >
                          Terms of Service
                        </button>{" "}
                        and{" "}
                        <button
                          type="button"
                          className="font-semibold text-blue-600 hover:text-blue-700"
                        >
                          Privacy Policy
                        </button>
                        .
                      </span>
                    </label>

                    {errors.terms && (
                      <p className="mt-1 text-xs text-red-600">
                        {errors.terms}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={isSubmitting}
                className="mt-5 w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-200 focus:ring-offset-2 active:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-300"
              >
                {isSubmitting ? "Creating Account..." : "Create Account"}
              </button>
            </form>

            {/* Login */}
            <p className="mt-4 text-center text-sm text-slate-500">
              Already have an account?{" "}
              <Link
                to="/login"
                className="font-semibold text-blue-600 hover:text-blue-700 focus:outline-none focus:underline"
              >
                Sign in
              </Link>
            </p>

            {/* Footer */}
            <p className="mt-4 border-t border-slate-100 pt-4 text-center text-xs text-slate-400">
              GridGuard AI · Secure customer registration
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}

/* -------------------------------------------------------
   BRAND PANEL
------------------------------------------------------- */

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

/* -------------------------------------------------------
   SIGNUP FIELD
------------------------------------------------------- */

function SignupField({
  id,
  label,
  icon: Icon,
  type,
  value,
  onChange,
  error,
  placeholder,
  trailing,
}) {
  return (
    <div>
      <label
        htmlFor={id}
        className="block text-sm font-semibold text-slate-700"
      >
        {label}
      </label>

      <div className="relative mt-1.5">
        <Icon
          size={17}
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
          } text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 ${
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
        <p id={`${id}-error`} className="mt-1 text-xs text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}

export default Signup;
