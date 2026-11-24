# Grading patterns

Recipes for `check_step_work`. Each check is a separate step with `continue-on-error: true` and an `id` that
appears in `results_table`. For each recipe: what it proves, what it does not, and a learner-facing row.

> [!IMPORTANT]
> Grade only when failure feedback is useful or later steps depend on the result. Test every check against a
> correct artifact, a wrong one, and a legitimate alternative.

Put learner-controlled values (branch names, titles, comment bodies) in `with:` inputs or `env:`, never inline in
`run:` scripts. See [workflow-security.md](workflow-security.md).

## 1. A file exists

```yaml
- name: Check plan file exists
  id: check-file
  continue-on-error: true
  uses: skills/exercise-toolkit/actions/file-exists@v0.9.3
  with:
    file: docs/plan.md
```

Proves the path exists in the checked-out commit. Does not prove content or understanding.
Row: "`docs/plan.md` exists on your branch".

## 2. A file contains a phrase

```yaml
- name: Check plan mentions testing
  id: check-phrase
  continue-on-error: true
  uses: skills/action-keyphrase-checker@v2
  with:
    text-file: docs/plan.md
    keyphrase: test
    case-sensitive: false
    minimum-occurrences: 1
```

Proves the phrase appears within the count range. Use short, unambiguous stems ("test" matches "tests",
"testing"). Never require exact sentences. Row: "Your plan mentions testing".

## 3. Accept any of several phrases

```yaml
- name: Check instructions mention a test framework
  id: check-any
  continue-on-error: true
  uses: actions/github-script@v9
  env:
    FILE: .github/copilot-instructions.md
    PATTERN: \b(jest|pytest|vitest|mocha)\b
  with:
    script: |
      const fs = require('fs');
      if (!fs.existsSync(process.env.FILE)) { core.setFailed(`${process.env.FILE} not found`); return; }
      const text = fs.readFileSync(process.env.FILE, 'utf8');
      if (!new RegExp(process.env.PATTERN, 'i').test(text)) core.setFailed('No test framework named');
```

Row: "Your instructions name a test framework (for example Jest or pytest)".

## 4. The branch or pull request has the right name

```yaml
- name: Check branch name
  id: check-branch
  continue-on-error: true
  uses: skills/action-keyphrase-checker@v2
  with:
    text: ${{ github.ref_name }}
    keyphrase: add-docs
    case-sensitive: true
    minimum-occurrences: 1
    maximum-occurrences: 1
```

Passing `${{ ... }}` into a `with:` input is safe; it is not executed by a shell. Row: "You pushed the
`add-docs` branch".

## 5. A specific file changed in this push or pull request

Native git, no third-party action:

```yaml
- name: Checkout with history
  uses: actions/checkout@v6
  with:
    fetch-depth: 0

- name: Check app.js changed
  id: check-changed
  continue-on-error: true
  env:
    BASE: ${{ github.event.pull_request.base.sha || github.event.before }}
    TARGET: src/app.js
  run: |
    # The first push of a new branch reports an all-zero "before"; compare with main instead.
    if [ -z "$BASE" ] || [ "$BASE" = "0000000000000000000000000000000000000000" ]; then
      BASE=$(git merge-base origin/main HEAD)
    fi
    git diff --name-only "$BASE" HEAD | grep -qx "$TARGET" || { echo "::error::$TARGET was not changed"; exit 1; }
```

Proves the file changed. Does not prove the change is correct; pair with a content or test check.

## 6. JSON or YAML is valid

```yaml
- name: Check settings JSON parses
  id: check-json
  continue-on-error: true
  run: python3 -c 'import json, sys; json.load(open(sys.argv[1]))' .vscode/mcp.json
```

For YAML, `yq eval '.' file.yml > /dev/null` works on GitHub-hosted Ubuntu runners, where `yq` is preinstalled.

## 7. Tests pass

```yaml
- name: Run tests
  id: check-tests
  continue-on-error: true
  run: |
    npm ci
    npm test
```

Proves the suite passes on the runner. Keep the suite fast. The job runs learner code, so keep permissions
minimal (no `actions: write`).

## 8. A workflow the learner wrote runs successfully

