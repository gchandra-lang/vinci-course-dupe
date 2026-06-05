import { useState, useMemo } from "react";
import { Gauge, Activity, Zap, Crosshair, AlertTriangle, CheckCircle, Play, Square } from "lucide-react";

type ControlSurface = "locomotion" | "arm_rpc" | "arm_sdk";

interface MotionState {
  velocityX: number;
  velocityYaw: number;
  stopMoveActive: boolean;
  fsmSafe: boolean;
}

interface ArmAction {
  name: string;
  safe: boolean;
  personContact: boolean;
}

const ARM_ACTIONS: ArmAction[] = [
  { name: "face wave", safe: true, personContact: false },
  { name: "high wave", safe: true, personContact: false },
  { name: "release arm", safe: true, personContact: false },
  { name: "shake hand", safe: false, personContact: true },
  { name: "high five", safe: false, personContact: true },
  { name: "hug", safe: false, personContact: true },
];

const ARM_SDK_STAGES = [
  { stage: 1, name: "Enable", desc: "Claim upper-body command authority (index-29)", duration: 3 },
  { stage: 2, name: "Demonstrate", desc: "Interpolate toward target arm pose", duration: 6 },
  { stage: 3, name: "Blend Back", desc: "Blend toward measured/neutral pose", duration: 9 },
  { stage: 4, name: "Disable", desc: "Ramp enable field toward disable", duration: 3 },
];

