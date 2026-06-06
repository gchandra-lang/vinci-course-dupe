/**
 * ── Vinci Curriculum Data Model ──
 * Strict TypeScript interfaces for syllabus JSON payloads.
 * Designed to survive partial / evolving data shapes without runtime crashes.
 */

// ──────────────────────────────────────────
// Base primitives
// ──────────────────────────────────────────

export interface LabFile {
  name: string;
  code: string;
}

export interface Lab {
  id: string;
  title: string;
  content: string;            // Markdown / HTML lab guide body
  code_files: LabFile[];
}

export interface PacingEntry {
  time: string;
  session: string;
  path: string;
}

// ──────────────────────────────────────────
// Slide board variants
// ──────────────────────────────────────────
//
// board_data shape is determined by board_type at runtime.
// The renderers dispatch on board_type before accessing board_data fields,
// so we keep board_data loosely typed. Documented shapes below:

/**
 * board_type === "table": { headers: string[]; rows: string[][] }
 * board_type === "grid":  { items: { title: string; body: string }[] }
 * board_type === "list":  { items: string[] }
 * board_type === "math":  { equation: string; steps: string[] }
 */
export type SlideBoardData = Record<string, any>;

export type SlideBoardType = "table" | "grid" | "list" | "math";

export interface Slide {
  title: string;
  thesis: string;
  board_type: SlideBoardType;
  board_data: SlideBoardData;
  bottom_band?: string;        // Optional: speaker notes / diagram cues
}

// ──────────────────────────────────────────
// Day-level curriculum container
// ──────────────────────────────────────────

export interface Deliverable {
  label: string;
  description: string;
  format: string;
  assetHint: string;
}

export interface CurriculumDay {
  /** Two-digit day key, e.g. "05" */
  id: string;
  /** Numeric day for sort / display, e.g. 5 */
  dayNumber: number;
  /** Display title, e.g. "G1 Humanoid Communication & Safety Workflow" */
  title: string;
  /** One-line subtitle (eyebrow header in UI) */
  eyebrow: string;
  /** Full thesis paragraph (Vinci left-column rule) */
  thesis: string;
  /** Technical highlight tags rendered as chips / badges */
  highlights: string[];
  /** Classroom safety rules (1–N bullet items) */
  rules: string[];
  /** Session pacing timeline */
  pacing: PacingEntry[];
  /** Lecture slide deck */
  slides: Slide[];
  /** Hands-on lab workspaces */
  labs: Lab[];
  /** Tangible deliverables for this day */
  deliverables: Deliverable[];
}

// ──────────────────────────────────────────
// Canonical day-key helpers
// ──────────────────────────────────────────

/** All valid day keys in the curriculum. Extend when days are added. */
export const VALID_DAY_KEYS = ["01", "02", "03", "04", "05", "06", "07"] as const;
export type DayKey = (typeof VALID_DAY_KEYS)[number];

/** Syllabus JSON top-level shape: Record<DayKey, CurriculumDay> */
export type Syllabus = Record<DayKey, CurriculumDay>;

// ──────────────────────────────────────────
// Fallback factory — prevents undefined-access crashes
// ──────────────────────────────────────────

export const EMPTY_CURRICULUM_DAY: CurriculumDay = {
  id: "00",
  dayNumber: 0,
  title: "No Curriculum Loaded",
  eyebrow: "",
  thesis: "Curriculum data could not be resolved. Check your data source or network connection.",
  highlights: [],
  rules: [],
  pacing: [],
  slides: [],
  labs: [],
  deliverables: [],
};

/**
 * Safe day resolver. Always returns a CurriculumDay — never undefined.
 * Use this instead of direct dictionary access in render paths.
 */
export function resolveDay(
  syllabus: Partial<Record<string, unknown>>,
  activeDay: string,
): CurriculumDay {
  const raw = syllabus[activeDay] as CurriculumDay | undefined;
  if (!raw || typeof raw !== "object") return EMPTY_CURRICULUM_DAY;

  return {
    id: raw.id ?? activeDay,
    dayNumber: raw.dayNumber ?? (parseInt(activeDay, 10) || 0),
    title: raw.title ?? EMPTY_CURRICULUM_DAY.title,
    eyebrow: raw.eyebrow ?? "",
    thesis: raw.thesis ?? "",
    highlights: Array.isArray(raw.highlights) ? raw.highlights : [],
    rules: Array.isArray(raw.rules) ? raw.rules : [],
    pacing: Array.isArray(raw.pacing) ? raw.pacing : [],
    slides: Array.isArray(raw.slides) ? raw.slides : [],
    labs: Array.isArray(raw.labs) ? raw.labs : [],
    deliverables: Array.isArray(raw.deliverables) ? raw.deliverables : [],
  };
}