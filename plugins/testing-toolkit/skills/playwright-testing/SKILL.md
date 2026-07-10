---
name: Playwright testing
description: Use this skill when you need robust Playwright tests with maintainable selectors, fixtures, page objects, and CI-friendly execution.
---

# Playwright testing

## Use this skill when
- You are writing or repairing browser-based end-to-end tests with Playwright.
- The suite is flaky because selectors, waits, or fixtures are poorly structured.
- You need guidance for local debugging, parallel execution, or CI integration.

## Preferred project structure
1. Group tests by user workflow, not by page URL alone.
2. Put reusable UI actions in page objects or screen helpers when they remove duplication.
3. Keep assertions in tests unless a page object can express an outcome more clearly.
4. Centralize auth setup, seeded test data, and environment configuration in fixtures.

## Selector strategy
- Prefer `getByRole`, `getByLabel`, and `getByText` when the UI exposes accessible semantics.
- Use `data-testid` only for unstable or non-semantic elements.
- Avoid CSS selectors that depend on styling classes or DOM depth.
- Make selectors intention-revealing: target what the user perceives, not implementation trivia.

## Assertion guidance
- Use Playwright auto-waiting assertions such as `await expect(locator).toBeVisible()`.
- Assert the final state that matters to the user instead of intermediate animation steps.
- Verify URL, network side effects, and persisted outcomes when the scenario depends on them.
- Add negative assertions for validation errors, disabled actions, or permission denials when relevant.

## Fixtures and test data
- Create worker-scoped fixtures for expensive setup such as authenticated storage state.
- Use test-scoped fixtures for mutable entities so parallel tests do not collide.
- Seed deterministic data through APIs or direct helpers instead of navigating the UI for every setup step.
- Ensure teardown removes side effects or uses isolated namespaces per run.

## Page object rules
- Model business actions like `checkout`, `createProject`, or `inviteUser`, not clicks on every element.
- Keep page objects thin; do not hide assertions, timing hacks, or unrelated cross-page logic.
- Return locators when tests need to assert state directly.
- Refactor only after duplication appears in more than one test flow.

## Parallel and cross-browser execution
- Configure projects for Chromium, Firefox, and WebKit only when the product supports them.
- Mark tests serial only when they share state that cannot be isolated.
- Use retries sparingly and investigate every flaky failure with traces, videos, and console logs.
- Tag slow or environment-dependent suites so they can run in the right CI stage.

## CI integration
- Fail on focused tests, skipped required suites, or snapshot drift that lacks review.
- Publish HTML reports, traces, and screenshots as build artifacts.
- Run headless in CI with predictable viewport, timezone, locale, and network configuration.
- Cache browsers and dependencies to keep feedback fast.

## Debugging workflow
1. Reproduce with `--project`, `--grep`, or a single spec.
2. Re-run with trace collection enabled and inspect actionability checks.
3. Check whether the failure is caused by app state, locator ambiguity, network timing, or test data pollution.
4. Fix the root cause instead of adding sleeps.

## Deliverable format
- Explain the fixture model and selector choices.
- Show where page objects help and where plain tests are better.
- List the CI settings, artifacts, and flake controls.
- End with concrete Playwright changes to implement.
