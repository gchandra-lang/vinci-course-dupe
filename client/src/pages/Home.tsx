import { useState, useEffect, useCallback } from "react";
import { createPortal } from "react-dom";
import { 
  BookOpen, 
  Clock, 
  Code, 
  Cpu, 
  Terminal, 
  Play, 
  CheckCircle, 
  AlertTriangle, 
  ArrowRight, 
  ArrowLeft, 
  Layers, 
  ExternalLink,
  ChevronRight,
  Shield,
  Award,
  FileText,
  Activity,
  Maximize2,
  Minimize2,
  Volume2
} from "lucide-react";
import syllabusData from "../data/syllabus.json";

// ── Semantic keyword classifier — maps technical terms to CSS color classes ──
const S_PATTERNS: [RegExp, string][] = [
  [new RegExp("subscribe|observe|listener|passive|read.only|lowest risk|monitor", "i"), "semantic-subscribe"],
  [new RegExp("publish|command topic|send|streaming|medium risk|arm.sdk", "i"), "semantic-publish"],
  [new RegExp("\\brpc\\b|service call|request|checkmode|motionswitcher", "i"), "semantic-rpc"],
  [new RegExp("ready|pass\\b|success|green|stable|squat.stand|go", "i"), "semantic-safe"],
  [new RegExp("fail|damp|danger|abort|blocked|red|zero torque|unsafe", "i"), "semantic-danger"],
];
const semanticClass = (text: string): string => {
  for (const [re, cls] of S_PATTERNS) if (re.test(text)) return cls;
  return "";
};

// ── Diagram placeholder extraction ──
const DIAGRAM_RE = new RegExp("\\[DIAGRAM:\\s*(.+?)\\]", "g");
const extractDiagrams = (text: string): { clean: string; diagrams: string[] } => {
  const diagrams: string[] = [];
  const clean = text.replace(DIAGRAM_RE, (_, d) => { diagrams.push(d.trim()); return ""; }).replace(/\s+/g, " ").trim();
  return { clean, diagrams };
};

// ── Safe HTML renderer — uses dangerouslySetInnerHTML only when the string contains HTML ──
const HTML_TAG_RE = new RegExp("<(details|summary|strong|em|code|span|br|div|p|ul|ol|li|pre|blockquote|table|thead|tbody|tr|td|th|h[1-6]|a|img|hr|sup|sub|del|ins|mark|abbr|kbd|samp|var|small|big|b|i|u|s|dl|dt|dd|figure|figcaption|section|article|aside|nav|header|footer|main|wbr|time|output|progress|meter|ruby|rt|rp|bdi|bdo)", "i");
const SafeHTML = ({ text, className }: { text: string; className?: string }) => {
  if (HTML_TAG_RE.test(text)) {
    return <span className={className} dangerouslySetInnerHTML={{ __html: text }} />;
  }
  return <>{text}</>;
};

import {
  Day2PatrolSimulator,
  Day3ControlAuthority,
  Day4RunFolderAuditor,
  Day5SafetyGatingCalculator,
  Day6MotionControlSimulator,
  Day7AudioCapstoneTool
} from "../components/telemetry";

interface LabFile {
  name: string;
  code: string;
}

interface Lab {
  id: string;
  title: string;
  content: string;
  code_files: LabFile[];
}

interface Slide {
  title: string;
  thesis: string;
  board_type: string;
  board_data: any;
  bottom_band: string;
}

interface Pacing {
  time: string;
  session: string;
  path: string;
}

interface DaySyllabus {
  day: string;
  title: string;
  eyebrow: string;
  thesis: string;
  rules: string[];
  pacing: Pacing[];
  slides: Slide[];
  labs: Lab[];
}

