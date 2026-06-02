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
  Maximize2
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
                          {currentDayData.slides[activeSlideIndex].title}
                        </h3>
                        <div className="h-0.5 w-16 bg-primary mb-6" />
                      </div>
                      <div className="bg-primary/5 border border-primary/10 rounded p-4">
                        <span className="text-[10px] uppercase tracking-widest font-mono text-primary block mb-2 font-bold">Thesis Statement</span>
                        <p className="text-xs font-serif text-muted-foreground leading-relaxed italic">
                          "{currentDayData.slides[activeSlideIndex].thesis}"
                        </p>
                      </div>
                    </div>

                    {/* Slide Right Column (Technical Board) */}
                    <div className="md:col-span-7 flex flex-col justify-center">
                      
                      {/* Render Table Board */}
                      {currentDayData.slides[activeSlideIndex].board_type === "table" && (
                        <div className="border border-border/80 rounded overflow-hidden shadow-sm">
                          <table className="w-full text-left text-xs border-collapse">
                            <thead>
                              <tr className="bg-primary/10 text-primary uppercase font-mono tracking-wider text-[10px] border-b border-border">
                                {currentDayData.slides[activeSlideIndex].board_data.headers.map((h: string, idx: number) => (
                                  <th key={idx} className="p-3 font-semibold">{h}</th>
                                ))}
                              </tr>
                            </thead>
                            <tbody>
                              {currentDayData.slides[activeSlideIndex].board_data.rows.map((row: string[], rIdx: number) => (
                                <tr key={rIdx} className="border-b border-border/40 last:border-0 hover:bg-muted/30">
                                  {row.map((cell: string, cIdx: number) => (
                                    <td key={cIdx} className="p-3 text-muted-foreground">
                                      {cIdx === 0 ? <strong className="text-foreground font-serif">{cell}</strong> : cell}
                                    </td>
                                  ))}
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}

                      {/* Render Grid Board */}
                      {currentDayData.slides[activeSlideIndex].board_type === "grid" && (
                        <div className="grid grid-cols-1 gap-4">
                          {currentDayData.slides[activeSlideIndex].board_data.map((item: any, idx: number) => (
                            <div key={idx} className="border border-border/60 rounded p-4 hover:border-primary/40 transition-all bg-card/50">
                              <span className="text-[10px] uppercase tracking-widest font-mono text-primary font-bold block mb-1">
                                {item.label}
                              </span>
                              <p className="text-xs text-muted-foreground leading-relaxed">
                                {item.value}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Render List Board */}
                      {currentDayData.slides[activeSlideIndex].board_type === "list" && (
                        <div className="space-y-4">
                          {currentDayData.slides[activeSlideIndex].board_data.map((item: string, idx: number) => {
                            const [title, desc] = item.split(":");
                            return (
                              <div key={idx} className="flex gap-3">
                                <div className="h-5 w-5 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-mono font-bold mt-0.5">
                                  {idx + 1}
                                </div>
                                <div className="flex-1">
                                  <span className="text-xs font-bold text-foreground font-serif block">{title}</span>
                                  <span className="text-xs text-muted-foreground leading-relaxed">{desc}</span>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}

                      {/* Render Math/Equation Board */}
                      {currentDayData.slides[activeSlideIndex].board_type === "math" && (
                        <div className="space-y-6">
                          <div className="bg-muted/40 border border-border rounded p-6 text-center shadow-inner">
                            <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block mb-2">Mathematical Formulation</span>
                            <code className="text-sm font-mono text-primary font-bold block bg-card py-2 px-4 rounded border border-border inline-block">
                              {currentDayData.slides[activeSlideIndex].board_data.equation}
                            </code>
                          </div>
                          <div className="space-y-2">
                            <span className="text-[10px] uppercase tracking-widest font-mono text-muted-foreground block">Execution Steps</span>
                            {currentDayData.slides[activeSlideIndex].board_data.steps.map((step: string, idx: number) => (
                              <div key={idx} className="text-xs text-muted-foreground pl-4 border-l border-primary/40">
                                {step}
                              </div>
                            ))}
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
                      <strong className="text-foreground">Debugging Habit:</strong> {currentDayData.slides[activeSlideIndex].bottom_band}
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
                        className={`h-1.5 w-6 rounded-full transition-all ${
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

            {/* Fallback if no content */}
            {(!currentDayData.slides || currentDayData.slides.length === 0) && activeTab === "lecture" && (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-12 border border-dashed border-border rounded-lg bg-card/20">
                <AlertTriangle className="h-8 w-8 text-amber-500 mb-3" />
                <h3 className="text-lg font-serif font-bold text-foreground">Slide Material Unreleased</h3>
                <p className="text-xs text-muted-foreground mt-1 max-w-sm">
                  This session is structured as a hands-on lab session. Switch to the "Lab Workspaces" tab to explore detailed lab tasks and source code.
                </p>
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
    </div>
  );
}
