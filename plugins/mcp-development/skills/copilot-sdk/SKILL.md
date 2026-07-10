---
name: GitHub Copilot SDK development
description: Use this skill when you are building Copilot extensions or SDK-based experiences with tools, hooks, events, JSON-RPC, and session lifecycle management.
---

# GitHub Copilot SDK development

## Use this skill when
- You are authoring a Copilot extension or SDK-based integration.
- A task involves tools, hooks, session lifecycle, event handling, or debugging a Copilot-hosted app.
- You need to reason about both developer ergonomics and runtime protocol behavior.

## Start with the extension contract
1. Define the user problem, available tools, expected outputs, and trust boundaries.
2. Decide which capabilities belong in a tool, which belong in prompts/instructions, and which belong in UI.
3. Keep the extension interface small and composable so each action has a clear purpose.

## Session lifecycle guidance
- Treat `joinSession` or equivalent initialization as the place to register tools, resources, and listeners.
- Load only the context needed for the current session to keep startup fast.
- Handle reconnects or repeated joins idempotently so duplicate handlers are not registered.
- Clean up long-lived resources when the host signals session end or extension unload.

## Tool design
- Define tool inputs with strict schemas and human-readable descriptions.
- Return structured outputs that downstream agents or UI surfaces can validate.
- Keep tool side effects explicit; avoid “do everything” tools that are hard to reason about.
- Distinguish read operations from mutating operations and guard the risky ones carefully.

## Hooks and events
- Use hooks to intercept lifecycle moments such as session start, tool invocation, or result handling only when necessary.
- Emit or subscribe to events with stable payload contracts and version them if the schema may evolve.
- Avoid hidden global state between events; persist only what must survive across turns.
- Log enough metadata to trace failures without leaking secrets or full user content unnecessarily.

## JSON-RPC and protocol considerations
- Treat the host/runtime interaction as JSON-RPC even if a framework abstracts it away.
- Validate request and response shapes rigorously because protocol mismatches are hard to debug later.
- Surface clear error codes and messages for invalid params, unavailable capabilities, or execution failures.
- Design for cancellation and timeout handling so tools do not hang the session.

## Hot reload and local development
- Keep the extension entry point deterministic so hot reload does not require a full environment reset.
- Use small smoke tests after changes: startup, tool registration, one successful call, one failing call.
- Prefer config-driven wiring where possible so capability changes do not require large code edits.
- Watch for stale module state when debugging reload-related bugs.

## Debugging checklist
- Confirm the extension is discovered, loaded, and advertising the expected capabilities.
- Inspect registration order when a tool or hook appears missing.
- Check schema validation, serialization, and transport-layer errors before suspecting model behavior.
- Reproduce issues with the smallest possible session transcript.

## Deliverable format
- Summarize the extension architecture and lifecycle touchpoints.
- Describe tool contracts, event flows, and protocol assumptions.
- Highlight debugging steps and likely failure modes.
- End with precise implementation tasks or code changes to make.
