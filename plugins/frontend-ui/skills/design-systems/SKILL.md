---
name: Design systems
description: Use this skill when you need guidance for tokens, component libraries, Storybook documentation, theme management, and sustainable UI governance.
---

# Design systems

## Use this skill when
- You are building or evolving a reusable component library or design system.
- A product team needs shared tokens, theming, documentation, and contribution patterns.
- The goal is consistency without making application teams slower.

## Foundation first
1. Define the system’s principles: consistency, accessibility, composability, performance, and brand expression.
2. Establish design tokens for color, typography, spacing, radius, elevation, motion, and breakpoints.
3. Separate semantic tokens from raw values so themes can evolve without rewriting components.
4. Document token naming rules and source of truth clearly.

## Component architecture
- Build primitives first: buttons, inputs, layout containers, text, and feedback components.
- Compose higher-level patterns from primitives instead of duplicating styles across features.
- Keep APIs predictable: variant, size, state, and slot patterns should feel consistent across components.
- Prefer controlled extensibility through props, slots, and composition over one-off styling escape hatches.

## Accessibility and quality gates
- Make accessibility requirements part of component acceptance criteria, not a later add-on.
- Include keyboard, focus, contrast, and screen-reader behavior in the component contract.
- Add visual regression, interaction, and unit/integration tests where they provide the most confidence.
- Track breaking changes carefully because component libraries ripple through many apps.

## Storybook and documentation
- Use Storybook or an equivalent catalog to document states, variants, and usage guidance.
- Write stories that show realistic content, edge states, and anti-patterns.
- Pair code examples with design rationale so consumers know when not to use a component.
- Keep docs versioned with the code so examples never drift.

## Theming and distribution
- Support light, dark, and brand themes through tokens rather than ad hoc overrides.
- Test components under every supported theme before release.
- Publish packages with clear versioning, changelogs, and migration notes.
- Decide which layers are public API: tokens, primitives, composite components, or CSS variables.

## Governance
- Define contribution rules for new components, deprecations, and breaking changes.
- Review whether a new request belongs in the shared system or should stay app-specific.
- Measure adoption, duplication, and escape-hatch usage to guide investment.
- Assign ownership for backlog, release cadence, and support.

## Deliverable format
- Summarize the token model, component layers, and theming approach.
- Call out documentation and testing expectations.
- Note governance decisions and public API boundaries.
- End with the recommended rollout or refactor sequence.