export default function Home() {
  const [activeDay, setActiveDay] = useState<string>("01");
  const [activeSlideIndex, setActiveSlideIndex] = useState<number>(0);
  const [activeLabId, setActiveLabId] = useState<string>("");
  const [activeLabFile, setActiveLabFile] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"lecture" | "labs">("lecture");
  const [copied, setCopied] = useState<boolean>(false);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);
  const [blueprintFullscreen, setBlueprintFullscreen] = useState<boolean>(false);
  const [labGuideFullscreen, setLabGuideFullscreen] = useState<boolean>(false);

  const currentDayData = (syllabusData as Record<string, DaySyllabus>)[activeDay];

  // Reset indices when active day changes
  useEffect(() => {
    setActiveSlideIndex(0);
    if (currentDayData?.labs && currentDayData.labs.length > 0) {
      setActiveLabId(currentDayData.labs[0].id);
      if (currentDayData.labs[0].code_files && currentDayData.labs[0].code_files.length > 0) {
        setActiveLabFile(currentDayData.labs[0].code_files[0].name);
      } else {
        setActiveLabFile("");
      }
    } else {
      setActiveLabId("");
      setActiveLabFile("");
    }
  }, [activeDay]);

  // Handle keyboard controls for slides
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (activeTab !== "lecture" || !currentDayData?.slides) return;
      
      if (e.key === "ArrowRight" || e.key === "Space") {
        e.preventDefault();
        setActiveSlideIndex(prev => Math.min(currentDayData.slides.length - 1, prev + 1));
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        setActiveSlideIndex(prev => Math.max(0, prev - 1));
      } else if (e.key === "Escape") {
        if (isFullscreen) {
          setIsFullscreen(false);
        } else if (blueprintFullscreen) {
          setBlueprintFullscreen(false);
        } else if (labGuideFullscreen) {
          setLabGuideFullscreen(false);
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [activeTab, currentDayData, isFullscreen, blueprintFullscreen, labGuideFullscreen]);

  // Sync labGuideFullscreen state with native Fullscreen API exit (e.g. Esc key)
  useEffect(() => {
    const handleFullscreenChange = () => {
      if (!document.fullscreenElement && labGuideFullscreen) {
        setLabGuideFullscreen(false);
      }
    };
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", handleFullscreenChange);
  }, [labGuideFullscreen]);

  // Handle active lab change
  const handleLabChange = (labId: string) => {
    setActiveLabId(labId);
    const lab = currentDayData.labs.find(l => l.id === labId);
    if (lab && lab.code_files && lab.code_files.length > 0) {
      setActiveLabFile(lab.code_files[0].name);
    } else {
      setActiveLabFile("");
    }
  };

  // Lab fullscreen toggle — activates native HTML5 Fullscreen API on the portal container
  const handleToggleFullscreen = useCallback(() => {
    if (!labGuideFullscreen) {
      // Enter: first set state so the portal mounts, then request native fullscreen
      setLabGuideFullscreen(true);
      // Use rAF to wait for the portal div to be in the DOM
      requestAnimationFrame(() => {
        const element = document.getElementById("lab-guide-container");
        if (element) {
          element.requestFullscreen().catch((err) => console.error("Fullscreen request failed:", err));
        }
      });
    } else {
      // Exit: native fullscreen first, state syncs via fullscreenchange listener
      if (document.fullscreenElement) {
        document.exitFullscreen().catch((err) => console.error("Exit fullscreen failed:", err));
      } else {
        setLabGuideFullscreen(false);
      }
    }
  }, [labGuideFullscreen]);

  const activeLab = currentDayData?.labs?.find(l => l.id === activeLabId);
  const activeCodeFile = activeLab?.code_files?.find(f => f.name === activeLabFile);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Schematic Image Mapping based on Day
  const getDaySchematic = (day: string) => {
    if (day === "01" || day === "02") {
      return "https://d2xsxph8kpxj0f.cloudfront.net/310519663722418623/LnV78sD4YhnG2kJCQKyWmC/quadruped_schematic-DUWbwKpo8zKzLia7SShhSM.webp";
    }
    if (day === "03" || day === "04") {
      return "https://d2xsxph8kpxj0f.cloudfront.net/310519663722418623/LnV78sD4YhnG2kJCQKyWmC/quadruped_schematic-RjoQuK9eKvxRP27zd8KsKz.png"; // Original or other asset
    }
    return "https://d2xsxph8kpxj0f.cloudfront.net/310519663722418623/LnV78sD4YhnG2kJCQKyWmC/humanoid_schematic-PwYwUQShDyDdHD5XrBQURm.webp";
  };

  const currentSlide = currentDayData?.slides?.[activeSlideIndex];

  return (
    <div className="h-screen flex flex-col bg-background text-foreground relative overflow-hidden">
      {/* Subtle Background Watermark (Vinci Style Rule) */}
      <div className="vinci-watermark" />

      {/* Header Bar */}
      <header className="border-b border-border bg-card/80 backdrop-blur-md sticky top-0 z-50 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          {/* User Provided Colored Logo */}
          <img 
            src="https://files.manuscdn.com/user_upload_by_module/session_file/310519663722418623/nYapRyYFGgQxKLFC.png" 
            alt="Vinci AI Logo" 
            className="h-10 object-contain"
          />
          <div className="h-6 w-px bg-border hidden sm:block" />
          <div className="hidden sm:block">
            <h1 className="text-sm font-bold font-serif tracking-tight text-foreground flex items-center gap-2">
              UNITREE ROBOTICS <span className="text-primary font-sans font-semibold text-xs px-2 py-0.5 bg-primary/10 rounded">TRAINING CAMP</span>
            </h1>
            <p className="text-[10px] text-muted-foreground font-mono">7-Day Technical Curriculum</p>
          </div>
        </div>

        {/* Brand Logo Placement (Top-Right Rule) */}
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <span className="text-xs uppercase tracking-widest font-mono text-primary font-bold">Academic Portal</span>
            <p className="text-[10px] text-muted-foreground font-mono">ROS 2 Humble / CycloneDDS</p>
          </div>
          <div className="h-8 w-8 rounded-full border border-primary/20 flex items-center justify-center bg-primary/5 text-primary font-bold text-xs font-mono">
            V
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex flex-col lg:flex-row z-10 relative">
        
        {/* Left Sidebar - Navigation and Pacing */}
        <aside className="w-full lg:w-80 border-r border-border bg-card/40 flex flex-col">
          {/* Day Navigation Tabs */}
          <div className="p-3 border-b border-border bg-card/80">
            <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">Syllabus Calendar</span>
            <div className="grid grid-cols-4 lg:grid-cols-1 gap-2">
              {Object.keys(syllabusData).map((dayKey) => {
                const dayData = (syllabusData as any)[dayKey];
                const isActive = activeDay === dayKey;
                return (
                  <button
                    key={dayKey}
                    onClick={() => setActiveDay(dayKey)}
                    className={`flex items-center gap-2 p-2.5 rounded text-left transition-all ${
                      isActive
                        ? "bg-primary text-primary-foreground shadow-md"
                        : "hover:bg-accent hover:text-accent-foreground text-muted-foreground"
                    }`}
                  >
                    <span className="font-mono text-sm font-bold opacity-80">0{parseInt(dayKey)}</span>
                    <span className="font-serif text-xs font-semibold truncate hidden lg:block">{dayData.title.split(" ")[0]} {dayData.title.split(" ")[1] || ""}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Current Day Metadata — title block locked at top, rules fill remaining space */}
          <div className="p-4 flex flex-col gap-4 flex-1 min-h-0">
            {/* Day title + thesis — locked at top */}
            <div className="shrink-0 space-y-3">
              <div>
                <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">{currentDayData.eyebrow}</span>
                <h2 className="text-xl font-serif font-bold text-foreground mt-1">{currentDayData.title}</h2>
                <div className="h-1 w-12 bg-primary mt-3" />
              </div>

              {/* Daily Thesis Statement (Vinci Left Column Rule) */}
              <div className="border-l-2 border-primary/40 pl-4 py-1">
                <p className="text-xs italic text-muted-foreground font-serif leading-relaxed">
                  <SafeHTML text={`"${currentDayData.thesis}"`} />
                </p>
              </div>
            </div>

            {/* Classroom Safety Rules — fills remaining sidebar space */}
            <div className="bg-primary/[0.06] border border-primary/15 rounded-lg p-4 flex-1 min-h-0 flex flex-col overflow-y-auto">
              <div className="flex items-center gap-2.5 text-primary mb-3 shrink-0">
                <Shield className="h-4 w-4 flex-shrink-0" />
                <span className="text-[10px] uppercase tracking-[0.15em] font-sans font-bold">Classroom Safety Rules</span>
              </div>
              <ul className="space-y-2 text-[11px] leading-relaxed">
                {currentDayData.rules.map((rule, idx) => (
                  <li key={idx} className="flex gap-2.5">
                    <span className="text-primary/70 font-bold select-none flex-shrink-0 mt-px">•</span>
                    <span className="text-muted-foreground">{rule}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </aside>

        {/* Right Main Panel */}
        <main className="flex-1 flex flex-col bg-card/10 relative">
          
          {/* Lecture vs Lab Switcher */}
          <div className="border-b border-border bg-card/60 px-5 py-2 flex items-center justify-between">
            <div className="flex gap-2 bg-muted p-1 rounded-md">
              <button
                onClick={() => setActiveTab("lecture")}
                className={`flex items-center gap-2 px-4 py-1.5 rounded text-xs font-semibold transition-all ${
                  activeTab === "lecture" 
                    ? "bg-card text-foreground shadow-sm" 
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <BookOpen className="h-3.5 w-3.5" />
                Lecture Slides
              </button>
              <button
                onClick={() => setActiveTab("labs")}
                className={`flex items-center gap-2 px-4 py-1.5 rounded text-xs font-semibold transition-all ${
                  activeTab === "labs" 
                    ? "bg-card text-foreground shadow-sm" 
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Code className="h-3.5 w-3.5" />
                Lab Workspaces
                {currentDayData.labs.length > 0 && (
                  <span className="ml-1 bg-primary/10 text-primary text-[10px] px-1.5 py-0.2 rounded-full font-mono font-bold">
                    {currentDayData.labs.length}
                  </span>
                )}
              </button>
            </div>

            <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
              <Clock className="h-3.5 w-3.5" />
              <span>3h Session Ready</span>
            </div>
          </div>

          {/* Tab Contents */}
          <div className="flex-1 p-4 flex flex-col overflow-y-auto">
            
            {/* LECTURE SLIDES TAB */}
            {activeTab === "lecture" && currentDayData.slides && currentDayData.slides.length > 0 && (
              <div className="flex-1 flex flex-col max-w-5xl mx-auto w-full gap-2.5 min-h-0">
                
                {/* Fullscreen Presentation Trigger */}
                <div className="flex justify-end shrink-0">
                  <button
                    onClick={() => setIsFullscreen(true)}
                    className="flex items-center gap-1.5 px-3 py-1.5 border border-primary/20 bg-primary/5 hover:bg-primary/10 text-primary text-[11px] font-bold rounded transition-all"
                  >
                    <Maximize2 className="h-3.5 w-3.5" />
                    Fullscreen Lecture Mode
                  </button>
                </div>

                {/* PPT Slide Wrapper (Styled exactly after Day 1 PPT design) */}
                <div className="border border-border bg-card rounded-lg shadow-xl overflow-hidden relative flex flex-col w-full flex-1 min-h-0">
                  
                  {/* Subtle Diagonal Watermark inside PPT frame */}
                  <div className="vinci-watermark opacity-30" />
                  
                  {/* PPT Slide Header */}
                  <div className="border-b border-border/60 bg-muted/20 px-6 py-3 flex items-center justify-between z-10">
                    <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">
                      Vinci AI Lecture — Day {activeDay}
                    </span>
                    <div className="flex items-center gap-1">
                      <div className="h-1.5 w-1.5 rounded-full bg-primary" />
                      <span className="text-[10px] font-mono text-muted-foreground">
                        Slide {activeSlideIndex + 1} of {currentDayData.slides.length}
                      </span>
                    </div>
                  </div>

                  {/* PPT Slide Body */}
                  <div className="flex-1 px-5 py-4 z-10 overflow-y-auto min-h-0">
                    {currentSlide.board_type === "table" ? (
                      /* Table Slide: Full-Width Layout */
                      <div className="space-y-4">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-border/40 pb-3">
                          <div>
                            <span className="text-xs uppercase tracking-widest font-mono text-primary block mb-1 font-bold">Concept Pillar</span>
                            <h3 className="text-2xl lg:text-3xl font-serif font-bold text-foreground leading-tight">
                              {currentSlide.title}
                            </h3>
                          </div>
                          <div className="bg-primary/5 border border-primary/10 rounded px-4 py-3 max-w-md md:text-right">
                            <span className="text-xs uppercase tracking-widest font-mono text-primary block mb-1 font-bold">Thesis Statement</span>
                            <p className="text-sm font-serif text-foreground/85 leading-relaxed font-medium">
                              <SafeHTML text={`"${currentSlide.thesis}"`} />
                            </p>
                          </div>
                        </div>
                        <div className="border border-border/80 rounded-lg overflow-hidden shadow-md bg-card/60 backdrop-blur-sm overflow-x-auto">
                          <table className="w-full text-left text-sm border-collapse min-w-[600px]">
                            <thead>
                              <tr className="bg-primary text-primary-foreground uppercase font-mono tracking-wider text-[11px] font-bold border-b border-border">
                                {currentSlide.board_data.headers.map((h: string, idx: number) => (
                                  <th key={idx} className="px-3 py-2.5 font-bold whitespace-nowrap">{h}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {currentSlide.board_data.rows.map((row: string[], rIdx: number) => (
                                <tr key={rIdx} className="border-b border-border/30 last:border-0 hover:bg-primary/5 transition-colors even:bg-muted/10">
                                  {row.map((cell: string, cIdx: number) => {
                                    const sCls = semanticClass(cell);
                                    return (
                                    <td key={cIdx} className="px-3 py-2.5 text-foreground/80 font-sans leading-relaxed text-sm">
                                      {cIdx === 0 ? <strong className={`text-foreground font-serif text-base font-bold block ${sCls}`}><SafeHTML text={cell} /></strong> : <SafeHTML text={cell} />}
                                    </td>
                                  )})}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                        {/* Diagram placeholders extracted from bottom_band */}
                        {extractDiagrams(currentSlide.bottom_band).diagrams.map((d, i) => (
                          <div key={i} className="diagram-placeholder">{d}</div>
                        ))}
                      </div>
                    ) : (
                      /* Non-Table Slide: Balanced 2-Column Layout — fluid height, no h-full to avoid overlap with debug-callout */
                      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
                        {/* Slide Left Column (Thesis & Title) — natural flex flow, no forced stretch */}
                        <div className="md:col-span-4 flex flex-col gap-4 border-r border-border/40 pr-5">
                          <div>
                            <span className="text-[10px] uppercase tracking-widest font-mono text-primary block mb-2">Concept Pillar</span>
                            <h3 className={`font-serif font-bold leading-tight mb-4 text-foreground break-words ${
                              currentSlide.title.length > 18 || !currentSlide.title.includes(" ")
                                ? "text-lg md:text-xl"
                                : "text-2xl"
                            }`}>
                              {currentSlide.title}
                            </h3>
                            <div className="h-0.5 w-16 bg-primary mb-6" />
                          </div>
                          <div className="bg-primary/5 border border-primary/10 rounded p-4">
                            <span className="text-xs uppercase tracking-widest font-mono text-primary block mb-2 font-bold">Thesis Statement</span>
                            <p className="text-sm font-serif text-foreground/85 leading-relaxed font-medium">
                              <SafeHTML text={`"${currentSlide.thesis}"`} />
                            </p>
                          </div>
                        </div>

                        {/* Slide Right Column (Technical Board) — start-aligned with isolated scroll */}
                        <div className="md:col-span-8 flex flex-col justify-start overflow-y-auto min-h-0 max-h-[70vh]">
                          {/* Render Grid Board */}
                          {currentSlide.board_type === "grid" && (
                            <div className="grid grid-cols-1 gap-4">
                              {currentSlide.board_data.map((item: any, idx: number) => {
                                const sCls = semanticClass(item.label);
                                return (
                                <div key={idx} className="border border-border/60 rounded-lg p-3 hover:border-primary/40 hover:shadow-md transition-all bg-card/60 backdrop-blur-sm relative overflow-hidden group">
                                  <div className={`absolute left-0 top-0 bottom-0 w-1 transition-colors ${sCls ? sCls.replace('semantic', 'bg-semantic') : 'bg-primary/40 group-hover:bg-primary'}`} />
                                  <span className={`text-xs uppercase tracking-widest font-mono font-bold block mb-1.5 pl-2 ${sCls || 'text-primary'}`}>
                                    <SafeHTML text={item.label} />
                                  </span>
                                  <p className="text-sm text-foreground/80 leading-relaxed pl-2">
                                    <SafeHTML text={item.value} />
                                  </p>
                                </div>
                              )})}
                            </div>
                          )}

                          {/* Render List Board */}
                          {currentSlide.board_type === "list" && (
                            <div className="space-y-3">
                              {currentSlide.board_data.map((item: string, idx: number) => {
                                const hasColon = item.includes(":");
                                const title = hasColon ? item.split(":")[0] : `Point ${idx + 1}`;
                                const desc = hasColon ? item.split(":")[1] : item;
                                return (
                                  <div key={idx} className="flex gap-3 p-2.5 rounded-lg hover:bg-primary/5 border border-transparent hover:border-primary/10 transition-all bg-card/30">
                                    <div className="h-7 w-7 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-mono font-bold mt-0.5 shadow-sm shrink-0">
                                      {idx + 1}
                                    </div>
                                    <div className="flex-1">
                                      <span className="text-base font-bold text-foreground font-serif block mb-0.5"><SafeHTML text={title} /></span>
                                      <span className="text-sm text-foreground/80 leading-relaxed block"><SafeHTML text={desc} /></span>
                                    </div>
                                  </div>
                                );
                              })}
                            </div>
                          )}

                          {/* Render Math/Equation Board */}
                          {currentSlide.board_type === "math" && (
                            <div className="space-y-4">
                              <div className="bg-primary/5 border border-primary/20 rounded-lg p-4 text-center shadow-inner relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-1.5 text-[9px] font-mono text-primary/60 bg-primary/10 rounded-bl-lg uppercase tracking-widest">Formulation</div>
                                <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">Mathematical Representation</span>
                                <code className="text-base font-mono text-primary font-bold block bg-card py-2.5 px-4 rounded border border-primary/20 inline-block shadow-sm">
                                  {currentSlide.board_data.equation}
                                </code>
                              </div>
                              <div className="space-y-2">
                                <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block font-bold">Derivation & Execution Steps</span>
                                <div className="space-y-1.5">
                                  {currentSlide.board_data.steps.map((step: string, idx: number) => (
                                    <div key={idx} className="text-sm text-foreground/80 pl-4 border-l-2 border-primary/40 py-0.5 hover:border-primary hover:text-foreground transition-all">
                                      {step}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            </div>
                          )}
                          {/* Diagram placeholders extracted from bottom_band */}
                          {extractDiagrams(currentSlide.bottom_band).diagrams.map((d, i) => (
                            <div key={i} className="diagram-placeholder">{d}</div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* PPT Slide Bottom Band — inside scrollable body to prevent clipping */}
                    <div className="debug-callout">
                      <div className="flex items-center gap-2 mb-0.5">
                        <AlertTriangle className="h-3.5 w-3.5 text-amber-500 flex-shrink-0" />
                        <strong>Debugging Habit</strong>
                      </div>
                      <span><SafeHTML text={extractDiagrams(currentSlide.bottom_band).clean} /></span>
                    </div>
                  </div>

                </div>

                {/* PPT Slide Controls */}
                <div className="flex items-center justify-between px-1 py-1.5 shrink-0">
                  <button
                    disabled={activeSlideIndex === 0}
                    onClick={() => setActiveSlideIndex(prev => Math.max(0, prev - 1))}
                    className="flex items-center gap-1.5 px-3 py-1.5 border border-border rounded bg-card hover:bg-accent text-xs font-semibold disabled:opacity-50 disabled:pointer-events-none transition-all"
                  >
                    <ArrowLeft className="h-3.5 w-3.5" />
                    Previous
                  </button>
                  <div className="flex gap-1">
                    {currentDayData.slides.map((_, idx) => (
                      <div
                        key={idx}
                        className={`h-1.5 w-4 rounded-full transition-all ${
                          idx === activeSlideIndex ? "bg-primary" : "bg-border"
                        }`}
                      />
                    ))}
                  </div>
                  <button
                    disabled={activeSlideIndex === currentDayData.slides.length - 1}
                    onClick={() => setActiveSlideIndex(prev => Math.min(currentDayData.slides.length - 1, prev + 1))}
                    className="flex items-center gap-1.5 px-3 py-1.5 border border-border rounded bg-card hover:bg-accent text-xs font-semibold disabled:opacity-50 disabled:pointer-events-none transition-all"
                  >
                    Next
                    <ArrowRight className="h-3.5 w-3.5" />
                  </button>
                </div>

                {/* Robotic Schematic Strip — clickable thumbnail */}
                <button
                  onClick={() => setBlueprintFullscreen(true)}
                  className="border border-border bg-card/40 hover:bg-card/60 rounded-lg px-4 py-3 flex flex-row items-center gap-4 shrink-0 transition-colors text-left cursor-pointer group"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">Hardware Blueprint</span>
                      <span className="text-[10px] font-mono text-muted-foreground">Day {activeDay} Platform</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-0.5 leading-relaxed line-clamp-2">
                      Examine the kinematic structure and coordinate frames. In lab, you will write controllers targeting these joint motors and listen to coordinate transformations (TFs).
                    </p>
                  </div>
                  <div className="w-32 h-20 md:w-40 md:h-24 border border-border rounded overflow-hidden relative bg-card shadow-sm shrink-0 group-hover:ring-2 group-hover:ring-primary/40 transition-all">
                    <img
                      src={getDaySchematic(activeDay)}
                      alt="Robot Schematic"
                      className="w-full h-full object-contain p-1"
                    />
                    <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <Maximize2 className="h-4 w-4 text-primary" />
                    </div>
                  </div>
                </button>

              </div>
            )}

            {/* LAB WORKSPACES TAB */}
            {activeTab === "labs" && currentDayData.labs && currentDayData.labs.length > 0 && (
              <div className="flex-1 flex flex-col lg:flex-row gap-6">
                
                {/* Lab Selection Sidebar */}
                <div className="w-full lg:w-72 flex flex-col gap-3">
                  <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground">Available Labs</span>
                  <div className="space-y-2">
                    {currentDayData.labs.map((lab) => {
                      const isActive = activeLabId === lab.id;
                      return (
                        <button
                          key={lab.id}
                          onClick={() => handleLabChange(lab.id)}
                          className={`w-full text-left p-4 rounded border transition-all flex flex-col gap-1 ${
                            isActive 
                              ? "bg-card border-primary shadow-sm" 
                              : "bg-card/40 border-border hover:bg-accent"
                          }`}
                        >
                          <span className="font-mono text-[10px] text-primary font-bold uppercase">{lab.id}</span>
                          <span className="text-xs font-serif font-bold text-foreground line-clamp-1">{lab.title}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Active Lab Workspace */}
                {activeLab && (
                  <div className="flex-1 flex flex-col gap-6">

                    {/* Lab Guide Section */}
                    <div className="border border-border bg-card rounded-lg p-6">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <span className="font-mono text-[10px] text-primary font-bold uppercase">{activeLab.id} Guide</span>
                          <h3 className="text-xl font-serif font-bold text-foreground mt-1">{activeLab.title}</h3>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="flex items-center gap-1.5 text-xs font-mono text-primary bg-primary/10 px-2.5 py-1 rounded">
                            <Terminal className="h-3.5 w-3.5" />
                            <span>Active Environment</span>
                          </div>
                          <button
                            onClick={handleToggleFullscreen}
                            className="flex items-center gap-1.5 text-[10px] font-mono text-muted-foreground hover:text-foreground bg-muted/30 hover:bg-muted/60 border border-border/40 px-2.5 py-1 rounded transition-colors"
                            aria-label="View guide fullscreen"
                          >
                            <Maximize2 className="h-3.5 w-3.5" />
                            <span>Fullscreen Guide</span>
                          </button>
                        </div>
                      </div>

                      <div className="h-px bg-border/60 my-4" />

                      {/* Render Lab Guide Content — rendered as sanitized HTML */}
                      <div className="lab-content max-h-64 overflow-y-auto pr-2
                        text-xs text-muted-foreground leading-relaxed
                        [&_ul]:list-decimal [&_ul]:pl-5 [&_ul]:space-y-1
                        [&_ol]:list-decimal [&_ol]:pl-5 [&_ol]:space-y-1
                        [&_p]:mb-3
                        [&_.font-serif]:font-serif [&_.font-serif]:italic [&_.font-serif]:text-foreground
                        [&_table]:w-full [&_table]:border-collapse
                        [&_th]:text-left [&_th]:p-2.5 [&_th]:font-semibold [&_th]:text-muted-foreground
                        [&_td]:p-2.5
                        [&_tr]:border-b [&_tr]:border-border/50
                        [&_tbody_tr:nth-child(even)]:bg-muted/20
                        [&_thead_tr]:bg-muted/40
                        [&_.step-header]:mb-6
                        [&_.step-header_h4]:text-base [&_.step-header_h4]:font-bold
                        [&_.step-header_h4]:text-primary [&_.step-header_h4]:tracking-tight
                      ">
                        <SafeHTML text={activeLab.content} />
                      </div>
                    </div>

                    {/* ── TRUE MONITOR-WIDE FULLSCREEN OVERLAY (Portal to body) ── */}
                    {labGuideFullscreen && createPortal(
                      <div id="lab-guide-container" className="fixed inset-0 w-screen h-screen z-[9999] bg-background flex flex-col animate-fade-in overflow-y-auto">
                        {/* Fullscreen header bar */}
                        <div className="flex items-center justify-between px-8 py-4 border-b border-border bg-card shrink-0 shadow-sm sticky top-0 z-10">
                          <div>
                            <span className="font-mono text-[11px] text-primary font-bold uppercase tracking-wider">{activeLab.id} Guide</span>
                            <h2 className="text-2xl font-serif font-bold text-foreground mt-0.5">{activeLab.title}</h2>
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-[11px] text-muted-foreground font-mono">
                              Press <kbd className="px-1.5 py-0.5 rounded border border-border bg-muted text-[10px] font-mono">Esc</kbd> to exit
                            </span>
                            <button
                              onClick={handleToggleFullscreen}
                              className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground hover:text-foreground bg-muted/30 hover:bg-muted/60 border border-border px-3 py-1.5 rounded transition-colors"
                              aria-label="Exit fullscreen"
                            >
                              <Minimize2 className="h-4 w-4" />
                              <span>Exit Fullscreen</span>
                            </button>
                          </div>
                        </div>

                        {/* Fullscreen scrollable content area */}
                        <div className="flex-1 px-8 py-8 max-w-5xl mx-auto w-full">
                          <div className="lab-content
                            text-sm text-muted-foreground leading-relaxed
                            [&_ul]:list-decimal [&_ul]:pl-6 [&_ul]:space-y-2 [&_ul]:my-4
                            [&_ol]:list-decimal [&_ol]:pl-6 [&_ol]:space-y-2 [&_ol]:my-4
                            [&_p]:mb-4 [&_p]:text-sm
                            [&_.font-serif]:font-serif [&_.font-serif]:italic [&_.font-serif]:text-foreground
                            [&_table]:w-full [&_table]:border-collapse [&_table]:my-4
                            [&_th]:text-left [&_th]:p-3 [&_th]:font-semibold [&_th]:text-muted-foreground [&_th]:text-sm
                            [&_td]:p-3 [&_td]:text-sm
                            [&_tr]:border-b [&_tr]:border-border/50
                            [&_tbody_tr:nth-child(even)]:bg-muted/20
                            [&_thead_tr]:bg-muted/40
                            [&_.step-header]:mb-8
                            [&_.step-header_h4]:text-lg [&_.step-header_h4]:font-bold
                            [&_.step-header_h4]:text-primary [&_.step-header_h4]:tracking-tight
                            [&_span.font-bold]:font-bold [&_span.font-bold]:text-foreground
                          ">
                            <SafeHTML text={activeLab.content} />
                          </div>
                        </div>
                      </div>,
                      document.body
                    )}

                    {/* Code Snippet Viewer */}
                    {activeLab.code_files && activeLab.code_files.length > 0 && (
                      <div className="border border-border bg-card rounded-lg overflow-hidden flex flex-col flex-1 min-h-[350px]">

                        {/* Code Header */}
                        <div className="bg-muted/40 border-b border-border px-4 py-3 flex items-center justify-between">
                          <div className="flex gap-2">
                            {activeLab.code_files.map((file) => (
                              <button
                                key={file.name}
                                onClick={() => setActiveLabFile(file.name)}
                                className={`px-3 py-1 rounded text-[11px] font-mono transition-all ${
                                  activeLabFile === file.name
                                    ? "bg-card border border-border text-primary font-semibold"
                                    : "text-muted-foreground hover:text-foreground"
                                }`}
                              >
                                {file.name}
                              </button>
                            ))}
                          </div>
                          <button
                            onClick={() => copyToClipboard(activeCodeFile?.code || "")}
                            className="text-[10px] font-mono text-primary hover:underline"
                          >
                            {copied ? "Copied!" : "Copy Code"}
                          </button>
                        </div>

                        {/* Code Editor Body */}
                        <div className="flex-1 bg-[#0a192f] p-4 font-mono text-xs text-[#a9b7c6] overflow-auto max-h-96">
                          <pre className="leading-relaxed">
                            <code>{activeCodeFile?.code || "# No code file selected."}</code>
                          </pre>
                        </div>
                      </div>
                    )}

                    {/* Interactive Telemetry Widget (Days 02-07) */}
                    {activeDay === "02" && <Day2PatrolSimulator />}
                    {activeDay === "03" && <Day3ControlAuthority />}
                    {activeDay === "04" && <Day4RunFolderAuditor />}
                    {activeDay === "05" && <Day5SafetyGatingCalculator />}
                    {activeDay === "06" && <Day6MotionControlSimulator />}
                    {activeDay === "07" && <Day7AudioCapstoneTool />}
                    {activeDay === "01" && (
                          <div className="border border-border bg-card rounded-lg p-6 flex flex-col items-center justify-center gap-3 min-h-[200px]">
                            <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center">
                              <Activity className="h-6 w-6 text-primary" />
                            </div>
                            <span className="text-xs font-mono text-muted-foreground">
                              Day 01 telemetry simulators are embedded within the lecture slides above.
                            </span>
                          </div>
                        )}

                  </div>
                )}

              </div>
            )}

          </div>

          {/* Footer Copyright Placement (Bottom-Left Rule) */}
          <footer className="border-t border-border bg-card/40 px-5 py-2.5 flex items-center justify-between text-[10px] text-muted-foreground font-mono">
            <span>© 2026 Vinci AI. All rights reserved.</span>
            <div className="flex items-center gap-2">
              <img
                src="https://files.manuscdn.com/user_upload_by_module/session_file/310519663722418623/TWbZYCYEmoxfCJuQ.png"
                alt="Vinci AI Logo"
                className="h-4 opacity-50"
              />
              <span className="text-primary font-bold">Academic Technology Training Program</span>
            </div>
          </footer>

          {/* HARDWARE BLUEPRINT FULLSCREEN OVERLAY — contained within main panel */}
          {blueprintFullscreen && (
            <>
              {/* Backdrop — covers main panel slides area only */}
              <div
                className="absolute inset-0 bg-background/80 backdrop-blur-sm z-40"
                onClick={() => setBlueprintFullscreen(false)}
              />
              {/* Blueprint card — centered in main panel */}
              <div className="absolute inset-4 z-50 flex items-center justify-center">
                <div className="w-full max-w-3xl max-h-full bg-card border border-border rounded-xl shadow-2xl flex flex-col overflow-hidden animate-fade-in">
                  {/* Header bar */}
                  <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-muted/30 shrink-0">
                    <div className="flex items-center gap-3">
                      <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
                        <Cpu className="h-4 w-4 text-primary" />
                      </div>
                      <div>
                        <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">Hardware Blueprint</span>
                        <h3 className="text-sm font-serif font-bold text-foreground">Day {activeDay} Kinematic Layout</h3>
                      </div>
                    </div>
                    <button
                      onClick={() => setBlueprintFullscreen(false)}
                      className="h-8 w-8 rounded-lg border border-border bg-card hover:bg-accent flex items-center justify-center transition-colors group"
                      aria-label="Close blueprint viewer"
                    >
                      <Minimize2 className="h-4 w-4 text-muted-foreground group-hover:text-foreground" />
                    </button>
                  </div>
                  {/* Image area */}
                  <div className="flex-1 p-6 flex items-center justify-center bg-muted/10 min-h-0">
                    <img
                      src={getDaySchematic(activeDay)}
                      alt={`Day ${activeDay} Robot Kinematic Blueprint`}
                      className="max-w-full max-h-full object-contain rounded-lg"
                    />
                  </div>
                  {/* Footer caption */}
                  <div className="px-6 py-3 border-t border-border bg-card/60 shrink-0">
                    <div className="flex items-center justify-between text-[11px] text-muted-foreground font-mono">
                      <span>{activeDay === "01" || activeDay === "02" ? "Unitree Go2 — Quadruped Platform" : activeDay === "03" || activeDay === "04" ? "Unitree B2 — Quadruped Platform" : "Unitree G1 — Humanoid Platform"}</span>
                      <span className="text-primary/80 font-semibold">Kinematic & TF Coordinate Reference</span>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

        </main>

      </div>

      {/* FULLSCREEN PRESENTATION MODE — Zero-Scroll Canvas Shell */}
      {isFullscreen && currentSlide && (
        <div className="fixed inset-0 w-screen h-screen bg-sidebar text-sidebar-foreground z-[9999] p-6 md:p-8 flex flex-col justify-between overflow-hidden select-none animate-fade-in">

          {/* Subtle Background Watermark for Cinematic Lecture Feel */}
          <div className="vinci-watermark opacity-10" />

          {/* Fullscreen Header */}
          <div className="flex items-center justify-between border-b border-white/10 pb-4 shrink-0 z-10">
            <div className="flex items-center gap-4">
              <img
                src="https://files.manuscdn.com/user_upload_by_module/session_file/310519663722418623/TWbZYCYEmoxfCJuQ.png"
                alt="Vinci AI Logo"
                className="h-8 object-contain"
              />
              <div className="h-6 w-px bg-white/20" />
              <span className="font-mono text-xs uppercase tracking-widest text-blue-400">
                Day {activeDay} Lecture — {currentDayData.title}
              </span>
            </div>
            <button
              onClick={() => setIsFullscreen(false)}
              className="flex items-center gap-2 px-3 py-1.5 border border-white/10 hover:bg-white/10 rounded text-xs font-semibold font-mono transition-all text-white/70 hover:text-white"
            >
              <Minimize2 className="h-4 w-4" />
              Exit [ESC]
            </button>
          </div>

          {/* Main Active Inner Layout Block — Fluid Row/Column Engine */}
          <div className="flex-1 w-full grid grid-cols-1 lg:grid-cols-12 gap-6 my-4 min-h-0 items-stretch overflow-hidden z-10">

            {currentSlide.board_type === "table" ? (
              /* TABLE SLIDE: Full-width spanning all 12 columns with internal scroll */
              <div className="col-span-full flex flex-col min-h-0 overflow-hidden">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-4 shrink-0">
                  <div className="space-y-1">
                    <span className="font-mono text-sm uppercase tracking-widest text-blue-400 font-bold">
                      Pillar {activeSlideIndex + 1} of {currentDayData.slides.length}
                    </span>
                    <h2 className="text-3xl lg:text-4xl font-serif font-bold leading-tight tracking-tight text-white">
                      {currentSlide.title}
                    </h2>
                  </div>
                  <div className="bg-white/5 border border-white/10 rounded-xl p-5 max-w-xl md:text-right">
                    <span className="font-mono text-sm uppercase tracking-widest text-blue-400 block mb-1 font-bold">Thesis Statement</span>
                    <p className="text-base lg:text-lg font-serif text-white/90 leading-relaxed font-medium">
                      <SafeHTML text={`"${currentSlide.thesis}"`} />
                    </p>
                  </div>
                </div>
                <div className="flex-1 border border-white/10 rounded-xl overflow-x-auto bg-[#0d1533] shadow-2xl mt-4 min-h-0">
                  <table className="w-full text-left text-base border-collapse min-w-[750px]">
                    <thead>
                      <tr className="bg-blue-600 text-white uppercase font-mono tracking-wider text-sm font-bold border-b border-white/10 sticky top-0">
                        {currentSlide.board_data.headers.map((h: string, idx: number) => (
                          <th key={idx} className="p-5 font-bold whitespace-nowrap">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {currentSlide.board_data.rows.map((row: string[], rIdx: number) => (
                        <tr key={rIdx} className="border-b border-white/5 last:border-0 hover:bg-white/5 transition-colors even:bg-white/[0.01]">
                          {row.map((cell: string, cIdx: number) => {
                            const sCls = semanticClass(cell);
                            return (
                            <td key={cIdx} className="p-5 text-white/85 font-sans leading-relaxed">
                              {cIdx === 0 ? <strong className={`text-white font-serif text-xl font-bold block ${sCls}`}><SafeHTML text={cell} /></strong> : <SafeHTML text={cell} />}
                            </td>
                          )})}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {/* Diagram placeholders extracted from bottom_band */}
                {extractDiagrams(currentSlide.bottom_band).diagrams.map((d, i) => (
                  <div key={i} className="diagram-placeholder border-white/10 text-white/50">{d}</div>
                ))}
              </div>
            ) : (
              /* NON-TABLE SLIDE: Balanced 2-Column Split */
              <>
                {/* Left Info Stack Panel — Title + Thesis + Debugging Habit Alert — scrollable with isolated overflow */}
                <div className="lg:col-span-5 flex flex-col gap-4 h-full min-h-0 overflow-y-auto custom-scrollbar">
                  <div className="flex flex-col gap-4">
                    <span className="font-mono text-sm uppercase tracking-widest text-blue-400 font-bold">
                      Pillar {activeSlideIndex + 1} of {currentDayData.slides.length}
                    </span>
                    <h2 className={`font-serif font-bold leading-tight tracking-tight text-white break-words ${
                      currentSlide.title.length > 18 || !currentSlide.title.includes(" ")
                        ? "text-3xl lg:text-4xl"
                        : "text-4xl lg:text-5xl"
                    }`}>
                      {currentSlide.title}
                    </h2>
                    <div className="h-1 w-24 bg-blue-500" />
                  </div>
                  <div className="bg-white/5 border border-white/10 rounded-lg p-5">
                    <span className="font-mono text-sm uppercase tracking-widest text-blue-400 block mb-2 font-bold">Thesis Statement</span>
                    <p className="text-base lg:text-lg font-serif text-white/90 leading-relaxed font-medium">
                      <SafeHTML text={`"${currentSlide.thesis}"`} />
                    </p>
                  </div>
                  {/* Debugging Habit Alert Card — scroll-protected with max-height clamp */}
                  <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded text-xs leading-relaxed overflow-y-auto max-h-[25vh] custom-scrollbar">
                    <div className="flex items-center gap-2 mb-1.5">
                      <AlertTriangle className="h-4 w-4 text-amber-400 flex-shrink-0" />
                      <span className="font-mono text-[10px] uppercase tracking-widest text-amber-400 font-bold">Debugging Habit</span>
                    </div>
                    <p className="font-mono text-amber-300">
                      <SafeHTML text={extractDiagrams(currentSlide.bottom_band).clean} />
                    </p>
                  </div>
                </div>

                {/* Right Content Stream Panel — Dynamic Data Board Renderer */}
                <div className="lg:col-span-7 bg-background/30 border border-border/60 rounded-lg p-6 flex flex-col min-h-0 overflow-hidden">
                  <div className="flex-1 w-full overflow-y-auto pr-2 custom-scrollbar min-h-0 space-y-3 layout-render-target">
                    {/* Render Grid Board */}
                    {currentSlide.board_type === "grid" && (
                      <div className="grid grid-cols-1 gap-4">
                        {currentSlide.board_data.map((item: any, idx: number) => {
                          const sCls = semanticClass(item.label);
                          return (
                          <div key={idx} className="border border-white/10 rounded-xl p-5 bg-white/[0.02] hover:border-blue-500/50 hover:bg-white/[0.04] transition-all relative overflow-hidden group shadow-md">
                            <div className={`absolute left-0 top-0 bottom-0 w-1 transition-colors ${sCls ? sCls.replace('semantic', 'bg-semantic') : 'bg-blue-500/30 group-hover:bg-blue-500'}`} />
                            <span className={`text-sm uppercase tracking-widest font-mono font-bold block mb-2 pl-2 ${sCls || 'text-blue-400'}`}>
                              <SafeHTML text={item.label} />
                            </span>
                            <p className="text-base lg:text-lg text-white/85 leading-relaxed pl-2">
                              <SafeHTML text={item.value} />
                            </p>
                          </div>
                        )})}
                      </div>
                    )}

                    {/* Render List Board */}
                    {currentSlide.board_type === "list" && (
                      <div className="space-y-3">
                        {currentSlide.board_data.map((item: string, idx: number) => {
                          const hasColon = item.includes(":");
                          const title = hasColon ? item.split(":")[0] : `Point ${idx + 1}`;
                          const desc = hasColon ? item.split(":")[1] : item;
                          return (
                            <div key={idx} className="flex gap-4 p-5 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] border border-transparent hover:border-white/10 transition-all shadow-md">
                              <div className="h-9 w-9 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-base font-mono font-bold mt-0.5 shadow-sm shrink-0">
                                {idx + 1}
                              </div>
                              <div className="flex-1">
                                <span className="text-lg font-bold text-white font-serif block mb-1"><SafeHTML text={title} /></span>
                                <span className="text-base lg:text-lg text-white/85 leading-relaxed block"><SafeHTML text={desc} /></span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {/* Render Math/Equation Board */}
                    {currentSlide.board_type === "math" && (
                      <div className="space-y-6">
                        <div className="bg-blue-950/30 border border-blue-500/30 rounded-xl p-6 text-center shadow-inner relative overflow-hidden">
                          <div className="absolute top-0 right-0 p-2 text-xs font-mono text-blue-300 bg-blue-500/20 rounded-bl-xl uppercase tracking-widest font-bold">Formulation</div>
                          <span className="text-sm uppercase tracking-widest font-mono text-blue-300 block mb-3 font-bold">Mathematical Representation</span>
                          <code className="text-xl lg:text-2xl font-mono text-blue-400 font-bold block bg-[#0c1533] py-4 px-6 rounded-lg border border-blue-500/30 inline-block shadow-lg">
                            {currentSlide.board_data.equation}
                          </code>
                        </div>
                        <div className="space-y-3">
                          <span className="text-sm uppercase tracking-widest font-mono text-blue-300 block font-bold">Derivation & Execution Steps</span>
                          <div className="space-y-2">
                            {currentSlide.board_data.steps.map((step: string, idx: number) => (
                              <div key={idx} className="text-base lg:text-lg text-white/80 pl-4 border-l-2 border-blue-500/50 py-0.5 hover:border-blue-500 hover:text-white transition-all">
                                {step}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                    {/* Diagram placeholders for non-table fullscreen slides */}
                    {extractDiagrams(currentSlide.bottom_band).diagrams.map((d, i) => (
                      <div key={i} className="diagram-placeholder border-white/10 text-white/50">{d}</div>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Fullscreen Footer — Navigation Controls Only */}
          <div className="border-t border-white/10 pt-4 flex items-center justify-between shrink-0 z-10">
            {/* Slide Counter */}
            <span className="font-mono text-sm text-white/70 font-bold">
              Slide {activeSlideIndex + 1} of {currentDayData.slides.length}
            </span>

            {/* Navigation Controls */}
            <div className="flex items-center gap-4">
              <button
                disabled={activeSlideIndex === 0}
                onClick={() => setActiveSlideIndex(prev => Math.max(0, prev - 1))}
                className="flex items-center gap-2 px-4 py-2 border border-white/10 hover:bg-white/10 rounded-lg text-sm font-semibold disabled:opacity-30 disabled:pointer-events-none transition-all"
              >
                <ArrowLeft className="h-4 w-4" />
                Previous
              </button>
              <button
                disabled={activeSlideIndex === currentDayData.slides.length - 1}
                onClick={() => setActiveSlideIndex(prev => Math.min(currentDayData.slides.length - 1, prev + 1))}
                className="flex items-center gap-2 px-4 py-2 border border-blue-500 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-semibold disabled:opacity-30 disabled:pointer-events-none transition-all"
              >
                Next
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
