# Walkthrough test plan: (replace-me: exercise title)

## Charter

- **Template under test:** (replace-me: owner/repository — staging template for unpublished work)
- **Commit under test:** (replace-me: SHA from `git rev-parse HEAD`; must equal preflight `head_sha`)
- **Mode:** (replace-me: ui / cli / static)
- **Sandbox owner:** (replace-me: account or test organization; never production)
- **Learner copy name:** (replace-me: skills-<repo>-wt-<timestamp>)
- **Visibility:** (replace-me: public / private / internal; never public for a private or internal template)
- **Persona(s):** (replace-me: literal novice (default), skimmer, keyboard-first)
- **Surfaces:** (replace-me: browser github.com / codespace / VS Code desktop / Copilot CLI / Copilot app)
- **Cleanup:** (replace-me: archive / delete / keep for review; delete test codespaces yes / no)

## Approvals needed

`ui` mode: ask right before each action below, one approval per action. `cli` mode: approving this plan covers
the listed changes only.

| # | Action | Consequence | How |
| --- | --- | --- | --- |
| 1 | Create the learner copy | New (replace-me: visibility) repository; exercise workflows start | `ui`: **Create repository** in the form / `cli`: harness `create --visibility <v> --yes` |
| 2 | (replace-me: e.g. commit docs/plan.md to add-docs) | (replace-me) | (replace-me: `ui`: **Commit changes** / `cli`: git push) |
| N | Archive or delete the copy (and its codespaces) | Repository becomes read-only or is removed | harness `cleanup --yes` |

## Action map

| Step | Instruction | Type (navigate / locate / type / submit / wait) | Expected UI element and label | Expected trigger or check | Negative test (graded or filtered) |
| --- | --- | --- | --- | --- | --- |
| 1 | (replace-me) | (replace-me) | (replace-me) | (replace-me) | (replace-me: e.g. "filtered: push to main → expect none") |

## Pass criteria

- Exercise starts within (replace-me: 60) seconds of the copy and posts step 1.
- Every step advances on the correct action within (replace-me: 120) seconds.
- Every graded mistake is rejected with actionable feedback, every filtered mistake produces no run, and the
  Having trouble block covers both; recovery works.
- No unrendered template syntax, broken images, or broken links in Mona's comments (`lint-comments` passes).
- Every UI label and location named in the instructions exists in the current UI.
- Review posted, issue closed, README shows the congratulations page.
