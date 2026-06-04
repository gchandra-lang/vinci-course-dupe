import { useState, useMemo } from "react";
import { CheckCircle, AlertTriangle, XCircle, FolderOpen, FileText, Save } from "lucide-react";

interface CheckpointEntry {
  id: string;
  frameExists: boolean;
  frameTooSmall: boolean;
  stateSliceExists: boolean;
  notesExist: boolean;
}

interface AuditResult {
  field: string;
  status: "pass" | "warn" | "fail";
  message: string;
}

const DEFAULT_CHECKPOINTS: CheckpointEntry[] = [
  { id: "cp01_entry", frameExists: true, frameTooSmall: false, stateSliceExists: true, notesExist: true },
  { id: "cp02_asset_label", frameExists: true, frameTooSmall: false, stateSliceExists: true, notesExist: false },
  { id: "cp03_exit", frameExists: true, frameTooSmall: false, stateSliceExists: false, notesExist: true },
];

export default function Day4RunFolderAuditor() {
  const [metaOperator, setMetaOperator] = useState("team_alpha");
  const [metaOperatorPresent, setMetaOperatorPresent] = useState(true);
  const [metaVersion, setMetaVersion] = useState("1.0");
  const [planCheckpoints, setPlanCheckpoints] = useState(true);
  const [planLegsCount, setPlanLegsCount] = useState(4);
  const [stateLines, setStateLines] = useState(45);
  const [checkpoints, setCheckpoints] = useState<CheckpointEntry[]>(DEFAULT_CHECKPOINTS);

  const results = useMemo((): AuditResult[] => {
    const r: AuditResult[] = [];
    if (!metaOperatorPresent) r.push({ field: "metadata.json → operator", status: "fail", message: "Operator field missing — inspection evidence needs accountability." });
    else r.push({ field: "metadata.json → operator", status: "pass", message: `Operator: ${metaOperator}` });
    r.push({ field: "metadata.json → schema_version", status: "pass", message: `Version: ${metaVersion}` });
    if (!planCheckpoints) r.push({ field: "patrol_plan.json → checkpoints", status: "fail", message: "No checkpoint IDs defined in plan." });
    else r.push({ field: "patrol_plan.json → checkpoints", status: "pass", message: `${checkpoints.length} checkpoints declared.` });
    if (planLegsCount === 0) r.push({ field: "patrol_plan.json → legs", status: "fail", message: "Plan has zero movement legs." });
    else if (planLegsCount < 3) r.push({ field: "patrol_plan.json → legs", status: "warn", message: `Only ${planLegsCount} legs — may need more for full coverage.` });
    else r.push({ field: "patrol_plan.json → legs", status: "pass", message: `${planLegsCount} legs defined.` });
    if (stateLines < 1) r.push({ field: "sportmodestate.jsonl", status: "fail", message: "State log is empty — cannot defend runtime robot state." });
    else if (stateLines < 10) r.push({ field: "sportmodestate.jsonl", status: "warn", message: `Only ${stateLines} lines — sparse for field run.` });
    else r.push({ field: "sportmodestate.jsonl", status: "pass", message: `${stateLines} JSONL entries.` });
    checkpoints.forEach((cp) => {
      if (!cp.frameExists) r.push({ field: `checkpoints/${cp.id}/frame.jpg`, status: "fail", message: "Missing — no checkpoint evidence image." });
      else if (cp.frameTooSmall) r.push({ field: `checkpoints/${cp.id}/frame.jpg`, status: "warn", message: "Image too small — may be corrupt or placeholder." });
      else r.push({ field: `checkpoints/${cp.id}/frame.jpg`, status: "pass", message: "Image present and usable." });
      if (!cp.stateSliceExists) r.push({ field: `checkpoints/${cp.id}/state_slice.jsonl`, status: "warn", message: "Optional state slice missing — context limited." });
      else r.push({ field: `checkpoints/${cp.id}/state_slice.jsonl`, status: "pass", message: "State context available." });
      if (!cp.notesExist) r.push({ field: `checkpoints/${cp.id}/notes.md`, status: "warn", message: "Optional notes missing — debrief may lack detail." });
    });
    return r;
  }, [metaOperator, metaOperatorPresent, metaVersion, planCheckpoints, planLegsCount, stateLines, checkpoints]);

  const overallVerdict = useMemo(() => {
    const hasFail = results.some((r) => r.status === "fail");
    const hasWarn = results.some((r) => r.status === "warn");
    if (hasFail) return { label: "FAIL", icon: XCircle, color: "text-destructive", bg: "bg-destructive/5 border-destructive/20" };
    if (hasWarn) return { label: "PASS (with warnings)", icon: AlertTriangle, color: "text-amber-400", bg: "bg-amber-400/5 border-amber-400/20" };
    return { label: "PASS", icon: CheckCircle, color: "text-emerald-400", bg: "bg-emerald-400/5 border-emerald-400/20" };
  }, [results]);

  const toggleCheckpoint = (id: string, field: keyof CheckpointEntry) => {
    setCheckpoints((prev) =>
      prev.map((cp) => (cp.id === id ? { ...cp, [field]: !(cp as any)[field] } : cp))
    );
  };

  const VerdictIcon = overallVerdict.icon;

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col flex-1 min-h-[400px]">
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <FolderOpen className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            Run Folder Package Auditor
          </span>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded border text-[10px] font-mono font-bold ${overallVerdict.bg} ${overallVerdict.color}`}>
          <VerdictIcon className="h-3.5 w-3.5" />
          {overallVerdict.label}
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Left: Folder Configurator */}
        <div className="w-full lg:w-72 border-r border-border bg-card/40 p-4 flex flex-col gap-4 overflow-y-auto">
          {/* Metadata */}
          <div className="space-y-2">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              <FileText className="h-3 w-3 inline" /> metadata.json
            </span>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={metaOperatorPresent}
                onChange={() => setMetaOperatorPresent((v) => !v)}
                className="accent-primary"
              />
              <span className="text-[10px] font-mono text-muted-foreground">operator present</span>
            </div>
            <input
              type="text"
              value={metaOperator}
              onChange={(e) => setMetaOperator(e.target.value)}
              disabled={!metaOperatorPresent}
              className="w-full bg-muted border border-border rounded px-2 py-1.5 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none disabled:opacity-40"
              placeholder="operator name"
            />
            <input
              type="text"
              value={metaVersion}
              onChange={(e) => setMetaVersion(e.target.value)}
              className="w-full bg-muted border border-border rounded px-2 py-1.5 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none"
              placeholder="schema_version"
            />
          </div>

          {/* Patrol Plan */}
          <div className="space-y-2">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              <Save className="h-3 w-3 inline" /> patrol_plan.json
            </span>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={planCheckpoints}
                onChange={() => setPlanCheckpoints((v) => !v)}
                className="accent-primary"
              />
              <span className="text-[10px] font-mono text-muted-foreground">checkpoints declared</span>
            </div>
            <div>
              <label className="text-[9px] font-mono text-muted-foreground block"># of legs</label>
              <input
                type="number"
                value={planLegsCount}
                onChange={(e) => setPlanLegsCount(parseInt(e.target.value) || 0)}
                className="w-full bg-muted border border-border rounded px-2 py-1.5 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none"
              />
            </div>
          </div>

          {/* State Log */}
          <div className="space-y-2">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              <Activity className="h-3 w-3 inline" /> sportmodestate.jsonl
            </span>
            <div>
              <label className="text-[9px] font-mono text-muted-foreground block">JSONL entries</label>
              <input
                type="number"
                value={stateLines}
                onChange={(e) => setStateLines(parseInt(e.target.value) || 0)}
                className="w-full bg-muted border border-border rounded px-2 py-1.5 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none"
              />
            </div>
          </div>

          {/* Checkpoints */}
          <div className="space-y-2 border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              checkpoints/ tree
            </span>
            {checkpoints.map((cp) => (
              <div key={cp.id} className="bg-muted/50 border border-border rounded p-2.5 space-y-1.5">
                <span className="text-[10px] font-mono text-foreground font-bold">{cp.id}/</span>
                <div className="space-y-1">
                  {(["frameExists", "frameTooSmall", "stateSliceExists", "notesExist"] as const).map((f) => (
                    <label key={f} className="flex items-center gap-1.5 text-[9px] font-mono text-muted-foreground cursor-pointer">
                      <input
                        type="checkbox"
                        checked={cp[f]}
                        onChange={() => toggleCheckpoint(cp.id, f)}
                        className="accent-primary h-3 w-3"
                      />
                      {f === "frameExists" ? "frame.jpg" : f === "frameTooSmall" ? "frame → too small" : f === "stateSliceExists" ? "state_slice.jsonl" : "notes.md"}
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Audit Results */}
        <div className="flex-1 p-5 flex flex-col gap-4 overflow-y-auto">
          <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block">
            Validator Output ({results.length} checks)
          </span>

          <div className="space-y-1.5 flex-1">
            {results.map((r, i) => (
              <div
                key={i}
                className={`flex items-center gap-3 px-3 py-2 rounded border text-[10px] font-mono ${
                  r.status === "pass"
                    ? "bg-emerald-400/5 border-emerald-400/15 text-emerald-400"
                    : r.status === "warn"
                    ? "bg-amber-400/5 border-amber-400/15 text-amber-400"
                    : "bg-destructive/5 border-destructive/15 text-destructive"
                }`}
              >
                {r.status === "pass" ? <CheckCircle className="h-3.5 w-3.5 shrink-0" /> : r.status === "warn" ? <AlertTriangle className="h-3.5 w-3.5 shrink-0" /> : <XCircle className="h-3.5 w-3.5 shrink-0" />}
                <span className="text-muted-foreground shrink-0">{r.field}</span>
                <span className="flex-1 text-right opacity-80">{r.message}</span>
              </div>
            ))}
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-3 gap-3 border-t border-border pt-3">
            {[
              { label: "PASS", count: results.filter((r) => r.status === "pass").length, color: "text-emerald-400" },
              { label: "WARN", count: results.filter((r) => r.status === "warn").length, color: "text-amber-400" },
              { label: "FAIL", count: results.filter((r) => r.status === "fail").length, color: "text-destructive" },
            ].map((s) => (
              <div key={s.label} className="text-center bg-muted/30 rounded-lg p-2.5 border border-border">
                <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block">{s.label}</span>
                <span className={`text-lg font-mono font-bold ${s.color}`}>{s.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}