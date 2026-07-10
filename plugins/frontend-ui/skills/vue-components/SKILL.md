---
name: Vue 3 component patterns
description: Use this skill when you need Vue 3 guidance for Composition API, composables, Pinia, component boundaries, and Vite-based workflows.
---

# Vue 3 component patterns

## Use this skill when
- You are building or refactoring Vue 3 components with the Composition API.
- A codebase needs clearer state management, composables, or tooling conventions.
- You need pragmatic guidance for component structure, Pinia stores, and testability.

## Preferred Vue 3 approach
1. Use `<script setup>` for most single-file components to keep intent obvious.
2. Keep templates declarative and move reusable logic into composables.
3. Separate presentational components from stateful container components when flows become complex.
4. Co-locate styles only when they are truly component-specific.

## Composition API guidance
- Use `ref` for primitives and `reactive` for grouped mutable state when it improves readability.
- Return the smallest public surface from a composable so consumers cannot misuse internal details.
- Prefer computed properties over watchers for derivations.
- Use watchers only for side effects such as persistence, routing, or imperative integrations.

## Composables
- Name composables after the capability they provide, such as `useAuth`, `usePagination`, or `useModal`.
- Keep composables framework-aware but UI-agnostic when possible.
- Accept explicit dependencies as arguments instead of importing every collaborator internally.
- Document lifecycle assumptions, especially if the composable registers listeners or timers.

## Pinia state management
- Use Pinia for shared application state, async caching, and cross-route coordination.
- Keep stores cohesive; do not create a single global dumping-ground store.
- Put derived state in getters and async mutations in clearly named actions.
- Reset or scope store state carefully in tests and SSR contexts.

## Vite and tooling
- Leverage Vite aliases, env handling, and fast HMR, but avoid environment-dependent surprises in component logic.
- Keep auto-import or component registration conventions explicit enough that new contributors can trace them.
- Configure type checking and linting so template and script issues are caught before runtime.
- Treat build-time code splitting and lazy routes as part of the component design discussion.

## Accessibility and testing
- Use semantic HTML and accessible names in templates before reaching for ARIA.
- Test components through rendered output and user interaction, not internal refs.
- Add store-backed integration tests for flows that span multiple components.
- Validate loading, empty, and error states for async views.

## Deliverable format
- Describe component boundaries, composables, and any store responsibilities.
- Call out where Composition API primitives are preferred.
- Note Vite or SSR concerns that affect implementation.
- End with the recommended component and test breakdown.
