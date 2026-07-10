# Distributing instructions and prompts with plugins

GitHub Copilot plugins currently cannot natively distribute instruction files or prompt files such as:

- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`

These file types are well supported through [repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) and [organization custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions), but they cannot be packaged inside a plugin today. If you want to distribute this type of content through a plugin marketplace, use one of the workarounds below.

> 📖 Official docs: [Creating plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating) · [Plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

## Workaround 1: Convert to skills (recommended)

The best option is usually to convert reusable domain expertise into a skill.

Why this works well:

- Skills are packaged and distributed by plugins today.
- Skills are auto-discoverable.
- Skills load on demand based on the task context instead of being copied into every repository.

### Example conversion

Before, as an instruction file:

```text
.github/instructions/terraform-guardrails.instructions.md
```

```markdown
---
applyTo: "**/*.tf"
---

Use approved Azure landing-zone naming, policy, tagging, and drift-remediation practices.
```

After, as a plugin skill:

```text
skills/terraform-guardrails/SKILL.md
```

```markdown
---
name: terraform-guardrails
description: Use when working on Terraform for Azure landing zones, policy compliance, naming, tagging, or drift remediation.
---

# Terraform guardrails

Use approved Azure landing-zone naming, policy, tagging, and drift-remediation practices.
```

### Frontmatter change summary

| Instruction file | Skill file |
| --- | --- |
| `applyTo` determines when the file applies | `description` explains when the skill should be used |
| File name ends in `.instructions.md` | File is always named `SKILL.md` inside a skill directory |
| Automatically scoped by file glob | Automatically discovered from task context and prompt intent |

If you already have good instruction content, this is mostly a packaging and framing change.

## Workaround 2: Include as reference materials

If you want to preserve the original content format, bundle it as reference material inside a skill.

Recommended layout:

```text
skills/
  terraform-guardrails/
    SKILL.md
    references/
      terraform-guardrails.instructions.md
```

In this model:

- The plugin still distributes the skill.
- The original instruction content lives under `references/`.
- The skill can tell Copilot to consult that reference material when it is loaded.

This is useful when you want to keep a familiar instruction document largely unchanged while still shipping it through a plugin-supported structure.

## Workaround 3: Manual copy with templates

If you must keep real instruction or prompt files in the target repository, ship them as templates and ask users to copy them manually.

Recommended plugin layout:

```text
templates/
  instructions/
    terraform-guardrails.instructions.md
  prompts/
    release-checklist.prompt.md
```

Users then copy the files into the standard repository locations:

```text
.github/instructions/terraform-guardrails.instructions.md
.github/prompts/release-checklist.prompt.md
```

### Naming conventions

- Instruction files should end with `.instructions.md`
- Prompt files should end with `.prompt.md`
- Store them under `.github/instructions/` and `.github/prompts/` in the consuming repository

This approach is manual, but it is the closest option when you need the final repository to contain those exact file types.

## What might change

This is a current plugin-format limitation, not necessarily a permanent one. The plugin model may evolve to support instruction files and prompt files natively in the future. Until then, skills, references, and manual templates are the practical options.
