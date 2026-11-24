---
name: exercise-scaffold
description: Build the repository for a GitHub Skills exercise from an approved outline - README with Copy Exercise button, step files, review, start/step/final workflows wired to the skills/exercise-toolkit, images, LICENSE, optional codespace - then validate it. Use when turning an outline into a working exercise, adding or renumbering steps, upgrading the exercise-toolkit pin, or repairing broken workflow wiring.
---

# Scaffold a GitHub Skills exercise

Turn an approved outline into a complete exercise repository that satisfies the
[framework contract](references/framework-contract.md). Content writing rules live in `exercise-content`;
trigger and grading design lives in `exercise-automation`. Load both while building.

## Preconditions

- An approved outline (Gate 1). If there is none, load `exercise-outline` first. If the user insists on
  skipping, state the assumptions you make.
- A target folder. Default: a new folder named after the approved repository name, outside other repositories.
- Do not create remote repositories here. Publishing is `exercise-publish` and needs explicit authorization.

## First, inspect

1. Is the folder empty, a copy of `skills/exercise-template`, or an existing exercise? Never overwrite
   existing steps or workflows without saying so.
2. Read `.github/exercise-outline.md` if present; it is the source of truth.
3. Resolve the toolkit version (below).

## Build order

1. **Shell**
   - `git init` (no history from templates), [assets/gitignore.txt](assets/gitignore.txt) as `.gitignore`,
     [assets/LICENSE](assets/LICENSE) with the year and copyright holder.
   - Save the approved outline verbatim to `.github/exercise-outline.md`.
2. **README** from [assets/README.md](assets/README.md): title, one-line promise, welcome block, one objective
   per step, honest time, Copy Exercise button, footer. Badge link:
   `https://github.com/new?template_owner=<owner>&template_name=<repo>&owner=%40me&name=skills-<repo>&description=Exercise:+<Title+Words>&visibility=public`.
   If the owner is not known yet, keep `(replace-me-owner)` and say so in the report.
3. **Steps** from [assets/steps/N-step.md](assets/steps/N-step.md) or
   [assets/steps/N-step-multi-activity.md](assets/steps/N-step-multi-activity.md), one file per step
   (`1-step.md`, `2-step.md`, ...), written with the `exercise-content` skill.
4. **Review** from [assets/steps/x-review.md](assets/steps/x-review.md).
5. **Workflows**
   - [assets/workflows/0-start-exercise.yml](assets/workflows/0-start-exercise.yml): set the title and a
     one-sentence intro message.
   - For each step `N` except the last: [N-step-graded.yml](assets/workflows/N-step-graded.yml) or
     [N-step-ungraded.yml](assets/workflows/N-step-ungraded.yml) saved as `N-step.yml`.
   - Last step: [N-step-final.yml](assets/workflows/N-step-final.yml) saved as `N-step.yml`.
   - Replace `<STEP>` with `N` and `<NEXT_STEP>` with `N+1`; set the trigger and checks from the outline using
     `exercise-automation`.
6. **Images** in `.github/images/`, referenced from steps as `../images/<file-name-without-spaces>`.
7. **Codespace** (only if the outline needs one): [assets/devcontainer.json](assets/devcontainer.json) as
   `.devcontainer/devcontainer.json` with the smallest suitable image and only the extensions the exercise uses.
8. **Validate** (below), fix, and report.

## Wiring rules

| Item | Rule |
| --- | --- |
| Workflow `N-step.yml` | `name: Step N`; posts step `N+1` through `STEP_<N+1>_FILE`; ends with `gh workflow enable "Step <N+1>"` |
| Final workflow | `name: Step N # Last step of the exercise`; posts `x-review.md`; calls `finish-exercise.yml` |
| Step 0 | `push` to `main` plus `workflow_dispatch`; `is_template` guard; posts step 1; enables `Step 1` |
| Grading | `check_step_work` present only when graded; then `post_next_step_content.needs` includes it |
| Comments with variables | Step files are always rendered with Nunjucks: pass every variable they use in `vars:` (`login`, `full_repo_name`), because missing ones render empty; wrap any `${{ }}` and literal `{{`, `{%`, `{#` in `{% raw %}` |
| Permissions | `permissions: {}` at the top, per-job grants as in the templates |
| Exercise title | Identical in README, Step 0 `exercise-title`, and the final `finish_exercise` input |
| Pins | One toolkit tag everywhere; `actions/checkout@v6`, `GrantBirki/comment@v2.1.1`, `peter-evans/find-comment@v4`, `skills/action-keyphrase-checker@v2` |

## Toolkit version

```bash
gh release view --repo skills/exercise-toolkit --json tagName,isDraft,isPrerelease
git ls-remote --tags https://github.com/skills/exercise-toolkit "refs/tags/<tag>"
```

If the latest published release is newer than the templates' `v0.9.3`, ask the user whether to adopt it. If
yes, read the new tag's `workflow_call` inputs and outputs, then replace the tag everywhere (workflow `uses:`,
action `uses:`, and toolkit checkout `ref:`). Never use `@main` or a draft release.

## Codespace notes

- In step 1, offer an **Open in Codespaces** button that targets the learner's copy:
  `[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/{{full_repo_name}}?quickstart=1)`,
  and tell learners to confirm the repository is their copy, not the original.
- To make a forwarded port public, run `gh cs ports visibility <PORT>:public -c $CODESPACE_NAME` in
  `postCreateCommand` (devcontainer settings cannot do it).
- Automate setup in `postCreateCommand`; never make learners install boilerplate by hand.

## Validate before handing off

Run the static validator from the exercise root and fix every blocking finding:

```bash
python <plugin>/skills/exercise-review/scripts/validate_exercise.py . --template-repo <owner>/<repo>
```

`<plugin>` is this plugin's install directory (the folder containing this skill's parent `skills/` folder).
Use `--online` to confirm the toolkit tag exists. Python 3.9+ is enough; PyYAML is optional.

## Report back

```markdown
## Build round <n>

- **Files created or changed:** <list>
- **Steps and triggers:** <step → trigger → graded? → checks>
- **Decisions made for you:** <names, pins, defaults>
- **Validator:** <Blocking / Important / Nice to improve counts; anything left and why>
- **Look at first:** <the riskiest step>
- **Next:** independent review (`exercise-review`), then a walkthrough test.
```
