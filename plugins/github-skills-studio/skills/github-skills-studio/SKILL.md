---
name: github-skills-studio
description: Entry point for creating GitHub Skills exercises and workshops end to end - discover the learner, design with learning science, outline, build, independently review, walkthrough-test with Computer Use, and publish - with approval gates between phases. Use when someone wants to create a GitHub Skills exercise or workshop, turn training material into steps automated by GitHub Actions, improve or adapt an existing exercise, or asks what to do next on an exercise in progress.
---

# GitHub Skills Studio

Coordinates the exercise lifecycle and routes each phase to the right skill. Every phase ends at a gate where the
user decides. For long sessions, the `exercise-architect` agent runs this loop.

## Lifecycle

| Phase | Load | Produces | Gate (user decides) |
| --- | --- | --- | --- |
| 1. Discover | `learning-design` | Persona, objective, constraints | — |
| 2. Plan a series (if several exercises or a live workshop) | `workshop-design` | Workshop plan, exercise list | Approve the plan |
| 3. Outline | `exercise-outline` | `.github/exercise-outline.md` | **Gate 1:** outline, title, repository name |
| 4. Build | `exercise-scaffold`, `exercise-content`, `exercise-automation` | Repository files, validator clean | **Gate 2:** build round accepted |
| 5. Review | `exercise-review` (via the `exercise-reviewer` agent for independence) | Review report | **Gate 3:** choose fixes; no blocking findings remain |
| 6. Stage and walkthrough test | `exercise-publish` (Path S: staging template), then `exercise-walkthrough-test` (via the `learner-simulator` agent) | Staging template at the reviewed commit, test report | **Gate 4:** authorize the staging template (owner, name, visibility). **Gate 5:** test passed or issues accepted |
| 7. Publish | `exercise-publish` | Live template from the tested commit, release notes | **Gate 6:** explicit authorization naming owner, name, visibility |
| 8. Maintain | `exercise-publish` (maintenance) | Updates, re-tests | — |

Fixes found in phases 5 and 6 go back to phase 4 as a new build round, then through review again.

## Routing by request

| The user asks to... | Start with |
| --- | --- |
| "Create an exercise about X" | Phase 1, then 3 |
| "Turn this workshop or deck into exercises" | `workshop-design`, then `exercise-outline` per exercise |
| "Make this step clearer / add hints / fix tone" | `exercise-content` |
| "Mona doesn't advance / grading is wrong" | `exercise-automation` |
| "Review this exercise" | `exercise-review` |
| "Test it like a learner / check the UI" | `exercise-walkthrough-test` |
| "Publish / move / update / retire it" | `exercise-publish` |
| "Why does this design work?" | `learning-design` |

## Gate rules

1. Never skip a gate; each needs an explicit user response.
2. Report after every build round and every review round, then wait.
3. Review is report-only; apply only the fixes the user picks, in a new build round.
4. If the same finding survives two fix rounds, stop and ask the user to decide.
5. Never create, push, transfer, delete, or change settings of a remote repository without explicit authorization
   for that action.
6. Walkthrough tests follow the Computer Use action policy: one approval per state change it marks ALWAYS
   CONFIRM, and a refusal never authorizes another route.
7. Test the exact commit you will publish: a walkthrough runs against a template, so stage unpublished work first.
8. Start every report with the phase and round, for example "Phase 4, build round 2".

## Resuming work on an existing exercise

Infer the phase from evidence and confirm it with the user before continuing:

| Evidence | Likely phase |
| --- | --- |
| No outline recorded | 3 (outline) |
| Outline but no `.github/steps/` | 4 (build) |
| Steps and workflows exist, no recorded review | 5 (review) |
| Review signed off, no walkthrough report | 6 (stage and walkthrough test) |
| Walkthrough passed, not published | 7 (publish) |
| Published | 8 (maintain) |

Files on disk do not prove a review or test happened. Without a report or the user's confirmation, assume it did
not.

## Report format

```markdown
## Phase <n>: <name>, round <m>

### What happened
### What needs your decision
### Suggested next step
```

## Quick start prompts

- "Create a GitHub Skills exercise that teaches developers to protect their main branch. Use /github-skills-studio."
- "Turn this two-hour Copilot workshop agenda into a series of exercises: <paste or path>."
- "Review the exercise in this repository and tell me what blocks release."
- "Run a walkthrough test of `<owner>/<template>` in ui mode with Computer Use under my account and report
  execution, UI, and usability issues."
