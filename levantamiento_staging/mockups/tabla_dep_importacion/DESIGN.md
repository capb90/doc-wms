---
name: Aura Logistics & Freight
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
  on-surface-variant: '#464555'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#005338'
  on-tertiary: '#ffffff'
  tertiary-container: '#006e4c'
  on-tertiary-container: '#7df1bd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#85f8c4'
  tertiary-fixed-dim: '#68dba9'
  on-tertiary-fixed: '#002114'
  on-tertiary-fixed-variant: '#005137'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Inter
    fontSize: 2.25rem
    fontWeight: '700'
    lineHeight: 2.75rem
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 1.75rem
    fontWeight: '600'
    lineHeight: 2.25rem
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 1.375rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
    letterSpacing: 0em
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
    letterSpacing: -0.01em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.02em
  label-md:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.03em
  label-sm:
    fontFamily: Inter
    fontSize: 0.6875rem
    fontWeight: '600'
    lineHeight: 0.875rem
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-compact: 0.5rem
  margin: 1.5rem
  margin-mobile: 0.75rem
  space-xs: 0.25rem
  space-sm: 0.375rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system is engineered for enterprise-grade customs operations, bonded warehousing, and freight tracking. Inspired by the clarity and precision of modern PrimeVue foundations (Aura / Lara), the aesthetic bridges corporate technical utility with modern architectural poise.

The target audience includes logistics coordinators, customs clearance brokers, dock supervisors, and compliance auditors who handle high-throughput, mission-critical operations. The UI communicates calm authority, precision, and zero-ambiguity execution. 

Key stylistic traits include:
- **High-Density Utility:** Compact vertical cadence, intentional borders, and clear spatial separation for dense datasets.
- **Controlled Indigo Accents:** Grounded, purposeful use of deep slate neutrals counterbalanced by vibrant, intelligent indigo focus points.
- **Operational Ergonomics:** Visual structures that minimize cognitive fatigue over extended shift usage.

## Colors

The palette is anchored by a structured slate scale, accented by a tailored industrial indigo for interactive focal points, and backed by crisp semantic markers for regulatory risk monitoring.

- **Primary (`#4f46e5` - Indigo):** Designates active states, primary commitments, navigational anchors, and interactive selections.
- **Secondary (`#0f172a` - Deep Slate):** Anchors headers, structural containers, high-emphasis metrics, and enterprise chrome.
- **Tertiary (`#059669` - Emerald):** Used strictly for regulatory clearance, completed transit, operational parity, and safe validation states.
- **Neutral (`#64748b` - Slate):** Powers borders, table dividers, secondary labels, disabled components, and surface scaffolding.

### Semantic Triage Indicators
- **Success (`#059669` / bg: `#ecfdf5` / border: `#a7f3d0`):** Cleared customs, sealed cargo, verified manifests.
- **Warning (`#d97706` / bg: `#fffbeb` / border: `#fde68a`):** Bond timeouts nearing, inspection pending, discrepancy flagged.
- **Danger (`#dc2626` / bg: `#fef2f2` / border: `#fecaca`):** Customs hold, contraband alert, weight violation, tariff mismatch.
- **Info (`#0284c7` / bg: `#f0f9ff` / border: `#bae6fd`):** In-transit telemetry, yard re-routing, dock reassigned.

## Typography

The type system implements a strict dual-engine strategy:
- **Inter** handles narrative flow, dashboard layouts, modals, and structured form fields. Its neutral geometry ensures legibility at small sizes during intensive data capture.
- **JetBrains Mono** is reserved exclusively for alphanumeric payloads: VINs, ISO container codes (e.g., `MSKU 928374-1`), customs declaration references, weigh-in tickets, and tariff schedule codes (HS/HTS).

All monospace components use tabular alignment so multi-line telemetry grids align vertically across character columns. Upper-case transformation is enforced for all identifier codes.

## Layout & Spacing

The layout runs on a responsive 12-column fluid grid tailored for widescreen logistics command centers (1440px+) while gracefully degrading to tablet and terminal resolutions.

- **Desktop (1024px+):** Fluid 12-column layout with `gutter` (1rem) and outer `margin` (1.5rem). High-density operational tables employ `gutter-compact` (0.5rem) inside sub-grids and filter toolbars.
- **Tablet (768px - 1023px):** 8-column layout. Split-pane customs inspection panels switch to vertically stacked accordions.
- **Mobile / Handheld Scanner (320px - 767px):** 4-column layout with `margin-mobile` (0.75rem). Data tables collapse into stacked metric cards with prominent barcode/ticket headers.

Vertical rhythm relies on tight, predictable increments (`space-xs` through `space-md` for internal component padding) to prioritize vertical screen real estate for maximum row visibility.

## Elevation & Depth

