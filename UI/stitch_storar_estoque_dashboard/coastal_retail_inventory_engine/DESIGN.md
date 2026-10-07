---
name: Coastal Retail Inventory Engine
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#434655'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006e2d'
  on-secondary: '#ffffff'
  secondary-container: '#7cf994'
  on-secondary-container: '#007230'
  tertiary: '#ae0010'
  on-tertiary: '#ffffff'
  tertiary-container: '#d52022'
  on-tertiary-container: '#ffecea'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#7ffc97'
  secondary-fixed-dim: '#62df7d'
  on-secondary-fixed: '#002109'
  on-secondary-fixed-variant: '#005320'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#93000b'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
  metric-display:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system targets independent coastal retail managers and shop operators balancing high seasonality, sudden tourist influxes, and perishable or fast-moving beach supplies. The tone is utilitarian, calm, and unmistakably decisive. It eliminates inventory anxiety by transforming complex predictive runout algorithms into clear operational signals.

The aesthetic follows Modern Corporate SaaS with an emphasis on high-legibility functional data density:
- **Calm, uncluttered canvas:** Light, low-glare surface foundations that remain comfortable in bright, sunlit coastal back-offices or counter tablets.
- **Signal-first hierarchy:** Color is never purely decorative; it serves strictly as status classification (healthy stock, warning runout, emergency stockout, stagnant inventory).
- **Physical precision:** Structured borders, modular data density, zero unnecessary gradients, and clear typographic contrast for scanning stock-keeping units (SKUs) at a glance.

## Colors

The palette is engineered for rapid visual diagnosis on point-of-sale tablets and desktop back-offices:

- **Canvas & Surfaces:**
  - Base Background: `#F7F8FA` provides low eye fatigue while creating clean separation against pure white cards.
  - Surface Card: `#FFFFFF`
  - Border Subdued: `#E5E7EB`
  - Border Interactive: `#D1D5DB`

- **Text & Content:**
  - Primary Text: `#111827` (High contrast, accessible for SKU tables and quantities).
  - Secondary Text: `#6B7280` (Supporting metadata, timestamps, units).
  - Subtle / Inactive Text: `#9CA3AF`

- **Action & Brand:**
  - Primary Action: `#2563EB` (Functional blue for order triggers, bulk updates, and focused states).
  - Primary Hover: `#1D4ED8`
  - Primary Surface / Tint: `#EFF6FF`

- **Inventory Health Status Tokens:**
  - **Healthy / OK:** Text `#16A34A`, Background `#F0FDF4`, Border `#BBF7D0`
  - **At Risk / Atenção:** Text `#D97706`, Background `#FFFBEB`, Border `#FDE68A`
  - **Critical Rupture / Crítico:** Text `#DC2626`, Background `#FEF2F2`, Border `#FECACA`
  - **Dormant / Sem Giro:** Text `#6B7280`, Background `#F3F4F6`, Border `#E5E7EB`
  - **Depleted / Esgotado:** Text `#4B5563`, Background `#E5E7EB`, Border `#D1D5DB`

## Typography

Inter serves as the single font family across the platform to ensure tabular figure alignment, optical clarity, and low rendering overhead across browser engines.

- **Tabular Figures (`tnum`):** All numerical quantities, SKU counts, financial figures, and estimated stockout days must enable `font-feature-settings: "tnum"` to prevent horizontal jitter during live inventory updates.
- **Hierarchy Rules:**
  - `metric-display`: Exclusively for KPI card top-level numbers (e.g., "3 dias restantes", "14 SKUs críticos").
  - `label-sm` and `label-md`: Applied to inventory status badges, table column headers (with optional uppercase styling and letter-spacing `0.05em`), and filter pills.
  - `body-md`: Standard table row text, modal copy, and form field entries.

## Layout & Spacing

The layout is structured on an 8pt baseline rhythm anchored by a standard modular distance of 24px (`1.5rem` / `space-lg`).

- **Grid Architecture:**
  - **Desktop (1024px+):** Fluid 12-column grid. Column gutters: 24px (`1.5rem`). Canvas side margins: 24px (`1.5rem`) within a max-width container of 1440px.
  - **Tablet (768px - 1023px):** 8-column layout. Gutters: 16px (`1rem`). Margins: 20px.
  - **Mobile (< 768px):** 4-column layout. Gutters: 16px (`1rem`). Margins: 16px (`1rem`).
- **Reflow & Hierarchy:**
  - Dashboard analytics cards span 3 columns on desktop (4 cards per row), 4 columns on tablet (2x2), and full width on mobile.
  - The critical inventory stockout alert table reflows from multi-column tabular data on desktop into horizontal priority cards on screens below 768px.

## Elevation & Depth

Visual hierarchy uses a hybrid of low-contrast hairline outlines and faint, diffused ambient shadows. Depth is kept flat and grounded to maintain data clarity.

