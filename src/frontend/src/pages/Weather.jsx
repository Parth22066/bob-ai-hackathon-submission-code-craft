import {
  CloudRain,
  CloudSun,
  Droplets,
  Gauge,
  MapPin,
  Thermometer,
  Wind,
  AlertTriangle,
  ShieldCheck,
} from "lucide-react";

const weather = {
  temperature: 32,
  rainfall: 18,
  windSpeed: 42,
  humidity: 78,
  stormRisk: "High",
  affectedAssets: 12,
};

const forecast = [
  { day: "Today", temp: "32°C", rain: "18 mm", wind: "42 km/h", risk: "High" },
  {
    day: "Tomorrow",
    temp: "31°C",
    rain: "12 mm",
    wind: "36 km/h",
    risk: "Medium",
  },
  { day: "Wed", temp: "30°C", rain: "8 mm", wind: "29 km/h", risk: "Medium" },
  { day: "Thu", temp: "33°C", rain: "4 mm", wind: "24 km/h", risk: "Low" },
  { day: "Fri", temp: "34°C", rain: "2 mm", wind: "21 km/h", risk: "Low" },
];

const affectedAreas = [
  {
    area: "Vadodara Central",
    risk: "Critical",
    assets: 5,
    reason: "Strong wind and rainfall may increase transformer stress.",
  },
  {
    area: "Makarpura Industrial Zone",
    risk: "High",
    assets: 4,
    reason: "High wind conditions may affect exposed grid equipment.",
  },
  {
    area: "Nizampura",
    risk: "Medium",
    assets: 2,
    reason: "Rainfall may increase equipment and feeder risk.",
  },
  {
    area: "Waghodia",
    risk: "Low",
    assets: 1,
    reason: "Weather conditions currently have limited impact.",
  },
];

const riskStyles = {
  Critical: "bg-red-50 text-red-700 border-red-100",
  High: "bg-orange-50 text-orange-700 border-orange-100",
  Medium: "bg-yellow-50 text-yellow-700 border-yellow-100",
  Low: "bg-emerald-50 text-emerald-700 border-emerald-100",
};

