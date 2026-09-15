import { useState } from "react";
import {
  Bot,
  Send,
  Sparkles,
  AlertTriangle,
  MapPin,
  Wrench,
  Activity,
  Loader2,
} from "lucide-react";
import { queryAIAssistant } from "../services/api";

const suggestions = [
  "Which asset has the highest risk?",
  "Why is TR-002 critical?",
  "Which areas are most likely to experience an outage?",
  "What maintenance should be done immediately?",
];

const responses = {
  "Which asset has the highest risk?":
    "TR-002 — Central Grid Transformer has the highest risk score of 92/100 with an estimated failure probability of 87%. Immediate inspection is recommended.",

  "Why is TR-002 critical?":
    "TR-002 is critical because its failure probability is 87%, temperature is 79°C, vibration is 49 mm/s, and partial discharge is 36 pC. Current weather conditions also increase operational stress.",

  "Which areas are most likely to experience an outage?":
    "Vadodara Central has the highest outage risk with 3 assets at risk and approximately 5,200 customers potentially affected. Makarpura Industrial Zone is the next highest-risk area.",

  "What maintenance should be done immediately?":
    "The highest-priority action is to inspect TR-002 immediately. Check its cooling system and oil condition, then perform a detailed sensor inspection.",
};

function AIAssistant() {
  const [messages, setMessages] = useState([
    {
      type: "ai",
      text: "Hello. I'm GridGuard AI Assistant. I can help you understand asset risks, outage threats, sensor anomalies and maintenance priorities.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message) => {
    const question = message.trim();
    if (!question || loading) return;

    // Add user question
    setMessages((current) => [
      ...current,
      { type: "user", text: question },
    ]);
    setInput("");
    setLoading(true);

    try {
      const data = await queryAIAssistant(question, "TR-002");
      const answer = data?.insight || responses[question] || "Operational assessment generated.";
      setMessages((current) => [
        ...current,
        { type: "ai", text: answer, mode: data?.mode },
      ]);
    } catch {
      const fallbackAnswer =
        responses[question] ||
        "Based on the current GridGuard data, TR-002 exhibits abnormal thermal and vibration patterns. Prioritize inspection of cooling circuits and oil insulation before next load peak.";
      setMessages((current) => [
        ...current,
        { type: "ai", text: fallbackAnswer },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage(input);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <p className="text-sm font-medium text-blue-600">
          AI Operations Assistant
        </p>

        <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
          GridGuard AI Assistant
        </h1>

        <p className="mt-1 text-sm text-slate-500">
          Ask questions about grid risk, assets, outages and maintenance.
        </p>
      </div>

      {/* Main Layout */}
      <div className="grid gap-6 xl:grid-cols-[1fr_320px]">
        {/* Chat */}
        <div className="flex min-h-[650px] flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          {/* Chat Header */}
          <div className="flex items-center gap-3 border-b border-slate-200 p-5">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
              <Bot size={21} />
            </div>

            <div>
              <p className="text-sm font-semibold text-slate-900">
                GridGuard AI
              </p>

              <div className="mt-1 flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                <p className="text-xs text-slate-500">
                  Operational intelligence online
                </p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 space-y-5 overflow-y-auto p-5">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                    message.type === "user"
                      ? "rounded-br-md bg-blue-600 text-white"
                      : "rounded-bl-md border border-slate-200 bg-slate-50 text-slate-700"
                  }`}
                >
                  {message.type === "ai" && (
                    <div className="mb-2 flex items-center gap-2">
                      <Sparkles size={14} className="text-blue-600" />

                      <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600">
                        GridGuard AI
                      </span>
                    </div>
                  )}

                  <p className="text-sm leading-6">{message.text}</p>
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="flex items-center gap-2 rounded-2xl rounded-bl-md border border-slate-200 bg-slate-50 px-4 py-3 text-xs text-slate-500">
                  <Loader2 size={14} className="animate-spin text-blue-600" />
                  Analyzing grid telemetry & watsonx context...
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <form
            onSubmit={handleSubmit}
            className="border-t border-slate-200 p-4"
          >
            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 p-2 focus-within:border-blue-400 focus-within:bg-white">
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask GridGuard about an asset or risk..."
                className="min-w-0 flex-1 bg-transparent px-2 text-sm text-slate-700 outline-none placeholder:text-slate-400"
              />

              <button
                type="submit"
                className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-600 text-white transition hover:bg-blue-700"
              >
                <Send size={17} />
              </button>
            </div>

            <p className="mt-2 px-1 text-[10px] text-slate-400">
              AI responses are based on currently available GridGuard data.
            </p>
          </form>
        </div>

        {/* Right Panel */}
        <div className="space-y-4">
          {/* Suggested Questions */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center gap-2">
              <Sparkles size={17} className="text-blue-600" />

              <p className="text-sm font-semibold text-slate-900">
                Suggested Questions
              </p>
            </div>

            <div className="mt-4 space-y-2">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => sendMessage(suggestion)}
                  className="w-full rounded-xl border border-slate-200 p-3 text-left text-xs font-medium leading-5 text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>

          {/* Current Risk */}
          <div className="rounded-2xl border border-red-100 bg-red-50/50 p-5">
            <div className="flex items-center gap-2">
              <AlertTriangle size={17} className="text-red-600" />

              <p className="text-sm font-semibold text-slate-900">
                Current Critical Risk
              </p>
            </div>

            <p className="mt-4 text-xl font-bold text-red-600">TR-002</p>

            <p className="mt-1 text-xs text-slate-500">
              Central Grid Transformer
            </p>

            <div className="mt-4 grid grid-cols-2 gap-3">
              <div className="rounded-xl bg-white p-3">
                <p className="text-[10px] text-slate-400">Risk Score</p>

                <p className="mt-1 text-lg font-bold text-slate-900">92</p>
              </div>

              <div className="rounded-xl bg-white p-3">
                <p className="text-[10px] text-slate-400">
                  Failure Probability
                </p>

                <p className="mt-1 text-lg font-bold text-red-600">87%</p>
              </div>
            </div>
          </div>

          {/* Quick Context */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-slate-400">
              Quick Context
            </p>

            <div className="mt-4 space-y-4">
              <div className="flex items-center gap-3">
                <Activity size={17} className="text-blue-500" />

                <div>
                  <p className="text-xs font-semibold text-slate-800">
                    18 high-risk assets
                  </p>

                  <p className="text-[11px] text-slate-400">
                    Require monitoring
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <MapPin size={17} className="text-orange-500" />

                <div>
                  <p className="text-xs font-semibold text-slate-800">
                    4 outage-prone areas
                  </p>

                  <p className="text-[11px] text-slate-400">
                    Based on current risk
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Wrench size={17} className="text-emerald-500" />

                <div>
                  <p className="text-xs font-semibold text-slate-800">
                    3 priority actions
                  </p>

                  <p className="text-[11px] text-slate-400">
                    Recommended by AI
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;
