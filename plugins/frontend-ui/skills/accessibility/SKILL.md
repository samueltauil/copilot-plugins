---
name: Web accessibility
description: Use this skill when you need WCAG 2.1 AA guidance for semantic markup, ARIA patterns, keyboard access, screen reader validation, and contrast compliance.
---

# Web accessibility

## Use this skill when
- You are designing, reviewing, or fixing UI for WCAG 2.1 AA accessibility.
- A component or page needs keyboard support, screen reader compatibility, or better semantics.
- Accessibility must be integrated into implementation decisions rather than checked at the end.

## Start with semantic structure
1. Use native HTML elements that already provide the needed interaction and semantics.
2. Ensure every page has a logical heading hierarchy and landmark structure.
3. Associate labels, descriptions, and errors with their form controls programmatically.
4. Preserve DOM order that matches visual reading and keyboard flow.

## ARIA guidance
- Use ARIA only when native semantics cannot express the widget behavior.
- Every ARIA role must be paired with the required keyboard interaction and states.
- Keep `aria-expanded`, `aria-selected`, `aria-controls`, and live region updates synchronized with actual UI state.
- Avoid over-annotating elements with redundant roles or labels.

## Keyboard interaction
- Make all interactive controls reachable and operable with the keyboard alone.
- Keep focus visible with a deliberate, high-contrast focus indicator.
- Manage focus on dialogs, menus, and route transitions so users never lose their place.
- Support escape, tab, shift-tab, arrow keys, and home/end where the pattern requires them.

## Visual accessibility
- Check color contrast for text, icons, controls, and focus indicators against WCAG thresholds.
- Do not rely on color alone to communicate status or errors.
- Respect zoom, reflow, and reduced motion preferences.
- Ensure responsive layouts still preserve readable line length, spacing, and target size.

## Screen reader validation
- Test core journeys with at least one screen reader on the target platform.
- Listen for accessible names, state announcements, and reading order rather than only inspecting DOM attributes.
- Validate error messages, live updates, and async loading announcements.
- Compare the announced experience with the intended user mental model.

## Common checks
- Images need meaningful alt text or empty alt when decorative.
- Tables require proper header associations when used for data.
- Modals must trap focus appropriately and restore it on close.
- Autocomplete, drag-and-drop, and custom widgets require extra scrutiny because they often break expected patterns.

## Deliverable format
- Summarize issues by semantic, keyboard, visual, and screen-reader categories.
- State the relevant WCAG 2.1 AA criteria when they clarify the fix.
- Recommend concrete markup, interaction, or styling changes.
- End with how to validate the fix manually and automatically.
