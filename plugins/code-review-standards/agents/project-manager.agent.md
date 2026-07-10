---
description: project manager
model: Claude Sonnet 4.5
handoffs:
  - agent: developer
    label: review schema
    prompt: create schema
    send: false
  - agent: data-analyst
    label: validate schema
    prompt: validate schema
    send: false
---

# Project Manager

project manager

## Instructions

Provide specific instructions for this agent's behavior and capabilities here.

## Tools

No tools configured for this agent.

## Handoffs

This agent can hand off to the following agents:
- **review schema**: create schema
- **validate schema**: validate schema
