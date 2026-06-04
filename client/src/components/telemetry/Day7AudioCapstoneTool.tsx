import { useState, useMemo } from "react";
import { Volume2, Lightbulb, Mic, Play, Square, SkipForward, CheckCircle, AlertTriangle } from "lucide-react";

type CapstonePhase = "idle" | "ready_check" | "announce" | "gesture" | "status" | "shutdown";

interface LedState {
  r: number;
  g: number;
  b: number;
}

const LED_COLORS: Record<string, LedState> = {
  blue: { r: 0, g: 0, b: 255 },
  red: { r: 255, g: 0, b: 0 },
  green: { r: 0, g: 255, b: 0 },
  off: { r: 0, g: 0, b: 0 },
  purple: { r: 128, g: 0, b: 128 },
  yellow: { r: 255, g: 200, b: 0 },
  cyan: { r: 0, g: 255, b: 255 },
};

const PHASE_SEQUENCE: { phase: CapstonePhase; label: string; led: keyof typeof LED_COLORS; tts: string; sleep: number; action?: string }[] = [
  { phase: "ready_check", label: "READY_CHECK", led: "blue", tts: "", sleep: 1, action: "Confirm rt/lowstate, operator role, clear space." },
  { phase: "announce", label: "ANNOUNCE_START", led: "blue", tts: "Starting Day 7 capstone.", sleep: 4, action: "TTS speaks + LED blue." },
  { phase: "gesture", label: "GESTURE", led: "red", tts: "", sleep: 4, action: "WaveHand() — one bounded physical action." },
  { phase: "status", label: "STATUS_UPDATE", led: "green", tts: "Gesture complete.", sleep: 3, action: "LED green + TTS confirms." },
  { phase: "shutdown", label: "SHUTDOWN_SIGNAL", led: "off", tts: "Capstone complete.", sleep: 2, action: "LED off, return to safe state." },
];

