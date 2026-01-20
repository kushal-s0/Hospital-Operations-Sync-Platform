# Hospital Management System - Design System Quick Reference

## Color Palette at a Glance

### Primary Colors (Medical Blue)
```
#e8f4fd  ──────  50  (Lightest)
#d0e9fb  ──────  100
#a1d2f7  ──────  200
#72bcf3  ──────  300
#43a5ef  ──────  400
#1e88e5  ██████  500  ← Main Brand Color
#1565c0  ██████  600  (Hover)
#0d47a1  ██████  700  (Active)
#083a7d  ██████  800
#042d59  ██████  900  (Darkest)
```

### Secondary Colors (Clinical Teal)
```
#e0f7f4  ──────  50
#b2ebe3  ──────  100
#80dfd1  ──────  200
#4dd2bf  ──────  300
#26c6b1  ──────  400
#00bfa5  ██████  500  ← Secondary Brand
#00a88f  ██████  600
#008f77  ██████  700
#00765f  ██████  800
#005847  ██████  900
```

### Semantic Colors (Medical Status)
```
Success (Available):    #4caf50  ██████  Green
Warning (In Progress):  #ff9800  ██████  Orange
Error (Critical):       #f44336  ██████  Red
Info (Waiting):         #2196f3  ██████  Blue
```

### Neutral Grays
```
#ffffff  ──────  0   (White - Cards, Backgrounds)
#f8f9fa  ──────  50  (Page Background)
#f1f3f5  ──────  100
#e9ecef  ──────  200 (Borders)
#dee2e6  ──────  300
#ced4da  ──────  400
#adb5bd  ──────  500 (Muted Text)
#6c757d  ──────  600 (Secondary Text)
#495057  ──────  700 (Labels)
#343a40  ──────  800
#212529  ██████  900 (Primary Text)
```

---

## Typography Scale

```
Display    36px (2.25rem)   Semibold   ───────  Major Headings
H1         30px (1.875rem)  Semibold   ───────  Page Titles
H2         24px (1.5rem)    Semibold   ───────  Section Headings
H3         20px (1.25rem)   Semibold   ───────  Subsections
H4         18px (1.125rem)  Medium     ───────  Card Titles
Base       16px (1rem)      Normal     ███████  Body Text (Default)
Small      14px (0.875rem)  Normal     ───────  Labels, Meta
Tiny       12px (0.75rem)   Normal     ───────  Badges, Captions
```

**Font Family**: `Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

---

## Spacing System (8px Grid)

```
spacing-1     4px   ─
spacing-2     8px   ──
spacing-3    12px   ───
spacing-4    16px   ────  ← Most Common
spacing-5    20px   ─────
spacing-6    24px   ──────  ← Common
spacing-8    32px   ────────
spacing-10   40px   ──────────
spacing-12   48px   ────────────
spacing-16   64px   ────────────────
```

---

## Component Sizes

### Buttons
```
Small    sm    32px height   padding: 8px 12px    font: 14px
Medium   md    40px height   padding: 12px 16px   font: 14px  ← Default
Large    lg    48px height   padding: 16px 24px   font: 16px
```

### Cards
```
Default      padding: 20px   border-radius: 8px
Compact      padding: 16px   border-radius: 8px
```

### Border Radius
```
Small     sm    4px   ─
Medium    md    6px   ──
Large     lg    8px   ───  ← Most Common
XLarge    xl   12px   ────
Full   full   999px  ●●●●  (Pills, Badges)
```

### Shadows
```
XS    0 1px 2px rgba(0,0,0,0.05)
SM    0 1px 3px rgba(0,0,0,0.1)        ← Cards
MD    0 4px 6px rgba(0,0,0,0.1)        ← Hover
LG    0 10px 15px rgba(0,0,0,0.1)      ← Modals
XL    0 20px 25px rgba(0,0,0,0.1)      ← Dropdowns
```

---

## Status Color Coding (Medical Standard)

```
Available / Completed / Active
  Background: #e8f5e9  (Green-50)
  Text:       #2e7d32  (Green-700)
  Dot:        #4caf50  ●

Occupied / In Consultation / In Progress  
  Background: #fff8e1  (Orange-50)
  Text:       #f57c00  (Orange-700)
  Dot:        #ff9800  ●

Emergency / Urgent / Critical / Maintenance
  Background: #ffebee  (Red-50)
  Text:       #c62828  (Red-700)
  Dot:        #f44336  ●

Waiting / Reserved / Scheduled
  Background: #e3f2fd  (Blue-50)
  Text:       #1976d2  (Blue-700)
  Dot:        #2196f3  ●

Default / Unknown
  Background: #f1f3f5  (Gray-100)
  Text:       #495057  (Gray-700)
  Dot:        #adb5bd  ●