In alignment with the PrimeVue Aura architectural philosophy, elevation is expressed through crisp, low-contrast border boundaries reinforced by diffused, ambient micro-shadows. Heavy dropshadows are rejected in favor of planar discipline.

- **Flat Layer (Canvas):** Base background `#f8fafc` (Slate 50) paired with card/surface containers `#ffffff`.
- **Structural Outlines:** Every container, table cell division, input, and panel uses a continuous `1px solid #e2e8f0` (Slate 200) boundary. In hover or active states, boundaries transition to `#cbd5e1` or `#4f46e5`.
- **Level 1 (Cards, Data Panels, Navbars):** `box-shadow: 0 1px 2px 0 rgba(15, 23, 42, 0.05); border: 1px solid #e2e8f0;`
- **Level 2 (Dropdown Menus, Flyout Filters, Popovers):** `box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05); border: 1px solid #cbd5e1;`
- **Level 3 (Customs Modals, Yard Drawers):** `box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 8px 10px -6px rgba(15, 23, 42, 0.05); border: 1px solid #94a3b8;`

## Shapes

The design system employs a soft, restrained geometry (`roundedness: 1` = 0.25rem / 4px base radius) evocative of technical enterprise interfaces. 

- **Inputs, Buttons, Cells, and Dropdowns:** Base 4px (`0.25rem`) radius preserves structural grid alignment and ensures high-density interfaces feel disciplined and crisp.
- **Cards, Filter Headers, and Modals:** Medium 8px (`0.5rem`) radius softening large macro-structures.
- **Pills / Status Chips:** Pill-shaped full radius is prohibited; chips and badges maintain a consistent 4px (`0.25rem`) or 2px (`0.125rem`) micro-radius to reflect official customs stamping aesthetics.

## Components

### Data Tables (High Density)
- **Header:** Background `#f8fafc`, uppercase text in `label-sm`, color `#475569`, border bottom `2px solid #cbd5e1`. Vertical cell padding is strictly `0.5rem` (`space-sm`), horizontal `0.75rem` (`space-md`).
- **Body Rows:** Background alternating `#ffffff` and `#fafafa` (zebra striping optional for 50+ row views). Border bottom `1px solid #f1f5f9`. Hover state shifts entire row to `#eef2ff` (Indigo-50 tint) with a `2px` left border in `#4f46e5`.
- **Numeric & Code Cells:** Monospace typography (`code-md`), right-aligned for weight metrics (KG/LBS), left-aligned for plate/seal numbers.

### Status Badges & Tags
- **Structure:** Inline-flex, items-center, border `1px solid`, radius `0.25rem`, padding `0.125rem 0.375rem`, font `label-sm`.
- **Cleared / In-Yard:** Text `#065f46`, bg `#ecfdf5`, border `#a7f3d0`. Preceded by an emerald 6px status dot.
- **Customs Hold / Risk:** Text `#991b1b`, bg `#fef2f2`, border `#fecaca`. Preceded by a danger crimson exclamation indicator.
- **Inspection Required:** Text `#92400e`, bg `#fffbeb`, border `#fde68a`.

### Buttons
- **Primary:** Background `#4f46e5`, border `1px solid #4338ca`, text `#ffffff`, radius `0.25rem`, font weight `500`. Hover state `#4338ca`. Focused state: 2px ring `#c7d2fe`.
- **Secondary / Outline:** Background `#ffffff`, border `1px solid #cbd5e1`, text `#0f172a`. Hover state `#f8fafc` with border `#94a3b8`.
- **Dense/Icon Action:** Compact 28px square buttons with `#64748b` icon color for in-table quick actions (Print Waybill, Release Gate, Inspect).

### Input Fields & Selectors
- **Height & Spacing:** Standard enterprise height of 32px (`2rem`) for compact operational views, 38px for form wizards. Padding: `0.375rem 0.625rem`.
- **Borders:** `1px solid #cbd5e1`, radius `0.25rem`. Focus applies `border-color: #4f46e5` and an ambient glow of `box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15)`.
- **Monospace Code Inputs:** Container number inputs, seal serials, and license plates leverage `code-md` typography with automatic capital formatting.

### Checkboxes & Radio Controls
- **Size:** 16px by 16px with a 3px radius for checkboxes, full circle for radios.
- **Active State:** `#4f46e5` fill with a crisp white checkmark / inner dot. Indeterminate states for multi-row warehouse pallet selection use a solid white minus bar.

### Operational KPI Metric Cards
- **Structure:** Background `#ffffff`, border `1px solid #e2e8f0`, radius `0.5rem`, padding `space-md`.
- **Layout:** Micro-label on top in uppercase `label-sm`, value in display weight `headline-lg` (slate 900), accompanied by a trend badge (+2.4% vs last shift) and secondary monospace subtext detailing active manifest counts.