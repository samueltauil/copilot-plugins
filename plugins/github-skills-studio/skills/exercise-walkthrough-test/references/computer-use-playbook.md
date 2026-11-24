# Computer Use playbook for exercise walkthroughs

How to drive and observe the real learner UI with Computer Use while testing a GitHub Skills exercise. The
Computer Use tool's own documentation is authoritative: it is returned on the first call and always wins over this
file.

## Start every agent the same way

1. Make sure Computer Use is on. In Copilot CLI: `/computer show`, and `/computer on` if needed. If the tools are
   not available in this client, switch to the fallback in [Fallbacks](#fallbacks).
2. First call, alone: `var windows = cua.listWindows();`. Read the documentation and the action policy it returns
   before binding, launching, or acting.
3. After a context summary or any loss of that documentation, call `cua.rewriteDocumentation()` alone and read it
   again.

## Choosing and binding windows

- Pick windows by the identity in the inventory (app and title); never guess. Bind with
  `var browser = cua.getApp({windowId: <id>, app: "<app>"})`, which returns an initial observation.
- Use separate windows per surface (browser for github.com, VS Code or a codespace, a terminal for Copilot CLI,
  the Copilot app). Give parallel agents separate apps.
- Only launch an app with `cua.startApp(...)` when it is needed and not running. Never launch or focus apps
  through a shell.
- Leave the user's other windows and tabs alone. Prefer a new browser window or tab you open for the test.

## Observe text-first

- `getAXState()` returns the accessibility tree as text with element indices. Read labels, headings, links,
  buttons, and their indices from it.
- Use `getAXState({emit: false})` to search programmatically without flooding the output, for example to check
  that a label from the instructions exists:

  ```js
  var state = browser.getAXState({emit: false});
  ["Create branch", "Commit changes"].map(label => [label, state.includes(label)]);
  ```

- Take a screenshot (`getScreenshot()`) only for things text cannot show: images in step comments, badges,
  layout, whether a screenshot in the instructions matches the current UI. Coordinates for clicks come only from
  the latest screenshot of that target.

## Acting

- Click by element index from the latest state; use `setValue` for whole fields (address bar, title fields),
  `typeText` to insert text (include `\n` to press Enter), `scroll` for long pages, `selectText` before replacing
  editor text.
- Bare navigation keys work in the background; Control, Alt, and Command chords (for example `Ctrl+I`,
  `Ctrl+Shift+P`) need the foreground fallback. If a chord is not delivered, use the equivalent menu or button
  and record "shortcut not verified" rather than failing the step.
- After an action, read the returned state before choosing new indices. Batch only actions already decided.
- A failed or interrupted action stops the evaluation. Re-observe in a new call before retrying. `interrupted`
  means the user is using that app: re-read its state and retry the same operation, or wait.

## Apply the action policy before every state change

The tool's policy decides; check it immediately before each state-changing operation. Typical outcomes for an
exercise run in `ui` mode:

| Learner action | Policy mode | What you do |
| --- | --- | --- |
| Navigate, scroll, open tabs, expand Having trouble blocks, read | Inspection or ALLOW | Do it |
| Type into a field without submitting | ALLOW | Do it |
| Click **Create repository** in the "Create a new repository" form | ALWAYS CONFIRM (submit a form) | Ask, wait, re-inspect, click once |
| **Commit changes**, open or merge a pull request, submit a review | ALWAYS CONFIRM (submit a form) | Ask right before each one |
| Post an issue or pull request comment | ALWAYS CONFIRM (send a message) | Ask right before each one |
| Create a codespace, install a VS Code extension | ALWAYS CONFIRM (creates a resource, installs software) | Ask right before |
| Delete a branch, file, or repository | ALWAYS CONFIRM (delete data) | Ask; prefer archiving the copy |
| Sign in or accept a browser permission prompt | PREAPPROVAL WORKS only if the user asked for that exact action; this skill hands sign-in to the user | Hand off |
| Change a password or credential, OS authentication prompt | HAND OFF | Ask the user to do it |

Ask in the form: "Do you approve clicking **Commit changes** to commit `docs/plan.md` to `add-docs` in
`<owner>/<repo>`?" One approval covers one action and is consumed once. After approval, bind the target again
(`var approvedTarget = cua.getApp(...)`), read it, then act in a separate call. If unsure whether something is a
submission, treat it as one. A refusal never authorizes doing the same thing another way.

`cli` mode does not use Computer Use at all: its `git`/`gh` changes are covered by the approved run plan and by the
CLI's own tool permissions.

## Surface recipes

### github.com in a browser

- **Go to a URL:** find the address bar in the state, `setValue(<index>, "https://github.com/<repo>/issues/1")`,
  then `pressKey("Return", {elementIndex: <index>})`.
- **Refresh after Mona acts:** press `F5` on the page, or click the browser's reload button. Do not poll the UI
  in a loop; wait with `exercise_harness.py wait-step` first, then refresh once.
- **Read the latest step:** open the exercise issue, scroll to the end, read the `Step N` heading and the
  instructions from the tree. Expand each `Having trouble?` summary by clicking it to confirm it opens.
- **Check the Copy Exercise button:** open the template's README and read the button's link target. On a
  published template, follow it and confirm the "Create a new repository" form shows the template, the
  `skills-<repo>` name, the description, and the visibility. On a staging template the button points at the final
  repository: compare its parameters as text and use the staging repository's **Use this template** button.
- **Web editor:** open the file, use the editor's text node (`selectText` + `typeText`, or `typeText` at the
  caret); the **Commit changes** dialog has message and branch fields; the final click is a submission.

### VS Code or a codespace

- Read editors text-first; if only a proxy value appears, click the editor text once, then read again.
- Terminal: click the terminal, then `typeText("git status\n")`; read the output from the terminal's text.
- Copilot Chat: click the chat input, `typeText(prompt + "\n")`, wait, then read the response text. Judge whether
  the **instructions** still work across reasonable response variations; never grade the exact wording.
- Command Palette: use the **View** menu entry if `Ctrl+Shift+P` is not delivered.

### Copilot CLI in a terminal

- Bind the terminal window; type commands and prompts with `typeText(... + "\n")`.
- Approval prompts inside the learner's Copilot CLI session are part of the experience: record what the learner
  sees. Before answering one that lets that session edit files or run commands, ask the user (one approval per
  prompt), even when the exercise tells learners to approve it.

### Copilot app

- Treat it like any desktop app: bind its window, read text-first, and follow the exercise's instructions
  literally.

## Evidence

- Keep a running log per instruction: what the instructions said, what the UI showed (label, location), what you
  did, what happened, and the walkthrough answers.
- Capture a screenshot only when it is evidence of a visual problem (stale screenshot, broken image, overlap).
- Never capture unrelated windows; never record secrets, tokens, or personal data.

## Fallbacks

Keep one UI driver per run; never mix Computer Use with another UI automation tool in the same run.

| Situation | Fallback |
| --- | --- |
| Computer Use unavailable | `cli` mode for execution; or, for exercises that only use github.com, a browser-automation tool (for example the Playwright MCP server) as the run's only UI driver. Mark desktop surfaces as not verified |
| No UI automation at all | `cli` mode for execution plus `static` mode for content |
| Element not in the accessibility tree | Screenshot, then click by pixel coordinates from that screenshot |
| Background delivery refused (`requires_escalation`) | Try a supported background-safe alternative in a new call; never force focus |