```

---

## Icon Library

### Available Icons (24x24px, Stroke-based)
```
BedIcon           🛏  Bed management, capacity
PatientIcon       👤  Patient records, profiles
QueueIcon         📋  OPD queue, documents
AdmissionIcon     📅  Admissions, appointments
InventoryIcon     📦  Inventory, stock items
AlertIcon         ⚠  Warnings, critical alerts
CheckCircleIcon   ✓  Success, completion
ActivityIcon      〰  Activity, monitoring
ClockIcon         🕐  Time, waiting, duration
StatsIcon         📊  Analytics, trends
```

Usage:
```jsx
import { BedIcon, PatientIcon } from '../../components/Common/Icons';
<BedIcon />
```

---

## Common Patterns

### Page Header
```jsx
<div className="page-header">
  <div>
    <h1 className="page-title">Dashboard</h1>
    <p className="page-subtitle">Real-time overview</p>
  </div>
  <div className="header-actions">
    <Button variant="primary">Action</Button>
  </div>
</div>
```

### KPI Grid (2-4 columns)
```jsx
<div className="stats-grid">
  <Card title="..." value={...} icon={<Icon />} color="blue" />
  <Card title="..." value={...} icon={<Icon />} color="green" />
  <Card title="..." value={...} icon={<Icon />} color="teal" />
  <Card title="..." value={...} icon={<Icon />} color="red" />
</div>
```

### Status in Table
```jsx
{
  key: 'status',
  label: 'Status',
  render: (row) => <StatusBadge status={row.status} />
}
```

### Action Buttons
```jsx
<Button variant="primary">Primary Action</Button>
<Button variant="secondary">Secondary Action</Button>
<Button variant="outline">Neutral Action</Button>
<Button variant="success">Confirm</Button>
<Button variant="danger">Delete</Button>
```

---

## Layout Dimensions

```
┌──────────────────────────────────────────┐
│  Header: 64px (fixed top)                 │
│  Background: #ffffff, Border-bottom: 1px  │
├─────────┬────────────────────────────────┤
│ Sidebar │  Main Content                   │
│ 260px   │  margin-left: 260px             │
│ (fixed) │  padding: 24px                  │
│         │  background: #f8f9fa            │
│         │  max-width: 1400px (centered)   │
│         │                                 │
└─────────┴────────────────────────────────┘
```

---

## Button Variants Quick Reference

```
Primary     Blue background, white text       #1e88e5
Secondary   Teal background, white text       #00bfa5
Success     Green background, white text      #4caf50
Warning     Orange background, white text     #ff9800
Danger      Red background, white text        #f44336
Outline     White bg, gray border/text        transparent
Ghost       Transparent, no border            transparent
```

---

## Responsive Breakpoints

```
Mobile:   < 768px      (1 column, hidden sidebar)
Tablet:   768-1024px   (2-3 columns, sidebar visible)
Desktop:  > 1024px     (3-4 columns, full layout)
```

---

## Animation Speeds

```
Fast    150ms   Hover states, small transitions
Base    250ms   Standard transitions, modals
Slow    350ms   Large movements, page transitions
```

Easing: `cubic-bezier(0.4, 0, 0.2, 1)` (Material Design standard)

---

## Accessibility Checklist

- [ ] Color contrast ≥ 4.5:1 for text
- [ ] Focus indicators on all interactive elements (2px outline)
- [ ] Keyboard navigation support (tab order)
- [ ] Semantic HTML (buttons, headings, labels)
- [ ] ARIA labels where needed
- [ ] Touch targets ≥ 44x44px
- [ ] Don't rely on color alone for meaning

---

## CSS Variable Quick Reference

### Usage in Your CSS
```css
.my-component {
  /* Colors */
  color: var(--color-primary-600);
  background: var(--color-neutral-0);
  border: 1px solid var(--color-neutral-200);
  
  /* Spacing */
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-6);
  gap: var(--spacing-3);
  
  /* Typography */
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  
  /* Border Radius */
  border-radius: var(--radius-lg);
  
  /* Shadows */
  box-shadow: var(--shadow-md);
  
  /* Transitions */
  transition: all var(--transition-fast);
}
```

---

## Component Import Cheatsheet

```jsx
// Common Components
import { 
  Card, 
  Table, 
  StatusBadge, 
  Button 
} from '../../components/Common';

// Icons
import { 
  BedIcon, 
  PatientIcon, 
  QueueIcon,
  AdmissionIcon,
  InventoryIcon,
  AlertIcon,
  CheckCircleIcon,
  ActivityIcon,
  ClockIcon,
  StatsIcon
} from '../../components/Common/Icons';
```

---

## When in Doubt...

**Refer to**:
- `Dashboard.js` - Reference implementation
- `UI_DESIGN_GUIDE.md` - Complete documentation
- `IMPLEMENTATION_GUIDE.md` - Step-by-step instructions

**Design Principle**: If it looks like a hospital admin system from Apollo/Fortis, you're on the right track.

---

**Design System Version**: 1.0.0  
**Last Updated**: January 2026
