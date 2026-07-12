# Copilot Plugins Marketplace

A curated marketplace of GitHub Copilot plugins aggregated from real-world customizations. Each plugin packages agents, skills, and extensions into a single installable unit for team standardization and org-wide sharing.

## Quick start

### Copilot CLI

```bash
# Add this marketplace
copilot plugin marketplace add samueltauil/copilot-plugins

# Browse available plugins
copilot plugin marketplace browse copilot-plugins

# Install a plugin
copilot plugin install sdlc-agents@copilot-plugins
```

Or in an interactive session:

```
/plugin marketplace add samueltauil/copilot-plugins
/plugin marketplace browse copilot-plugins
/plugin install sdlc-agents@copilot-plugins
```

### VS Code

1. Ensure `chat.plugins.enabled` is enabled by your org admin
2. Add this marketplace to the `chat.plugins.marketplaces` setting in VS Code:
   ```json
   "chat.plugins.marketplaces": ["samueltauil/copilot-plugins"]
   ```
3. Open the Extensions view, search `@agentPlugins`, and install plugins

### Copilot cloud agent

Add to your repository's `.github/copilot/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "enabledPlugins": {
    "sdlc-agents@copilot-plugins": true,
    "code-review-standards@copilot-plugins": true
  }
}
```

### Enterprise / org-wide deployment

In your enterprise's `.github-private` repository, create `copilot/managed-settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "copilot-plugins": {
      "source": {
        "source": "github",
        "repo": "samueltauil/copilot-plugins"
      }
    }
  },
  "enabledPlugins": {
    "code-review-standards@copilot-plugins": true,
    "git-workflow@copilot-plugins": true,
    "testing-toolkit@copilot-plugins": true
  }
}
```

This automatically installs the specified plugins for every user on the enterprise's Copilot plan across CLI, VS Code (1.122+), and cloud agent. See [docs/setup-org-enterprise.md](docs/setup-org-enterprise.md) for details.

## Plugin catalog

| Plugin | Description | Contains |
|--------|-------------|----------|
| [**sdlc-agents**](plugins/sdlc-agents/) | Multi-agent SDLC workflow: orchestrator → planner → architect → developer → tester | 5 agents, 1 skill |
| [**code-review-standards**](plugins/code-review-standards/) | Code review agents and standards for PRs, BigQuery SQL, and data pipelines | 6 agents, 2 skills |
| [**terraform-landing-zone**](plugins/terraform-landing-zone/) | Azure landing zone guardrails for Terraform with drift remediation | 3 skills |
| [**ssis-toolkit**](plugins/ssis-toolkit/) | SSIS package authoring and validation via metadata JSON | 2 agents, 4 skills |
| [**presentation-builder**](plugins/presentation-builder/) | Build Reveal.js presentations with structured requirements | 2 skills |
| [**databricks-dev**](plugins/databricks-dev/) | Databricks platform expert for notebooks, jobs, and Delta Lake | 1 agent |
| [**git-workflow**](plugins/git-workflow/) | Standardized commit messages, GitHub CLI, issue management | 4 skills |
| [**testing-toolkit**](plugins/testing-toolkit/) | Web testing strategies, Playwright, Chrome DevTools, AI agent eval | 5 skills |
| [**devops-azure**](plugins/devops-azure/) | Azure DevOps, CI/CD, App Insights, Bicep preflight, Terraform diffs | 5+ skills |
| [**mcp-development**](plugins/mcp-development/) | Build Copilot extensions, MCP servers, and agentic workflows | 1 agent, 2+ skills |
| [**frontend-ui**](plugins/frontend-ui/) | Frontend and UI patterns for React, Vue, components, and design systems | 5+ skills |

## What plugins can and cannot distribute

Plugins support:
- ✅ Agents (`.agent.md` files)
- ✅ Skills (`SKILL.md` files with references)
- ✅ Hooks (`hooks.json`)
- ✅ MCP server configurations (`.mcp.json`)
- ✅ LSP server configurations (`lsp.json`)
- ✅ Extensions (`extension.mjs`)

Plugins do **not** natively support:
- ❌ Instruction files (`.github/instructions/*.instructions.md`)
- ❌ Prompt files (`.github/prompts/*.prompt.md`)
- ❌ Repo-level `copilot-instructions.md`

For these, we convert domain expertise into skills (which are auto-discoverable) or provide templates you can copy manually. See [docs/distributing-instructions-prompts.md](docs/distributing-instructions-prompts.md).

## Why this exists

A common question from teams adopting GitHub Copilot is: *"How do I share customizations across my organization?"*

GitHub already provides powerful built-in mechanisms for this. Organizations can set [custom instructions at the org level](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions), and repositories can include [repo-level instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions) via `.github/copilot-instructions.md` and `.github/instructions/` files. The `.github` and `.github-private` repos at the org level are great for distributing shared instructions and configuration across repositories.

[Plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) add a complementary distribution model on top of these foundations. They're especially useful when you want to share **agents**, **skills**, **hooks**, and **MCP server configurations** — assets that go beyond instruction files:

| Capability | Org-level instructions | Plugins |
|------------|----------------------|---------|
| Scope | Org / repo | Any project, cross-org |
| Best for | Standards, guidelines, coding conventions | Agents, skills, workflows, tools |
| Distribution | Automatic via `.github` repo | `copilot plugin install` or managed settings |
| Discovery | Repository navigation | `copilot plugin marketplace browse` |
| Enterprise rollout | Org settings UI | `managed-settings.json` auto-install |

Both approaches work well together. Use org instructions for coding standards and conventions, and plugins for reusable agents, skills, and tooling. This marketplace is both a working tool and a reference implementation you can fork for your own organization.

## Managing plugins

```bash
copilot plugin list                    # View installed plugins
copilot plugin update sdlc-agents     # Update a plugin
copilot plugin update --all            # Update all plugins
copilot plugin disable sdlc-agents    # Disable without removing
copilot plugin enable sdlc-agents     # Re-enable
copilot plugin uninstall sdlc-agents  # Remove completely
```

## Documentation

- [Setup: Copilot CLI](docs/setup-cli.md)
- [Setup: VS Code](docs/setup-vscode.md)
- [Setup: Copilot cloud agent](docs/setup-copilot-cloud-agent.md)
- [Setup: Enterprise / org-wide](docs/setup-org-enterprise.md)
- [Distributing instructions and prompts](docs/distributing-instructions-prompts.md)

### Official GitHub documentation

- [Finding and installing plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)
- [Creating plugins](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
- [Plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [Plugin reference (manifest schema)](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Organization custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-organization-instructions)
- [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

## Contributing

Want to add a plugin? Create a directory under `plugins/` with a `plugin.json` manifest and your agents/skills, then add an entry to `.github/plugin/marketplace.json`. See the [plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) for the full manifest schema.

## License

MIT
