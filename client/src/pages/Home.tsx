import { useState, useEffect } from "react";
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
      } else if (e.key === "Escape" && isFullscreen) {
        setIsFullscreen(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [activeTab, currentDayData, isFullscreen]);

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
    <div className="min-h-screen flex flex-col bg-background text-foreground relative overflow-hidden">
      {/* Subtle Background Watermark (Vinci Style Rule) */}
      <div className="vinci-watermark" />

      {/* Header Bar */}
      <header className="border-b border-border bg-card/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
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
          <div className="p-4 border-b border-border bg-card/80">
            <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">Syllabus Calendar</span>
            <div className="grid grid-cols-4 lg:grid-cols-1 gap-2">
              {Object.keys(syllabusData).map((dayKey) => {
                const dayData = (syllabusData as any)[dayKey];
                const isActive = activeDay === dayKey;
                return (
                  <button
                    key={dayKey}
                    onClick={() => setActiveDay(dayKey)}
                    className={`flex items-center gap-3 p-3 rounded text-left transition-all ${
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

          {/* Current Day Metadata */}
          <div className="p-6 flex-1 flex flex-col gap-6 overflow-y-auto max-h-[calc(100vh-280px)] lg:max-h-[none]">
            <div>
              <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">{currentDayData.eyebrow}</span>
              <h2 className="text-xl font-serif font-bold text-foreground mt-1">{currentDayData.title}</h2>
              <div className="h-1 w-12 bg-primary mt-3" />
            </div>

            {/* Daily Thesis Statement (Vinci Left Column Rule) */}
            <div className="border-l-2 border-primary/40 pl-4 py-1">
              <p className="text-xs italic text-muted-foreground font-serif leading-relaxed">
                "{currentDayData.thesis}"
              </p>
            </div>

            {/* Daily Pacing Timeline */}
            <div>
              <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block mb-3">3-Hour Pacing Outline</span>
              <div className="space-y-3">
                {currentDayData.pacing.map((item, idx) => (
                  <div key={idx} className="flex gap-3 text-xs">
                    <div className="flex flex-col items-center">
                      <div className="h-2 w-2 rounded-full bg-primary/60" />
                      {idx !== currentDayData.pacing.length - 1 && <div className="w-0.5 flex-1 bg-border my-1" />}
                    </div>
                    <div>
                      <span className="font-mono text-primary font-semibold block">{item.time}</span>
                      <span className="text-foreground/80 font-medium block">{item.session}</span>
                      <span className="text-[10px] text-muted-foreground font-mono">{item.path}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Classroom Rules / Safety Guards (Vinci Style Rule) */}
            <div className="bg-primary/5 border border-primary/10 rounded p-4 mt-auto">
              <div className="flex items-center gap-2 text-primary mb-2">
                <Shield className="h-4 w-4" />
                <span className="text-[10px] uppercase tracking-widest font-mono font-bold">Classroom Safety Rules</span>
              </div>
              <ul className="space-y-2 text-[11px] text-muted-foreground leading-relaxed">
                {currentDayData.rules.map((rule, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-primary font-bold">•</span>
                    <span>{rule}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </aside>

        {/* Right Main Panel */}
        <main className="flex-1 flex flex-col bg-card/10">
          
          {/* Lecture vs Lab Switcher */}
          <div className="border-b border-border bg-card/60 px-6 py-3 flex items-center justify-between">
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
          <div className="flex-1 p-6 flex flex-col overflow-y-auto">
            
            {/* LECTURE SLIDES TAB */}
            {activeTab === "lecture" && currentDayData.slides && currentDayData.slides.length > 0 && (
              <div className="flex-1 flex flex-col justify-between max-w-5xl mx-auto w-full gap-8">
                
                {/* Fullscreen Presentation Trigger */}
                <div className="flex justify-end">
                  <button
                    onClick={() => setIsFullscreen(true)}
                    className="flex items-center gap-2 px-4 py-2 border border-primary/20 bg-primary/5 hover:bg-primary/10 text-primary text-xs font-bold rounded transition-all"
                  >
                    <Maximize2 className="h-4 w-4" />
                    Launch Fullscreen Lecture Mode
                  </button>
                </div>

                {/* PPT Slide Wrapper (Styled exactly after Day 1 PPT design) */}
                <div className="border border-border bg-card rounded-lg shadow-xl overflow-hidden relative flex flex-col min-h-[480px]">
                  
                  {/* Subtle Diagonal Watermark inside PPT frame */}
                  <div className="vinci-watermark opacity-30" />
                  
                  {/* PPT Slide Header */}
                  <div className="border-b border-border/60 bg-muted/20 px-8 py-4 flex items-center justify-between z-10">
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
                  <div className="flex-1 p-8 grid grid-cols-1 md:grid-cols-12 gap-8 z-10">
                    
                    {/* Slide Left Column (Thesis & Title) */}
                    <div className="md:col-span-5 flex flex-col justify-between border-r border-border/40 pr-6">
                      <div>
                        <span className="text-[10px] uppercase tracking-widest font-mono text-primary block mb-2">Concept Pillar</span>
                        <h3 className="text-2xl font-serif font-bold text-foreground leading-tight mb-4">
                          {currentSlide.title}
                        </h3>
                        <div className="h-0.5 w-16 bg-primary mb-6" />
                      </div>
                      <div className="bg-primary/5 border border-primary/10 rounded p-4">
                        <span className="text-[10px] uppercase tracking-widest font-mono text-primary block mb-2 font-bold">Thesis Statement</span>
                        <p className="text-xs font-serif text-muted-foreground leading-relaxed italic">
                          "{currentSlide.thesis}"
                        </p>
                      </div>
                    </div>

                    {/* Slide Right Column (Technical Board) */}
                    <div className="md:col-span-7 flex flex-col justify-center">
                      
                      {/* Render Table Board */}
                      {currentSlide.board_type === "table" && (
                        <div className="border border-border/80 rounded-lg overflow-hidden shadow-md bg-card/60 backdrop-blur-sm">
                          <table className="w-full text-left text-xs border-collapse">
                            <thead>
                              <tr className="bg-primary text-primary-foreground uppercase font-mono tracking-wider text-[9px] border-b border-border">
                                {currentSlide.board_data.headers.map((h: string, idx: number) => (
                                  <th key={idx} className="p-3.5 font-bold">{h}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {currentSlide.board_data.rows.map((row: string[], rIdx: number) => (
                                <tr key={rIdx} className="border-b border-border/30 last:border-0 hover:bg-primary/5 transition-colors even:bg-muted/10">
                                  {row.map((cell: string, cIdx: number) => (
                                    <td key={cIdx} className="p-3.5 text-muted-foreground font-sans leading-relaxed">
                                      {cIdx === 0 ? <strong className="text-foreground font-serif text-sm font-bold block">{cell}</strong> : cell}
                                    </td>
                                  ))}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}

                      {/* Render Grid Board */}
                      {currentSlide.board_type === "grid" && (
                        <div className="grid grid-cols-1 gap-4">
                          {currentSlide.board_data.map((item: any, idx: number) => (
                            <div key={idx} className="border border-border/60 rounded-lg p-4 hover:border-primary/40 hover:shadow-md transition-all bg-card/60 backdrop-blur-sm relative overflow-hidden group">
                              <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary/40 group-hover:bg-primary transition-colors" />
                              <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold block mb-1.5 pl-2">
                                {item.label}
                              </span>
                              <p className="text-xs text-muted-foreground leading-relaxed pl-2">
                                {item.value}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Render List Board */}
                      {currentSlide.board_type === "list" && (
                        <div className="space-y-4">
                          {currentSlide.board_data.map((item: string, idx: number) => {
                            const hasColon = item.includes(":");
                            const title = hasColon ? item.split(":")[0] : `Point ${idx + 1}`;
                            const desc = hasColon ? item.split(":")[1] : item;
                            return (
                              <div key={idx} className="flex gap-4 p-3 rounded-lg hover:bg-primary/5 border border-transparent hover:border-primary/10 transition-all bg-card/30">
                                <div className="h-6 w-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-mono font-bold mt-0.5 shadow-sm shrink-0">
                                  {idx + 1}
                                </div>
                                <div className="flex-1">
                                  <span className="text-sm font-bold text-foreground font-serif block mb-0.5">{title}</span>
                                  <span className="text-xs text-muted-foreground leading-relaxed block">{desc}</span>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {/* Render Math/Equation Board */}
                      {currentSlide.board_type === "math" && (
                        <div className="space-y-6">
                          <div className="bg-primary/5 border border-primary/20 rounded-lg p-6 text-center shadow-inner relative overflow-hidden">
                            <div className="absolute top-0 right-0 p-1.5 text-[9px] font-mono text-primary/60 bg-primary/10 rounded-bl-lg uppercase tracking-widest">Formulation</div>
                            <span className="text-[9px] uppercase tracking-widest font-mono text-muted-foreground block mb-2.5">Mathematical Representation</span>
                            <code className="text-sm font-mono text-primary font-bold block bg-card py-2.5 px-5 rounded border border-primary/20 inline-block shadow-sm">
                              {currentSlide.board_data.equation}
                            </code>
                          </div>
                          <div className="space-y-3">
                            <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block font-bold">Derivation & Execution Steps</span>
                            <div className="space-y-2">
                              {currentSlide.board_data.steps.map((step: string, idx: number) => (
                                <div key={idx} className="text-xs text-muted-foreground pl-4 border-l-2 border-primary/40 py-0.5 hover:border-primary hover:text-foreground transition-all">
                                  {step}
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}

                    </div>
                  </div>

                  {/* PPT Slide Bottom Band */}
                  <div className="border-t border-border bg-muted/30 px-8 py-4 flex items-center gap-3 z-10">
                    <div className="p-1 rounded bg-amber-500/10 text-amber-500">
                      <AlertTriangle className="h-4 w-4" />
                    </div>
                    <p className="text-[11px] font-mono text-muted-foreground leading-relaxed">
                      <strong className="text-foreground">Debugging Habit:</strong> {currentSlide.bottom_band}
                    </p>
                  </div>

                </div>

                {/* PPT Slide Controls */}
                <div className="flex items-center justify-between px-2">
                  <button
                    disabled={activeSlideIndex === 0}
                    onClick={() => setActiveSlideIndex(prev => Math.max(0, prev - 1))}
                    className="flex items-center gap-2 px-4 py-2 border border-border rounded bg-card hover:bg-accent text-xs font-semibold disabled:opacity-50 disabled:pointer-events-none transition-all"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    Previous Slide
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
                    className="flex items-center gap-2 px-4 py-2 border border-border rounded bg-card hover:bg-accent text-xs font-semibold disabled:opacity-50 disabled:pointer-events-none transition-all"
                  >
                    Next Slide
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </div>

                {/* Robotic Schematic Overlay */}
                <div className="border border-border bg-card/40 rounded-lg p-6 flex flex-col md:flex-row items-center gap-6">
                  <div className="flex-1">
                    <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold">Interactive Hardware Blueprint</span>
                    <h4 className="text-lg font-serif font-bold text-foreground mt-1">Day {activeDay} Platform Layout</h4>
                    <p className="text-xs text-muted-foreground mt-2 leading-relaxed">
                      Examine the kinematic structure and coordinate frames of the active platform. In your hands-on lab, you will write controllers targeting these joint motors and listen to these coordinate transformations (TFs).
                    </p>
                  </div>
                  <div className="w-full md:w-80 h-48 border border-border rounded overflow-hidden relative bg-card shadow-sm">
                    <img 
                      src={getDaySchematic(activeDay)} 
                      alt="Robot Schematic" 
                      className="w-full h-full object-contain p-2"
                    />
                  </div>
                </div>

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
                        <div className="flex items-center gap-1.5 text-xs font-mono text-primary bg-primary/10 px-2.5 py-1 rounded">
                          <Terminal className="h-3.5 w-3.5" />
                          <span>Active Environment</span>
                        </div>
                      </div>

                      <div className="h-px bg-border/60 my-4" />

                      {/* Render Lab Guide Content */}
                      <div className="text-xs text-muted-foreground leading-relaxed space-y-4 max-h-64 overflow-y-auto pr-2">
                        <div className="font-serif italic text-foreground mb-2">Lab Objective:</div>
                        <p>{activeLab.content.split("\n\n")[0] || "No objective defined."}</p>
                        <div className="font-serif italic text-foreground mt-4 mb-2">Instructions:</div>
                        <ul className="list-disc pl-5 space-y-2">
                          {activeLab.content.split("\n")
                            .filter(line => line.trim().startsWith("-") || line.trim().startsWith("*") || /^\d+\./.test(line.trim()))
                            .slice(0, 6)
                            .map((line, idx) => (
                              <li key={idx}>{line.replace(/^[-*\d.]\s*/, "")}</li>
                            ))
                          }
                        </ul>
                      </div>
                    </div>

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

                  </div>
                )}

              </div>
            )}

          </div>

          {/* Footer Copyright Placement (Bottom-Left Rule) */}
          <footer className="border-t border-border bg-card/40 px-6 py-4 flex items-center justify-between text-[10px] text-muted-foreground font-mono">
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

        </main>

      </div>

      {/* FULLSCREEN PRESENTATION MODE MODAL */}
      {isFullscreen && currentSlide && (
        <div className="fixed inset-0 bg-[#0a1128] text-white z-[9999] flex flex-col justify-between p-12 select-none animate-fade-in">
          
          {/* Subtle Background Watermark for Cinematic Lecture Feel */}
          <div className="vinci-watermark opacity-10" />

          {/* Fullscreen Header */}
          <div className="flex items-center justify-between border-b border-white/10 pb-6">
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

          {/* Fullscreen Body (Cinematic Lecture Layout) */}
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center my-12 max-w-7xl mx-auto w-full">
            
            {/* Left Column (Big Bold Titles) */}
            <div className="lg:col-span-5 flex flex-col gap-6">
              <span className="font-mono text-xs uppercase tracking-widest text-blue-400 font-bold">
                Pillar {activeSlideIndex + 1} of {currentDayData.slides.length}
              </span>
              <h2 className="text-4xl lg:text-5xl font-serif font-bold leading-tight tracking-tight text-white">
                {currentSlide.title}
              </h2>
              <div className="h-1 w-24 bg-blue-500" />
              <div className="bg-white/5 border border-white/10 rounded-lg p-6 mt-4">
                <span className="font-mono text-[10px] uppercase tracking-widest text-blue-400 block mb-2 font-bold">Thesis Statement</span>
                <p className="text-sm lg:text-base font-serif text-white/80 leading-relaxed italic">
                  "{currentSlide.thesis}"
                </p>
              </div>
            </div>

            {/* Right Column (Huge Board Data for High-Impact Reading) */}
            <div className="lg:col-span-7 bg-white/[0.02] border border-white/10 rounded-xl p-8 shadow-2xl">
              
              {/* Render Table Board */}
              {currentSlide.board_type === "table" && (
                <div className="border border-white/10 rounded-xl overflow-hidden bg-[#0d1533] shadow-2xl">
                  <table className="w-full text-left text-sm border-collapse">
                    <thead>
                      <tr className="bg-blue-600 text-white uppercase font-mono tracking-wider text-xs border-b border-white/10">
                        {currentSlide.board_data.headers.map((h: string, idx: number) => (
                          <th key={idx} className="p-4 font-bold">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {currentSlide.board_data.rows.map((row: string[], rIdx: number) => (
                        <tr key={rIdx} className="border-b border-white/5 last:border-0 hover:bg-white/5 transition-colors even:bg-white/[0.01]">
                          {row.map((cell: string, cIdx: number) => (
                            <td key={cIdx} className="p-4 text-white/70 font-sans leading-relaxed">
                              {cIdx === 0 ? <strong className="text-white font-serif text-lg font-bold block">{cell}</strong> : cell}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Render Grid Board */}
              {currentSlide.board_type === "grid" && (
                <div className="grid grid-cols-1 gap-6">
                  {currentSlide.board_data.map((item: any, idx: number) => (
                    <div key={idx} className="border border-white/10 rounded-xl p-6 bg-white/[0.02] hover:border-blue-500/50 hover:bg-white/[0.04] transition-all relative overflow-hidden group shadow-md">
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500/30 group-hover:bg-blue-500 transition-colors" />
                      <span className="text-xs uppercase tracking-widest font-mono text-blue-400 font-bold block mb-2 pl-2">
                        {item.label}
                      </span>
                      <p className="text-sm lg:text-base text-white/80 leading-relaxed pl-2">
                        {item.value}
                      </p>
                    </div>
                  ))}
                </div>
              )}

              {/* Render List Board */}
              {currentSlide.board_type === "list" && (
                <div className="space-y-4">
                  {currentSlide.board_data.map((item: string, idx: number) => {
                    const hasColon = item.includes(":");
                    const title = hasColon ? item.split(":")[0] : `Point ${idx + 1}`;
                    const desc = hasColon ? item.split(":")[1] : item;
                    return (
                      <div key={idx} className="flex gap-4 p-4 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] border border-transparent hover:border-white/10 transition-all shadow-md">
                        <div className="h-8 w-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-sm font-mono font-bold mt-0.5 shadow-sm shrink-0">
                          {idx + 1}
                        </div>
                        <div className="flex-1">
                          <span className="text-lg font-bold text-white font-serif block mb-1">{title}</span>
                          <span className="text-sm lg:text-base text-white/70 leading-relaxed block">{desc}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Render Math/Equation Board */}
              {currentSlide.board_type === "math" && (
                <div className="space-y-8">
                  <div className="bg-blue-950/30 border border-blue-500/30 rounded-xl p-8 text-center shadow-inner relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-2 text-[10px] font-mono text-blue-300 bg-blue-500/20 rounded-bl-xl uppercase tracking-widest">Formulation</div>
                    <span className="text-xs uppercase tracking-widest font-mono text-blue-300 block mb-3">Mathematical Representation</span>
                    <code className="text-lg lg:text-xl font-mono text-blue-400 font-bold block bg-[#0c1533] py-3.5 px-6 rounded-lg border border-blue-500/30 inline-block shadow-lg">
                      {currentSlide.board_data.equation}
                    </code>
                  </div>
                  <div className="space-y-4">
                    <span className="text-xs uppercase tracking-widest font-mono text-blue-300 block font-bold">Derivation & Execution Steps</span>
                    <div className="space-y-2">
                      {currentSlide.board_data.steps.map((step: string, idx: number) => (
                        <div key={idx} className="text-sm lg:text-base text-white/70 pl-4 border-l-2 border-blue-500/50 py-0.5 hover:border-blue-500 hover:text-white transition-all">
                          {step}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

            </div>

          </div>

          {/* Fullscreen Footer */}
          <div className="border-t border-white/10 pt-6 flex items-center justify-between">
            
            {/* Debugging Band */}
            <div className="flex items-center gap-3 bg-amber-500/10 border border-amber-500/20 px-4 py-2.5 rounded-lg max-w-2xl">
              <AlertTriangle className="h-5 w-5 text-amber-400 flex-shrink-0" />
              <p className="text-xs lg:text-sm font-mono text-amber-300 leading-relaxed">
                <strong>Debugging Habit:</strong> {currentSlide.bottom_band}
              </p>
            </div>

            {/* Navigation Controls */}
            <div className="flex items-center gap-6">
              <button
                disabled={activeSlideIndex === 0}
                onClick={() => setActiveSlideIndex(prev => Math.max(0, prev - 1))}
                className="flex items-center gap-2 px-4 py-2 border border-white/10 hover:bg-white/10 rounded-lg text-sm font-semibold disabled:opacity-30 disabled:pointer-events-none transition-all"
              >
                <ArrowLeft className="h-4 w-4" />
                Previous
              </button>
              <span className="font-mono text-xs text-white/60">
                {activeSlideIndex + 1} / {currentDayData.slides.length}
              </span>
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
