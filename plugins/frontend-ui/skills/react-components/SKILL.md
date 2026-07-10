---
name: React component patterns
description: Use this skill when you need practical React component architecture guidance covering hooks, context, suspense, server components, performance, and testing.
---

# React component patterns

## Use this skill when
- You are designing or refactoring React components, hooks, or state boundaries.
- The UI needs better composition, performance, or testability.
- You must choose between client components, server components, context, or local state.

## Component design principles
1. Start with the user interaction and the data dependencies, not the folder structure.
2. Keep components focused on one responsibility: rendering, state coordination, or data fetching.
3. Prefer composition over inheritance and props over implicit global coupling.
4. Split components when state changes or re-render triggers affect unrelated UI regions.

## Hooks and state
- Keep local UI state close to the component that owns the interaction.
- Extract custom hooks when stateful logic is reused or when a component becomes hard to read.
- Use reducers for state machines or multi-action flows rather than stacking many interdependent `useState` calls.
- Avoid effects for derivations that can be computed during render.

## Context usage
- Use context for low-churn cross-cutting concerns such as theme, auth session, or feature flags.
- Split large contexts to avoid rerendering the entire subtree on every change.
- Expose focused hooks like `useTheme` or `useCurrentUser` instead of raw context objects everywhere.
- Do not use context as a substitute for all application state.

## Suspense and async boundaries
- Place Suspense boundaries around slow or independently loadable regions.
- Provide fallbacks that preserve layout and communicate progress.
- Keep error boundaries near the async boundary they are meant to protect.
- When using server components, fetch data on the server by default and opt into client state only where interaction demands it.

## Performance guidance
- Measure before optimizing; use React DevTools profiler or browser performance traces.
- Memoize only when prop churn or expensive computation is proven to matter.
- Stabilize callback and object props passed into memoized children when it reduces unnecessary rerenders.
- Virtualize long lists and defer non-critical work for interaction-heavy screens.

## Accessibility and semantics
- Prefer native controls and semantic markup before custom roles.
- Ensure focus management, keyboard support, and accessible names are part of the component API.
- Treat loading, error, and empty states as first-class UI states.
- Verify component variants still preserve contrast, labels, and announcements.

## Testing guidance
- Test components through user-visible behavior with React Testing Library or equivalent.
- Reserve snapshot tests for stable, low-noise markup contracts.
- Test custom hooks through components or dedicated hook helpers only when behavior is stateful and reusable.
- Add integration tests for context wiring, suspense behavior, and critical flows.

## Deliverable format
- Explain the component boundaries and state ownership.
- Call out hook extraction, context design, and async boundaries.
- Note performance and accessibility considerations.
- End with the recommended component/test structure to implement.
