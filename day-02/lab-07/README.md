# Lab 7 — Team capstone presentation

| | |
|--|--|
| **Duration** | ~5 min per team + Q&A |
| **Motion** | Per chosen scenario (supervised) |
| **Prerequisite** | [Lab 5](../lab-05/) run folder or approved equivalent |

---

## What you will learn

- How to present **architecture + evidence** (not demo-only).
- How to explain one **failure, tuning change, or abort** from your field day.
- How the rubric maps to Labs 0–6 artifacts.

---

## What you will run

No new camp script — you **present** outputs from earlier labs:

| Artifact | From |
|----------|------|
| `my_team_scenario.json` | Lab 0 |
| `run_*` + validator PASS | Lab 5 (or Lab 6 trial) |
| `field_test.md` | Lab 6 (recommended) |
| Block diagram | Draw: PC → DDS → Sport / Avoid / Video |

---

## Pick one scenario

| # | Scenario | Must show |
|---|----------|-----------|
| 1 | Corridor patrol | ≥ 3 checkpoints; SOC in metadata |
| 2 | Anomaly abort | Stop + `incident.json` on rule |
| 3 | Return-to-base | Final leg toward start |
| 4 | Post-run report | JSONL → table/CSV insight |

---

## Presentation checklist

1. **Scenario** — arena, checkpoints, limits (30 s)  
2. **Pipeline** — sense → log → plan → avoid → capture → report (60 s)  
3. **Demo evidence** — run folder listing or short clip (90 s)  
4. **Lesson learned** — tuning, capture fail, or safety stop (60 s)  

---

## Rubric (pass)

| Criterion | Pass |
|-----------|------|
| Safety | Cleared arena, spotter, speeds within scenario |
| Evidence | Valid run folder or instructor-approved dry-run + sample |
| Technical | Avoid + capture from Labs 2–5 referenced correctly |

---

## Deliverable

- Slides or wiki page linked to your `run_*` path  
- One paragraph for instructor feedback form  

**Course:** [Day 2 overview](../README.md)
