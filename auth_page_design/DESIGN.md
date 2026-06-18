---
name: Vinci Lab Industrial-Editorial
colors:
  surface: '#f9f9ff'
  surface-dim: '#d6dae7'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f0f3ff'
  surface-container: '#e9eefb'
  surface-container-high: '#e4e8f6'
  surface-container-highest: '#dee2f0'
  on-surface: '#171c25'
  on-surface-variant: '#3f484c'
  inverse-surface: '#2b303b'
  inverse-on-surface: '#ecf0fe'
  outline: '#6f787d'
  outline-variant: '#bfc8cc'
  surface-tint: '#05677e'
  primary: '#05677e'
  on-primary: '#ffffff'
  primary-container: '#509bb4'
  on-primary-container: '#002f3b'
  inverse-primary: '#87d1eb'
  secondary: '#5c5f61'
  on-secondary: '#ffffff'
  secondary-container: '#e0e3e6'
  on-secondary-container: '#626567'
  tertiary: '#595f63'
  on-tertiary: '#ffffff'
  tertiary-container: '#8c9296'
  on-tertiary-container: '#252b2e'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b6ebff'
  primary-fixed-dim: '#87d1eb'
  on-primary-fixed: '#001f28'
  on-primary-fixed-variant: '#004e60'
  secondary-fixed: '#e0e3e6'
  secondary-fixed-dim: '#c4c7ca'
  on-secondary-fixed: '#191c1e'
  on-secondary-fixed-variant: '#44474a'
  tertiary-fixed: '#dde3e7'
  tertiary-fixed-dim: '#c1c7cb'
  on-tertiary-fixed: '#161c1f'
  on-tertiary-fixed-variant: '#41484b'
  background: '#f9f9ff'
  on-background: '#171c25'
  surface-variant: '#dee2f0'
  pale-blue-gray: '#F4F6F7'
  dark-navy: '#212630'
  teal-accent: '#509BB4'
  status-amber: '#B58C3D'
  status-purple: '#8A69AD'
  status-green: '#589C7E'
  status-red: '#AD4E4E'
typography:
  display-lg:
    fontFamily: Cinzel
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Cinzel
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Cinzel
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Cinzel
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  tech-label:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.05em
  micro-label:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  gutter: 12px
  margin: 24px
  container-max: 1440px
---

## Brand & Style

The design system embodies the "Industrial-Editorial" aesthetic—a hybrid approach that merges the authoritative, high-contrast layout of a premium print journal with the rigorous, high-fidelity precision of a technical workspace. It is designed for engineers, researchers, and architects who value information density and technical clarity without sacrificing sophisticated presentation.

The visual style is characterized by:
- **Corporate Minimalism:** Expansive use of the Pale Blue-Gray background to create a focused "canvas" feel.
- **Technical Rigor:** Monospaced data points and sharp-ish corners that evoke laboratory equipment and blueprints.
- **Editorial Authority:** Large, classically inspired serif headings that provide structural hierarchy and a sense of permanence.
- **Glassmorphism (Subtle):** Very light use of backdrop blurs on floating navigation or toolbars to maintain a sense of layered complexity.
- **Tactile Grid:** Clear vertical and horizontal lines, dashed borders for diagrams, and a diagonal watermark texture that reinforces the "documentary" nature of the interface.

## Colors

The palette is rooted in the **OKLCH** color space to ensure perceptual uniformity, particularly for status-driven data visualization.

- **Surface Strategy:** The primary canvas uses a pale blue-gray (`#F4F6F7`), providing a cooler, more technical alternative to pure white. Cards and containers use a slightly brighter white to "lift" content from the background.
- **Contrast:** Text and primary structural elements use Dark Navy (`#212630`) to maintain high legibility and an institutional feel.
- **Accentuation:** A muted Teal-Blue is used for interactive elements and focus states. 
- **Semantic Coding:** A dedicated range of technical hues is used to categorize information: Amber for active commands, Purple for service requests, Green for safe states, and Red for blocking errors. These should be used sparingly as indicators rather than primary branding.

