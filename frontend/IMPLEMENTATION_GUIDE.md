# Quick Implementation Guide - Applying Design to Other Pages

## Step-by-Step: How to Redesign Any Page

### 1. Page Header Pattern
Replace old headers with this standard pattern:

```jsx
<div className="page-header">
  <div>
    <h1 className="page-title">Page Title Here</h1>
    <p className="page-subtitle">Brief description of the page</p>
  </div>
  <div className="header-actions">
    {/* Action buttons go here */}
    <Button variant="primary" icon={<AddIcon />}>
      Add New Item
    </Button>
  </div>
</div>
```

### 2. Replace Emojis with Icons

**Before**:
```jsx
icon="🛏️"
icon="🎫"
icon="⚠️"
```

**After**:
```jsx
import { BedIcon, QueueIcon, AlertIcon } from '../../components/Common/Icons';

icon={<BedIcon />}
icon={<QueueIcon />}
icon={<AlertIcon />}
```

### 3. Update Card Usage

**Before**:
```jsx
<Card
  title="Total Beds"
  value={summary.total_beds}
  icon="🛏️"
  color="blue"
/>
```

**After**:
```jsx
<Card
  title="Total Beds"
  value={summary.total_beds}
  icon={<BedIcon />}
  color="blue"
  subtitle="Additional context here"
  trend={{ direction: 'up', value: '+5%' }} // Optional
/>
```

### 4. Status Badges in Tables

**Before**:
```jsx
<span className={`status ${patient.status}`}>
  {patient.status}
</span>
```

**After**:
```jsx
import { StatusBadge } from '../../components/Common';

<StatusBadge status={patient.status} />
```

### 5. Button Patterns

**Before**:
```jsx
<button className="btn-primary" onClick={handleClick}>
  Add Patient
</button>
```

**After**:
```jsx
import { Button } from '../../components/Common';

<Button variant="primary" onClick={handleClick}>
  Add Patient
</Button>

<Button variant="success" loading={isSaving} icon={<SaveIcon />}>
  Save Changes
</Button>

<Button variant="danger" size="sm">
  Delete
</Button>
```

### 6. Loading States

**Before**:
```jsx
{loading && <div>Loading...</div>}
```

**After**:
```jsx
{loading && (
  <div className="loading-state">
    <div className="loading-spinner"></div>
    <p>Loading data...</p>
  </div>
)}
```

### 7. Error States

**Before**:
```jsx
{error && <div className="error">{error}</div>}
```

**After**:
```jsx
import { AlertIcon } from '../../components/Common/Icons';

{error && (
  <div className="error-alert">
    <AlertIcon />
    <span>{error}</span>
  </div>
)}
```

### 8. Empty States

**Before**:
```jsx
{data.length === 0 && <p>No data</p>}
```

**After**:
```jsx
import { QueueIcon } from '../../components/Common/Icons';

{data.length === 0 && (
  <div className="empty-state">
    <QueueIcon />
    <p className="empty-state-title">No data available</p>
    <p className="empty-state-text">Data will appear here once available</p>
  </div>
)}
```

---

## OPD Queue Page - Specific Redesign Steps

### Current Issues to Fix:
1. Replace emoji icons
2. Update table styling
3. Clean up wait time prediction panel
4. Professional form layout for "Add Patient"

### Implementation:

```jsx
// At top of OPDQueue.js
import { Card, Button, StatusBadge, Table } from '../../components/Common';
import { QueueIcon, PatientIcon, ClockIcon, AlertIcon } from '../../components/Common/Icons';

// Replace emoji-based icons
<QueueIcon /> instead of "🎫"
<PatientIcon /> instead of "👤"
<ClockIcon /> instead of "⏱️"

// Update wait time prediction panel
{showPredictionPanel && waitTimePrediction && (
  <Card
    title="Estimated Wait Time"
    value={`${waitTimePrediction.estimated_wait_time} min`}
    icon={<ClockIcon />}
    color="teal"
    subtitle={`Based on ${waitTimePrediction.current_queue_length} patients ahead`}
  />
)}

// Update status rendering in table
{
  key: 'status',
  label: 'Status',
  render: (patient) => <StatusBadge status={patient.status} />
}

// Update action buttons
<Button variant="primary" icon={<AddIcon />} onClick={() => setShowAddPatientForm(true)}>
  Add Patient
</Button>

<Button variant="success" size="sm" onClick={() => handleCallNext(patient.id)}>
  Call Next
</Button>

<Button variant="outline" size="sm" onClick={() => handleComplete(patient.id)}>
  Complete
</Button>
```

