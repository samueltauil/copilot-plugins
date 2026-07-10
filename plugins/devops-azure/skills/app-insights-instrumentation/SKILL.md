---
name: Application Insights instrumentation
description: Use this skill when you need Azure Application Insights or OpenTelemetry instrumentation, metrics, traces, availability tests, and alerting guidance.
---

# Application Insights instrumentation

## Use this skill when
- You need observability for a web app, API, background worker, or distributed service on Azure.
- The goal is to instrument traces, metrics, logs, and availability checks in a way teams can operate.
- You need to translate a vague “add telemetry” request into concrete instrumentation steps.

## Start with an observability plan
1. Identify the critical user journeys, service boundaries, and operational questions to answer.
2. Define the golden signals to capture: latency, traffic, errors, and saturation.
3. Decide what must be correlated across services with trace and span context.

## Instrumentation approach
- Prefer OpenTelemetry SDKs and exporters so instrumentation stays portable.
- Configure resource attributes for service name, version, environment, and cloud metadata.
- Capture incoming requests, outbound HTTP calls, database spans, queue spans, and key background jobs.
- Enrich spans with business-safe attributes such as tenant, feature, or operation type when they aid diagnosis.

## Metrics and custom telemetry
- Define a small set of custom metrics for business-critical throughput or backlog indicators.
- Use stable naming and units so dashboards remain comparable across releases.
- Avoid high-cardinality dimensions that explode cost and degrade query performance.
- Emit custom events only when they add operational value beyond logs and traces.

## Logging and correlation
- Ensure application logs include trace IDs or operation IDs for pivoting into traces.
- Structure logs for queryability and avoid dumping entire payloads with sensitive data.
- Sample noisy success paths if volume is extreme, but protect rare failures from being dropped.
- Document what information is intentionally excluded for privacy and compliance reasons.

## Availability tests and synthetic monitoring
- Configure simple uptime checks for public endpoints from multiple regions.
- Add scenario-based synthetic tests for login, checkout, or API health when uptime alone is insufficient.
- Align alert thresholds with actual SLOs instead of arbitrary percentages.
- Validate that alerts route to the right team and include enough context to act.

## Dashboards and alerts
- Build dashboards around services and user journeys, not raw telemetry tables.
- Create alerts for sustained error spikes, latency regressions, and dependency failures.
- Separate warning thresholds from paging thresholds to reduce alert fatigue.
- Test alert rules after deployment with safe, reversible fault injection where possible.

## Troubleshooting checklist
- Verify the connection string and environment configuration for every deployment slot.
- Check sampling settings before concluding data is missing.
- Confirm clock skew, proxy behavior, or firewall rules are not breaking export.
- Compare telemetry across app versions when a deployment appears to silence signals.

## Deliverable format
- Summarize the telemetry model: traces, metrics, logs, and synthetic checks.
- Call out naming conventions, cardinality risks, and alert thresholds.
- List exact instrumentation touchpoints in the code or infrastructure.
- End with validation queries or dashboards to inspect after rollout.