## Typography

Typography is the cornerstone of this design system's editorial character. 

- **Headings (Cinzel):** Used for all levels of headings. Its classical proportions and sharp serifs evoke historical engineering journals. Use semibold weights with tight tracking for a modern, compact look.
- **Body (Plus Jakarta Sans):** A contemporary sans-serif that balances the traditionalism of the headings. It provides excellent legibility for long-form technical documentation.
- **Technical/Label (JetBrains Mono):** All metadata, technical terms, and status badges must use JetBrains Mono. This clearly differentiates "data" from "narrative."
- **Editorial Details:** Use `micro-label` in all-caps for diagram headers and risk pills to mimic the aesthetic of blueprint notations.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. Content is contained within a 1440px max-width container on desktop, centered with 24px margins. 

- **Grid Model:** A 12-column grid is used for primary layouts, with a 12px (`gutter`) gap between columns. 
- **Rhythm:** All vertical spacing should be a multiple of the 4px base unit. 
- **Technical Panels:** Sidebars and detail panels (often 320px-400px wide) use "dual-col" arrangements for comparing technical data.
- **Responsive Behavior:** 
  - **Desktop (1024px+):** Full 12-column visibility with persistent technical sidebars.
  - **Tablet (768px - 1023px):** 8-column grid; sidebars collapse into drawers.
  - **Mobile (<767px):** 4-column grid; 16px margins; typography scales down (e.g., `headline-lg-mobile`).

## Elevation & Depth

This system avoids heavy, soft shadows in favor of **structural depth**.

- **Tonal Layers:** Elevation is primarily communicated through color shifts. The background is the lowest level (`oklch(0.965 0.01 240)`), while cards and active work surfaces use a lighter tone to appear closer to the user.
- **Precision Borders:** Use 1px solid borders (`#E6E8EB`) for standard separation. For diagrams or "placeholder" areas, use 2px dashed borders to imply a "work-in-progress" or architectural state.
- **Low-Contrast Outlines:** Instead of shadows, use soft 1px outlines with a 2px inner glow or subtle tonal shift for hover states.
- **Watermark Layer:** A repeating linear gradient watermark (diagonal lines at -45 degrees) should be applied to the base background to give the UI a tactile, paper-like quality.

## Shapes

The shape language is "Precise and Sharp-ish." 

- **Base Radius:** Most components (callouts, detail panels) use a `radius-md` (4px), creating a disciplined, industrial appearance.
- **Major Components:** Large cards and primary containers use `radius-lg` (6px) for a slightly softer feel that remains professional.
- **Technical Elements:** Small badges or state indicators may use `radius-sm` (2px) to look more like physical labels or hardware buttons.
- **Status Pills:** Only status indicators (e.g., Risk Levels) should use a full pill-shape (9999px) to differentiate them from functional UI components.

## Components

- **Buttons:** Primary buttons use a solid Dark Navy background with light text. Secondary buttons use a 1px border with no fill. All buttons use `radius-md` and `tech-label` typography for the text label.
- **Technical Badges (Pills):** Monospaced text, 700 weight, all-caps. Use semantic colors for the background (low opacity) and a high-contrast version of the same color for the text and left-border (3px width).
- **Input Fields:** Sharp corners (`radius-sm`), 1px border. Focus state uses the Teal-Blue accent for the border and a subtle ring. Placeholders use `muted-foreground`.
- **Cards:** White background, 1px solid border, `radius-lg`. No shadows. Use a `headline-md` for the title.
- **Diagram Containers:** 2px dashed borders with the diagonal watermark background. Labels should be placed in the top-left corner using `micro-label` typography.
- **Scrollbars:** Industrial thin (6px width) with a 3px radius thumb, using the Teal-Blue accent on hover to provide a subtle interactive feedback loop.