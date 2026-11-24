# Delivery and logistics

## Delivery modes

| Mode | Strengths | Design implications |
| --- | --- | --- |
| Instructor-led (live) | Pacing, motivation, live help | Short intro per exercise, checkpoints, a help queue, buffer time |
| Self-paced | Scale, flexibility | Very clear Having trouble blocks, async help channel, realistic time estimates |
| Hybrid (kickoff plus self-paced) | Social start, flexible finish | Live setup and first exercise, then self-paced with office hours |

## Where learners copy exercises

| Environment | What to configure | Notes |
| --- | --- | --- |
| Personal accounts | Nothing special | Public copies avoid Actions minute charges; private copies use the owner's minutes |
| Learning organization (non-EMU) | Member repository creation, Codespaces access, Actions policy | Learners add a unique suffix to the suggested repository name |
| Enterprise Managed Users (EMU) | A dedicated learning organization, repository creation for members, Codespaces access, Actions policy (all actions, or the allowlist) | Follow [GitHub Skills for EMU](https://github.com/skills/skills-for-emu). Data residency enterprises on `ghe.com` are not supported |

### EMU and allowlists

- Allowing all actions and reusable workflows is the simplest and stays compatible as exercises change.
- With "allow enterprise, and select non-enterprise actions", use the maintained
  [simple](https://github.com/skills/skills-for-emu/blob/main/actions-allowlist/simple.txt) (wildcards) or
  [strict](https://github.com/skills/skills-for-emu/blob/main/actions-allowlist/strict.txt) (pinned versions)
  lists, and add any action your custom exercises use that is not on them.
- Codespaces are not available for EMU user accounts, so exercises that need a codespace must be copied into an
  organization with Codespaces enabled.

## Prerequisites to communicate before the session

- GitHub account (or EMU account) and the organization to use.
- Copilot plan required by the exercises (for example, Copilot Free has monthly limits; some features need a paid
  plan or an organization policy).
- Codespaces quota or a local setup alternative.
- Browser support and any VPN or proxy constraints.
- Pre-work exercises with links.
- Accessibility: tell learners which tools are used (browser, VS Code, terminal) so they can prepare assistive
  technology.

## Facilitation runbook

### Roles

- **Lead facilitator:** frames each exercise, keeps time, runs checkpoints.
- **Helpers:** one per 10 to 15 learners for live sessions; monitor the help queue.
- **Producer (optional):** manages chat, links, and timing signals.

### Stuck-learner protocol

1. Ask what they see and what they expected (do not take over the keyboard).
2. Check the exercise issue: is Mona's last comment "watching", "checking", a failed results table, or nothing?
3. Use the troubleshooting table below.
4. If not fixed in five minutes, let them continue with the next exercise and follow up asynchronously.

### Common failures and fixes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| No issue appears after copying | Actions disabled for the owner, or the copy was made while Actions was blocked | Enable Actions, then run **Step 0** from the Actions tab if the exercise offers `workflow_dispatch`, or copy again |
| Step does not advance | Action did not match the trigger (wrong branch, wrong file path, wrong event) | Compare with the step's instructions; check the Actions tab for a run |
| Failed results table | Check failed | Follow the tips; fix and repeat the triggering action |
| Run failed with "not allowed" | Organization allowlist blocks an action | Add the action to the allowlist (see above) |
| Codespace will not start | Quota, policy, or EMU user account | Use the organization with Codespaces enabled, or a local setup if the exercise supports it |
| Copilot features missing | Plan or policy | Confirm the plan and organization policy before the session |
| Repository name taken | Shared organization | Add a suffix such as initials |

### Reset options

- Start over: delete or archive the learner's copy, then copy the exercise again.
- Re-run a step: re-do the triggering action, or re-run the step workflow from the Actions tab when it offers
  `workflow_dispatch`.

## Costs

- Public copies in personal accounts do not use paid Actions minutes; private copies do.
- Codespaces use the owner's or organization's quota.
- Copilot usage follows each learner's plan and any premium request limits.