export default function Day6MotionControlSimulator() {
  const [activeSurface, setActiveSurface] = useState<ControlSurface>("locomotion");
  const [motion, setMotion] = useState<MotionState>({ velocityX: 0.15, velocityYaw: 0, stopMoveActive: true, fsmSafe: true });
  const [selectedAction, setSelectedAction] = useState<string>("face wave");
  const [sdkStage, setSdkStage] = useState(0);
  const [sdkRunning, setSdkRunning] = useState(false);
  const [sdkElapsed, setSdkElapsed] = useState(0);
  const [armReleased, setArmReleased] = useState(true);
  const [log, setLog] = useState<string[]>([]);

  const readinessGate = motion.fsmSafe; // simplified

  const addLogEntry = (msg: string) => {
    setLog((prev) => [...prev.slice(-19), `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const handleLocomotion = (action: string) => {
    if (!readinessGate) { addLogEntry("BLOCKED: FSM not safe — locomotion rejected."); return; }
    switch (action) {
      case "move":
        setMotion((m) => ({ ...m, stopMoveActive: false }));
        addLogEntry("Move(vx=0.15, vy=0, vyaw=0) → executing...");
        break;
      case "stop":
        setMotion((m) => ({ ...m, stopMoveActive: true }));
        addLogEntry("StopMove() → velocity zeroed.");
        break;
      case "stand":
        addLogEntry("HighStand() / LowStand() → posture cycle (visual).");
        break;
      case "wave":
        addLogEntry("WaveHand() via LocoClient → wave gesture.");
        break;
      case "damp":
        setMotion((m) => ({ ...m, fsmSafe: false }));
        addLogEntry("⚠ Damp() invoked — FSM now blocked. Use only for emergency.");
        break;
      case "recover":
        setMotion((m) => ({ ...m, fsmSafe: true }));
        addLogEntry("RecoveryStand() → FSM restored.");
        break;
    }
  };

  const handleArmAction = () => {
    if (!readinessGate) { addLogEntry("BLOCKED: FSM not safe — arm action rejected."); return; }
    const action = ARM_ACTIONS.find((a) => a.name === selectedAction);
    if (!action) return;
    if (!action.safe) {
      addLogEntry(`⚠ ${selectedAction}: instructor-approved only (person-contact).`);
      return;
    }
    addLogEntry(`G1ArmActionClient → ExecuteAction("${selectedAction}") → rc=0`);
    setArmReleased(false);
    if (selectedAction === "release arm") setArmReleased(true);
  };

  const handleRelease = () => {
    addLogEntry("release arm → neutral state.");
    setArmReleased(true);
  };

  const startSdk = () => {
    if (!readinessGate) { addLogEntry("BLOCKED: FSM not safe — arm SDK rejected."); return; }
    setSdkRunning(true);
    setSdkStage(1);
    setSdkElapsed(0);
    addLogEntry("rt/arm_sdk: Stage 1 ENABLE (index-29, blend to zero pose).");
  };

  const stopSdk = () => {
    setSdkRunning(false);
    setSdkStage(0);
    setSdkElapsed(0);
    addLogEntry("rt/arm_sdk: Disable → command ownership returned.");
  };

  const advanceSdk = () => {
    if (sdkStage < 4) {
      const next = sdkStage + 1;
      setSdkStage(next);
      setSdkElapsed(ARM_SDK_STAGES[next - 1].duration);
      addLogEntry(`rt/arm_sdk: Stage ${next} ${ARM_SDK_STAGES[next - 1].name.toUpperCase()} — ${ARM_SDK_STAGES[next - 1].desc}.`);
    } else {
      stopSdk();
    }
  };

  const activeArm = ARM_ACTIONS.find((a) => a.name === selectedAction);

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col min-h-[420px]">
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Gauge className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            G1 Motion & Arm Control Simulator
          </span>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded border text-[10px] font-mono font-bold ${
          readinessGate ? "bg-emerald-400/10 border-emerald-400/30 text-emerald-400" : "bg-destructive/10 border-destructive/30 text-destructive"
        }`}>
          {readinessGate ? <CheckCircle className="h-3.5 w-3.5" /> : <AlertTriangle className="h-3.5 w-3.5" />}
          {readinessGate ? "FSM SAFE" : "FSM BLOCKED"}
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Left: Control Surface Selector */}
        <div className="w-full lg:w-72 border-r border-border bg-card/40 p-4 flex flex-col gap-4 overflow-y-auto">
          {/* Surface Tabs */}
          <div>
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">
              Active Control Surface
            </span>
            <div className="grid grid-cols-3 gap-1">
              {([
                { key: "locomotion", label: "Locomotion", icon: Activity },
                { key: "arm_rpc", label: "Arm RPC", icon: Crosshair },
                { key: "arm_sdk", label: "Arm SDK", icon: Zap },
              ] as const).map(({ key, label, icon: Icon }) => (
                <button
                  key={key}
                  onClick={() => { setActiveSurface(key); if (key !== "arm_sdk") stopSdk(); }}
                  className={`flex flex-col items-center gap-1 px-2 py-3 rounded text-[9px] font-mono font-bold transition-all ${
                    activeSurface === key
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "bg-muted text-muted-foreground hover:bg-accent"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Surface-specific controls */}
          {activeSurface === "locomotion" && (
            <div className="space-y-2 border-t border-border pt-3">
              <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">LocoClient</span>
              <div className="grid grid-cols-2 gap-1.5">
                {[
                  { key: "move", label: "Move()", cls: "bg-primary/10 hover:bg-primary/20 text-primary" },
                  { key: "stop", label: "StopMove()", cls: "bg-emerald-400/10 hover:bg-emerald-400/20 text-emerald-400" },
                  { key: "wave", label: "WaveHand()", cls: "hover:bg-accent" },
                  { key: "stand", label: "Stand()", cls: "hover:bg-accent" },
                  { key: "damp", label: "Damp() ⚠", cls: "bg-destructive/10 hover:bg-destructive/20 text-destructive" },
                  { key: "recover", label: "Recover", cls: "bg-amber-400/10 hover:bg-amber-400/20 text-amber-400" },
                ].map(({ key, label, cls }) => (
                  <button
                    key={key}
                    onClick={() => handleLocomotion(key)}
                    disabled={!readinessGate && key !== "recover" && key !== "damp"}
                    className={`px-2 py-2 rounded text-[10px] font-mono font-bold transition-all disabled:opacity-40 disabled:pointer-events-none border border-border ${cls}`}
                  >
                    {label}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2 mt-2 p-2 bg-muted/30 rounded border border-border">
                <span className="text-[9px] font-mono text-muted-foreground">Status:</span>
                <span className={`text-[9px] font-mono font-bold ${motion.stopMoveActive ? "text-emerald-400" : "text-primary"}`}>
                  {motion.stopMoveActive ? "STOPPED" : `MOVING vx=${motion.velocityX}`}
                </span>
              </div>
            </div>
          )}

          {activeSurface === "arm_rpc" && (
            <div className="space-y-2 border-t border-border pt-3">
              <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
                G1ArmActionClient ("arm" RPC)
              </span>
              <div className="space-y-1">
                {ARM_ACTIONS.map((action) => (
                  <button
                    key={action.name}
                    onClick={() => setSelectedAction(action.name)}
                    className={`w-full text-left px-3 py-2 rounded text-[10px] font-mono font-bold transition-all border ${
                      selectedAction === action.name
                        ? action.safe ? "border-primary bg-primary/10 text-foreground" : "border-destructive bg-destructive/10 text-destructive"
                        : "border-transparent hover:bg-accent text-muted-foreground"
                    }`}
                  >
                    {action.name}
                    {!action.safe && <span className="ml-1 text-[8px] text-destructive">⚠ contact</span>}
                  </button>
                ))}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleArmAction}
                  disabled={!readinessGate || !activeArm?.safe}
                  className="flex-1 px-3 py-2 bg-primary text-primary-foreground rounded text-[10px] font-mono font-bold disabled:opacity-40 disabled:pointer-events-none"
                >
                  <Play className="h-3 w-3 inline mr-1" /> Execute
                </button>
                <button
                  onClick={handleRelease}
                  className="px-3 py-2 bg-emerald-500/10 border border-emerald-400/30 text-emerald-400 rounded text-[10px] font-mono font-bold hover:bg-emerald-500/20"
                >
                  Release Arm
                </button>
              </div>
            </div>
          )}

          {activeSurface === "arm_sdk" && (
            <div className="space-y-2 border-t border-border pt-3">
              <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
                rt/arm_sdk Streaming
              </span>
              <div className="space-y-1.5">
                {ARM_SDK_STAGES.map((s) => (
                  <div
                    key={s.stage}
                    className={`flex items-center gap-2 px-3 py-2 rounded border text-[10px] font-mono transition-all ${
                      sdkStage === s.stage
                        ? "border-primary bg-primary/10 text-foreground"
                        : sdkStage > s.stage
                        ? "border-emerald-400/20 bg-emerald-400/5 text-emerald-400"
                        : "border-border bg-muted/30 text-muted-foreground"
                    }`}
                  >
                    <span className="h-5 w-5 rounded-full bg-primary/20 text-primary flex items-center justify-center text-[9px] font-bold">
                      {s.stage}
                    </span>
                    <span>{s.name}</span>
                    <span className="ml-auto text-[8px] text-muted-foreground">{s.duration}s</span>
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                {!sdkRunning ? (
                  <button onClick={startSdk} disabled={!readinessGate} className="flex-1 px-3 py-2 bg-primary text-primary-foreground rounded text-[10px] font-mono font-bold disabled:opacity-40">
                    <Play className="h-3 w-3 inline mr-1" /> Start Stream
                  </button>
                ) : (
                  <>
                    <button onClick={advanceSdk} className="flex-1 px-3 py-2 bg-primary text-primary-foreground rounded text-[10px] font-mono font-bold">
                      Next Stage →
                    </button>
                    <button onClick={stopSdk} className="px-3 py-2 bg-destructive/10 border border-destructive/30 text-destructive rounded text-[10px] font-mono font-bold">
                      <Square className="h-3 w-3" />
                    </button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Integration Policy Reminder */}
          <div className="mt-auto border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-amber-400 block mb-1.5">
              One Command Path at a Time
            </span>
            <p className="text-[9px] font-mono text-muted-foreground leading-relaxed">
              Finish one pipeline completely. Wait 10+ seconds. Re-check readiness. Never interleave arm SDK and RPC in one process.
            </p>
          </div>
        </div>

        {/* Right: State Visualization & Log */}
        <div className="flex-1 p-5 flex flex-col gap-4">
          {/* Command-Owner Dashboard */}
          <div className="grid grid-cols-3 gap-3">
            {([
              { label: "Readiness", status: readinessGate ? "PASS" : "FAIL", color: readinessGate ? "emerald" : "destructive" },
              { label: "Active Surface", status: activeSurface === "locomotion" ? "LOCO" : activeSurface === "arm_rpc" ? "RPC" : "SDK", color: "primary" },
              { label: "Arm State", status: armReleased ? "NEUTRAL" : "ACTIVE", color: armReleased ? "muted" : "amber" },
            ] as const).map((s) => (
              <div
                key={s.label}
                className={`bg-muted/30 border rounded-lg p-3 text-center ${
                  s.color === "emerald" ? "border-emerald-400/20" : s.color === "destructive" ? "border-destructive/20" : s.color === "amber" ? "border-amber-400/20" : "border-border"
                }`}
              >
                <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-1">{s.label}</span>
                <span className={`text-sm font-mono font-bold ${
                  s.color === "emerald" ? "text-emerald-400" : s.color === "destructive" ? "text-destructive" : s.color === "amber" ? "text-amber-400" : "text-primary"
                }`}>
                  {s.status}
                </span>
              </div>
            ))}
          </div>

          {/* Arm SDK Timeline */}
          {activeSurface === "arm_sdk" && (
            <div className="bg-muted/30 border border-border rounded-lg p-4">
              <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">
                Four-Stage Streaming Timeline (~21s @ duration_=3.0)
              </span>
              <div className="relative h-10 bg-muted rounded-lg border border-border overflow-hidden">
                {ARM_SDK_STAGES.map((s) => (
                  <div
                    key={s.stage}
                    className={`absolute top-0 bottom-0 border-r border-border/50 flex items-center justify-center transition-all ${
                      sdkStage >= s.stage ? "bg-primary/30" : "bg-muted/50"
                    }`}
                    style={{ left: `${((s.stage - 1) / 4) * 100}%`, width: `${(1 / 4) * 100}%` }}
                  >
                    <span className={`text-[8px] font-mono font-bold ${sdkStage >= s.stage ? "text-primary" : "text-muted-foreground"}`}>
                      {s.name}
                    </span>
                  </div>
                ))}
                {sdkRunning && (
                  <div
                    className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg shadow-white/30 transition-all"
                    style={{ left: `${Math.min(98, ((sdkStage - 1) / 4 * 100) + (sdkElapsed / 21) * 25)}%` }}
                  />
                )}
              </div>
            </div>
          )}

          {/* Motion Visualization (locomotion only) */}
          {activeSurface === "locomotion" && (
            <div className="bg-muted/30 border border-border rounded-lg p-4 flex-1 flex flex-col">
              <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">
                Body-Frame Velocity Visualization
              </span>
              <div className="flex-1 flex items-center justify-center relative">
                {/* Robot body center */}
                <div className="relative w-32 h-32">
                  <div className="absolute inset-0 border-2 border-border rounded-lg bg-muted/50 flex items-center justify-center">
                    <div className="w-12 h-16 border-2 border-primary/60 rounded bg-primary/10 flex items-center justify-center">
                      <span className="text-[9px] font-mono text-primary font-bold">G1</span>
                    </div>
                    {/* Direction indicator */}
                    {!motion.stopMoveActive && (
                      <>
                        <div className="absolute top-1/2 left-1/2 -translate-y-1/2" style={{ transform: `translate(-50%, -50%) rotate(${motion.velocityYaw * 30}deg) ` }}>
                          <div className="w-0 h-0 border-l-[8px] border-r-[8px] border-b-[20px] border-l-transparent border-r-transparent border-b-primary animate-pulse"
                            style={{ marginTop: "-40px" }}
                          />
                        </div>
                        <span className="absolute -top-1 left-1/2 -translate-x-1/2 text-[9px] font-mono text-primary font-bold">
                          vx={motion.velocityX.toFixed(2)}
                        </span>
                      </>
                    )}
                    {motion.stopMoveActive && (
                      <div className="absolute -top-6 left-1/2 -translate-x-1/2">
                        <Square className="h-4 w-4 text-emerald-400" />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Non-locomotion: Arm State Display */}
          {activeSurface !== "locomotion" && (
            <div className="bg-muted/30 border border-border rounded-lg p-4 flex-1 flex flex-col items-center justify-center gap-3">
              <div className={`w-20 h-24 border-2 rounded-lg flex items-center justify-center transition-all ${
                armReleased ? "border-emerald-400/30 bg-emerald-400/5" : sdkRunning ? "border-primary/30 bg-primary/5" : "border-amber-400/30 bg-amber-400/5"
              }`}>
                <div className={`text-[9px] font-mono font-bold text-center leading-relaxed ${
                  armReleased ? "text-emerald-400" : sdkRunning ? "text-primary" : "text-amber-400"
                }`}>
                  {armReleased ? "ARMS\nNEUTRAL" : sdkRunning ? "ARMS\nSTREAMING" : "ARMS\nACTIVE"}
                </div>
              </div>
              <p className="text-[9px] font-mono text-muted-foreground text-center max-w-xs">
                {armReleased ? "Arms in neutral position. Safe to switch control surfaces." :
                 sdkRunning ? "rt/arm_sdk owns upper-body command authority. Do not interleave with RPC." :
                 "Arm RPC gesture active. Wait for completion, then release arm."}
              </p>
            </div>
          )}

          {/* Event Log */}
          <div className="bg-[#0a192f] border border-border rounded-lg p-3 max-h-[120px] overflow-y-auto">
            <span className="text-[8px] uppercase tracking-widest font-mono text-primary/70 block mb-1.5">Command Log</span>
            <div className="space-y-0.5">
              {log.length === 0 && (
                <span className="text-[9px] font-mono text-muted-foreground/40">Awaiting commands...</span>
              )}
              {log.map((entry, i) => (
                <div key={i} className="text-[9px] font-mono text-[#a9b7c6] leading-relaxed">{entry}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}