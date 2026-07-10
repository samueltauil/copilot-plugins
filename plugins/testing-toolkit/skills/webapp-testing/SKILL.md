---
name: Web application testing strategies
description: Use this skill when you need a practical test strategy for a web application across unit, integration, and end-to-end layers.
---

# Web application testing strategies

## Use this skill when
- You need to design or improve a test strategy for a frontend, backend, or full-stack web application.
- The team is overusing end-to-end tests or has unclear coverage goals.
- You need guidance on what to mock, what to integrate, and what to validate in CI.

## Start by mapping the system under test
1. List the user-facing flows, business rules, external dependencies, and failure modes.
2. Identify which behavior is pure logic, which touches framework code, and which crosses process boundaries.
3. Write down the minimum confidence needed before merge: critical paths, regulatory checks, money movement, auth, or data integrity.

## Apply the test pyramid deliberately
1. Put most checks at the unit level for deterministic business rules and data transformations.
2. Use integration tests for API contracts, database interactions, queues, caching, and framework wiring.
3. Keep E2E tests focused on a small set of cross-stack journeys such as sign-in, checkout, and error recovery.
4. If a behavior can be proven with a cheaper test, do not duplicate it at a more expensive layer unless the risk justifies it.

## Unit testing guidance
- Test pure functions, validators, mappers, reducers, serializers, and permission checks in isolation.
- Prefer table-driven cases for boundary values, null handling, invalid inputs, and branching logic.
- Mock time, randomness, UUID generation, and remote I/O so failures are reproducible.
- Keep units fast enough to run on every save or pre-commit hook.

## Integration testing guidance
- Exercise repositories, HTTP handlers, controllers, background jobs, and service boundaries with real collaborators where practical.
- Use ephemeral test databases or isolated schemas instead of mocking persistence for data access tests.
- Verify request validation, auth middleware, transaction behavior, retry handling, and idempotency.
- Prefer contract-level assertions over fragile implementation details.

## End-to-end testing guidance
- Cover only journeys that prove the stack works together: happy path, one important sad path, and one security-sensitive path.
- Assert observable outcomes: rendered state, persisted data, emitted events, or downstream side effects.
- Avoid using E2E tests to verify every branch that is already covered below.
- Run E2E against production-like configuration, seeded data, and realistic auth flows.

## Mocking strategy
- Mock third-party systems that are slow, costly, rate-limited, or difficult to control.
- Do not mock the exact layer you are trying to validate.
- Use fakes for stable domain abstractions and stubs for one-off responses.
- Record the contract of each mock so it stays aligned with the real dependency.

## Coverage expectations
- Treat coverage as a lagging indicator, not proof of quality.
- Set higher expectations for core business rules than for UI glue code.
- Track branch coverage where condition-heavy logic matters.
- Add explicit regression tests for every escaped defect, even if raw coverage is already high.

## CI recommendations
- Run unit and lightweight integration tests on every pull request.
- Run browser or cross-service suites in parallel jobs with retries only for known infrastructure flakes.
- Fail fast on deterministic tests; quarantine flaky cases with an owner and expiration plan.
- Publish coverage, test duration, and flaky-test trends so teams can prune slow or low-value checks.

## Deliverable format
- Summarize the proposed pyramid split.
- List the critical flows and which layer owns each one.
- Call out mocks, fixtures, data strategy, and CI execution order.
- End with specific next steps: tests to add, tests to remove, and risks still untested.