export default function Day7AudioCapstoneTool() {
  const [volume, setVolume] = useState(70);
  const [speakerId, setSpeakerId] = useState(1);
  const [customText, setCustomText] = useState("Day seven audio lab is ready.");
  const [currentLed, setCurrentLed] = useState<keyof typeof LED_COLORS>("off");
  const [activePhase, setActivePhase] = useState<CapstonePhase>("idle");
  const [phaseIdx, setPhaseIdx] = useState(-1);
  const [running, setRunning] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const [readinessOk, setReadinessOk] = useState(true);
  const [singleOwner, setSingleOwner] = useState(true);

  const addLog = (msg: string) => {
    setLog((prev) => [...prev.slice(-24), `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const setLed = (color: keyof typeof LED_COLORS) => {
    setCurrentLed(color);
    const c = LED_COLORS[color];
    addLog(`LedControl(${c.r}, ${c.g}, ${c.b}) → rc=0`);
  };

  const doTts = (text: string) => {
    addLog(`TtsMaker("${text}", speaker_id=${speakerId}) → rc=0`);
  };

  const runVolumeProbe = () => {
    addLog(`GetVolume() → ${volume}`);
    addLog(`SetVolume(${volume}) → rc=0`);
  };

  const startCapstone = () => {
    if (!readinessOk) { addLog("BLOCKED: Readiness gate not satisfied."); return; }
    if (!singleOwner) { addLog("BLOCKED: Multiple DDS session owners detected."); return; }
    setRunning(true);
    setPhaseIdx(0);
    const first = PHASE_SEQUENCE[0];
    setActivePhase(first.phase);
    setLed(first.led);
    if (first.tts) doTts(first.tts);
    addLog(`CAPSTONE START → ${first.label}: ${first.action}`);
  };

  const advancePhase = () => {
    const nextIdx = phaseIdx + 1;
    if (nextIdx >= PHASE_SEQUENCE.length) {
      setRunning(false);
      setPhaseIdx(-1);
      setActivePhase("idle");
      setLed("off");
      addLog("CAPSTONE COMPLETE — log results saved.");
      return;
    }
    setPhaseIdx(nextIdx);
    const step = PHASE_SEQUENCE[nextIdx];
    setActivePhase(step.phase);
    setLed(step.led);
    if (step.tts) doTts(step.tts);
    addLog(`${step.label}: ${step.action}`);
  };

  const resetAll = () => {
    setRunning(false);
    setPhaseIdx(-1);
    setActivePhase("idle");
    setLed("off");
    addLog("RESET — all state returned to idle.");
  };

  const currentLedColor = LED_COLORS[currentLed];

  const rgbString = `rgb(${currentLedColor.r}, ${currentLedColor.g}, ${currentLedColor.b})`;

  return (
    <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col flex-1 min-h-[400px]">
      <div className="bg-muted/40 border-b border-border px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Volume2 className="h-4 w-4 text-primary" />
          <span className="font-mono text-[10px] text-primary font-bold uppercase tracking-widest">
            Capstone Audio, Speech & LED Console
          </span>
        </div>
        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-1.5 text-[9px] font-mono ${readinessOk ? "text-emerald-400" : "text-destructive"}`}>
            {readinessOk ? <CheckCircle className="h-3 w-3" /> : <AlertTriangle className="h-3 w-3" />}
            {readinessOk ? "READY" : "NOT READY"}
          </div>
          <div className={`flex items-center gap-1.5 text-[9px] font-mono ${singleOwner ? "text-emerald-400" : "text-destructive"}`}>
            {singleOwner ? <CheckCircle className="h-3 w-3" /> : <AlertTriangle className="h-3 w-3" />}
            {singleOwner ? "SINGLE OWNER" : "MULTI OWNER"}
          </div>
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Left: Audio & LED Controls */}
        <div className="w-full lg:w-72 border-r border-border bg-card/40 p-4 flex flex-col gap-4">
          {/* Readiness Gate */}
          <div className="border border-border rounded-lg p-3 bg-muted/20 space-y-2">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary block">
              Readiness Gate
            </span>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={readinessOk} onChange={() => setReadinessOk((v) => !v)} className="accent-primary" />
              rt/lowstate + interface ok
            </label>
            <label className="flex items-center gap-2 text-[10px] font-mono text-muted-foreground cursor-pointer">
              <input type="checkbox" checked={singleOwner} onChange={() => setSingleOwner((v) => !v)} className="accent-primary" />
              Single DDS session owner
            </label>
          </div>

          {/* Audio */}
          <div className="space-y-2">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary flex items-center gap-1.5">
              <Volume2 className="h-3 w-3" /> AudioClient
            </span>
            <div>
              <label className="text-[9px] font-mono text-muted-foreground flex justify-between">
                <span>Volume</span>
                <span>{volume}</span>
              </label>
              <input
                type="range"
                min={0}
                max={100}
                value={volume}
                onChange={(e) => setVolume(parseInt(e.target.value))}
                className="w-full accent-primary"
              />
            </div>
            <button
              onClick={runVolumeProbe}
              className="w-full px-3 py-2 bg-muted border border-border rounded text-[10px] font-mono font-bold hover:bg-accent transition-all"
            >
              Probe Volume
            </button>
            <div>
              <label className="text-[9px] font-mono text-muted-foreground block mb-1">
                Speaker ID ({speakerId === 0 ? "Chinese" : "English"})
              </label>
              <div className="grid grid-cols-2 gap-1">
                {[0, 1].map((id) => (
                  <button
                    key={id}
                    onClick={() => setSpeakerId(id)}
                    className={`px-2 py-1.5 rounded text-[10px] font-mono font-bold transition-all ${
                      speakerId === id ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                    }`}
                  >
                    {id} — {id === 0 ? "中文" : "EN"}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-[9px] font-mono text-muted-foreground block mb-1">Custom TTS Text</label>
              <input
                type="text"
                value={customText}
                onChange={(e) => setCustomText(e.target.value)}
                className="w-full bg-muted border border-border rounded px-2 py-1.5 text-[11px] font-mono text-foreground focus:border-primary focus:outline-none"
              />
            </div>
            <button
              onClick={() => doTts(customText)}
              disabled={!readinessOk}
              className="w-full px-3 py-2 bg-primary text-primary-foreground rounded text-[10px] font-mono font-bold disabled:opacity-40"
            >
              <Mic className="h-3 w-3 inline mr-1" /> Speak Custom Text
            </button>
          </div>

          {/* LED */}
          <div className="space-y-2 border-t border-border pt-3">
            <span className="text-[9px] uppercase tracking-widest font-mono text-primary flex items-center gap-1.5">
              <Lightbulb className="h-3 w-3" /> LedControl
            </span>
            <div className="grid grid-cols-3 gap-1">
              {Object.keys(LED_COLORS).filter((c) => !["purple", "yellow", "cyan"].includes(c)).map((color) => (
                <button
                  key={color}
                  onClick={() => setLed(color as keyof typeof LED_COLORS)}
                  className={`px-2 py-2 rounded text-[9px] font-mono font-bold transition-all border ${
                    currentLed === color ? "border-foreground shadow-sm scale-105" : "border-border hover:bg-accent"
                  }`}
                >
                  <div
                    className="w-full h-4 rounded mb-1 border border-border/30"
                    style={{ backgroundColor: `rgb(${LED_COLORS[color].r},${LED_COLORS[color].g},${LED_COLORS[color].b})` }}
                  />
                  {color}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right: Capstone State Machine + LED Visualizer */}
        <div className="flex-1 p-5 flex flex-col gap-4">
          {/* LED Visualizer */}
          <div className="bg-muted/30 border border-border rounded-lg p-4 flex items-center gap-4">
            <div
              className="w-16 h-16 rounded-lg border-2 border-border shadow-lg transition-all duration-500 flex-shrink-0"
              style={{ backgroundColor: rgbString, boxShadow: `0 0 24px ${rgbString}40` }}
            />
            <div>
              <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block">
                Current LED State
              </span>
              <span className="text-lg font-serif font-bold text-foreground capitalize">{currentLed}</span>
              <p className="text-[9px] font-mono text-muted-foreground">
                R:{currentLedColor.r} G:{currentLedColor.g} B:{currentLedColor.b}
              </p>
              {/* Phase meaning */}
              <p className="text-[9px] font-mono text-primary/80 mt-0.5">
                {currentLed === "blue" && "Starting / standby / demo mode"}
                {currentLed === "red" && "Attention / action in progress"}
                {currentLed === "green" && "Ready / safe / successful completion"}
                {currentLed === "off" && "Sequence complete or reset"}
              </p>
            </div>
          </div>

          {/* Capstone State Machine */}
          <div className="bg-muted/30 border border-border rounded-lg p-4 flex-1 flex flex-col">
            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">
              Capstone State Machine
            </span>
            <div className="flex-1 flex items-center gap-2">
              {PHASE_SEQUENCE.map((step, i) => {
                const isActive = phaseIdx === i;
                const isDone = phaseIdx > i;
                const isFuture = phaseIdx < i;
                return (
                  <div key={step.phase} className="flex-1 flex flex-col items-center gap-1.5">
                    {/* Phase card */}
                    <div
                      className={`w-full rounded-lg border p-3 text-center transition-all ${
                        isActive
                          ? "border-primary bg-primary/10 shadow-md shadow-primary/20 scale-105"
                          : isDone
                          ? "border-emerald-400/30 bg-emerald-400/5"
                          : "border-border bg-muted/40 opacity-50"
                      }`}
                    >
                      <span className={`text-[8px] font-mono font-bold block ${
                        isActive ? "text-primary" : isDone ? "text-emerald-400" : "text-muted-foreground"
                      }`}>
                        {step.label}
                      </span>
                      <div
                        className={`w-full h-3 rounded mt-1.5 mb-1 border border-border/20`}
                        style={{
                          backgroundColor: isDone || isActive ? `rgb(${LED_COLORS[step.led].r},${LED_COLORS[step.led].g},${LED_COLORS[step.led].b})` : "transparent",
                        }}
                      />
                      <span className="text-[7px] font-mono text-muted-foreground block leading-tight">
                        {step.tts ? `TTS: "${step.tts}"` : `${step.sleep}s wait`}
                      </span>
                    </div>
                    {/* Connector */}
                    {i < PHASE_SEQUENCE.length - 1 && (
                      <div className={`w-full h-0.5 rounded ${isDone ? "bg-emerald-400/40" : "bg-border"}`} />
                    )}
                  </div>
                );
              })}
            </div>

            {/* Capstone Controls */}
            <div className="flex items-center gap-2 mt-4 justify-center">
              {!running ? (
                <button
                  onClick={startCapstone}
                  disabled={!readinessOk || !singleOwner}
                  className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded text-xs font-mono font-bold disabled:opacity-40"
                >
                  <Play className="h-3.5 w-3.5" /> Start Capstone
                </button>
              ) : (
                <>
                  <button
                    onClick={advancePhase}
                    className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded text-xs font-mono font-bold"
                  >
                    <SkipForward className="h-3.5 w-3.5" /> Next Phase
                  </button>
                  <button
                    onClick={resetAll}
                    className="flex items-center gap-2 px-4 py-2 bg-destructive/10 border border-destructive/30 text-destructive rounded text-xs font-mono font-bold"
                  >
                    <Square className="h-3.5 w-3.5" /> Abort
                  </button>
                </>
              )}
              {!running && (
                <button
                  onClick={resetAll}
                  className="px-4 py-2 bg-muted border border-border rounded text-xs font-mono font-bold text-muted-foreground hover:text-foreground"
                >
                  Reset
                </button>
              )}
            </div>
          </div>

          {/* Event Log */}
          <div className="bg-[#0a192f] border border-border rounded-lg p-3 max-h-[100px] overflow-y-auto">
            <span className="text-[8px] uppercase tracking-widest font-mono text-primary/70 block mb-1.5">Audio/LED Event Log</span>
            <div className="space-y-0.5">
              {log.length === 0 && (
                <span className="text-[9px] font-mono text-muted-foreground/40">Console ready — probe volume or start capstone...</span>
              )}
              {log.map((entry, i) => (
                <div key={i} className="text-[9px] font-mono text-[#a9b7c6] leading-relaxed">{entry}</div>
              ))}
            </div>
          </div>

          {/* Interaction Contract Summary */}
          <div className="border-t border-border pt-3 grid grid-cols-2 lg:grid-cols-4 gap-2 text-[9px] font-mono">
            {[
              { label: "Operator", val: "Single DDS owner" },
              { label: "Language", val: speakerId === 0 ? "Chinese (0)" : "English (1)" },
              { label: "Physical", val: "WaveHand() only" },
              { label: "Stop Rule", val: "Unexpected motion / rc≠0 / instructor" },
              { label: "Volume", val: `${volume}%` },
              { label: "LED Wait", val: "≥ 1s between calls" },
              { label: "Hand Scope", val: "No dexterous hand" },
              { label: "Evidence", val: "Terminal output + log" },
            ].map((item) => (
              <div key={item.label} className="bg-muted/30 border border-border rounded px-2 py-1.5">
                <span className="text-muted-foreground block text-[8px]">{item.label}</span>
                <span className="text-foreground font-bold">{item.val}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}