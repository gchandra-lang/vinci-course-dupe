import { useState, useMemo } from "react";
import { Shield, Activity, Wifi, AlertTriangle, CheckCircle, XCircle } from "lucide-react";

type ReadinessState = "FAIL" | "PARTIAL" | "READY";

interface GateParams {
  lowstateStreaming: boolean;
  checkModeAi: boolean;
  fsmValue: number;
  interfaceOk: boolean;
  pingOk: boolean;
  cycloneddsOk: boolean;
}

const FSM_HINTS: Record<number, { label: string; desc: string; danger: boolean }> = {
  0: { label: "Zero Torque", desc: "No active torque — do not infer balance readiness.", danger: true },
  1: { label: "Damp", desc: "Damping active — robot may fall if unsupported. BLOCKED.", danger: true },
  3: { label: "Sit", desc: "Seated — safe for observation but not walking.", danger: false },
  500: { label: "Start", desc: "Transitional/startup — wait and re-check.", danger: false },
  702: { label: "Lie-to-Stand", desc: "Transition — do not interrupt casually.", danger: true },
  706: { label: "Squat/Stand", desc: "Transition — maintain distance, wait for stability.", danger: true },
};

export default function Day5SafetyGatingCalculator() {
  const [params, setParams] = useState<GateParams>({
    lowstateStreaming: true,
    checkModeAi: true,
    fsmValue: 500,
    interfaceOk: true,
    pingOk: true,
    cycloneddsOk: true,
  });

  const toggle = (key: keyof GateParams) => {
    if (key === "fsmValue") return;
    setParams((prev) => ({ ...prev, [key]: !prev[key as keyof GateParams] }));
  };

  const fsmHint = FSM_HINTS[params.fsmValue] || { label: `FSM ${params.fsmValue}`, desc: "Unknown FSM state — consult documentation.", danger: false };

  const readiness = useMemo((): { state: ReadinessState; color: string; bg: string; reasoning: string[] } => {
    const r: string[] = [];
    let hasFail = false;
    let hasPartial = false;

    // Layer 1: Local setup
    if (!params.cycloneddsOk) { r.push("FAIL — Local: CycloneDDS not found. Fix installation."); hasFail = true; }
    else r.push("PASS — CycloneDDS ready.");

    // Layer 2: Network
    if (!params.interfaceOk) { r.push("FAIL — Network: Interface lacks 192.168.123.x address. Check cable/adapter."); hasFail = true; }
    else if (!params.pingOk) { r.push("FAIL — Network: Ping to 192.168.123.161 failed. Check robot power and subnet."); hasFail = true; }
    else r.push("PASS — Network: IP reachability confirmed.");

    // Layer 3: DDS
    if (hasFail) { /* skip DDS check */ }
    else if (!params.lowstateStreaming) {
      r.push("PARTIAL — DDS: rt/lowstate not streaming. Check interface binding, DDS profile, IDL type.");
      hasPartial = true;
    } else r.push("PASS — DDS: rt/lowstate streaming confirmed.");

    // Layer 4: Service
    if (hasFail) { /* skip */ }
    else if (!params.lowstateStreaming) { /* skip */ }
    else if (!params.checkModeAi) {
      r.push("PARTIAL — Service: CheckMode != 'ai'. High-level service ownership not confirmed.");
      hasPartial = true;
    } else r.push("PASS — Service: CheckMode == 'ai'.");

    // Layer 5: FSM
    if (hasFail) { /* skip */ }
    else if (!params.lowstateStreaming) { /* skip */ }
    else if (params.fsmValue === 1) {
      r.push("PARTIAL — FSM: Damped (1). Robot NOT motion-ready. May lose balance.");
      hasPartial = true;
    } else if (fsmHint.danger) {
      r.push(`PARTIAL — FSM: ${fsmHint.label}. Transitional or unsafe posture. Wait.`);
      hasPartial = true;
    } else r.push(`PASS — FSM: ${fsmHint.label}.`);

    // Final classification
    if (hasFail) return { state: "FAIL", color: "text-destructive", bg: "bg-destructive/10 border-destructive/30", reasoning: r };
    if (hasPartial) return { state: "PARTIAL", color: "text-amber-400", bg: "bg-amber-400/10 border-amber-400/30", reasoning: r };
    if (params.lowstateStreaming && params.checkModeAi && !fsmHint.danger && params.pingOk && params.interfaceOk && params.cycloneddsOk)
      return { state: "READY", color: "text-emerald-400", bg: "bg-emerald-400/10 border-emerald-400/30", reasoning: r };
    return { state: "PARTIAL", color: "text-amber-400", bg: "bg-amber-400/10 border-amber-400/30", reasoning: r };
  }, [params, fsmHint]);

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col min-h-[420px]">
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Shield className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            G1 Safety Gating Calculator
          </span>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded border text-[10px] font-mono font-bold ${readiness.bg} ${readiness.color}`}>
          {readiness.state === "READY" ? <CheckCircle className="h-3.5 w-3.5" /> : readiness.state === "FAIL" ? <XCircle className="h-3.5 w-3.5" /> : <AlertTriangle className="h-3.5 w-3.5" />}
          {readiness.state} {readiness.state === "READY" ? "for next supervised step" : ""}
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Left: Gate Controls */}
        <div className="w-full lg:w-64 border-r border-border bg-card/40 p-4 flex flex-col gap-3 overflow-y-auto">
          <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-1">
            Diagnostic Layers (bottom-up)
          </span>

          {/* Layer 1: Local */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] font-mono text-foreground font-bold flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-primary" /> Layer 1: Local Env
            </span>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={params.cycloneddsOk} onChange={() => toggle("cycloneddsOk")} className="accent-primary" />
              CycloneDDS found
            </label>
          </div>

          {/* Layer 2: Network */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] font-mono text-foreground font-bold flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-400" /> Layer 2: Network
            </span>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={params.interfaceOk} onChange={() => toggle("interfaceOk")} className="accent-primary" />
              192.168.123.x interface
            </label>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={params.pingOk} onChange={() => toggle("pingOk")} className="accent-primary" />
              Ping .161 succeeds
            </label>
          </div>

          {/* Layer 3: DDS */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] font-mono text-foreground font-bold flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-cyan-400" /> Layer 3: DDS
            </span>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={params.lowstateStreaming} onChange={() => toggle("lowstateStreaming")} className="accent-primary" />
              rt/lowstate streaming
            </label>
          </div>

          {/* Layer 4: Service */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] font-mono text-foreground font-bold flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-violet-400" /> Layer 4: Service
            </span>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={params.checkModeAi} onChange={() => toggle("checkModeAi")} className="accent-primary" />
              CheckMode == 'ai'
            </label>
          </div>

          {/* Layer 5: FSM */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] font-mono text-foreground font-bold flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-amber-400" /> Layer 5: FSM
            </span>
            <div className="flex flex-wrap gap-1">
              {Object.entries(FSM_HINTS).map(([val, hint]) => (
                <button
                  key={val}
                  onClick={() => setParams((p) => ({ ...p, fsmValue: parseInt(val) }))}
                  className={`px-2 py-1 rounded text-[9px] font-mono font-bold transition-all ${
                    params.fsmValue === parseInt(val)
                      ? hint.danger ? "bg-destructive text-destructive-foreground" : hint.label === "Start"
                        ? "bg-primary text-primary-foreground" : "bg-emerald-500 text-white"
                      : "bg-muted text-muted-foreground hover:bg-accent"
                  }`}
                >
                  {val}
                </button>
              ))}
            </div>
            <p className="text-[9px] font-mono text-muted-foreground leading-relaxed">
              {fsmHint.desc}
            </p>
          </div>
        </div>

        {/* Right: Readiness Pipeline */}
        <div className="flex-1 p-5 flex flex-col gap-4">
          {/* 5-Layer Pipeline Visualization */}
          <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block">
            Readiness Pipeline
          </span>
          <div className="space-y-2">
            {[
              { layer: "1", label: "Local Env", key: "cycloneddsOk" as const, color: "bg-primary" },
              { layer: "2", label: "Network", key: "pingOk" as const, color: "bg-blue-400" },
              { layer: "3", label: "DDS Topic", key: "lowstateStreaming" as const, color: "bg-cyan-400" },
              { layer: "4", label: "Service", key: "checkModeAi" as const, color: "bg-violet-400" },
              { layer: "5", label: `FSM (${params.fsmValue})`, key: "lowstateStreaming" as const, color: !fsmHint.danger ? "bg-emerald-400" : "bg-amber-400" },
            ].map(({ layer, label, key, color }) => {
              // For layer 2, check both interfaceOk and pingOk
              let ok: boolean;
              if (key === "pingOk") ok = params.interfaceOk && params.pingOk;
              else ok = params[key as keyof GateParams] as boolean;
              // For layer 5, override with fsm safety
              if (layer === "5") ok = !fsmHint.danger && params.lowstateStreaming && params.checkModeAi && params.interfaceOk && params.pingOk;
              if (layer !== "1") {
                const prevOk = layer === "2" ? params.cycloneddsOk
                  : layer === "3" ? params.cycloneddsOk && params.interfaceOk && params.pingOk
                  : layer === "4" ? params.cycloneddsOk && params.interfaceOk && params.pingOk && params.lowstateStreaming
                  : params.cycloneddsOk && params.interfaceOk && params.pingOk && params.lowstateStreaming && params.checkModeAi && !fsmHint.danger;
                if (!prevOk) ok = false;
              }
              return (
                <div key={layer} className="flex items-center gap-3">
                  <div className={`h-8 w-8 rounded-full flex items-center justify-center text-[10px] font-mono font-bold text-white shadow-sm ${ok ? color : "bg-border"}`}>
                    {layer}
                  </div>
                  <div className={`flex-1 h-8 rounded-lg border flex items-center px-3 ${ok ? "border-primary/30 bg-primary/5" : "border-border bg-muted/30 opacity-50"}`}>
                    <span className={`text-[10px] font-mono font-bold ${ok ? "text-foreground" : "text-muted-foreground"}`}>{label}</span>
                    <span className="ml-auto text-[9px] font-mono">
                      {ok ? <CheckCircle className="h-3.5 w-3.5 text-emerald-400" /> : <XCircle className="h-3.5 w-3.5 text-muted-foreground" />}
                    </span>
                  </div>
                  {layer !== "5" && (
                    <div className="w-0.5 h-4 bg-border ml-[15px] -mt-1" />
                  )}
                </div>
              );
            })}
          </div>

          {/* Reasoning Output */}
          <div className="flex-1 border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Diagnostic Reasoning
            </span>
            <div className="space-y-1">
              {readiness.reasoning.map((line, i) => (
                <div
                  key={i}
                  className={`text-[10px] font-mono px-3 py-1.5 rounded border ${
                    line.startsWith("FAIL")
                      ? "bg-destructive/5 border-destructive/15 text-destructive"
                      : line.startsWith("PARTIAL")
                      ? "bg-amber-400/5 border-amber-400/15 text-amber-400"
                      : "bg-emerald-400/5 border-emerald-400/15 text-emerald-400"
                  }`}
                >
                  {line}
                </div>
              ))}
            </div>
          </div>

          {/* Evidence Checklist */}
          <div className="border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Required Day 5 Evidence
            </span>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 text-[9px] font-mono">
              {[
                { label: "Interface name", ok: params.interfaceOk },
                { label: "Ping result", ok: params.pingOk },
                { label: "First lowstate msg", ok: params.lowstateStreaming },
                { label: "CheckMode() output", ok: params.checkModeAi },
                { label: "FSM id & interpret", ok: !fsmHint.danger },
                { label: "IMU values", ok: params.lowstateStreaming },
                { label: "Motor count", ok: params.lowstateStreaming },
                { label: "Instructor sign-off", ok: readiness.state === "READY" },
              ].map((e) => (
                <div key={e.label} className={`flex items-center gap-1.5 px-2 py-1.5 rounded border ${e.ok ? "border-emerald-400/20 bg-emerald-400/5" : "border-border bg-muted/30 opacity-50"}`}>
                  {e.ok ? <CheckCircle className="h-3 w-3 text-emerald-400" /> : <XCircle className="h-3 w-3 text-muted-foreground" />}
                  <span className={e.ok ? "text-foreground" : "text-muted-foreground"}>{e.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}