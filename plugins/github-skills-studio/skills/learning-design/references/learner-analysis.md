# Learner analysis

Design for a specific learner. The same exercise cannot be optimal for a first-week GitHub user and a platform
engineer: support that helps the first gets in the second's way (expertise reversal).

## Questions to answer before outlining

| Question | Why it matters | Where it lands |
| --- | --- | --- |
| Who exactly is the learner (role, daily tools, GitHub experience)? | Sets the support level and the scenario | README "Who is this for", persona |
| What can they already do without help? | Prerequisites and what to skip | README prerequisites, fast path |
| What do they believe that is wrong or partial (misconceptions)? | Theory and hints must address them | Theory, Having trouble |
| Why would they want this skill this week? | Relevance drives persistence | Story, README promise |
| Where will they take it (own account, organization, EMU, workshop room)? | Permissions, Codespaces, Actions minutes, allowlists | Prerequisites, preflight |
| Which tools and plans do they have (Copilot Free/Pro/Business, Codespaces quota, desktop vs browser)? | Activities must work for every supported path | Activities, prerequisites |
| What accessibility needs should we expect (screen reader, keyboard only, low vision, captions)? | Every route must stay usable | All content |
| Self-paced alone, or with a facilitator? | Help routes and timing | Workshop plan, review |
| How will we know they learned it (evidence)? | Drives activities and grading | Objectives and evidence matrix |

## Persona template

Write one primary persona and, if needed, one secondary persona. Keep them short and factual.

```markdown
### Persona: (name)

- **Role and context:** (e.g., backend developer at a bank, uses VS Code and Azure DevOps, new to GitHub Actions)
- **Can already:** (e.g., clone, commit, open a pull request in the web UI)
- **New to:** (the one skill this exercise teaches)
- **Likely misconceptions:** (e.g., "workflows run from any branch by default", "Copilot sees my whole organization")
- **Motivation:** (the task this skill unlocks for them)
- **Constraints:** (time box, EMU organization, no admin rights, Copilot Business only, corporate proxy)
- **Access needs:** (e.g., keyboard-only navigation, screen reader, captions)
- **Success looks like:** (observable behavior after the exercise)
```

## Prior knowledge probes

Use these during outlining (ask the requester) or in a workshop pre-survey:

- "Without looking it up, how would you [prerequisite action]?" Inability means it belongs in a prerequisite
  exercise or in step 1, not in passing.
- "When would you use [concept] instead of [similar concept]?" Confusion signals a discrimination task worth
  practicing.
- "What have you already tried?" Experienced learners bring workarounds you may need to address.

## Common misconceptions worth designing for

Collect them from facilitators, issue trackers of existing exercises, and walkthrough tests. Typical examples:

| Area | Misconception | Design response |
| --- | --- | --- |
| Git and branches | Committing in the web editor always goes to `main` | Show the branch selector state in the confirmation cue |
| Pull requests | Closing a pull request merges it | Distinguish closed and merged in theory and in the trigger guard |
| Actions | A workflow on a feature branch runs for every event | Explain trigger filters before asking learners to edit them |
| Copilot | Copilot output is always correct | Include a review or verify action after each generation |
| Exercises | Mona reacts to everything | State exactly which action Mona is watching for |

## Two-track design (expertise reversal)

When the audience mixes novices and experienced practitioners:

1. Keep the full, explicit route as the default.
2. Add an optional collapsed "Already comfortable with X? Skip ahead" note where safe.
3. Never make the grading depend on which track was used.
4. Prefer a separate advanced exercise over branching one exercise into many paths.