---

## Bed Management Page - Redesign Pattern

```jsx
import { Card, StatusBadge, Button } from '../../components/Common';
import { BedIcon, CheckCircleIcon, AlertIcon } from '../../components/Common/Icons';

// KPI Cards
<div className="stats-grid">
  <Card
    title="Total Beds"
    value={bedStats.total}
    icon={<BedIcon />}
    color="blue"
  />
  <Card
    title="Available"
    value={bedStats.available}
    icon={<CheckCircleIcon />}
    color="green"
  />
  <Card
    title="Occupied"
    value={bedStats.occupied}
    icon={<BedIcon />}
    color="orange"
  />
  <Card
    title="Maintenance"
    value={bedStats.maintenance}
    icon={<AlertIcon />}
    color="red"
  />
</div>

// Bed status in table/grid
<StatusBadge status={bed.status} />
```

---

## Forms - Professional Pattern

```jsx
<div className="form-container">
  <div className="form-section">
    <h3 className="form-section-title">Patient Information</h3>
    
    <div className="form-row">
      <div className="form-field">
        <label className="form-label">First Name *</label>
        <input
          type="text"
          className="form-input"
          value={form.firstName}
          onChange={(e) => setForm({...form, firstName: e.target.value})}
        />
      </div>
      
      <div className="form-field">
        <label className="form-label">Last Name *</label>
        <input
          type="text"
          className="form-input"
          value={form.lastName}
          onChange={(e) => setForm({...form, lastName: e.target.value})}
        />
      </div>
    </div>
  </div>
  
  <div className="form-actions">
    <Button variant="outline" onClick={handleCancel}>
      Cancel
    </Button>
    <Button variant="primary" loading={saving} onClick={handleSave}>
      Save Patient
    </Button>
  </div>
</div>
```

### Form CSS Needed:
```css
.form-container {
  background: var(--color-neutral-0);
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
}

.form-section {
  margin-bottom: var(--spacing-6);
}

.form-section-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--color-neutral-900);
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-3);
  border-bottom: 1px solid var(--color-neutral-200);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-4);
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-neutral-700);
}

.form-input,
.form-select {
  padding: var(--spacing-3);
  border: 1px solid var(--color-neutral-300);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  transition: border var(--transition-fast);
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-3);
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-6);
  border-top: 1px solid var(--color-neutral-200);
}
```

---

## Common CSS Utilities

Add these to your page CSS files as needed:

```css
/* Section Spacing */
.section {
  margin-bottom: var(--spacing-8);
}

.section-header {
  margin-bottom: var(--spacing-6);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-neutral-900);
}

/* Action Bar */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-6);
  padding: var(--spacing-4);
  background: var(--color-neutral-50);
  border-radius: var(--radius-lg);
}

/* Filter Group */
.filter-group {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

/* Grid Layouts */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-5);
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-5);
}

.grid-4 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--spacing-4);
}
```

---

## Checklist for Each Page

When redesigning a page, check off these items:

- [ ] Replace all emojis with SVG icons from Icons.js
- [ ] Update page header to use page-title/page-subtitle classes
- [ ] Use Card component for KPIs and metrics
- [ ] Use StatusBadge for all status indicators
- [ ] Use Button component for all actions
- [ ] Use CSS variables instead of hard-coded colors
- [ ] Add professional loading states
- [ ] Add professional error states
- [ ] Add professional empty states
- [ ] Ensure responsive grid layouts
- [ ] Test on mobile/tablet views
- [ ] Check accessibility (keyboard navigation, color contrast)

---

## Need New Icons?

If you need icons not in the current set, add them to `Icons.js`:

```jsx
export const YourNewIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
    {/* SVG paths here */}
  </svg>
);
```

**Good Icon Resources**:
- Heroicons (heroicons.com)
- Phosphor Icons (phosphoricons.com)
- Lucide Icons (lucide.dev)

Make sure they're stroke-based (not filled) for consistency.

---

## Questions?

Refer to:
- `UI_DESIGN_GUIDE.md` - Full design system documentation
- `UI_REDESIGN_SUMMARY.md` - What's been completed
- Component files - Working examples
- Dashboard page - Reference implementation

**Remember**: The goal is clean, professional, clinical-grade UI suitable for real hospital use. Avoid flashy effects, emojis, and arbitrary styling.
