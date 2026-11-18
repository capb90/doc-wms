---
name: Fleet Track Aura
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006591'
  on-secondary: '#ffffff'
  secondary-container: '#39b8fd'
  on-secondary-container: '#004666'
  tertiary: '#006242'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d55'
  on-tertiary-container: '#bdffdb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#c9e6ff'
  secondary-fixed-dim: '#89ceff'
  on-secondary-fixed: '#001e2f'
  on-secondary-fixed-variant: '#004c6e'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.05em
  numeric-metric:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 28px
    letterSpacing: -0.02em
  numeric-stat:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '700'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-2xs: 0.125rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
  space-2xl: 2rem
---

## Brand & Style

The design system establishes a high-density, mission-critical enterprise operations aesthetic built for yard management, supply chain tracking, and plant logistics. Designed to align with the precision and cleanliness of modern component frameworks (such as PrimeVue's Lara and Aura design languages) powered by Tailwind CSS utility ergonomics, the UI projects extreme reliability, clarity, and systematic order under high cognitive load.

The design movement is **Modern Corporate & Functional Minimalism**:
- **Clarity over ornament:** Crisp borders, balanced tonal contrast, and low visual noise ensure dispatchers, site supervisors, and billing coordinators can scan hundreds of vehicle states without fatigue.
- **Tonal state signifiers:** Semantic color tinting (sky/blue for gate intake, emerald for completed runs, amber for operational bottlenecks/dwell time, rose for critical billing alerts or overdue dwell) provides instant peripheral cues without overpowering the workspace.
- **Structured density:** Compact information grouping with two-tier hierarchy (metadata headers alongside micro key-value definition grids).

## Colors

The palette leverages a structured slate-neutral foundation paired with an intentional enterprise blue primary.

- **Canvas & Surface Architecture:** 
  - Application background: `#F8FAFC` (Slate-50) or `#F1F5F9` (Slate-100) for layered sidebars.
  - Active card and modal containers: Pure White `#FFFFFF`.
  - Structural borders: `#E2E8F0` (Slate-200) for standard dividers, `#CBD5E1` (Slate-300) for active form borders.
- **Typography & Neutral Tokens:**
  - High-emphasis labels and headlines: `#0F172A` (Slate-900) to `#1E293B` (Slate-800).
  - Secondary metadata & inactive labels: `#64748B` (Slate-500).
  - De-emphasized or placeholder text: `#94A3B8` (Slate-400).
- **Primary & Interactive Accents:**
  - Primary `#2563EB` (Blue-600) drives key navigation states, active segmented tabs, stepper nodes, and primary action buttons.
  - Hover primary: `#1D4ED8` (Blue-700); surface soft active: `#EFF6FF` (Blue-50).
- **Semantic Status Tints:**
  - **In Gate / Active Transit:** Badge fill `#EFF6FF` (Blue-50), text/icon `#1D4ED8` (Blue-700), border `#DBEAFE`.
  - **Completed / Ready:** Badge fill `#ECFDF5` (Emerald-50), text/icon `#047857` (Emerald-700), border `#D1FAE5`.
  - **Pending / Dwell Time Warning:** Badge fill `#FFFBEB` (Amber-50), text `#B45309` (Amber-700), highlighted stat `#D97706` (Amber-600).
  - **Critical Alert / Overdue:** Badge fill `#FEF2F2` (Red-50), text `#B91C1C` (Red-700), border `#FEE2E2`.

## Typography

The typography leverages `Inter` across all interfaces to guarantee maximum tabular readability, numeric precision, and clean rendering across high-DPI and standard display monitors.

- **Uppercase Section Tags:** Category labels (e.g., `OPERACIONES`, `FACTURACIÓN`, `INFORMACIÓN GENERAL`, `PROGRESO`) render in `label-sm` or `label-md` with full uppercase tracking (`letter-spacing: 0.05em`) and Slate-500 coloring to define module boundaries without heavy divider rules.
- **Tabular Figures:** All metrics, license plates (`UGV869`), durations (`1d 13h 00m`), and timestamps (`10/11/2026 21:35`) must enforce `font-feature-settings: 'tnum' on, 'zero' on` to prevent layout shift during live automated polling updates.
- **Hierarchical Pairs:** Data cards employ a strict stacked pair formula: micro uppercase or muted label (`body-sm`) resting immediately above dark medium-weight values (`label-lg` or `body-md`).

## Layout & Spacing

The layout is built upon an 8pt base grid with a fluid master-detail split layout structure:

- **Master Surface & Sidebar Panel:**
  - **Main Dashboard Stage:** Uses a responsive fluid grid. KPI counters display in 4-column decks (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`).
  - **Entity Card Grid:** Vehicle unit cards align to a dynamic grid (`grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4`) separated by a uniform `1rem` (16px) gutter.
  - **Detail Inspector Drawer / Right Panel:** Fixed width of `360px` to `420px` along the right viewport boundary, housing vertical process steppers and nested property definition blocks.
- **Adaptive Breakpoints:**
  - **Desktop (>= 1280px):** Two-tier header, multi-card operational overview, persistent right inspector panel, and wide table/card views.
  - **Tablet (768px - 1279px):** Inspector collapses into an overlay slide-out drawer (PrimeVue `Sidebar`/`Drawer`). KPI grids switch to 2 columns.
  - **Mobile (< 768px):** Single-column stacked cards, horizontal scroll for segmented period filters, sticky top search/filter header.
- **Component Padding Rhythms:**
  - Standard cards utilize `1rem` (16px) internal padding (`space-lg`).
  - Micro stat badges and input controls use `0.375rem` vertical by `0.75rem` horizontal padding.

## Elevation & Depth

Visual hierarchy and layering rely primarily on **Tonal Layers** combined with **Low-Contrast Outlines** rather than dramatic cast drop shadows.

- **Level 0 (App Canvas):** `#F8FAFC`. Completely flat base with zero elevation.
- **Level 1 (Card & Content Blocks):** Pure White `#FFFFFF` backed by a 1px solid hairline border `#E2E8F0`. Shadow is minimal: `0 1px 2px 0 rgba(0, 0, 0, 0.03)` to gently separate white cards from Slate-50 canvas.
- **Level 2 (Interactive Hover / Hovered Cards):** Hairline border transitions to `#CBD5E1` with an elevated ambient shadow `0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.04)`.
- **Level 3 (Floating Drawers & Modals):** Fixed detail drawers and modal dialogues use a crisp border `#E2E8F0`, deep diffused shadow `0 20px 25px -5px rgba(15, 23, 42, 0.08)`, and backdrop tint `rgba(15, 23, 42, 0.25)`.
- **Icon Container Badges:** Stat icons inside metrics cards are recessed or resting on soft tinted surface fills (`#F1F5F9`, `#EFF6FF`, `#ECFDF5`, `#FFFBEB`) without border outlines.

## Shapes

The interface embraces a balanced semi-rounded curvature (`roundedness: 2`), reflecting the modern PrimeVue Aura look:

- **Cards & Data Panels:** `12px` (`0.75rem` / `rounded-xl`) outer radius provides a clean modern feel without consuming excessive corner real estate.
- **Inputs & Standard Buttons:** `8px` (`0.5rem` / `rounded-lg`) corner radius ensures crisp mechanical alignment across inputs and dropdown toggles.
- **Status Tags & Pill Badges:** Full pill radius (`9999px` / `rounded-full`) for operational statuses (`En portería`, `Listo para pesaje`, `Completado`), immediately distinguishing contextual state metadata from structural rectangular buttons.
- **Segmented Controls:** Container uses `8px` with individual segmented tab buttons at `6px`.

## Components

### Buttons & Interactive Controls
- **Primary Action:** Solid Blue `#2563EB` fill, white bold text, `8px` border radius, subtle hover glow `#1D4ED8`. Focus state displays a 2px outer ring in `#93C5FD` with 2px offset.
- **Segmented Time Filters (Today / This Week / This Month / All):** Slate-100 capsule container housing pill or soft-rect buttons. Active item is styled with solid `#1E293B` or `#FFFFFF` with soft drop shadow and Slate-900 text.
- **Ghost Action Buttons:** Transparent background with Slate-600 text, hover to Slate-100.

### Status Badges & Pills
- **Geometry:** Height 24px, pill rounded (`rounded-full`), horizontal padding `10px`, typography `11px` weight 600.
- **Variants:**
  - *In Gate / Intake:* Soft blue background (`#EFF6FF`), Slate-800 or Blue-700 text, leading intake icon (`pi-building` or similar).
  - *Ready for Weighing / Transit:* Light blue-sky tint (`#F0F9FF`), `#0369A1` text, leading check icon.
  - *Completed:* Emerald tint (`#ECFDF5`), `#047857` text, leading check circle icon.
  - *Overdue / Alert:* Red tint (`#FEF2F2`), `#B91C1C` text.

### KPI & Metric Cards
- White `#FFFFFF` surface container, 1px border `#E2E8F0`, padding 16px.
- Left side: 40x40px rounded icon container with contextual pastel background (e.g., green tint for billing, blue tint for yard trucks, amber for delays).
- Right side: Stacked bold numerical display (`numeric-metric`) with muted descriptor label underneath.

### Truck / Vehicle Entity Cards
- Header row displaying vehicle ID (`UGV869`) in bold dark text alongside the dynamic status badge.
- 2-column or 3-column micro definition grid:
  - Label: `Conductor` / Value: driver name or `Sin asignar` (italicized Slate-400).
  - Label: `Transportadora` / Value: company name.
  - Label: `Ingreso` / Value: formatted timestamp.
  - Label: `Tiempo` / Value: dwell duration (colored amber `#D97706` if exceeding threshold).
- Footer tag pill indicating load type (e.g., `Input` or `OutputCargo`) in a low-key Slate-100 badge.

### Vertical Process Stepper (Timeline)
- Circular node markers (36px):
  - **Active Stage:** Solid blue ring `#2563EB`, soft blue background `#EFF6FF`, primary blue centered icon.
  - **Completed Stage:** Crisp slate or emerald ring with check icon.
  - **Pending Stage:** Hairline Slate-300 ring, Slate-400 icon, transparent background.
- Connecting line: 2px solid vertical rail `#E2E8F0`.
- Text pairing: Step label in dark bold font alongside completion timestamp in muted `body-sm`.

### Form Inputs & Search Fields
- PrimeVue Aura styling: Input height 38px, padding 8px 12px, border 1px solid `#CBD5E1`, background `#FFFFFF`. Integrated leading search magnifier icon (`pi-search`) in Slate-400.