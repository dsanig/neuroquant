# Design System - NeuroQuant

## Design principles
- Serious, efficient, non-decorative UI.
- Dense but readable information hierarchy.
- Dark institutional palette with restrained emphasis.

## Foundations
- **Typography**: Inter/system sans, small supporting labels, medium-weight key labels, bold metric values.
- **Color tokens**:
  - Background: `#0b0f17`
  - Panels: `#121926`, `#161f30`
  - Borders: `#253146`
  - Text: `#d8e1f5`
  - Muted: `#8b9bbc`
  - Accent focus: `#4067b5`
  - Risk tone: `#90546d`
  - Warning tone: `#7f6a33`

## Components
- `MetricCard`: key figures with optional tone (`default`, `risk`, `warning`).
- `DataTable`: reusable typed table primitive with caption and empty-state handling.
- `FilterBar`: reusable search/strategy/sort controls.
- `AppShell`: persistent sidebar and top header for operator identity/session context.

## State patterns
- **Loading**: neutral card-level loading language.
- **Empty**: explicit no-data messaging, never blank containers.
- **Error**: bounded module-level error block with operator action guidance.

## Accessibility and operations ergonomics
- Visible focus styles for form controls and nav.
- Keyboard skip-link to main content.
- Sidebar + dense tables optimized for desktop/laptop screens; mobile remains functional but secondary.
