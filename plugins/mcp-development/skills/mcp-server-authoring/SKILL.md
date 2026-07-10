---
name: MCP server authoring
description: Use this skill when you need to design or implement a Model Context Protocol server with tools, resources, prompts, transports, auth, and tests.
---

# MCP server authoring

## Use this skill when
- You are creating a new MCP server or extending an existing one.
- A task involves tool schemas, resource exposure, prompt templates, or transport setup.
- You need implementation guidance that keeps the server secure, discoverable, and testable.

## Define the server surface area first
1. List the user tasks the server must enable.
2. Decide whether each need is best modeled as a tool, a resource, or a prompt template.
3. Keep the public surface minimal; every exposed capability becomes a maintenance and security burden.

## Tool definition guidance
- Give each tool a single clear responsibility and a schema that rejects ambiguous input.
- Describe side effects, rate limits, and required permissions directly in the tool metadata.
- Return structured, machine-friendly results with enough text for humans to debug failures.
- Make long-running operations cancellable or split them into pollable steps.

## Resources and prompt templates
- Use resources for data that the client may want to browse or cache without executing a tool.
- Ensure resource URIs are stable and hierarchical so clients can navigate them predictably.
- Use prompt templates for reusable orchestration instructions, not as a dumping ground for logic.
- Document when a prompt depends on certain tools or resources being available.

## Transport decisions
- Prefer stdio for local integrations and simple process-hosted workflows.
- Use SSE or HTTP-based transports when clients and servers need remote or multi-tenant connectivity.
- Be explicit about connection lifecycle, keepalives, and error semantics for the chosen transport.
- Test startup, shutdown, reconnect, and backpressure behavior, not just the happy path.

## Authentication and security
- Choose the narrowest auth model that supports the use case: API key, OAuth, signed session, or local trust.
- Never expose raw secrets in tool outputs, logs, or prompt templates.
- Validate all external inputs and sanitize anything forwarded to shells, SQL, or downstream APIs.
- Enforce server-side authorization for every operation even if the client is trusted.

## Testing strategy
- Write contract tests for capability discovery, schema validation, and representative tool calls.
- Include negative tests for invalid params, expired auth, and downstream service failure.
- Use fixture-based resources or mock backends so tests remain fast and deterministic.
- Capture protocol transcripts when debugging interoperability issues.

## Operational guidance
- Version the server and any capability schema changes.
- Emit structured logs with request IDs and timing information.
- Document environment variables, required permissions, and local run commands.
- Provide example invocations that prove the server is healthy after startup.

## Deliverable format
- Describe the chosen tool/resource/prompt model.
- State the transport, auth approach, and test plan.
- Highlight risk points such as side effects or long-running calls.
- End with the concrete implementation sequence to follow.
