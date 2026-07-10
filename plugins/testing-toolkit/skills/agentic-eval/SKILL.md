---
name: AI agent evaluation
description: Use this skill when you need a structured evaluation framework for AI agents, prompts, or multi-step workflows.
---

# AI agent evaluation

## Use this skill when
- You need to measure whether an AI agent is improving or regressing.
- A team needs repeatable tests, scoring criteria, and release gates for prompt or tool changes.
- You are comparing agent variants, models, tools, or orchestration strategies.

## Define the evaluation target
1. Write the exact task the agent is expected to solve.
2. List the allowed tools, constraints, inputs, and success conditions.
3. Separate task completion from style preferences so scoring stays objective.

## Build a representative test set
- Include happy paths, edge cases, adversarial inputs, ambiguous requests, and recovery scenarios.
- Sample from production traces when possible, then redact secrets and private data.
- Label each case by difficulty, domain, risk, and expected output structure.
- Keep a frozen regression set for release decisions and a rotating discovery set for exploration.

## Choose metrics deliberately
- Measure task success first: correct answer, completed workflow, or verified side effect.
- Add quality metrics such as factuality, policy compliance, latency, token cost, and tool efficiency.
- Track failure modes explicitly: hallucination, premature completion, unsafe actions, or brittle tool usage.
- Use human review only where automated checks cannot reliably judge correctness.

## Design the scoring rubric
- Use a small ordinal scale with crisp anchors, for example 0 = fail, 1 = partial, 2 = correct.
- Define what counts as a critical failure versus a minor issue.
- Score each dimension independently before computing a weighted rollup.
- Store rationales for disputed cases so future reviewers stay consistent.

## Harness and execution guidance
- Run the same test set across all candidate versions with fixed seeds or temperature where possible.
- Capture raw prompts, tool calls, outputs, latency, and reviewer notes for every run.
- Validate structured outputs with schemas and functional outputs with programmatic checks.
- Version the dataset, rubric, and harness together so comparisons are reproducible.

## Interpreting results
- Look at category-level performance, not just one aggregate score.
- Investigate regressions by failure cluster: prompt routing, tool selection, retrieval, or output formatting.
- Watch for benchmark overfitting by holding back unseen evaluation cases.
- Prefer changes that improve both success rate and variance, not just average performance.

## Release criteria
- Set minimum pass thresholds for critical categories before deployment.
- Require no regression on safety, security, or compliance cases.
- Define acceptable latency and cost envelopes for real workloads.
- Re-run the regression suite after any change to prompts, tools, models, or policies.

## Deliverable format
- Describe the task taxonomy, dataset sources, and scoring rubric.
- Report key metrics and notable regressions.
- Highlight the most common failure patterns with examples.
- End with concrete next experiments and the decision to ship, hold, or revise.
