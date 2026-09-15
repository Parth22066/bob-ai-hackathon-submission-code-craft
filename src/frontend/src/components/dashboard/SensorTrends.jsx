import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const sensorData = [
  { time: "08:00", temperature: 64, vibration: 32, discharge: 18 },
  { time: "09:00", temperature: 67, vibration: 35, discharge: 21 },
  { time: "10:00", temperature: 71, vibration: 39, discharge: 24 },
  { time: "11:00", temperature: 74, vibration: 42, discharge: 29 },
  { time: "12:00", temperature: 78, vibration: 48, discharge: 34 },
  { time: "13:00", temperature: 81, vibration: 52, discharge: 38 },
  { time: "14:00", temperature: 79, vibration: 49, discharge: 36 },
];

function SensorTrends() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-900">
            Sensor Intelligence
          </p>

          <p className="mt-1 text-xs text-slate-500">
            Recent sensor behavior across high-risk assets
          </p>
        </div>

        <div className="flex flex-wrap gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-blue-500" />
            Temperature
          </div>

          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-orange-500" />
            Vibration
          </div>

          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-red-500" />
            Discharge
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="mt-6 h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={sensorData}
            margin={{
              top: 5,
              right: 10,
              left: -15,
              bottom: 5,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#E5E7EB"
            />

            <XAxis
              dataKey="time"
              tick={{ fontSize: 12, fill: "#64748B" }}
              axisLine={false}
              tickLine={false}
            />

            <YAxis
              tick={{ fontSize: 12, fill: "#64748B" }}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip
              contentStyle={{
                borderRadius: "12px",
                border: "1px solid #E5E7EB",
                boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
              }}
            />

            <Line
              type="monotone"
              dataKey="temperature"
              stroke="#3B82F6"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 5 }}
            />

            <Line
              type="monotone"
              dataKey="vibration"
              stroke="#F97316"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 5 }}
            />

            <Line
              type="monotone"
              dataKey="discharge"
              stroke="#EF4444"
              strokeWidth={2.5}
              dot={false}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Sensor status */}
      <div className="mt-5 grid gap-3 border-t border-slate-100 pt-5 sm:grid-cols-3">
        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-xs text-slate-500">Temperature</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">79°C</p>
          <p className="text-xs text-orange-600">Above normal</p>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-xs text-slate-500">Vibration</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">49 mm/s</p>
          <p className="text-xs text-orange-600">Elevated</p>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-xs text-slate-500">Partial Discharge</p>
          <p className="mt-1 text-lg font-semibold text-slate-900">36 pC</p>
          <p className="text-xs text-red-600">Abnormal</p>
        </div>
      </div>
    </div>
  );
}

export default SensorTrends;
