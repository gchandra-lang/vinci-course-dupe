import { useState, useMemo } from "react";
import { Activity, Shield, Zap, Radio } from "lucide-react";

type CommPath = "rpc" | "500hz";

interface Profile {
  rate: number;
  jitter: number;
  dropped: number;
  safetyMargin: number;
}

export default function Day3ControlAuthority() {
  const [commPath, setCommPath] = useState<CommPath>("rpc");
  const [rpc, setRpc] = useState<Profile>({ rate: 22, jitter: 4.2, dropped: 1, safetyMargin: 72 });
  const [hz500, setHz500] = useState<Profile>({ rate: 485, jitter: 1.8, dropped: 8, safetyMargin: 35 });

  const active = commPath === "rpc" ? rpc : hz500;
  const update = commPath === "rpc" ? setRpc : setHz500;

  const setField = (field: keyof Profile) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = parseFloat(e.target.value) || 0;
    update((prev) => ({ ...prev, [field]: v }));
  };

  const safetyVerdict = useMemo(() => {
    const { rate, jitter, dropped, safetyMargin } = active;
    if (safetyMargin < 25) return { label: "FAIL", color: "text-destructive", bg: "bg-destructive/10 border-destructive/30" };
    if (safetyMargin < 50 || dropped > 5 || jitter > 5)
      return { label: "PARTIAL", color: "text-amber-400", bg: "bg-amber-400/10 border-amber-400/30" };
    return { label: "READY", color: "text-emerald-400", bg: "bg-emerald-400/10 border-emerald-400/30" };
  }, [active]);

  const thresholdCrossings = useMemo(() => {
    const crossings: { label: string; value: string; status: "ok" | "warn" | "fail" }[] = [];
    const { rate, jitter, dropped, safetyMargin } = active;
    if (commPath === "500hz") {
      crossings.push({ label: "Min Rate", value: `${rate} Hz`, status: rate >= 450 ? "ok" : rate >= 400 ? "warn" : "fail" });
    } else {
      crossings.push({ label: "RPC Rate", value: `${rate}/s`, status: rate >= 15 ? "ok" : "warn" });
    }
    crossings.push({ label: "Jitter", value: `${jitter.toFixed(1)} ms`, status: jitter < 3 ? "ok" : jitter < 6 ? "warn" : "fail" });
    crossings.push({ label: "Dropped", value: `${dropped} pkts`, status: dropped <= 3 ? "ok" : dropped <= 8 ? "warn" : "fail" });
    crossings.push({ label: "Safety Margin", value: `${safetyMargin.toFixed(0)}%`, status: safetyMargin >= 50 ? "ok" : safetyMargin >= 25 ? "warn" : "fail" });
    return crossings;
  }, [active, commPath]);

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col min-h-[420px]">
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Radio className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            B2 Control Authority Simulator
          </span>
        </div>
        <div className={`text-[10px] font-mono font-bold px-3 py-1.5 rounded border ${safetyVerdict.bg} ${safetyVerdict.color}`}>
          {safetyVerdict.label}
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Control Panel */}
        <div className="w-full lg:w-64 border-r border-border bg-card/40 p-4 flex flex-col gap-4 overflow-y-auto">
          {/* Comm Path Toggle */}
          <div>
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Communication Path
            </span>
            <div className="grid grid-cols-2 gap-1.5">
              {(["rpc", "500hz"] as CommPath[]).map((p) => (
                <button
                  key={p}
                  onClick={() => setCommPath(p)}
                  className={`px-3 py-2 rounded text-xs font-mono font-bold transition-all ${
                    commPath === p
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground hover:bg-accent"
                  }`}
                >
                  {p === "rpc" ? "RPC Srv" : "500 Hz Stream"}
                </button>
              ))}
            </div>
          </div>

          {/* Profile Sliders */}
          <div className="space-y-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              {commPath === "rpc" ? "RPC" : "DDS"} Profile
            </span>
            {[
              { key: "rate", label: "Data Rate", unit: commPath === "rpc" ? "msg/s" : "Hz", min: commPath === "rpc" ? 1 : 100, max: commPath === "rpc" ? 40 : 550 },
              { key: "jitter", label: "Jitter", unit: "ms", min: 0, max: 15, step: 0.1 },
              { key: "dropped", label: "Dropped", unit: "pkts", min: 0, max: 30 },
              { key: "safetyMargin", label: "Safety Margin", unit: "%", min: 0, max: 100 },
            ].map(({ key, label, unit, min, max, step }) => (
              <div key={key}>
                <label className="text-[9px] font-mono text-muted-foreground flex justify-between">
                  <span>{label}</span>
                  <span className="text-foreground font-bold">{(active as any)[key as keyof Profile].toFixed?.(key === "jitter" ? 1 : 0) ?? (active as any)[key as keyof Profile]}{unit}</span>
                </label>
                <input
                  type="range"
                  min={min}
                  max={max}
                  step={step || 1}
                  value={(active as any)[key as keyof Profile]}
                  onChange={setField(key as keyof Profile)}
                  className="w-full accent-primary h-1.5"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Visualization */}
        <div className="flex-1 p-5 flex flex-col gap-4">
          {/* Authority Gauge */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {thresholdCrossings.map((t) => (
              <div
                key={t.label}
                className={`border rounded-lg p-3 text-center transition-all ${
                  t.status === "ok"
                    ? "bg-emerald-400/5 border-emerald-400/20"
                    : t.status === "warn"
                    ? "bg-amber-400/5 border-amber-400/20"
                    : "bg-destructive/5 border-destructive/20"
                }`}
              >
                <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block">{t.label}</span>
                <span
                  className={`text-lg font-mono font-bold ${
                    t.status === "ok" ? "text-emerald-400" : t.status === "warn" ? "text-amber-400" : "text-destructive"
                  }`}
                >
                  {t.value}
                </span>
                <span className={`block text-[9px] font-mono ${t.status === "ok" ? "text-emerald-400/70" : t.status === "warn" ? "text-amber-400/70" : "text-destructive/70"}`}>
                  {t.status === "ok" ? "PASS" : t.status === "warn" ? "LIMIT" : "FAIL"}
                </span>
              </div>
            ))}
          </div>

          {/* Data Rate Gauge */}
          <div className="bg-muted/30 border border-border rounded-lg p-5">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">
              {commPath === "rpc" ? "RPC" : "DDS"} Authority Window
            </span>
            <div className="relative h-16 bg-muted rounded-lg border border-border overflow-hidden">
              {/* Background zones */}
              <div className="absolute inset-y-0 left-0 bg-destructive/10" style={{ width: "25%" }} />
              <div className="absolute inset-y-0 left-[25%] bg-amber-400/10" style={{ width: "25%" }} />
              <div className="absolute inset-y-0 left-[50%] bg-emerald-400/10" style={{ width: "50%" }} />

              {/* Active pointer */}
              <div
                className="absolute top-0 bottom-0 w-1 bg-primary shadow-lg shadow-primary/40 transition-all duration-300 rounded"
                style={{ left: `${Math.min(98, active.safetyMargin)}%` }}
              >
                <div className="absolute -top-1.5 -left-1.5 w-3.5 h-3.5 bg-primary rounded-full shadow" />
              </div>

              {/* Labels */}
              {[0, 25, 50, 75, 100].map((p) => (
                <div key={p} className="absolute top-0 bottom-0 flex flex-col items-center" style={{ left: `${p}%` }}>
                  <div className="w-px h-2 bg-border" />
                  <span className="text-[8px] font-mono text-muted-foreground mt-0.5">{p}%</span>
                </div>
              ))}

              {/* Zone labels */}
              <span className="absolute bottom-1 left-2 text-[8px] font-mono text-destructive/60 font-bold">FAIL</span>
              <span className="absolute bottom-1 left-[30%] text-[8px] font-mono text-amber-400/60 font-bold">PARTIAL</span>
              <span className="absolute bottom-1 right-4 text-[8px] font-mono text-emerald-400/60 font-bold">READY</span>
            </div>
          </div>

          {/* Loss / Jitter Chart */}
          <div className="bg-muted/30 border border-border rounded-lg p-4">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">
              Link Health Visualization
            </span>
            <div className="flex items-end gap-2 h-24">
              {Array.from({ length: 20 }).map((_, i) => {
                const baseH = 40 + Math.sin(i * 0.8) * 20 + Math.random() * 15;
                const dropChance = active.dropped / 30;
                const jitterScale = 1 - Math.min(1, active.jitter / 10);
                const h = i < active.dropped ? 5 : baseH * jitterScale;
                const danger = i < active.dropped;
                return (
                  <div key={i} className="flex-1 flex flex-col items-center gap-0.5">
                    <div
                      className="w-full rounded-t transition-all duration-300"
                      style={{
                        height: `${Math.max(3, h)}%`,
                        backgroundColor: danger
                          ? "rgb(239 68 68 / 0.6)"
                          : h < 30
                          ? "rgb(251 191 36 / 0.6)"
                          : "rgb(16 185 129 / 0.6)",
                      }}
                    />
                    {danger && <span className="text-[7px] font-mono text-destructive font-bold">✕</span>}
                  </div>
                );
              })}
            </div>
            <div className="flex justify-between text-[8px] font-mono text-muted-foreground mt-1.5">
              <span>Sample Window (20 pkts)</span>
              <span className="flex items-center gap-2">
                <span className="flex items-center gap-1"><span className="inline-block w-2 h-2 bg-emerald-400/60 rounded-sm" /> OK</span>
                <span className="flex items-center gap-1"><span className="inline-block w-2 h-2 bg-amber-400/60 rounded-sm" /> Jitter</span>
                <span className="flex items-center gap-1"><span className="inline-block w-2 h-2 bg-destructive/60 rounded-sm" /> Drop</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}