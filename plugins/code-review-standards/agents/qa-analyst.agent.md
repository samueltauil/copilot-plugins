---
description: good in testing
model: Claude Sonnet 4.5
handoffs:
  - agent: project-manager
    label: review implementation
    prompt: review code
    send: false
  - agent: devops
    label: automate deploy
    prompt: create deploy script
    send: false
---

# Qa Analyst

good in testing

## Instructions

Provide specific instructions for this agent's behavior and capabilities here.

## Tools

No tools configured for this agent.

## Handoffs

This agent can hand off to the following agents:
- **review implementation**: review code
- **automate deploy**: create deploy script