`wait-for-workflow` succeeds as soon as the awaited run reaches the target status, **even when that run
failed**. It fails only on a timeout or an unknown workflow. Always assert the `conclusion` output in a separate
check, and report that check in the results table:

```yaml
- name: Wait for the learner's CI workflow
  id: wait-ci
  continue-on-error: true # a timeout is reported by the next check
  uses: skills/exercise-toolkit/actions/wait-for-workflow@v0.9.3
  with:
    workflow-id: ci.yml
    head-sha: ${{ github.sha }}
    timeout: 300

- name: Check the CI workflow passed
  id: check-ci
  continue-on-error: true
  env:
    CONCLUSION: ${{ steps.wait-ci.outputs.conclusion }}
  run: |
    [ "$CONCLUSION" = "success" ] || { echo "::error::CI finished with: ${CONCLUSION:-no result}"; exit 1; }
```

Needs `actions: read` on the grading job. Not on the EMU strict allowlist at `v0.9.3`; tell facilitators. Row,
using `steps.check-ci.outcome`: "Your CI workflow ran and passed". The validator flags a `wait-for-workflow` step
whose `conclusion` is never checked (W046).

## 9. Pull request details through the API

```yaml
- name: Check a reviewer was requested
  id: check-reviewer
  continue-on-error: true
  uses: actions/github-script@v9
  with:
    script: |
      const pr = context.payload.pull_request;
      if (!pr || (pr.requested_reviewers || []).length === 0) core.setFailed('No reviewer requested');
```

Grant `pull-requests: read` to the job when you call pull request APIs.

## 10. An answer in an issue comment

Trigger: `issue_comment` (`created`) guarded to the exercise issue.

```yaml
- name: Check the answer
  id: check-answer
  continue-on-error: true
  uses: skills/action-keyphrase-checker@v2
  with:
    text: ${{ github.event.comment.body }}
    keyphrase: pull_request
    case-sensitive: false
```

Prefer self-check questions with collapsible answers for open questions; grade comments only for short,
unambiguous answers (a URL, a choice letter, a keyword).

## 11. A URL the learner shares responds

```yaml
- name: Check the app responds
  id: check-url
  continue-on-error: true
  env:
    BODY: ${{ github.event.comment.body }}
  run: |
    url=$(printf '%s' "$BODY" | grep -oE 'https://[A-Za-z0-9.-]+\.app\.github\.dev[^ )]*' | head -n1)
    [ -n "$url" ] || { echo "::error::No codespace URL found"; exit 1; }
    curl -fsS --max-time 20 "$url" > /dev/null
```

Only works when the port is public (`gh cs ports visibility <PORT>:public -c $CODESPACE_NAME`).

## 12. Copilot customization files are well formed

```yaml
- name: Check agent file has a description
  id: check-agent
  continue-on-error: true
  uses: skills/action-keyphrase-checker@v2
  with:
    text-file: .github/agents/planner.agent.md
    keyphrase: "description:"
    minimum-occurrences: 1
```

Check the structure the learner controls, never the wording of an AI response.

## Reporting results

```yaml
- name: Update comment - step results
  uses: GrantBirki/comment@v2.1.1
  with:
    repository: ${{ env.ISSUE_REPOSITORY }}
    issue-number: ${{ env.ISSUE_NUMBER }}
    comment-id: ${{ steps.find-last-comment.outputs.comment-id }}
    edit-mode: replace
    file: exercise-toolkit/markdown-templates/step-feedback/step-results-table.md
    vars: |
      step_number: 2
      results_table:
        - description: "`docs/plan.md` exists on your branch"
          passed: ${{ steps.check-file.outcome == 'success' }}
        - description: "Your plan mentions testing"
          passed: ${{ steps.check-phrase.outcome == 'success' }}
      tips: ${{ contains(steps.*.outcome, 'failure') && '["Create docs/plan.md on the add-docs branch, not on main.", "Add a sentence about how you will test the change, then push again."]' || '[]' }}

- name: Fail job if not all checks passed
  if: contains(steps.*.outcome, 'failure')
  run: exit 1
```

Rows describe expectations in learner language. Tips render only when something failed; write them as next
actions without single quotes.