function Weather() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          Environmental Intelligence
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          Weather Intelligence
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Monitor weather conditions and understand their potential impact on
          grid assets.
        </p>
      </div>

      {/* Current Conditions */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <WeatherCard
          label="Temperature"
          value={`${weather.temperature}°C`}
          description="Current grid region"
          icon={Thermometer}
          iconClass="bg-orange-50 text-orange-600"
        />

        <WeatherCard
          label="Rainfall"
          value={`${weather.rainfall} mm`}
          description="Recent rainfall"
          icon={CloudRain}
          iconClass="bg-blue-50 text-blue-600"
        />

        <WeatherCard
          label="Wind Speed"
          value={`${weather.windSpeed} km/h`}
          description="Current wind conditions"
          icon={Wind}
          iconClass="bg-slate-100 text-slate-600"
        />

        <WeatherCard
          label="Humidity"
          value={`${weather.humidity}%`}
          description="Current humidity"
          icon={Droplets}
          iconClass="bg-cyan-50 text-cyan-600"
        />
      </div>

      {/* Main Weather Risk */}
      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Weather Risk Assessment
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Current environmental conditions affecting grid operations
              </p>
            </div>

            <span className="flex w-fit items-center gap-2 rounded-full border border-orange-100 bg-orange-50 px-3 py-1.5 text-xs font-bold text-orange-700">
              <AlertTriangle size={14} />
              High Risk
            </span>
          </div>

          <div className="mt-6 grid gap-5 md:grid-cols-2">
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-orange-50 p-3 text-orange-600">
                  <CloudSun size={22} />
                </div>

                <div>
                  <p className="text-xs text-slate-500">Storm Risk</p>
                  <p className="text-xl font-bold text-slate-900">
                    {weather.stormRisk}
                  </p>
                </div>
              </div>

              <p className="mt-4 text-xs leading-5 text-slate-500">
                Strong wind, rainfall and humidity may increase stress on
                exposed grid assets.
              </p>
            </div>

            <div className="rounded-xl border border-slate-200 bg-slate-50 p-5">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-red-50 p-3 text-red-600">
                  <Gauge size={22} />
                </div>

                <div>
                  <p className="text-xs text-slate-500">
                    Potentially Affected Assets
                  </p>

                  <p className="text-xl font-bold text-slate-900">
                    {weather.affectedAssets}
                  </p>
                </div>
              </div>

              <p className="mt-4 text-xs leading-5 text-slate-500">
                Assets with increased environmental risk based on current
                weather conditions.
              </p>
            </div>
          </div>

          {/* Risk Meter */}
          <div className="mt-6">
            <div className="flex items-center justify-between">
              <p className="text-xs font-semibold text-slate-700">
                Environmental Risk Level
              </p>

              <p className="text-xs font-bold text-orange-600">78 / 100</p>
            </div>

            <div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100">
              <div className="h-full w-[78%] rounded-full bg-orange-500" />
            </div>

            <div className="mt-2 flex justify-between text-[10px] text-slate-400">
              <span>Low</span>
              <span>Medium</span>
              <span>High</span>
              <span>Critical</span>
            </div>
          </div>
        </div>

        {/* Location */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-blue-50 p-3 text-blue-600">
              <MapPin size={22} />
            </div>

            <div>
              <p className="text-xs text-slate-500">Monitoring Region</p>

              <p className="text-lg font-bold text-slate-900">
                Vadodara Grid Region
              </p>
            </div>
          </div>

          <div className="mt-6 space-y-4">
            <WeatherMetric label="Temperature" value="32°C" percentage="64%" />

            <WeatherMetric label="Rainfall" value="18 mm" percentage="45%" />

            <WeatherMetric label="Wind" value="42 km/h" percentage="70%" />

            <WeatherMetric label="Humidity" value="78%" percentage="78%" />
          </div>

          <div className="mt-6 rounded-xl border border-emerald-100 bg-emerald-50 p-4">
            <div className="flex gap-3">
              <ShieldCheck
                size={18}
                className="mt-0.5 shrink-0 text-emerald-600"
              />

              <div>
                <p className="text-xs font-bold text-emerald-700">
                  Monitoring Active
                </p>

                <p className="mt-1 text-[11px] leading-5 text-emerald-700/80">
                  Weather conditions are being continuously evaluated against
                  asset risk.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Forecast */}
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Weather Forecast
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Expected environmental conditions for the upcoming days
          </p>
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-5">
          {forecast.map((item) => (
            <div
              key={item.day}
              className="rounded-xl border border-slate-200 p-4"
            >
              <p className="text-xs font-bold text-slate-900">{item.day}</p>

              <div className="mt-4 flex items-center gap-2">
                <CloudRain size={18} className="text-blue-500" />

                <p className="text-lg font-bold text-slate-900">{item.temp}</p>
              </div>

              <div className="mt-4 space-y-2 text-[11px] text-slate-500">
                <div className="flex justify-between">
                  <span>Rain</span>
                  <span className="font-semibold text-slate-700">
                    {item.rain}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span>Wind</span>
                  <span className="font-semibold text-slate-700">
                    {item.wind}
                  </span>
                </div>
              </div>

              <div className="mt-4">
                <span
                  className={`rounded-full border px-2 py-1 text-[9px] font-bold ${riskStyles[item.risk]}`}
                >
                  {item.risk} Risk
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Affected Areas */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-200 p-5">
          <p className="text-sm font-semibold text-slate-900">
            Weather Impact by Area
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Grid locations with increased weather-related risk
          </p>
        </div>

        <div className="divide-y divide-slate-100">
          {affectedAreas.map((area) => (
            <div
              key={area.area}
              className="flex flex-col gap-4 p-5 lg:flex-row lg:items-center lg:justify-between"
            >
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="text-sm font-bold text-slate-900">
                    {area.area}
                  </p>

                  <span
                    className={`rounded-full border px-2.5 py-1 text-[9px] font-bold ${riskStyles[area.risk]}`}
                  >
                    {area.risk}
                  </span>
                </div>

                <p className="mt-1 text-xs text-slate-500">{area.reason}</p>
              </div>

              <div className="shrink-0 rounded-xl bg-slate-50 px-4 py-3">
                <p className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
                  Assets affected
                </p>

                <p className="mt-1 text-lg font-bold text-slate-900">
                  {area.assets}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function WeatherCard({ label, value, description, icon: Icon, iconClass }) {
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

function WeatherMetric({ label, value, percentage }) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-500">{label}</span>

        <span className="text-xs font-bold text-slate-700">{value}</span>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-blue-500"
          style={{ width: percentage }}
        />
      </div>
    </div>
  );
}

export default Weather;