- **Base Level (Canvas):** `#F7F8FA` with no elevation.
- **Layer 1 (Cards, KPI blocks, Data Tables):** Surface `#FFFFFF`, border `1px solid #E5E7EB`, shadow: `0 1px 3px 0 rgba(0, 0, 0, 0.04), 0 1px 2px -1px rgba(0, 0, 0, 0.02)`.
- **Layer 2 (Dropdowns, Popovers, Filter Menus):** Surface `#FFFFFF`, border `1px solid #E5E7EB`, shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05)`.
- **Layer 3 (Modals, Slide-over Drawer for Order Creation):** Surface `#FFFFFF`, border `1px solid #E5E7EB`, shadow: `0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)`. Dimmer backdrop: `#111827` at 40% opacity.
- **Interactive State (Hovered Table Rows / Clickable Cards):** Cards elevate slightly to shadow `0 4px 12px 0 rgba(0, 0, 0, 0.05)` with border shifting to `#D1D5DB`.

## Shapes

The design system maintains a structured, professional geometry with an 8px (`0.5rem`) radius standard:

- **Cards & Data Panels:** `8px` (`rounded-lg`).
- **Buttons, Text Inputs, and Filter Controls:** `6px` to `8px` for ergonomic touch and tap targets without appearing excessively circular.
- **Badges & Status Chips:** `4px` (`rounded-sm`) or fully rounded pill style (`9999px`) for compact tag differentiation.
- **Modals & Drawers:** `8px` for modal dialogs; drawers maintain square edges touching the screen boundaries (`0px` on docked sides).

## Components

### Buttons
- **Primary:** Background `#2563EB`, text `#FFFFFF`, radius 8px, padding `8px 16px` (sm) or `10px 20px` (md). Hover `#1D4ED8`. Active `#1E40AF`. Focus outline `2px solid #2563EB`, offset `2px`.
- **Secondary / Outline:** Background `#FFFFFF`, border `1px solid #E5E7EB`, text `#111827`. Hover background `#F9FAFB`, border `#D1D5DB`.
- **Destructive:** Background `#DC2626`, text `#FFFFFF`. Hover `#B91C1C`.
- **Ghost:** Background transparent, text `#6B7280`. Hover background `#F3F4F6`, text `#111827`.

### Status Badges & Chips
- Designed with high legibility, including an optional leading 6px colored dot indicator.
- **OK:** Text `#16A34A`, background `#F0FDF4`, border `1px solid #BBF7D0`.
- **Atenção:** Text `#D97706`, background `#FFFBEB`, border `1px solid #FDE68A`.
- **Crítico:** Text `#DC2626`, background `#FEF2F2`, border `1px solid #FECACA`.
- **Sem Giro:** Text `#6B7280`, background `#F3F4F6`, border `1px solid #E5E7EB`.
- **Esgotado:** Text `#4B5563`, background `#E5E7EB`, border `1px solid #D1D5DB`.

### Data Tables & Lists
- Table wrapper: Background `#FFFFFF`, border `1px solid #E5E7EB`, border-radius `8px`, overflow hidden.
- Table headers: Background `#F9FAFB`, text `#6B7280`, font-size `12px`, font-weight `600`, text-transform uppercase, tracking `0.05em`, padding `12px 16px`.
- Table rows: Height `48px` to `56px`, bottom border `1px solid #F3F4F6`, hover color `#F9FAFB`. Numeric metrics use right alignment and monospace/tabular figures.

### Inputs & Select Fields
- Container: Background `#FFFFFF`, border `1px solid #D1D5DB`, radius `6px` to `8px`, padding `8px 12px`, text `#111827`, placeholder text `#9CA3AF`.
- Focus state: Border color `#2563EB`, box-shadow `0 0 0 3px rgba(37, 99, 235, 0.15)`.
- Error state: Border color `#DC2626`, box-shadow `0 0 0 3px rgba(220, 38, 38, 0.15)`.

### Checkboxes & Radios
- Size `16px x 16px`, border `1px solid #D1D5DB`, radius `4px` (checkbox) or `50%` (radio).
- Checked: Background `#2563EB`, checkmark `#FFFFFF`. Focus ring: 2px `#2563EB` offset 2px.

### Cards & KPI Blocks
- Background `#FFFFFF`, border `1px solid #E5E7EB`, padding `24px`, border-radius `8px`.
- Title: `14px` weight `500` color `#6B7280`. Value: `28px` weight `700` color `#111827`. Sub-label: inline chip indicating deviation or runout trend (e.g., "-48h até ruptura").

### Domain-Specific Components (Inventory Forecasting)
- **Runout Timeline Bar (Previsão de Esgotamento):** Horizontal segmented meter depicting stock progression over upcoming peak days (weekends/holidays in Porto de Galinhas), shifting from `#16A34A` to `#D97706` and `#DC2626`.
- **Restock Action Pill:** Quick-trigger inline button placed inside critical rows allowing instant purchase order initiation with local distributors.