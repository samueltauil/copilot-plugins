---
name: Chrome DevTools automation and profiling
description: Use this skill when you need Chrome DevTools Protocol guidance for debugging, performance analysis, and browser automation.
---

# Chrome DevTools automation and profiling

## Use this skill when
- You need to inspect or automate a browser through Chrome DevTools Protocol or a DevTools MCP integration.
- A page has performance, network, memory, or JavaScript execution issues.
- You need evidence from the browser rather than guesses from server logs alone.

## Initial workflow
1. Reproduce the issue in a clean browser profile.
2. Capture the target URL, user action sequence, expected behavior, and actual behavior.
3. Decide which DevTools domains matter most: Network, Performance, Console, Sources, Memory, or Application.

## Network analysis
- Record all requests during the failing flow and identify blockers, redirects, cache misses, and long tail resources.
- Verify status codes, response size, content type, and server timing headers.
- Look for duplicate requests, waterfall gaps, CORS failures, and third-party latency.
- Use throttling to compare baseline behavior with slow 3G, offline, or high-latency conditions.

## Performance profiling
- Capture a performance trace around one user interaction or page load, not an entire session.
- Identify long tasks, layout thrashing, expensive script evaluation, and render-blocking resources.
- Distinguish CPU-bound JavaScript from paint or layout bottlenecks.
- Correlate timeline events with the exact components, handlers, or bundles that caused them.

## JavaScript debugging
- Watch console errors, rejected promises, CSP violations, and deprecation warnings first.
- Set breakpoints on exceptions, event listeners, or XHR/fetch calls when the bug is timing-sensitive.
- Inspect the current DOM, computed styles, and event state instead of inferring from source code alone.
- Validate source maps before trusting stack traces in bundled builds.

## Memory and leak checks
- Compare heap snapshots before and after repeating the suspect workflow.
- Look for detached DOM trees, retained listeners, unbounded caches, and large array growth.
- Verify cleanup on route change, modal close, subscription teardown, and worker shutdown.
- Use allocation sampling if snapshots alone do not isolate the culprit.

## Automation guidance
- Drive the browser with stable selectors and explicit page lifecycle waits.
- Collect console output, network failures, and screenshots in the same run.
- Use protocol events to capture low-level evidence such as request blocking, coverage, or execution timing.
- Keep automation scripts focused on one diagnostic question per run.

## Common anti-patterns to avoid
- Do not optimize based on lighthouse-style scores alone without a trace.
- Do not profile with noisy extensions, multiple tabs, or inconsistent cache state.
- Do not dismiss warnings that appear only in throttled or mobile emulation modes.
- Do not treat a single trace as definitive if the issue is intermittent.

## Deliverable format
- State the reproduction steps and the DevTools panels or protocol domains used.
- Summarize the highest-confidence findings with evidence.
- Separate root causes from secondary symptoms.
- Finish with targeted fixes and how to re-measure after changes.
