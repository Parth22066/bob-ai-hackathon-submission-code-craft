import {
  CloudRain,
  Droplets,
  Wind,
  Thermometer,
  CloudLightning,
  AlertTriangle,
} from "lucide-react";

const weatherData = {
  temperature: 32,
  rainfall: 18,
  windSpeed: 42,
  humidity: 78,
  stormRisk: "High",
  affectedAssets: 12,
};

function WeatherIntelligence() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Weather Intelligence
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Current weather conditions and their potential impact on grid assets
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-xl bg-orange-50 px-3 py-2 text-xs font-semibold text-orange-700">
          <AlertTriangle size={15} />
          High weather risk
        </div>
      </div>

      {/* Weather Metrics */}
      <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {/* Temperature */}
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Temperature</p>

            <Thermometer size={18} className="text-orange-500" />
          </div>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            {weatherData.temperature}°C
          </p>

          <p className="mt-1 text-xs text-slate-500">Current grid area</p>
        </div>

        {/* Rainfall */}
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Rainfall</p>

            <CloudRain size={18} className="text-blue-500" />
          </div>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            {weatherData.rainfall} mm
          </p>

          <p className="mt-1 text-xs text-slate-500">Recent rainfall</p>
        </div>

        {/* Wind */}
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Wind Speed</p>

            <Wind size={18} className="text-blue-600" />
          </div>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            {weatherData.windSpeed} km/h
          </p>

          <p className="mt-1 text-xs text-orange-600">Strong winds</p>
        </div>

        {/* Humidity */}
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-slate-500">Humidity</p>

            <Droplets size={18} className="text-cyan-600" />
          </div>

          <p className="mt-3 text-2xl font-bold text-slate-900">
            {weatherData.humidity}%
          </p>

          <p className="mt-1 text-xs text-slate-500">Atmospheric humidity</p>
        </div>
      </div>

      {/* Weather Risk Summary */}
      <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_auto]">
        <div className="rounded-xl border border-orange-100 bg-orange-50 p-4">
          <div className="flex items-start gap-3">
            <div className="rounded-lg bg-orange-100 p-2 text-orange-600">
              <CloudLightning size={19} />
            </div>

            <div>
              <p className="text-sm font-semibold text-orange-900">
                Weather Risk Assessment
              </p>

              <p className="mt-1 text-xs leading-5 text-orange-800">
                Strong winds and high humidity may increase the risk of
                equipment stress and outages in exposed grid areas.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-between gap-6 rounded-xl border border-slate-200 bg-white px-5 py-4 lg:min-w-[220px] lg:flex-col lg:items-start lg:justify-center">
          <div>
            <p className="text-xs text-slate-500">
              Potentially affected assets
            </p>

            <p className="mt-1 text-2xl font-bold text-slate-900">
              {weatherData.affectedAssets}
            </p>
          </div>

          <span className="rounded-full bg-orange-100 px-2.5 py-1 text-[11px] font-semibold text-orange-700">
            {weatherData.stormRisk} risk
          </span>
        </div>
      </div>
    </div>
  );
}

export default WeatherIntelligence;
