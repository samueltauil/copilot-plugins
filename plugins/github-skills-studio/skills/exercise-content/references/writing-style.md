# Writing style and formatting

Follows the [exercise-creator step formatting reference](https://github.com/skills/exercise-creator/blob/main/docs/reference/step-formatting.md)
and the [GitHub Docs content style guide](https://github.com/github/docs/blob/main/contributing/content-style-guide.md),
with accessibility improvements.

## Voice

- Second person, present tense, active voice: "Click **Commit changes**."
- Friendly, casual, professional, and inviting; sparing emoji; never sarcastic.
- Plain words: "use" not "utilize"; one idea per sentence; spell out acronyms on first use; "repository" not
  "repo".
- Name UI controls exactly as the UI shows them, in **bold**. Put values, names, and paths in `code`.
- Mona speaks in comments; instructions speak directly to the learner. Do not mix narrators in one paragraph.

## UI directions

Describe the general area first, then the control, then the value, then the result:

> In the right sidebar, under **Assignees**, click **Assign yourself**. Your avatar now appears under
> **Assignees**.

- Easier: "In the right settings area, near the bottom, click the **Duplicate issue** button."
- Harder: "Click the **Duplicate issue** button at the bottom of the right settings area."

Announce context switches: "Return to the exercise issue tab", "Switch to your codespace".

## Lists and spacing

- Number every instruction `1.`; GitHub renders the sequence.
- Leave one blank line between instructions.
- Indent anything that belongs to an instruction (images, code, tips) by three spaces so the list continues.
- Keep instructions to two levels.

## Callouts

Outside lists, use GitHub alerts sparingly, left-aligned:

```markdown
> [!TIP]
> You can also start from the **Code** tab.
```

GitHub alerts do not render when indented inside a list. Inside instructions, use these instead:

| Purpose | Markdown |
| --- | --- |
| Note | `> 🪧 **Note:** ...` |
| Tip | `> 💡 **Tip:** ...` |
| Important | `> ❕ **Important:** ...` |
| Warning | `> ⚠️ **Warning:** ...` |
| Caution | `> ❗ **Caution:** ...` |
| Wait | `> ⏳ **Wait:** The following will take a moment.` |
| Bonus | `> ✨ **Bonus:** ...` |
| Try this | `> 🧪 **Try this:** ...` |

For a long tip or one with an image, use a collapsible block indented under the instruction:

```markdown
   <details>
   <summary><b>💡 Tip:</b> Short description</summary><br/>

   Additional explanation.

   </details>
```

## Prompts and commands

Put anything the learner types into a badge-led blockquote, indented under its instruction. Give badges
meaningful alt text so screen readers announce what kind of input it is.

Copilot Chat, Copilot app, or IDE prompt:

```markdown
   > ![Copilot prompt](https://img.shields.io/badge/-Prompt-text?style=social&logo=github%20copilot)
   >
   > ```prompt
   > Explain what this workflow does, step by step.
   > ```
```

Copilot CLI prompt (typed inside a `copilot` session):

```markdown
   > ![Copilot CLI prompt](https://img.shields.io/badge/CLI-Prompt-text?style=flat-square&logo=github-copilot&labelColor=8250df&color=fbefff)
   >
   > ```prompt
   > Create a branch named add-docs and switch to it.
   > ```
```

Terminal command:

```markdown
   > ![Terminal command](https://img.shields.io/badge/Terminal-text?style=flat&logo=gnometerminal&labelColor=1f2328&color=eee)
   >
   > ```bash
   > git switch -c add-docs
   > ```
```

Rules: keep the badge line, a bare `>` line, and the fence in one blockquote; use the `prompt` fence for prompts
and `bash` (or `powershell`) for commands; never put a copyable command inside prose.

## Template variables

GitHub Skills posts step files with `GrantBirki/comment`, which always renders them with Nunjucks. Values come
only from the posting step's `vars:` (the scaffold templates pass `login` and `full_repo_name`); anything else
renders as an empty string.

- Personalize links: `https://github.com/{{ full_repo_name }}/settings`.
- Greet once if you like: `Hi @{{ login }}!`
- Wrap GitHub Actions expressions in raw tags: `{% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}`. Do the same for
  any literal `{{`, `{%`, or `{#` learners should see (for example Liquid or Jinja snippets).
- Avoid placeholders the learner must replace by hand; use a variable instead.

## Links

- Link key words inline instead of a references list at the end.
- Use descriptive link text ("[About branches](...)"), never "click here".
- In step files, never use relative links like `../../actions`: comments are posted on the issue page, so they
  resolve wrongly. Use `https://github.com/{{ full_repo_name }}/actions` or a root-relative `/owner/repo` path.
- Prefer official sources: GitHub Docs, GitHub Learn, GitHub Blog and Changelog, VS Code docs.

## Images and diagrams

- Store images in `.github/images/` and reference them as `../images/<file>` (no spaces in file names).
- Use `<img width="..." alt="..." src="../images/...">` to control size; describe the relevant state in `alt`.
- Add a screenshot only when words cannot locate the control or show the state; keep the explaining sentence next
  to it.
- Prefer mermaid diagrams or editable `.drawio.svg` files over exported images.
- Screenshots go stale when the UI changes; the walkthrough test flags mismatches.

## Links to other exercises

```markdown
[![Skills](https://img.shields.io/badge/Skills-Introduction_to_GitHub_→-text?style=flat&logo=github&labelColor=1f2328&color=1f883d)](https://github.com/skills/introduction-to-github)
```
