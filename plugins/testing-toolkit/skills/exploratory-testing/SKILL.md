---
name: Exploratory testing
description: Use this skill when you need a session-based exploratory testing approach with charters, heuristics, and defect-focused observation.
---

# Exploratory testing

## Use this skill when
- Requirements are incomplete, rapidly changing, or too nuanced for scripted checks alone.
- You need to uncover surprising failures in a UI, API, workflow, or integrated system.
- The goal is discovery, risk assessment, and actionable bug reports rather than exhaustive automation.

## Start with a session charter
1. Define one mission for the session, such as onboarding, permissions, or error recovery.
2. Limit the session to a focused timebox, usually 45 to 90 minutes.
3. Identify the target environment, data setup, personas, and known risks.
4. Decide what evidence to capture: notes, screenshots, console logs, traces, or videos.

## Heuristics to drive exploration
- Use SFDPOT: structure, function, data, platform, operations, and time.
- Exercise CRUD flows, boundaries, invalid inputs, and interrupted journeys.
- Vary browser, device, locale, timezone, permissions, and network conditions.
- Probe state transitions such as refresh, back button, expired sessions, and concurrent edits.

## Session-based workflow
- Spend the first minutes learning the current behavior and vocabulary of the system.
- Generate hypotheses as you observe the product: where could hidden assumptions break?
- Alternate between broad tours and focused deep dives on suspicious areas.
- Keep notes of questions, observations, and defects separately so reporting stays clear.

## Useful exploratory tours
- Landmark tour: visit every major feature once to map the terrain.
- Data tour: stress unusual characters, large payloads, empty states, and duplicate entries.
- Configuration tour: vary roles, flags, integrations, and environment-dependent behavior.
- Error tour: force timeouts, invalid credentials, dropped connectivity, and partial failures.

## Bug reporting expectations
- Capture exact reproduction steps, expected behavior, actual behavior, and scope.
- Record environment details, account type, build/version, and data prerequisites.
- Attach evidence that shortens triage: HAR, screenshot, console output, or screen recording.
- State the user impact and whether the issue blocks workflow completion.

## Debrief and follow-through
- Review what was covered, what was not covered, and what new risks were discovered.
- Convert repeatable, high-value findings into automated regression tests.
- Update charters based on defect patterns and product changes.
- Track themes such as usability gaps, confusing copy, fragile state, or security concerns.

## Anti-patterns to avoid
- Do not wander without a mission or timebox.
- Do not rely on memory instead of notes.
- Do not stop at the first failure if the area may hide related defects.
- Do not confuse exploratory depth with randomness.

## Deliverable format
- State the charter, timebox, environment, and heuristics used.
- Summarize notable findings by severity and theme.
- List follow-up automation candidates and open questions.
- End with a concise risk assessment for the tested area.
