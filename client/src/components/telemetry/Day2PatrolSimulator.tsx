import { useState, useMemo } from "react";
import { Activity, Crosshair, RotateCw } from "lucide-react";

interface Leg {
  id: string;
  targetX: number;
  targetY: number;
  driftX: number;
  driftY: number;
  corrX: number;
  corrY: number;
}

const DEFAULT_LEGS: Leg[] = [
  { id: "CP-01", targetX: 1.0, targetY: 0.5, driftX: 0.12, driftY: -0.08, corrX: 0.85, corrY: 0.90 },
  { id: "CP-02", targetX: 2.5, targetY: 1.2, driftX: -0.15, driftY: 0.10, corrX: 0.78, corrY: 0.82 },
  { id: "CP-03", targetX: 3.8, targetY: 0.3, driftX: 0.08, driftY: 0.18, corrX: 0.92, corrY: 0.75 },
];

export default function Day2PatrolSimulator() {
  const [legs, setLegs] = useState<Leg[]>(DEFAULT_LEGS);
  const [activeLegIdx, setActiveLegIdx] = useState(0);
  const [globalGain, setGlobalGain] = useState(0.80);

  const activeLeg = legs[activeLegIdx];

  const updateActive = (field: keyof Leg, value: number) => {
    setLegs((prev) =>
      prev.map((l, i) => (i === activeLegIdx ? { ...l, [field]: value } : l))
    );
  };

  const stats = useMemo(() => {
    const corrected = legs.map((l) => ({
      ...l,
      cx: l.targetX + l.driftX * (1 - l.corrX * globalGain),
      cy: l.targetY + l.driftY * (1 - l.corrY * globalGain),
    }));
    const maxDrift = Math.max(...legs.map((l) => Math.hypot(l.driftX, l.driftY)));
    const avgCorr = legs.reduce((s, l) => s + (l.corrX + l.corrY) / 2, 0) / legs.length;
    return { corrected, maxDrift, avgCorr };
  }, [legs, globalGain]);

  const resetToDefaults = () => setLegs(DEFAULT_LEGS.map((l) => ({ ...l })));

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col min-h-[420px]">
      {/* Header */}
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Crosshair className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            Multi-Leg Patrol Simulator
          </span>
        </div>
        <button
          onClick={resetToDefaults}
          className="flex items-center gap-1.5 text-[10px] font-mono text-muted-foreground hover:text-primary transition-colors"
        >
          <RotateCw className="h-3 w-3" />
          Reset
        </button>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Left: Controls */}
        <div className="w-full lg:w-64 border-r border-border bg-card/40 p-4 flex flex-col gap-4 overflow-y-auto">
          {/* Leg Selection */}
          <div>
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Patrol Checkpoints
            </span>
            <div className="space-y-1">
              {legs.map((leg, idx) => (
                <button
                  key={leg.id}
                  onClick={() => setActiveLegIdx(idx)}
                  className={`w-full text-left px-3 py-2 rounded text-xs font-mono transition-all ${
                    idx === activeLegIdx
                      ? "bg-primary text-primary-foreground font-bold"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  {leg.id} → ({leg.targetX.toFixed(1)}, {leg.targetY.toFixed(1)})
                </button>
              ))}
            </div>
          </div>

          {/* Global Gain */}
          <div>
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-1.5">
              Global Correction Gain
            </span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={globalGain}
              onChange={(e) => setGlobalGain(parseFloat(e.target.value))}
              className="w-full accent-primary"
            />
            <span className="text-[10px] font-mono text-primary font-bold">{globalGain.toFixed(2)}</span>
          </div>

          {/* Active Leg Editor */}
          <div className="border-t border-border pt-3 space-y-2.5">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              Edit {activeLeg.id}
            </span>
            <div className="grid grid-cols-2 gap-2">
              {(["driftX", "driftY", "corrX", "corrY"] as const).map((field) => (
                <div key={field}>
                  <label className="text-[9px] font-mono text-muted-foreground block">
                    {field}
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={activeLeg[field]}
                    onChange={(e) => updateActive(field, parseFloat(e.target.value) || 0)}
                    className="w-full bg-muted border border-border rounded px-2.5 py-2 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Visualization */}
        <div className="flex-1 p-5 flex flex-col gap-4">
          {/* Scatter Plot */}
          <div className="relative h-48 bg-muted/30 border border-border rounded-lg overflow-hidden">
            {/* Grid lines */}
            <div className="absolute inset-0">
              {[0, 25, 50, 75, 100].map((p) => (
                <div key={`v${p}`} className="absolute top-0 bottom-0 border-l border-border/30" style={{ left: `${p}%` }} />
              ))}
              {[0, 25, 50, 75, 100].map((p) => (
                <div key={`h${p}`} className="absolute left-0 right-0 border-t border-border/30" style={{ top: `${p}%` }} />
              ))}
            </div>
            {/* Axes labels */}
            <span className="absolute bottom-1 left-1 text-[8px] font-mono text-muted-foreground">Y</span>
            <span className="absolute bottom-1 right-1 text-[8px] font-mono text-muted-foreground">X</span>

            {/* Target + Drift + Corrected for each leg */}
            {stats.corrected.map((l) => {
              const tx = ((l.targetX + 0.5) / 5) * 100;
              const ty = ((l.targetY + 0.5) / 2.5) * 100;
              const dx = ((l.targetX + l.driftX + 0.5) / 5) * 100;
              const dy = ((l.targetY + l.driftY + 0.5) / 2.5) * 100;
              const cx = ((l.cx + 0.5) / 5) * 100;
              const cy = ((l.cy + 0.5) / 2.5) * 100;
              const isActive = l.id === activeLeg.id;
              return (
                <div key={l.id}>
                  {/* Target (square) */}
                  <div
                    className={`absolute w-3 h-3 -ml-1.5 -mt-1.5 border-2 rounded-sm transition-all ${
                      isActive ? "border-primary bg-primary/20 z-20 scale-125" : "border-foreground/40 bg-foreground/10"
                    }`}
                    style={{ left: `${tx}%`, top: `${ty}%` }}
                    title={`${l.id} Target`}
                  />
                  {/* Drifted (dashed circle) */}
                  <div
                    className="absolute w-3 h-3 -ml-1.5 -mt-1.5 border border-dashed border-destructive/60 rounded-full bg-destructive/10"
                    style={{ left: `${dx}%`, top: `${dy}%` }}
                    title={`${l.id} Drifted`}
                  />
                  {/* Corrected (filled circle) */}
                  <div
                    className={`absolute w-2.5 h-2.5 -ml-1.25 -mt-1.25 rounded-full transition-all ${
                      isActive ? "bg-emerald-500 shadow-sm shadow-emerald-500/40 z-20 scale-125" : "bg-emerald-500/60"
                    }`}
                    style={{ left: `${cx}%`, top: `${cy}%` }}
                    title={`${l.id} Corrected`}
                  />
                  {/* Connector line target → drifted */}
                  <svg className="absolute inset-0 pointer-events-none" style={{ overflow: "visible" }}>
                    <line x1={`${tx}%`} y1={`${ty}%`} x2={`${dx}%`} y2={`${dy}%`} stroke="rgb(239 68 68 / 0.3)" strokeWidth="1" strokeDasharray="3 2" />
                    <line x1={`${dx}%`} y1={`${dy}%`} x2={`${cx}%`} y2={`${cy}%`} stroke="rgb(16 185 129 / 0.5)" strokeWidth="1.5" />
                  </svg>
                  {/* Label */}
                  <span
                    className="absolute text-[8px] font-mono text-foreground/70 font-bold"
                    style={{ left: `${tx + 1.5}%`, top: `${ty - 5}%` }}
                  >
                    {l.id}
                  </span>
                </div>
              );
            })}

            {/* Legend */}
            <div className="absolute top-2 right-2 flex gap-3 text-[8px] font-mono text-muted-foreground bg-card/80 px-2 py-1 rounded border border-border">
              <span className="flex items-center gap-1"><span className="w-2 h-2 border border-foreground/40 rounded-sm" /> Target</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 border border-dashed border-destructive/60 rounded-full" /> Drift</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 bg-emerald-500 rounded-full" /> Corrected</span>
            </div>
          </div>

          {/* Stats Panel */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              { label: "Max Drift", value: `${(stats.maxDrift * 100).toFixed(1)} cm`, color: "text-amber-400" },
              { label: "Avg Correction", value: `${(stats.avgCorr * 100).toFixed(0)}%`, color: "text-primary" },
              { label: "Gain", value: `${(globalGain * 100).toFixed(0)}%`, color: "text-emerald-400" },
              { label: "Checkpoints", value: `${legs.length}`, color: "text-muted-foreground" },
            ].map((s) => (
              <div key={s.label} className="bg-muted/30 border border-border rounded-lg p-3 text-center">
                <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-1">
                  {s.label}
                </span>
                <span className={`text-sm font-mono font-bold ${s.color}`}>{s.value}</span>
              </div>
            ))}
          </div>

          {/* Per-Leg Drift Detail */}
          <div className="border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Per-Checkpoint Residual Error
            </span>
            <div className="space-y-1.5">
              {stats.corrected.map((l) => {
                const residual = Math.hypot(l.driftX * (1 - l.corrX * globalGain), l.driftY * (1 - l.corrY * globalGain));
                const barW = Math.min(100, residual * 500);
                return (
                  <div key={l.id} className="flex items-center gap-2 text-[10px] font-mono">
                    <span className="w-12 text-muted-foreground">{l.id}</span>
                    <div className="flex-1 h-3 bg-muted rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{
                          width: `${barW}%`,
                          backgroundColor: residual < 0.05 ? "rgb(16 185 129)" : residual < 0.15 ? "rgb(251 191 36)" : "rgb(239 68 68)",
                        }}
                      />
                    </div>
                    <span className="w-12 text-right text-muted-foreground">{(residual * 100).toFixed(1)} cm</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}