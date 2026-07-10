---
name: Responsive design
description: Use this skill when you need responsive layout guidance with mobile-first CSS, Grid, Flexbox, container queries, and fluid type and spacing.
---

# Responsive design

## Use this skill when
- A page or component must adapt cleanly across phones, tablets, laptops, and wide screens.
- You need layout guidance beyond a few ad hoc media queries.
- The design should respond to both viewport size and container size.

## Mobile-first workflow
1. Start with the smallest practical layout and add complexity as space increases.
2. Define content priorities early so low-value chrome does not crowd small screens.
3. Let components wrap and stack naturally before introducing breakpoint-specific overrides.
4. Test real content lengths, not placeholder text, because overflow often appears late.

## Layout primitives
- Use Flexbox for one-dimensional alignment and Grid for two-dimensional page or card layouts.
- Prefer intrinsic sizing, auto-fit, minmax, and gap before hard-coded widths.
- Avoid brittle absolute positioning for layouts that must stretch with content.
- Design empty, loading, and error states so they remain stable at all sizes.

## Container queries and component responsiveness
- Use container queries when a component’s layout depends on the space allocated by its parent, not the full viewport.
- Keep components self-contained so they can render well in sidebars, dialogs, and dashboards.
- Define clear thresholds for when content changes from stacked to split layouts.
- Verify nested responsive behavior so local rules do not fight page-level breakpoints.

## Typography and spacing
- Use fluid typography with `clamp()` for large ranges instead of many breakpoint-specific font sizes.
- Scale spacing, hit targets, and icon sizes with the same design logic as type.
- Maintain readable line length and vertical rhythm on both narrow and wide screens.
- Ensure form controls and navigation remain touch-friendly on coarse pointers.

## Media and assets
- Use responsive images, appropriate aspect ratios, and lazy loading where it improves performance.
- Prevent cumulative layout shift by reserving media space.
- Test how embedded charts, tables, and code blocks behave when the viewport shrinks.
- Provide alternative presentations for dense data that cannot simply “scale down.”

## Validation checklist
- Test portrait and landscape orientations.
- Check zoomed text, browser UI chrome, and safe-area insets on mobile devices.
- Validate navigation, overflow, and sticky elements at breakpoint edges.
- Compare keyboard and screen reader usability after responsive changes.

## Deliverable format
- Describe the layout system, breakpoints, and container query rules.
- Call out typography, spacing, and media handling decisions.
- Highlight risky components such as tables, menus, or long forms.
- End with the manual viewport/device checks to run.
